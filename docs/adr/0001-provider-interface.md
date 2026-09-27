# ADR 0001: Provider interface for triage

`backend/app/providers/triage/base.py` defines the provider contract. `factory.py` selects rule-based, simulated, LLM, or Ollama implementations, while `services/triage_service.py` consumes them without vendor-specific logic. This keeps CI deterministic with `TRIAGE_PROVIDER=simulated` and allows external-provider failures to fall back to rules. The fallback is covered by `test_fallback` in `backend/tests/unit/test_backend.py`.
