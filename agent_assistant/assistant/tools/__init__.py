"""Tool interface, permission model, and registry."""

from .base import Permission, Tool, ToolResult
from .registry import ToolRegistry, build_registry

__all__ = [
    "Permission",
    "Tool",
    "ToolResult",
    "ToolRegistry",
    "build_registry",
]
