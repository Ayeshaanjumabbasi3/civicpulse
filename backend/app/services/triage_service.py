import hashlib
import json
import time
import logging
from collections import deque
from app.providers.triage.factory import get_provider
from app.providers.triage.rules import RuleBasedTriage
from app.schemas.triage import TriageResult
from app.core.metrics import metrics
class TriageService:
    def __init__(self,provider_name:str,cache=None,failure_mode=''): self.provider_name=provider_name; self.provider=get_provider(provider_name,failure_mode); self.cache=cache; self.outcomes=deque(maxlen=20)
    def triage(self,text,location,complaint_id='pending'):
        started=time.perf_counter(); fallback=False
        cache_key='triage:'+hashlib.sha256(f'{self.provider_name}|{text}|{location}'.encode()).hexdigest()
        if self.cache:
            cached=self.cache.get(cache_key)
            if cached:
                try:
                    result=TriageResult.model_validate(json.loads(cached))
                    metrics.record_cache(True)
                    self.outcomes.append({'provider':result.provider,'latency_ms':0,'fallback':False,'cache_hit':True})
                    return result,0
                except Exception:
                    pass
            metrics.record_cache(False)
        try:
            result=TriageResult.model_validate(self.provider.triage(text,location))
            # ``simulated`` is a development selector, not a persisted provider
            # identity. Keep the database contract stable when it is enabled.
            if self.provider_name == 'simulated' and result.provider == 'simulated':
                result.provider = 'rules'
        except Exception as exc:
            logging.getLogger(__name__).warning('triage fallback complaint_id=%s provider=%s error_class=%s',complaint_id,self.provider_name,type(exc).__name__)
            result=RuleBasedTriage().triage(text,location); result.provider='rules:fallback'; fallback=True
        latency=round((time.perf_counter()-started)*1000); metrics.record_triage(latency,fallback); self.outcomes.append({'provider':result.provider,'latency_ms':latency,'fallback':fallback,'cache_hit':False})
        if self.cache:self.cache.set(cache_key,result.model_dump_json(),86400)
        return result,latency
