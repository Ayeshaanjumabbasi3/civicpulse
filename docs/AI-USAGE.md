# AI usage disclosure

## Triage verification notes

The active provider is selected with `TRIAGE_PROVIDER`. CI uses `simulated`, while `rules` is the deterministic local fallback. Every provider result is validated by `TriageResult` before persistence. Triage cache usage is observable through `/metrics` using `civicpulse_triage_cache_hits_total`, `civicpulse_triage_cache_lookups_total`, and `civicpulse_triage_cache_hit_ratio`; the last 20 outcomes, including `cache_hit`, `fallback`, and `latency_ms`, are available at `/api/meta/providers`.

To measure a real cache ratio, submit the same text and location twice, then read `/metrics`: the first request should be a miss and the second a hit, producing a ratio of `1 / 2 = 0.5` for a fresh metrics process. The cache entry expires after 24 hours.

This project was developed with assistance from OpenAI Codex in this workspace. AI assistance drafted and revised application scaffolding, tests, Docker/Compose/Kubernetes configuration, CI/CD workflows, troubleshooting commands, and documentation.

The work was verified with backend tests, frontend Vitest tests, a production frontend build, Docker Compose services, k3d/Kubernetes deployments, HPA/VPA inspection, and GitHub Actions. Human verification is still required for screenshots, partner collaboration, branch protection, rollback demonstrations, merge-conflict evidence, and the demo video.
