# CivicPulse Kubernetes deployment

The manifests target the local `civicpulse` k3d cluster. Images are loaded from
the local Docker daemon and use `IfNotPresent` so the cluster does not require a
registry.

## Prepare images and secrets

```powershell
docker compose build backend frontend
k3d image import newfolder-backend:latest newfolder-frontend:latest -c civicpulse
kubectl apply -f k8s/base/namespace.yaml
kubectl -n civicpulse create secret generic civicpulse-secrets `
  --from-literal=POSTGRES_PASSWORD=civicpulse-dev-password `
  --from-literal=REDIS_PASSWORD=redis-dev-password `
  --from-literal=LLM_API_KEY=CHANGE_ME `
  --dry-run=client -o yaml | kubectl apply -f -
```

The committed Secret contains placeholders only. Use real local values with the
command above; never commit them.

## Deploy and verify

```powershell
kubectl apply -k k8s/overlays/dev
kubectl get pods,svc,ingress,hpa,pdb -n civicpulse
kubectl get endpoints -n civicpulse
```

Add `127.0.0.1 civicpulse.local` to the Windows hosts file, then open
`http://civicpulse.local`. The HPA uses CPU requests and metrics-server; VPA is
recommendation-only (`updateMode: Off`) so it cannot evict pods or alter the HPA
signal automatically.

VPA requires its CRDs/controller to be installed separately before applying
the base because k3d ships metrics-server, not VPA.
