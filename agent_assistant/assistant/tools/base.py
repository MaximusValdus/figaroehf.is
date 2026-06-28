"""The tool interface and permission model.

Every capability the assistant has is exposed as a ``Tool``. A tool declares
a ``permission``:

    * READ  — safe, side-effect-free; executes immediately.
    * WRITE — mutates state or has an external effect; gated by the approval
              workflow unless ``auto_approve`` is enabled.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"


@dataclass
class ToolResult:
    """The outcome of attempting to run a tool."""

    status: str  # "ok" | "pending_approval" | "error"
    data: Any = None
    message: str = ""
    approval_id: int | None = None

    @property
    def ok(self) -> bool:
        return self.status == "ok"

    @property
    def pending(self) -> bool:
        return self.status == "pending_approval"


class Tool(ABC):
    """Base class for all tools."""

    name: str
    description: str
    permission: Permission

    @abstractmethod
    def run(self, **params: Any) -> Any:
        """Execute the tool and return raw data.

        This performs the actual side effect (for WRITE tools) and is only
        called after any required approval has been granted.
        """

    def summarize(self, **params: Any) -> str:
        """A short, human-readable description of a pending invocation."""
        if params:
            args = ", ".join(f"{k}={v!r}" for k, v in params.items())
            return f"{self.name}({args})"
        return f"{self.name}()"
