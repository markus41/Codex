# Keycloak Organizations and Admin References

## Canonical docs
- https://www.keycloak.org/docs/latest/server_admin/index.html#_managing_organizations
- https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.0/html/server_administration_guide/managing_organizations
- https://access.redhat.com/products/red-hat-build-of-keycloak
- https://phasetwo.io/docs/organizations/

## IaC-focused guidance
- Model realm, clients, roles, groups, and org mappings as code where provider/tooling allows.
- Promote config across environments with explicit export/import/versioning strategy.
- Keep identity bootstrap secrets in Vault or equivalent, not in repo.
- Treat identity changes like infra changes: PR, plan/diff, approval, apply, verification.
