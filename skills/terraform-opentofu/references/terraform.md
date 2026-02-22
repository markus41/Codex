# Terraform Reference (HashiCorp)

## Canonical docs
- https://developer.hashicorp.com/terraform/docs
- https://developer.hashicorp.com/terraform/language
- https://developer.hashicorp.com/terraform/cli

## Operational defaults for Codex
- Prefer reusable modules over large root configs.
- Keep environments isolated via backend/workspace strategy and explicit variable files.
- Always run: `fmt` -> `validate` -> `plan` before `apply`.
- Treat plan output as a review artifact in PRs.

## High-signal language patterns
- `locals` for derived values; keep variable inputs minimal and typed.
- `for_each` over `count` when identity matters.
- `dynamic` blocks only for nested arguments that are truly optional/repeated.
- `depends_on` only when implicit graph edges are insufficient.

## State and backend guidance
- Use remote state for teams.
- Enable state locking where supported.
- Avoid direct state editing except controlled break-glass procedures.

## Module guidance
- Pin module versions.
- Expose stable inputs/outputs; avoid leaking provider internals through outputs.
- Include examples and README for each reusable module.
