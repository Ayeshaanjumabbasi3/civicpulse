from typing import Protocol
from app.schemas.triage import TriageResult
class TriageProviderError(Exception): pass
class TriageProvider(Protocol):
    name: str
    def triage(self,text:str,location:str)->TriageResult: ...
