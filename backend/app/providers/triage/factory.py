import logging

from app.providers.triage.base import TriageProvider
from app.providers.triage.llm import LLMTriage
from app.providers.triage.ollama import OllamaTriage
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def get_provider(name: str, failure_mode: str = "") -> TriageProvider:
    if name == "simulated":
        return SimulatedTriage(failure_mode)
    if name == "llm":
        return LLMTriage()
    if name == "ollama":
        return OllamaTriage()
    if name == "rules":
        return RuleBasedTriage()
    logging.getLogger(__name__).warning("Unknown TRIAGE_PROVIDER=%s; using rules", name)
    return RuleBasedTriage()
