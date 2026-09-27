from fastapi import APIRouter,HTTPException
from fastapi.responses import PlainTextResponse
from app.db.session import database_is_ready
from app.core.metrics import metrics
router=APIRouter(tags=['health'])
@router.get('/health')
def health(): return {'status':'ok'}
@router.get('/ready')
def ready():
    if not database_is_ready(): raise HTTPException(503,'Database unavailable')
    return {'status':'ready'}
@router.get('/metrics',response_class=PlainTextResponse)
def metrics_endpoint(): return metrics.prometheus()
