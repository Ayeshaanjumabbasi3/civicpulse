import re
from app.models.enums import Category,Priority
from app.schemas.triage import TriageResult
class RuleBasedTriage:
    name='rules'
    keywords={Category.water:('water','leak','pipe','flood','flooding','pani'),Category.electricity:('electric','bijli','power','wire','outage','transformer'),Category.sanitation:('garbage','trash','waste','sewer','kachra','sanitation'),Category.roads:('road','pothole','street','footpath','pavement'),Category.streetlights:('light','streetlight','bulb','dark')}
    def triage(self,text,location):
        value=text.lower()
        category=next((kind for kind,words in self.keywords.items() if any(word in value for word in words)),Category.other)
        high=('flood','flooding','burst','fire','danger','urgent','emergency','overflow','sparks','accident')
        low=('cosmetic','minor','small')
        priority=Priority.high if any(word in value for word in high) else Priority.low if any(word in value for word in low) else Priority.normal
        clean=re.sub(r'\s+',' ',text.strip()).strip(' .')
        summary=(clean[:137]+'...') if len(clean)>140 else clean
        return TriageResult(category=category,priority=priority,ai_summary=summary,provider=self.name,confidence=.5)
