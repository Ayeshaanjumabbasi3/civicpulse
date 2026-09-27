# CivicPulse runbook

## Compose

```powershell
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps
```

Open `http://localhost:8080` and check `http://localhost:8000/health`.

## Kubernetes

```powershell
docker compose build backend frontend
k3d image import newfolder-backend:latest newfolder-frontend:latest -c civicpulse
kubectl apply -k k8s/overlays/dev
kubectl get pods,svc,ingress,hpa,vpa -n civicpulse
```

## Health and logs

```powershell
kubectl logs deployment/backend -n civicpulse --tail=200
kubectl get events -n civicpulse --sort-by=.lastTimestamp
kubectl port-forward -n civicpulse svc/backend-service 8001:8000
curl.exe http://127.0.0.1:8001/health
```

## HPA/VPA

```powershell
kubectl get hpa -n civicpulse -w
kubectl describe vpa backend-vpa -n civicpulse
```

Run `load/k6-script.js` against the real ingress and save the actual HPA output before making scaling claims.

## Rollback

```powershell
kubectl rollout undo deployment/backend -n civicpulse
kubectl rollout undo deployment/frontend -n civicpulse
kubectl rollout status deployment/backend -n civicpulse
```

For an image rollback, pin the previous known-good SHA in `k8s/overlays/prod/kustomization.yaml`, then run `kubectl apply -k k8s/overlays/prod` and verify both rollouts.

## Triage and data services

Check `/providers` and backend logs when provider calls fail; `TriageService` falls back to rules. Check `/ready`, the PostgreSQL StatefulSet/PVC, and Redis pod/service logs when dependencies are unavailable. Keep PostgreSQL and Redis ports internal in production.
