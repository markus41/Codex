# Structurizr Architecture Skill

This skill standardizes architecture documentation workflows using Structurizr DSL.

## Standard Task 1: Generate a Structurizr DSL workspace from requirements

### Required inputs
- System name and short description.
- Primary personas/users.
- Core containers/components and responsibilities.
- External dependencies (databases, queues, third-party services).
- Output workspace path (for example: `architecture/workspace.dsl`).

### Command/snippet workflow
1. Create output directory:
   ```bash
   mkdir -p architecture
   ```
2. Create the workspace DSL file:
   ```bash
   cat > architecture/workspace.dsl <<'DSL'
   workspace "<System Name>" "<System Description>" {
     model {
       user = person "<Persona>" "<Persona goal>"

       softwareSystem = softwareSystem "<System Name>" "<System Description>" {
         webapp = container "Web App" "User-facing frontend" "React"
         api = container "API" "Business logic and orchestration" "Kotlin + Spring Boot"
         db = container "Database" "System of record" "PostgreSQL"

         webapp -> api "Calls"
         api -> db "Reads/Writes"
       }

       user -> webapp "Uses"
     }

     views {
       systemContext softwareSystem "SystemContext" {
         include *
         autoLayout
       }

       container softwareSystem "Containers" {
         include *
         autoLayout
       }

       theme default
     }
   }
   DSL
   ```
3. Validate syntax:
   ```bash
   structurizr validate -workspace architecture/workspace.dsl
   ```

### Expected output format
- A valid DSL file at the requested path.
- Validation output indicating success (no syntax errors).
- Optional summary block:
  ```text
  Workspace: architecture/workspace.dsl
  Views: SystemContext, Containers
  Validation: PASS
  ```

### Validation checklist
- [ ] Workspace file exists at specified path.
- [ ] All required actors, systems, and relationships are present.
- [ ] `structurizr validate` exits with status code `0`.
- [ ] At least one context and one container view are defined.

## Standard Task 2: Export static architecture site from DSL

### Required inputs
- Path to Structurizr DSL workspace.
- Output directory for static site artifacts.
- Export format target (`static` or `plantuml/mermaid` bundle as needed).

### Command/snippet workflow
1. Prepare output directory:
   ```bash
   mkdir -p docs/architecture
   ```
2. Export static site:
   ```bash
   structurizr export \
     -workspace architecture/workspace.dsl \
     -format static \
     -output docs/architecture
   ```
3. (Optional) Generate additional diagram format:
   ```bash
   structurizr export \
     -workspace architecture/workspace.dsl \
     -format plantuml \
     -output docs/architecture/plantuml
   ```
4. Verify generated files:
   ```bash
   test -f docs/architecture/index.html
   ```

### Expected output format
- `docs/architecture/index.html` and related asset files.
- Optional supplemental diagram directory.
- Result summary:
  ```text
  Export path: docs/architecture
  Primary artifact: index.html
  Optional artifacts: plantuml/*.puml
  ```

### Validation checklist
- [ ] Export command completes with exit code `0`.
- [ ] `index.html` exists in target directory.
- [ ] Assets folder and at least one view artifact are present.
- [ ] Links load correctly when served locally.

## Standard Task 3: Add deployment view for environment topology

### Required inputs
- Existing workspace DSL path.
- Target environment name (for example `Production`).
- Deployment nodes/infrastructure services.
- Container-to-node mapping requirements.

### Command/snippet workflow
1. Add deployment environment and nodes in the `model` section:
   ```dsl
   production = deploymentEnvironment "Production" {
     k8s = deploymentNode "Kubernetes Cluster" {
       webappInstance = containerInstance webapp
       apiInstance = containerInstance api
     }
     dbNode = deploymentNode "Managed PostgreSQL" {
       dbInstance = containerInstance db
     }
   }
   ```
2. Add deployment view under `views`:
   ```dsl
   deployment softwareSystem production "ProductionDeployment" {
     include *
     autoLayout
   }
   ```
3. Re-validate and export:
   ```bash
   structurizr validate -workspace architecture/workspace.dsl
   structurizr export -workspace architecture/workspace.dsl -format static -output docs/architecture
   ```

### Expected output format
- Updated DSL including `deploymentEnvironment` and `deployment` view.
- Validation and export success output.
- Summary:
  ```text
  Deployment view: ProductionDeployment
  Environment: Production
  Validation: PASS
  Export: docs/architecture
  ```

### Validation checklist
- [ ] Deployment environment exists in `model`.
- [ ] Deployment view references intended environment.
- [ ] Container instances map to valid containers.
- [ ] Validation and export commands succeed.
