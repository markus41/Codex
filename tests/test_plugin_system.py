from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from kodex_plugin_system import CapabilityRegistry, HookExecutionError, PluginLoadError, PluginManager


def _write_plugin(path: Path, body: str) -> None:
    path.write_text(body)


def test_load_local_plugin_and_emit_hook() -> None:
    manager = PluginManager()
    loaded = manager.load_file_plugins(Path("plugins"))

    assert loaded == 1
    outputs = manager.emit("prompt.preprocess", {"text": "hello"})
    assert outputs == [{"plugin": "context-enricher", "text": "[default-org] hello"}]


def test_capability_registry_indexes_discovered_plugins() -> None:
    manager = PluginManager()
    manager.load_file_plugins(Path("plugins"))

    registry = CapabilityRegistry()
    registry.index_many(list(manager.plugins))

    assert registry.all_capabilities() == ("context.enrich", "prompt.preprocess")
    assert registry.describe()["context.enrich"] == ["context-enricher"]


def test_missing_plugin_dir_adds_diagnostic(tmp_path: Path) -> None:
    manager = PluginManager()
    loaded = manager.load_file_plugins(tmp_path / "does-not-exist")

    assert loaded == 0
    assert manager.diagnostics[-1].status == "skipped"


def test_invalid_plugin_factory_is_skipped(tmp_path: Path) -> None:
    plugin_file = tmp_path / "bad.py"
    _write_plugin(plugin_file, "x=1\n")
    manager = PluginManager()

    loaded = manager.load_file_plugins(tmp_path)

    assert loaded == 0
    assert any(d.status == "skipped" and "missing get_plugin" in d.message for d in manager.diagnostics)


def test_strict_mode_raises_on_plugin_load_failure(tmp_path: Path) -> None:
    plugin_file = tmp_path / "explode.py"
    _write_plugin(
        plugin_file,
        "def get_plugin():\n    raise RuntimeError('boom')\n",
    )
    manager = PluginManager(continue_on_error=False)

    with pytest.raises(PluginLoadError):
        manager.load_file_plugins(tmp_path)


def test_emit_fail_fast_raises_hook_error(tmp_path: Path) -> None:
    plugin_file = tmp_path / "hook_boom.py"
    _write_plugin(
        plugin_file,
        "from kodex_plugin_system.base import PluginManifest\n"
        "class P:\n"
        "    manifest = PluginManifest(name='x', version='1', description='d')\n"
        "    def activate(self, context):\n"
        "        pass\n"
        "    def handle_hook(self, hook, payload):\n"
        "        raise RuntimeError('hook failed')\n"
        "def get_plugin():\n"
        "    return P()\n",
    )
    manager = PluginManager()
    manager.load_file_plugins(tmp_path)

    with pytest.raises(HookExecutionError):
        manager.emit("anything", {}, fail_fast=True)


def test_cli_scaffold_and_doctor(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins"
    cmd_scaffold = [
        sys.executable,
        "-m",
        "kodex_plugin_system.cli",
        "--plugin-dir",
        str(plugin_dir),
        "scaffold",
        "sample_plugin",
    ]
    env = {**os.environ, "PYTHONPATH": "src"}
    result = subprocess.run(cmd_scaffold, capture_output=True, text=True, check=True, env=env)
    assert "sample_plugin.py" in result.stdout

    cmd_doctor = [
        sys.executable,
        "-m",
        "kodex_plugin_system.cli",
        "--plugin-dir",
        str(plugin_dir),
        "doctor",
    ]
    doctor = subprocess.run(cmd_doctor, capture_output=True, text=True, check=True, env=env)
    payload = json.loads(doctor.stdout)
    assert payload["plugin_count"] >= 1
