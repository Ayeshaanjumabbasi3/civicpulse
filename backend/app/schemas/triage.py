from pydantic import BaseModel, Field
from app.models.enums import Category, Priority
class TriageResult(BaseModel): category: Category; priority: Priority; ai_summary: str = Field(max_length=140); provider: str; confidence: float = Field(ge=0, le=1)
