from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.db.session import get_engine
from app.models.complaint import ComplaintORM
from app.models.enums import Category,Priority,Status
class StatsRepository:
    def __init__(self,session_factory=None): self.session_factory=session_factory; self._invalidated=True
    def _session(self): return self.session_factory() if self.session_factory else Session(get_engine())
    def invalidate(self): self._invalidated=True
    def get_aggregates(self):
        with self._session() as db:
            total=db.scalar(select(func.count()).select_from(ComplaintORM)) or 0
            categories={x:0 for x in Category}; priorities={x:0 for x in Priority}
            for value,count in db.execute(select(ComplaintORM.category,func.count()).group_by(ComplaintORM.category)): categories[Category(value)]=count
            for value,count in db.execute(select(ComplaintORM.priority,func.count()).group_by(ComplaintORM.priority)): priorities[Priority(value)]=count
            resolved=db.scalar(select(func.count()).where(ComplaintORM.status==Status.resolved)) or 0
            return {'total':total,'by_category':categories,'by_priority':priorities,'resolved':resolved}
