from pydantic import BaseModel, Field

from app.models.enums import Category, Priority


class TriageResult(BaseModel):
    """Validated provider output; raw model output never leaves this schema."""

    category: Category
    priority: Priority
    summary: str = Field(max_length=140)
    confidence: float = Field(ge=0.0, le=1.0)
    # Provider is operational metadata used for persistence and observability.
    provider: str = "unknown"

    @property
    def ai_summary(self) -> str:
        """Compatibility name used by the public complaint response."""
        return self.summary
