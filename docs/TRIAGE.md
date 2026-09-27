# Triage system

`backend/app/providers/triage/base.py` defines the provider contract. `factory.py` selects `rules`, `simulated`, `llm`, or `ollama`; `services/triage_service.py` records outcomes and handles fallback.

`RuleBasedTriage` lowercases text and matches keyword groups for water, electricity, sanitation, roads, and streetlights. Flood, burst, fire, danger, urgent, emergency, overflow, sparks, and accident indicate high priority. Cosmetic, minor, and small indicate low priority; otherwise priority is normal. Whitespace is normalized for the summary.

`SimulatedTriage` hashes text and location with SHA-256. Rule matches remain meaningful; otherwise the digest deterministically selects category and priority. It is the CI provider, not an AI model.

The LLM provider sends a structured prompt to a chat-completions endpoint and parses category, priority, and summary JSON. Ollama sends a JSON-format generation request to its configured URL. Provider errors trigger a rules result labeled `rules:fallback`.

Known limitations include coarse keyword matching, limited multilingual coverage, provider-output validation requirements, and privacy review requirements for external providers.
