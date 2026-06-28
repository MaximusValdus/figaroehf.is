"""Shared dependencies for the API layer."""

from __future__ import annotations

from functools import lru_cache

from ..config import get_settings
from ..connectors import build_mock_connectors
from ..tools.registry import ToolRegistry, build_registry


@lru_cache
def get_registry() -> ToolRegistry:
    """Return a process-wide registry wired to mock connectors.

    Cached so the in-memory mock connectors keep their state across requests
    within a single running process.
    """
    settings = get_settings()
    connectors = build_mock_connectors()
    return build_registry(connectors, auto_approve=settings.auto_approve)
