# Engineering notes

## 1. Laptop versus CI

Laptop execution depends on Docker Desktop/k3d, local ports, `.env`, and Windows shell behavior. CI uses Ubuntu, service containers, GitHub Secrets, and an ephemeral k3d cluster. The differences are encoded in `.github/workflows/ci.yml` and `.github/workflows/cd.yml`.

## 2. CI/CD maturity

The project has automated test, build, scan, SBOM, image publication, and ephemeral deployment stages. It is beyond build-only automation, but it is not a complete production platform because the CD cluster is ephemeral and production promotion/observability are not automated.

## 3. Build once, deploy many

The `build-push` job tags images with `${{ github.sha }}`. The `deploy` job uses the same SHA in its image variables and Kustomize rewrite before applying the production overlay.

## 4. Deterministic LLM tests

CI sets `TRIAGE_PROVIDER=simulated`. `backend/app/providers/triage/simulated.py` derives output from a SHA-256 digest of text and location, avoiding network calls and model variability.

## 5. HPA lag

HPA timing depends on metrics-server sampling, the HPA sync period, scheduling, image startup, and readiness. Actual scale-up timing and replica counts must come from the real captured `kubectl get hpa -w` output; this repository does not invent those numbers.

## 6. VPA mode

`k8s/base/vpa.yaml` uses `updateMode: Off`, so recommendations can be observed without evicting pods or fighting the CPU-based HPA.

## 7. Hosted LLM egress

The backend is attached to the edge and internal Compose networks; PostgreSQL and Redis are internal only. The backend can make outbound provider calls through normal container egress while the data services have no published host ports. Production should add explicit NetworkPolicies for hard egress guarantees.

## 8. Biggest debugging experience

CD initially failed because the ephemeral cluster lacked the VPA CRD, then because a password containing URL-reserved characters broke `DATABASE_URL`, and finally because the ingress smoke test used `/health` and `localhost` even though the ingress routed `/` to frontend and required `Host: civicpulse.local`. These failures produced the current workflow fixes.

## 9. Data indexes and Redis persistence

The `(status, priority)` index supports filtered operator queries, while the `created_at` index supports newest-first pagination. Redis uses AOF on a named volume so rate-limit windows and warm cache entries survive a service restart; the cache remains rebuildable, but preserving it avoids a cold-start burst and keeps distributed throttling state consistent.
