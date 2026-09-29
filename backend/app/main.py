import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.errors import ConflictError, NotFoundError
from app.core.logging import configure_logging, reset_request_id, set_request_id
from app.core.metrics import metrics
from app.db.session import dispose_engine
from app.providers.cache.redis import RedisCache
from app.repositories.complaint_repository import SqlAlchemyComplaintRepository
from app.repositories.stats_repository import StatsRepository
from app.routes import complaints, health, meta, stats
from app.services.complaint_service import ComplaintService
from app.services.stats_service import StatsService
from app.services.status_service import StatusService
from app.services.triage_service import TriageService

configure_logging()


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    client = getattr(application.state.redis_cache, "client", None)
    if client is not None:
        close = getattr(client, "close", None)
        if close:
            close()
    dispose_engine()


app = FastAPI(title="CivicPulse API", version="0.1.0", lifespan=lifespan)
settings = get_settings()
cors_origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):517[3-9]$",
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
    expose_headers=["X-Cache", "X-Request-ID"],
)
repo = SqlAlchemyComplaintRepository()
stats_repo = StatsRepository()
redis_cache = RedisCache(settings.redis_url)
triage = TriageService(
    settings.triage_provider, redis_cache, settings.triage_failure_mode
)
app.state.repo = repo
app.state.stats_repo = stats_repo
app.state.redis_cache = redis_cache
app.state.triage_service = triage
app.state.complaint_service = ComplaintService(repo, triage)
app.state.status_service = StatusService(repo)
app.state.stats_service = StatsService(stats_repo, redis_cache)


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if (
        request.method != "POST"
        or request.url.path != "/api/complaints"
        or request.method == "OPTIONS"
    ):
        return await call_next(request)
    minute = int(time.time() // 60)
    key = f"ratelimit:{request.client.host if request.client else 'unknown'}:{minute}"
    count = redis_cache.incr_with_expiry(key, 60)
    if count is not None and count > settings.rate_limit_per_minute:
        return JSONResponse(
            {"detail": "Too many requests, please try again shortly."},
            status_code=429,
            headers={"Retry-After": "60"},
        )
    return await call_next(request)


@app.middleware("http")
async def request_id(request: Request, call_next):
    started = time.perf_counter()
    rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = set_request_id(rid)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        metrics.record_request(started)
        reset_request_id(token)


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        {
            "detail": [
                {"loc": list(error["loc"]), "msg": error["msg"], "type": error["type"]}
                for error in exc.errors()
            ]
        },
        status_code=400,
    )


@app.exception_handler(ConflictError)
async def conflict(_: Request, exc: ConflictError):
    return JSONResponse(content={"detail": exc.detail}, status_code=409)


@app.exception_handler(NotFoundError)
async def not_found(_: Request, exc: NotFoundError):
    return JSONResponse(content={"detail": exc.detail}, status_code=404)


app.include_router(complaints.router)
app.include_router(stats.router)
app.include_router(meta.router)
app.include_router(health.router)
