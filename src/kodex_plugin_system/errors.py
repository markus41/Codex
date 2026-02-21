"""Typed exceptions for plugin runtime errors."""

from __future__ import annotations


class PluginError(Exception):
    """Base class for plugin-related errors."""


class PluginValidationError(PluginError):
    """Raised when plugin objects do not match runtime expectations."""


class PluginLoadError(PluginError):
    """Raised when plugin loading fails."""


class HookExecutionError(PluginError):
    """Raised when a plugin hook execution fails in fail-fast mode."""
