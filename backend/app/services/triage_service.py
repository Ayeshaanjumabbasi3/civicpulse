import time
from collections import deque
from app.providers.triage.base import TriageProviderError
from app.providers.triage.factory import get_provider
from app.providers.triage.rules import RuleBasedTriage
class TriageService:
    def __init__(self,provider_name:str): self.provider_name=provider_name; self.provider=get_provider(provider_name); self.outcomes=deque(maxlen=20)
    def triage(self,text,location):
        started=time.perf_counter(); fallback=False
        try: result=self.provider.triage(text,location)
        except TriageProviderError:
            result=RuleBasedTriage().triage(text,location); result.provider='rules:fallback'; fallback=True
        latency=round((time.perf_counter()-started)*1000); self.outcomes.append({'provider':result.provider,'latency_ms':latency,'fallback':fallback}); return result,latency
