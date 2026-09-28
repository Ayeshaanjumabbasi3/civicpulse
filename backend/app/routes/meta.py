from fastapi import APIRouter,Request
from app.core.config import get_settings
from app.models.enums import Category,Priority,Status
router=APIRouter(prefix='/api/meta',tags=['meta'])
@router.get('/providers')
def providers(request:Request): return {'provider':get_settings().triage_provider,'outcomes':list(request.app.state.triage_service.outcomes)[-20:]}
@router.get('/contract')
def contract():
    return {'categories':[x.value for x in Category],'priorities':[x.value for x in Priority],'statuses':[x.value for x in Status],'transitions':{'open':['in_progress','rejected'],'in_progress':['resolved','rejected'],'resolved':[],'rejected':[]}}
