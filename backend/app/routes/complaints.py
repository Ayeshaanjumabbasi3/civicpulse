from fastapi import APIRouter,Depends,Query,Request,status
from app.models.enums import Category,Priority,Status
from app.schemas.complaint import ComplaintCreate,ComplaintListResponse,ComplaintResponse,ComplaintStatusUpdate
router=APIRouter(prefix='/api/complaints',tags=['complaints'])
def svc(request:Request): return request.app.state.complaint_service
@router.post('',response_model=ComplaintResponse,status_code=status.HTTP_201_CREATED)
def create(payload:ComplaintCreate,request:Request,service=Depends(svc)):
    result=service.create(payload); request.app.state.stats_service.invalidate(); return result
@router.get('/{complaint_id}',response_model=ComplaintResponse)
def get_one(complaint_id:str,service=Depends(svc)): return service.get(complaint_id)
@router.get('',response_model=ComplaintListResponse)
def list_complaints(request:Request,category:Category|None=None,priority:Priority|None=None,status_:Status|None=Query(None,alias='status'),page:int=Query(1,ge=1),page_size:int=Query(10,ge=1,le=100)):
    items,total=request.app.state.repo.list(category,priority,status_,page,page_size); return {'items':items,'page':page,'page_size':page_size,'total':total}
@router.patch('/{complaint_id}/status',response_model=ComplaintResponse)
def update_status(complaint_id:str,payload:ComplaintStatusUpdate,request:Request):
    item=request.app.state.complaint_service.get(complaint_id); result=request.app.state.status_service.update(item,payload.status); request.app.state.stats_service.invalidate(); return result
