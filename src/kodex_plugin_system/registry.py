"""Simple in-memory capability index for plugins."""

from __future__ import annotations

from collections import defaultdict

from .base import Plugin


class CapabilityRegistry:
    def __init__(self) -> None:
        self._by_capability: dict[str, list[Plugin]] = defaultdict(list)

    def index(self, plugin: Plugin) -> None:
        for capability in plugin.manifest.capabilities:
            self._by_capability[capability].append(plugin)

    def index_many(self, plugins: tuple[Plugin, ...] | list[Plugin]) -> None:
        for plugin in plugins:
            self.index(plugin)

    def get(self, capability: str) -> tuple[Plugin, ...]:
        return tuple(self._by_capability.get(capability, []))

    def all_capabilities(self) -> tuple[str, ...]:
        return tuple(sorted(self._by_capability.keys()))

    def describe(self) -> dict[str, list[str]]:
        return {
            capability: [plugin.manifest.name for plugin in plugins]
            for capability, plugins in sorted(self._by_capability.items())
        }
