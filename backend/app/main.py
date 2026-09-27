import uuid
import time
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.logging import configure_logging
from app.core.errors import ConflictError,NotFoundError
from app.core.config import get_settings
from app.repositories.complaint_repository import SqlAlchemyComplaintRepository
from app.repositories.stats_repository import StatsRepository
from app.services.triage_service import TriageService
from app.services.complaint_service import ComplaintService
from app.services.status_service import StatusService
from app.services.stats_service import StatsService
from app.providers.cache.redis import RedisCache
from app.routes import complaints,stats,meta,health
configure_logging()
app=FastAPI(title='CivicPulse API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_origin_regex=r'^https?://(localhost|127\.0\.0\.1):517[3-9]$',allow_methods=['GET','POST','PATCH','OPTIONS'],allow_headers=['Content-Type','X-Request-ID'],expose_headers=['X-Cache','X-Request-ID'])
settings=get_settings(); repo=SqlAlchemyComplaintRepository(); stats_repo=StatsRepository(); triage=TriageService(settings.triage_provider); redis_cache=RedisCache(settings.redis_url)
app.state.repo=repo; app.state.stats_repo=stats_repo; app.state.redis_cache=redis_cache; app.state.triage_service=triage; app.state.complaint_service=ComplaintService(repo,triage); app.state.status_service=StatusService(repo); app.state.stats_service=StatsService(stats_repo,redis_cache)
@app.middleware('http')
async def rate_limit(request:Request,call_next):
    if request.url.path in ('/health','/ready') or request.method=='OPTIONS': return await call_next(request)
    minute=int(time.time()//60); key=f'ratelimit:{request.client.host if request.client else "unknown"}:{minute}'
    count=redis_cache.incr_with_expiry(key,60)
    if count is not None and count>settings.rate_limit_per_minute: return JSONResponse({'detail':'Too many requests, please try again shortly.'},status_code=429)
    return await call_next(request)
@app.middleware('http')
async def request_id(request:Request,call_next):
    rid=request.headers.get('X-Request-ID',str(uuid.uuid4())); response=await call_next(request); response.headers['X-Request-ID']=rid; return response
@app.exception_handler(ConflictError)
async def conflict(_:Request,exc:ConflictError): return JSONResponse(content={'detail':exc.detail},status_code=409)
@app.exception_handler(NotFoundError)
async def not_found(_:Request,exc:NotFoundError): return JSONResponse(content={'detail':exc.detail},status_code=404)
app.include_router(complaints.router); app.include_router(stats.router); app.include_router(meta.router); app.include_router(health.router)
