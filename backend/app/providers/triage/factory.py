import logging

from app.providers.triage.base import TriageProvider
from app.providers.triage.llm import LLMTriage
from app.providers.triage.ollama import OllamaTriage
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def get_provider(name: str, failure_mode: str = "") -> TriageProvider:
    providers = {
        "llm": LLMTriage,
        "ollama": OllamaTriage,
        "rules": RuleBasedTriage,
        "simulated": SimulatedTriage,
    }
    provider = providers.get(name)
    if provider is None:
        logging.getLogger(__name__).warning(
            "Unknown TRIAGE_PROVIDER=%s; using rules", name
        )
        return RuleBasedTriage()
    return provider(failure_mode) if name == "simulated" else provider()
