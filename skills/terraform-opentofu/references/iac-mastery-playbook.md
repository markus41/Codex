# IaC Mastery Playbook (Cross-stack)

## Source docs used
- Kubernetes: https://kubernetes.io/docs/home/
- Helm: https://helm.sh/
- Docker: https://docs.docker.com/
- OpenTofu: https://opentofu.org/
- Terraform: https://developer.hashicorp.com/terraform/docs
- Vault: https://developer.hashicorp.com/vault
- Red Hat Build of Keycloak: https://access.redhat.com/products/red-hat-build-of-keycloak

## Layered model
1. **Foundation IaC**: Terraform/OpenTofu for cloud/network/platform primitives.
2. **Workload packaging**: Docker for build/runtime reproducibility.
3. **Cluster orchestration**: Kubernetes manifests + Helm charts.
4. **Security/identity**: Vault for secrets, Keycloak for IAM/SSO realm/org configuration.

## Delivery cadence
- **PR stage**: fmt/lint/validate, render templates, policy checks.
- **Plan stage**: produce Terraform/OpenTofu plan + Helm diff.
- **Review stage**: human approval for destructive/high-risk changes.
- **Apply stage**: environment-scoped rollout with drift monitoring.
- **Post-apply**: smoke tests, audit links, and rollback references.

## Non-negotiables
- Version pinning for providers/modules/charts/images.
- Remote state + locking + encrypted state storage.
- Secrets only via runtime injection (Vault/KMS), never plaintext in git.
- Environment parity through reusable modules/chart values layering.

## Useful response pattern for Codex
When asked to "do IaC", return:
1. Assumptions (cloud, cluster, identity, secret source).
2. Repo layout proposal.
3. Minimal viable module/chart definitions.
4. CI/CD stages with validation + policy checks.
5. Rollback and incident considerations.
