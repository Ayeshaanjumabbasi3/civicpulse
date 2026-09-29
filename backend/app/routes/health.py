from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse

from app.core.metrics import metrics
from app.db.session import database_is_ready

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
def ready(request: Request):
    database_ok = database_is_ready()
    redis_ok = request.app.state.redis_cache.ready()
    if not database_ok or not redis_ok:
        raise HTTPException(
            503,
            {
                "database": "ok" if database_ok else "unavailable",
                "redis": "ok" if redis_ok else "unavailable",
            },
        )
    return {"status": "ready"}


@router.get("/metrics", response_class=PlainTextResponse)
def metrics_endpoint():
    return metrics.prometheus()
