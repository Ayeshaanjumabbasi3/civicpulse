# ADR 0003: Deploy immutable commit-SHA images

`cd.yml` builds and pushes backend/frontend images with `${{ github.sha }}`, then deploys those exact tags to the ephemeral k3d cluster after rewriting the production Kustomize overlay. This is build-once, deploy-many behavior and makes rollback auditable; `latest` is not the deployment identity.
