# CI/CD Pipeline Response

## Pipeline Overview
- **Service/Application:** {{name}}
- **Repository:** {{repo}}
- **Environment(s):** {{dev/stage/prod}}
- **Trigger Strategy:** {{push/pr/manual/schedule}}

## Stages
1. **Build**
   - {{build steps / tooling}}
2. **Test**
   - {{unit/integration/security tests}}
3. **Package**
   - {{artifact/container details}}
4. **Deploy**
   - {{deployment strategy}}
5. **Verify**
   - {{post-deploy checks}}

## Controls and Governance
- **Approvals:** {{where required}}
- **Policy/Compliance Checks:** {{tools and rules}}
- **Secrets Management:** {{vault/secret manager approach}}

## Failure Handling
- **Rollback Strategy:** {{auto/manual rollback plan}}
- **Alerting:** {{channels/on-call routing}}
- **Retry/Timeout Rules:** {{key thresholds}}

## Implementation Notes
- {{critical assumptions}}
- {{known risks or dependencies}}
