# ADR 0004: PII and complaint data governance

Complaint text, location, and optional `reporter_contact` are stored in PostgreSQL. With `rules` or `simulated`, no complaint data leaves the machine. The LLM/Ollama providers can send complaint text and location to their configured provider; the current code does not redact free text first. `reporter_contact` is not sent to the provider. External LLM use therefore requires consent, redaction, retention, access-control, and provider-review work before production use.
