# Vault for IaC (HashiCorp)

## Canonical docs
- https://developer.hashicorp.com/vault

## Integration principles
- Never commit static secrets to IaC repos.
- Use short-lived credentials generated at runtime where possible.
- Separate secret definition (Vault) from infrastructure declaration (Terraform/OpenTofu).

## Common patterns
- Pull secrets with Vault provider/data sources only when required for provisioning.
- Use dynamic cloud/database secrets for CI runs.
- Rotate root/static credentials after bootstrap.

## Guardrails
- Enforce least privilege policies per pipeline/environment.
- Audit secret access and map it to change requests.
- Fail plans when required secret paths/policies are missing.
