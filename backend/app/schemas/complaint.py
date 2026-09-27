from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import Category, Priority, Status
class ComplaintCreate(BaseModel): text: str = Field(min_length=10,max_length=2000); location: str = Field(min_length=3,max_length=200); reporter_contact: str | None = None
class ComplaintStatusUpdate(BaseModel): status: Status
class ComplaintResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; text:str; location:str; reporter_contact:str|None=None; category:Category; priority:Priority; status:Status; ai_summary:str; triaged_by:str; triage_latency_ms:int; created_at:datetime; updated_at:datetime
class ComplaintListResponse(BaseModel): items:list[ComplaintResponse]; page:int; page_size:int; total:int
