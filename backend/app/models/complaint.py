import uuid
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import DateTime,Integer,String,Text,func
from sqlalchemy.dialects.postgresql import ENUM,UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
from .enums import Category,Priority,Status
class ComplaintORM(Base):
    __tablename__='complaints'
    id: Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,server_default=func.gen_random_uuid())
    text: Mapped[str]=mapped_column(Text,nullable=False)
    location: Mapped[str]=mapped_column(String(200),nullable=False)
    reporter_contact: Mapped[str|None]=mapped_column(String,nullable=True)
    category: Mapped[Category]=mapped_column(ENUM(Category,name='category_enum',create_type=False),nullable=False)
    priority: Mapped[Priority]=mapped_column(ENUM(Priority,name='priority_enum',create_type=False),nullable=False)
    status: Mapped[Status]=mapped_column(ENUM(Status,name='status_enum',create_type=False),nullable=False,server_default=Status.open.value)
    ai_summary: Mapped[str]=mapped_column(String(140),nullable=False)
    triaged_by: Mapped[str]=mapped_column(String,nullable=False)
    triage_latency_ms: Mapped[int|None]=mapped_column(Integer,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
@dataclass
class Complaint:
    id: str; text: str; location: str; category: Category; priority: Priority; status: Status; ai_summary: str; triaged_by: str; triage_latency_ms: int; created_at: datetime; updated_at: datetime; reporter_contact: str|None=None
