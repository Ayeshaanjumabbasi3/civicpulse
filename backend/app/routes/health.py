from fastapi import APIRouter,HTTPException
from app.db.session import database_is_ready
router=APIRouter(tags=['health'])
@router.get('/health')
def health(): return {'status':'ok'}
@router.get('/ready')
def ready():
    if not database_is_ready(): raise HTTPException(503,'Database unavailable')
    return {'status':'ready'}
@router.get('/metrics')
def metrics(): return {'requests_total':0}
