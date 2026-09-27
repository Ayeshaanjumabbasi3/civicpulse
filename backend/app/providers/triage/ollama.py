import json,httpx
from app.core.config import get_settings
from app.models.enums import Category,Priority
from app.providers.triage.base import TriageProviderError
from app.schemas.triage import TriageResult
class OllamaTriage:
    name='llm:ollama'
    def triage(self,text,location):
        settings=get_settings(); prompt=f'Return strict JSON only with category, priority, ai_summary, confidence. Categories: {[x.value for x in Category]}; priorities: {[x.value for x in Priority]}. Complaint: {text}. Location: {location}'
        try:
            response=httpx.post(f'{settings.ollama_url.rstrip("/")}/api/generate',json={'model':settings.ollama_model,'prompt':prompt,'format':'json','stream':False},timeout=10); response.raise_for_status(); data=json.loads(response.json()['response'])
            return TriageResult(category=data['category'],priority=data['priority'],ai_summary=data['ai_summary'],provider=self.name,confidence=data['confidence'])
        except Exception as exc: raise TriageProviderError(f'Ollama triage failed: {exc}') from exc
