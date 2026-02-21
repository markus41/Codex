# Kodex Plugin System (Codex-Style Extensibility)

This repository now includes a lightweight plugin runtime that can be embedded into a Kodex-style coding agent.

## 10 high-impact developer experience upgrades added

1. **Typed runtime exceptions** (`PluginLoadError`, `PluginValidationError`, `HookExecutionError`) for cleaner debugging and integration behavior.
2. **Manifest normalization + validation** to prevent malformed plugin metadata from silently entering runtime.
3. **Duplicate plugin-name guardrails** to avoid ambiguous routing or accidental override.
4. **Load diagnostics ledger** that records loaded/skipped/error states for every plugin source.
5. **Strict mode (`continue_on_error=False`)** for CI pipelines that should fail immediately on plugin issues.
6. **Resilient hook execution** with optional `fail_fast` behavior for production safety vs exploratory usage.
7. **Machine-readable doctor report** (`doctor_report`) for troubleshooting and health checks.
8. **CLI `doctor` command** to inspect plugin health without writing custom scripts.
9. **CLI `scaffold` command** to generate starter plugin files quickly.
10. **CLI JSON output + capabilities command** to simplify scripting and automated tooling around plugins.

## What this gives you

- **Plugin contract** via `PluginManifest` + `Plugin` protocol.
- **Two discovery modes**:
  - Local file plugins (`./plugins/*.py`) for quick prototyping.
  - Python package entry points (`kodex.plugins`) for installable third-party extensions.
- **Hook/event model** with `emit(hook, payload)`.
- **Capability indexing** so an orchestrator can route tasks to plugins by capability.
- **CLI** for listing plugins, dispatching hooks, diagnostics, scaffolding, and capability introspection.

## Why this is similar to Claude-style plugin systems

Claude-style extension systems generally have:
1. A clear plugin manifest/identity.
2. Runtime discovery/loading.
3. A contract for request/response hooks.
4. Optional tool routing by declared capabilities.

This repository implements all four in a minimal, production-friendly Python baseline.

## Quick start

```bash
PYTHONPATH=src python -m kodex_plugin_system.cli list
PYTHONPATH=src python -m kodex_plugin_system.cli capabilities
PYTHONPATH=src python -m kodex_plugin_system.cli doctor
PYTHONPATH=src python -m kodex_plugin_system.cli emit prompt.preprocess --payload '{"text":"hello"}'
```

## Next steps for a full "Kodex marketplace"

1. Add signed plugin manifests and trust policies.
2. Add plugin sandboxing (subprocess/container boundaries).
3. Add plugin permission scopes (filesystem/network/model access).
4. Add remote plugin registry metadata + semantic version resolution.
5. Add per-plugin metrics, timeout limits, and circuit breakers.
