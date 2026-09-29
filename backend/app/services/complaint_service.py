import uuid
from datetime import UTC, datetime

from app.core.errors import NotFoundError
from app.models.complaint import Complaint


class ComplaintService:
    def __init__(self, repo, triage):
        self.repo = repo
        self.triage_service = triage

    def create(self, data):
        complaint_id = str(uuid.uuid4())
        result, latency = self.triage_service.triage(
            data.text, data.location, complaint_id
        )
        now = datetime.now(UTC)
        complaint = Complaint(
            id=complaint_id,
            text=data.text,
            location=data.location,
            reporter_contact=data.reporter_contact,
            category=result.category,
            priority=result.priority,
            status="open",
            ai_summary=result.ai_summary,
            triaged_by=result.provider,
            triage_latency_ms=latency,
            created_at=now,
            updated_at=now,
        )
        return self.repo.add(complaint)

    def get(self, id):
        item = self.repo.get(id)
        if not item:
            raise NotFoundError("Complaint not found")
        return item

    def list(self, category, priority, status, page, page_size):
        return self.repo.list(category, priority, status, page, page_size)
