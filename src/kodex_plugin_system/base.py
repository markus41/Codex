"""Core plugin contracts for Kodex extensibility."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .errors import PluginValidationError


@dataclass(frozen=True)
class PluginManifest:
    """Metadata that describes a plugin and how it should be surfaced."""

    name: str
    version: str
    description: str
    capabilities: tuple[str, ...] = field(default_factory=tuple)

    def normalized(self) -> "PluginManifest":
        unique_caps = tuple(sorted({c.strip() for c in self.capabilities if c.strip()}))
        return PluginManifest(
            name=self.name.strip(),
            version=self.version.strip(),
            description=self.description.strip(),
            capabilities=unique_caps,
        )

    def validate(self) -> None:
        if not self.name.strip():
            raise PluginValidationError("Plugin manifest name must be non-empty")
        if not self.version.strip():
            raise PluginValidationError(f"Plugin '{self.name}' must define a version")
        if not self.description.strip():
            raise PluginValidationError(f"Plugin '{self.name}' must define a description")


class Plugin(Protocol):
    """Protocol every Kodex plugin should implement."""

    manifest: PluginManifest

    def activate(self, context: dict[str, Any]) -> None:
        """Initialize plugin state before hooks are invoked."""

    def handle_hook(self, hook: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Handle a named hook and optionally return structured output."""
