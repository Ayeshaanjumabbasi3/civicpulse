from datetime import datetime,timezone
from app.core.errors import ConflictError
from app.models.enums import Status
class StatusService:
    valid={(Status.open,Status.in_progress),(Status.open,Status.rejected),(Status.in_progress,Status.resolved),(Status.in_progress,Status.rejected)}
    def __init__(self,repo): self.repo=repo
    def update(self,complaint,new_status):
        current=Status(complaint.status); target=Status(new_status)
        if (current,target) not in self.valid: raise ConflictError(f'Cannot transition from {current.value} to {target.value}')
        complaint.status=target; complaint.updated_at=datetime.now(timezone.utc); return self.repo.update(complaint)
