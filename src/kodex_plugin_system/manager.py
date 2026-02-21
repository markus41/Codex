"""Plugin manager and discovery mechanics."""

from __future__ import annotations

import traceback
from dataclasses import dataclass
from importlib.metadata import entry_points
from pathlib import Path
from types import ModuleType
from typing import Any

from .base import Plugin, PluginManifest
from .errors import HookExecutionError, PluginLoadError, PluginValidationError


@dataclass(frozen=True)
class LoadDiagnostic:
    source: str
    plugin_name: str
    status: str
    message: str


class PluginManager:
    """Loads plugins and invokes hooks across all active plugins."""

    def __init__(self, *, continue_on_error: bool = True, default_context: dict[str, Any] | None = None) -> None:
        self._plugins: list[Plugin] = []
        self._plugin_names: set[str] = set()
        self._diagnostics: list[LoadDiagnostic] = []
        self.continue_on_error = continue_on_error
        self.default_context = default_context or {}

    @property
    def plugins(self) -> tuple[Plugin, ...]:
        return tuple(self._plugins)

    @property
    def diagnostics(self) -> tuple[LoadDiagnostic, ...]:
        return tuple(self._diagnostics)

    def register(self, plugin: Plugin, *, context: dict[str, Any] | None = None, source: str = "runtime") -> None:
        manifest = self._validate_plugin(plugin)
        if manifest.name in self._plugin_names:
            raise PluginValidationError(f"Duplicate plugin name '{manifest.name}' is not allowed")

        runtime_context = {**self.default_context, **(context or {})}
        plugin.activate(runtime_context)
        self._plugins.append(plugin)
        self._plugin_names.add(manifest.name)
        self._diagnostics.append(LoadDiagnostic(source=source, plugin_name=manifest.name, status="loaded", message="ok"))

    def load_entry_point_plugins(self, group: str = "kodex.plugins") -> int:
        loaded = 0
        for ep in entry_points(group=group):
            try:
                plugin_cls = ep.load()
                plugin = plugin_cls()
                self.register(plugin, source=f"entrypoint:{ep.name}")
                loaded += 1
            except Exception as exc:  # noqa: BLE001
                if not self._record_or_raise_load_error(f"entrypoint:{ep.name}", str(exc), exc):
                    break
        return loaded

    def load_file_plugins(self, directory: str | Path, *, pattern: str = "*.py") -> int:
        plugin_dir = Path(directory)
        if not plugin_dir.exists():
            self._diagnostics.append(LoadDiagnostic(source=str(plugin_dir), plugin_name="-", status="skipped", message="plugin directory missing"))
            return 0

        loaded = 0
        for path in sorted(plugin_dir.glob(pattern)):
            if path.name.startswith("_"):
                continue
            module_name = f"kodex_local_plugin_{path.stem}"
            try:
                module = _import_module_from_path(module_name, path)
                plugin_factory = getattr(module, "get_plugin", None)
                if plugin_factory is None:
                    self._diagnostics.append(LoadDiagnostic(source=str(path), plugin_name="-", status="skipped", message="missing get_plugin()"))
                    continue

                plugin = plugin_factory()
                self.register(plugin, source=str(path))
                loaded += 1
            except Exception as exc:  # noqa: BLE001
                if not self._record_or_raise_load_error(str(path), str(exc), exc):
                    break
        return loaded

    def emit(self, hook: str, payload: dict[str, Any], *, fail_fast: bool = False) -> list[dict[str, Any]]:
        outputs: list[dict[str, Any]] = []
        for plugin in self._plugins:
            try:
                result = plugin.handle_hook(hook, payload)
                if result is not None:
                    outputs.append(result)
            except Exception as exc:  # noqa: BLE001
                if fail_fast:
                    raise HookExecutionError(f"Plugin '{plugin.manifest.name}' failed on hook '{hook}': {exc}") from exc
                outputs.append({"plugin": plugin.manifest.name, "error": str(exc), "hook": hook})
        return outputs

    def list_manifests(self) -> tuple[PluginManifest, ...]:
        return tuple(plugin.manifest for plugin in self._plugins)

    def doctor_report(self) -> dict[str, Any]:
        return {
            "plugin_count": len(self._plugins),
            "plugin_names": sorted(self._plugin_names),
            "diagnostics": [d.__dict__ for d in self._diagnostics],
        }

    def _validate_plugin(self, plugin: Plugin) -> PluginManifest:
        manifest = getattr(plugin, "manifest", None)
        if not isinstance(manifest, PluginManifest):
            raise PluginValidationError("Plugin must expose a PluginManifest as 'manifest'")
        normalized = manifest.normalized()
        normalized.validate()
        plugin.manifest = normalized
        if not callable(getattr(plugin, "activate", None)):
            raise PluginValidationError(f"Plugin '{normalized.name}' is missing activate()")
        if not callable(getattr(plugin, "handle_hook", None)):
            raise PluginValidationError(f"Plugin '{normalized.name}' is missing handle_hook()")
        return normalized

    def _record_or_raise_load_error(self, source: str, message: str, exc: Exception) -> bool:
        self._diagnostics.append(LoadDiagnostic(source=source, plugin_name="-", status="error", message=message))
        if not self.continue_on_error:
            raise PluginLoadError(f"Failed to load plugin from {source}: {message}\n{traceback.format_exc()}") from exc
        return True


def _import_module_from_path(module_name: str, path: Path) -> ModuleType:
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load plugin module from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
