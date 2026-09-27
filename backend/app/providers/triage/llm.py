import httpx
from app.core.config import get_settings
from app.models.enums import Category,Priority
from app.providers.triage.base import TriageProviderError
from app.schemas.triage import TriageResult
class LLMTriage:
    name='llm:groq'
    def triage(self,text,location):
        settings=get_settings()
        if not settings.llm_api_key: raise TriageProviderError('LLM_API_KEY is not configured')
        prompt=f'''Return JSON only with keys category, priority, ai_summary, confidence.\nAllowed category values: {[x.value for x in Category]}. Allowed priority values: {[x.value for x in Priority]}.\nComplaint: {text}\nLocation: {location}'''
        try:
            response=httpx.post('https://api.groq.com/openai/v1/chat/completions',headers={'Authorization':f'Bearer {settings.llm_api_key}'},json={'model':settings.groq_model,'messages':[{'role':'system','content':'You are a civic complaint triage classifier. Return strict JSON only.'},{'role':'user','content':prompt}],'temperature':0},timeout=10)
            response.raise_for_status(); raw=response.json()['choices'][0]['message']['content']; data=__import__('json').loads(raw)
            return TriageResult(category=data['category'],priority=data['priority'],ai_summary=data['ai_summary'],provider=self.name,confidence=data['confidence'])
        except Exception as exc: raise TriageProviderError(f'Groq triage failed: {exc}') from exc
