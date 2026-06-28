"""Pydantic request/response models for the HTTP API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ToolInvocation(BaseModel):
    name: str = Field(..., description="Registered tool name, e.g. 'tasks.create_task'.")
    params: dict[str, Any] = Field(default_factory=dict)


class ToolResultOut(BaseModel):
    status: str
    data: Any | None = None
    message: str = ""
    approval_id: int | None = None


class ApprovalOut(BaseModel):
    id: int
    tool_name: str
    summary: str
    status: str

    @classmethod
    def from_model(cls, approval) -> "ApprovalOut":
        return cls(
            id=approval.id,
            tool_name=approval.tool_name,
            summary=approval.summary,
            status=approval.status,
        )


class BriefOut(BaseModel):
    date: str
    markdown: str
    events: list[dict]
    tasks: list[dict]
    notes: list[dict]
    pending_approvals: list[str]
