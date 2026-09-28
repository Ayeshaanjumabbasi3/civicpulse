import uuid
from abc import ABC,abstractmethod
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.models.complaint import Complaint,ComplaintORM
from app.models.enums import Category,Priority,Status
from app.db.session import get_engine
class ComplaintRepository(ABC):
    @abstractmethod
    def add(self,complaint:Complaint)->Complaint: ...
    @abstractmethod
    def get(self,complaint_id:str)->Complaint|None: ...
    @abstractmethod
    def list(self,category:Category|None,priority:Priority|None,status:Status|None,page:int,page_size:int)->tuple[list[Complaint],int]: ...
    @abstractmethod
    def update(self,complaint:Complaint)->Complaint: ...
class SqlAlchemyComplaintRepository(ComplaintRepository):
    def __init__(self,session_factory=None): self.session_factory=session_factory
    def _session(self):
        return self.session_factory() if self.session_factory else Session(get_engine())
    @staticmethod
    def _domain(row):
        return Complaint(id=str(row.id),text=row.text,location=row.location,reporter_contact=row.reporter_contact,category=Category(row.category),priority=Priority(row.priority),status=Status(row.status),ai_summary=row.ai_summary,triaged_by=row.triaged_by,triage_latency_ms=row.triage_latency_ms or 0,created_at=row.created_at,updated_at=row.updated_at)
    def add(self,complaint):
        with self._session() as db:
            row=ComplaintORM(id=uuid.UUID(complaint.id),text=complaint.text,location=complaint.location,reporter_contact=complaint.reporter_contact,category=complaint.category,priority=complaint.priority,status=complaint.status,ai_summary=complaint.ai_summary,triaged_by=complaint.triaged_by,triage_latency_ms=complaint.triage_latency_ms)
            db.add(row);db.commit();db.refresh(row);return self._domain(row)
    def get(self,complaint_id):
        try: key=uuid.UUID(complaint_id)
        except ValueError: return None
        with self._session() as db: return self._domain(row) if (row:=db.get(ComplaintORM,key)) else None
    def list(self,category,priority,status,page,page_size):
        with self._session() as db:
            query=select(ComplaintORM)
            if category is not None: query=query.where(ComplaintORM.category==category)
            if priority is not None: query=query.where(ComplaintORM.priority==priority)
            if status is not None: query=query.where(ComplaintORM.status==status)
            total=db.scalar(select(func.count()).select_from(query.subquery())) or 0
            rows=db.scalars(query.order_by(ComplaintORM.created_at.desc()).offset((page-1)*page_size).limit(min(page_size,100))).all()
            return [self._domain(x) for x in rows],total
    def update(self,complaint):
        key=uuid.UUID(complaint.id)
        with self._session() as db:
            row=db.get(ComplaintORM,key)
            if row is None:return complaint
            row.status=complaint.status;db.commit();db.refresh(row);return self._domain(row)
