from fastapi import APIRouter,Request
from app.core.config import get_settings
router=APIRouter(prefix='/api/meta',tags=['meta'])
@router.get('/providers')
def providers(request:Request): return {'provider':get_settings().triage_provider,'outcomes':list(request.app.state.triage_service.outcomes)[-20:]}
