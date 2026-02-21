"""Example local plugin loaded from ./plugins."""

from __future__ import annotations

from kodex_plugin_system.base import PluginManifest


class ContextEnricherPlugin:
    manifest = PluginManifest(
        name="context-enricher",
        version="0.1.0",
        description="Adds extra prompt context before execution.",
        capabilities=("prompt.preprocess", "context.enrich"),
    )

    def activate(self, context: dict[str, object]) -> None:
        self._org = context.get("org", "default-org")

    def handle_hook(self, hook: str, payload: dict[str, object]) -> dict[str, object] | None:
        if hook != "prompt.preprocess":
            return None

        text = str(payload.get("text", ""))
        return {
            "plugin": self.manifest.name,
            "text": f"[{self._org}] {text}".strip(),
        }


def get_plugin() -> ContextEnricherPlugin:
    return ContextEnricherPlugin()
