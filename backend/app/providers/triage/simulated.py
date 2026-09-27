import hashlib
from app.models.enums import Category,Priority
from app.schemas.triage import TriageResult
from app.providers.triage.rules import RuleBasedTriage
class SimulatedTriage:
    name='rules'
    def triage(self,text,location):
        digest=int(hashlib.sha256(f'{text}|{location}'.encode()).hexdigest()[:8],16)
        categories=list(Category); priorities=list(Priority); heuristic=RuleBasedTriage().triage(text,location); category=heuristic.category if heuristic.category is not Category.other else categories[digest%len(categories)]; priority=priorities[(digest//7)%len(priorities)]
        return TriageResult(category=category,priority=priority,ai_summary=f'Simulated triage: {text.strip()[:120]}',provider=self.name,confidence=.9)
