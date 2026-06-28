"""The tool registry: dispatch, permission enforcement, approval gating."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from ..connectors.base import Connectors
from ..models import Approval, ApprovalStatus
from .base import Permission, Tool, ToolResult
from .calendar_tool import CreateEventTool, ListEventsTool
from .email_tool import SendEmailTool
from .notes_tool import CreateNoteTool, ListNotesTool
from .tasks_tool import CompleteTaskTool, CreateTaskTool, ListTasksTool


class ToolRegistry:
    """Holds the available tools and runs them with permission checks.

    READ tools execute immediately. WRITE tools are routed through the
    approval workflow: a pending ``Approval`` row is created and the tool is
    *not* executed until that approval is granted (unless ``auto_approve``).
    """

    def __init__(self, tools: list[Tool], *, auto_approve: bool = False) -> None:
        self._tools: dict[str, Tool] = {t.name: t for t in tools}
        self.auto_approve = auto_approve

    # -- introspection -------------------------------------------------
    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def requires_approval(self, name: str) -> bool:
        return self.get(name).permission is Permission.WRITE and not self.auto_approve

    # -- execution -----------------------------------------------------
    def execute(
        self, name: str, params: dict[str, Any] | None = None, session: Session | None = None
    ) -> ToolResult:
        """Run a tool, enforcing its permission level.

        For WRITE tools (without auto-approve) a ``session`` is required so a
        pending approval can be persisted.
        """
        params = params or {}
        try:
            tool = self.get(name)
        except KeyError as exc:
            return ToolResult(status="error", message=str(exc))

        if tool.permission is Permission.READ or self.auto_approve:
            return self._run_tool(tool, params)

        # WRITE without auto-approve -> create a pending approval.
        if session is None:
            raise ValueError(
                f"Tool {name!r} requires approval; a database session is required."
            )
        approval = Approval(
            tool_name=name,
            params_json=json.dumps(params),
            summary=tool.summarize(**params),
            status=ApprovalStatus.PENDING,
        )
        session.add(approval)
        session.flush()  # assign an id without forcing a commit
        return ToolResult(
            status="pending_approval",
            approval_id=approval.id,
            message=f"Approval required: {approval.summary}",
        )

    def execute_approved(self, name: str, params: dict[str, Any]) -> ToolResult:
        """Run a previously-approved WRITE tool. Bypasses the approval gate."""
        try:
            tool = self.get(name)
        except KeyError as exc:
            return ToolResult(status="error", message=str(exc))
        return self._run_tool(tool, params)

    @staticmethod
    def _run_tool(tool: Tool, params: dict[str, Any]) -> ToolResult:
        try:
            data = tool.run(**params)
        except Exception as exc:  # surface tool failures as error results
            return ToolResult(status="error", message=f"{type(exc).__name__}: {exc}")
        return ToolResult(status="ok", data=data)


def build_registry(connectors: Connectors, *, auto_approve: bool = False) -> ToolRegistry:
    """Construct a registry wired to the given connectors."""
    tools: list[Tool] = [
        ListEventsTool(connectors.calendar),
        CreateEventTool(connectors.calendar),
        ListTasksTool(connectors.tasks),
        CreateTaskTool(connectors.tasks),
        CompleteTaskTool(connectors.tasks),
        ListNotesTool(connectors.notes),
        CreateNoteTool(connectors.notes),
        SendEmailTool(connectors.email),
    ]
    return ToolRegistry(tools, auto_approve=auto_approve)
