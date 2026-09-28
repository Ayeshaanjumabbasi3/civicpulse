import hashlib
from app.models.enums import Category,Priority
from app.schemas.triage import TriageResult
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.base import TriageProviderError
class SimulatedTriage:
    name='rules'
    def __init__(self, failure_mode: str = ''):
        self.failure_mode = failure_mode
    def triage(self,text,location):
        if self.failure_mode == 'raise':
            raise TriageProviderError('simulated provider failure')
        if self.failure_mode == 'malformed':
            return {'category': 'invalid', 'priority': 'invalid', 'summary': 'malformed', 'confidence': 2}
        digest=int(hashlib.sha256(f'{text}|{location}'.encode()).hexdigest()[:8],16)
        categories=list(Category); priorities=list(Priority); heuristic=RuleBasedTriage().triage(text,location); category=heuristic.category if heuristic.category is not Category.other else categories[digest%len(categories)]; priority=heuristic.priority if heuristic.priority is not Priority.normal else priorities[(digest//7)%len(priorities)]
        return TriageResult(category=category,priority=priority,summary=f'Simulated triage: {text.strip()[:120]}',provider=self.name,confidence=.9)
