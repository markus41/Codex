"""CLI for listing and running plugins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manager import PluginManager

TEMPLATE = '''"""Scaffolded Kodex plugin."""

from __future__ import annotations

from kodex_plugin_system.base import PluginManifest


class MyPlugin:
    manifest = PluginManifest(
        name="my-plugin",
        version="0.1.0",
        description="Describe what your plugin does.",
        capabilities=("hook.name",),
    )

    def activate(self, context: dict[str, object]) -> None:
        self._context = context

    def handle_hook(self, hook: str, payload: dict[str, object]) -> dict[str, object] | None:
        if hook != "hook.name":
            return None
        return {"plugin": self.manifest.name, "payload": payload}


def get_plugin() -> MyPlugin:
    return MyPlugin()
'''


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kodex plugin runtime")
    parser.add_argument("--plugin-dir", default="plugins", help="Directory with local plugins")
    parser.add_argument("--json", action="store_true", help="Print command output as JSON when supported")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List discovered plugins")

    emit = sub.add_parser("emit", help="Emit a hook event")
    emit.add_argument("hook", help="Hook name")
    emit.add_argument("--payload", default="{}", help="JSON payload")
    emit.add_argument("--fail-fast", action="store_true", help="Raise if any plugin hook errors")

    sub.add_parser("doctor", help="Print plugin loader diagnostics")

    scaffold = sub.add_parser("scaffold", help="Create a starter plugin file")
    scaffold.add_argument("name", help="Plugin filename (without .py)")

    sub.add_parser("capabilities", help="List discovered capabilities")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    manager = PluginManager()
    manager.load_file_plugins(Path(args.plugin_dir))
    manager.load_entry_point_plugins()

    if args.command == "list":
        records = [
            {
                "name": m.name,
                "version": m.version,
                "description": m.description,
                "capabilities": list(m.capabilities),
            }
            for m in manager.list_manifests()
        ]
        if args.json:
            print(json.dumps(records, indent=2))
            return
        for r in records:
            caps = ",".join(r["capabilities"]) if r["capabilities"] else "-"
            print(f"{r['name']} v{r['version']} | {caps} | {r['description']}")
        return

    if args.command == "doctor":
        print(json.dumps(manager.doctor_report(), indent=2))
        return

    if args.command == "scaffold":
        plugin_dir = Path(args.plugin_dir)
        plugin_dir.mkdir(parents=True, exist_ok=True)
        plugin_path = plugin_dir / f"{args.name}.py"
        if plugin_path.exists():
            raise SystemExit(f"Refusing to overwrite existing plugin: {plugin_path}")
        plugin_path.write_text(TEMPLATE)
        print(str(plugin_path))
        return

    if args.command == "capabilities":
        capabilities = sorted({c for m in manager.list_manifests() for c in m.capabilities})
        if args.json:
            print(json.dumps(capabilities, indent=2))
            return
        for capability in capabilities:
            print(capability)
        return

    payload = json.loads(args.payload)
    print(json.dumps(manager.emit(args.hook, payload, fail_fast=args.fail_fast), indent=2))


if __name__ == "__main__":
    main()
