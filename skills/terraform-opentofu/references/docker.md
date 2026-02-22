# Docker in IaC Delivery Pipelines

## Canonical docs
- https://docs.docker.com/

## How Docker fits IaC mastery
- Standardize execution environment for lint/plan/apply jobs.
- Build immutable tooling images with pinned Terraform/OpenTofu, kubectl, and helm versions.
- Reduce "works on my machine" drift in infrastructure pipelines.

## Suggested pipeline shape
1. Build/pull trusted IaC runner image.
2. Run static checks and tests in container.
3. Generate and archive plan artifact.
4. Gate apply behind approval/policy checks.

## Security baseline
- Use minimal base images.
- Sign/verify images when possible.
- Avoid baking secrets into images or build args.
