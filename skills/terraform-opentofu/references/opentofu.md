# OpenTofu Reference

## Canonical docs
- https://opentofu.org/
- https://opentofu.org/docs/
- https://opentofu.org/docs/language/

## Usage posture
- Default to OpenTofu-compatible syntax when mixed estates are expected.
- Validate provider availability/compatibility before migration.
- Pin CLI and provider versions in CI to ensure deterministic plans.

## Migration checklist (Terraform -> OpenTofu)
1. Pin current Terraform and provider versions.
2. Produce a clean, reviewed Terraform plan baseline.
3. Swap CLI in CI and rerun `init`, `validate`, and `plan`.
4. Compare plans and investigate all drift before applying.
5. Update team docs/runbooks with new CLI and release policy.

## Team conventions
- Keep lock files committed.
- Prefer explicit provider source/version constraints.
- Capture plan JSON for policy and cost checks.
