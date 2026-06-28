"""The approval workflow: list, approve (execute), and reject pending actions."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Approval, ApprovalStatus
from ..tools.base import ToolResult
from ..tools.registry import ToolRegistry


def list_approvals(session: Session, status: str | None = None) -> list[Approval]:
    stmt = select(Approval).order_by(Approval.created_at.desc())
    if status:
        stmt = stmt.where(Approval.status == status)
    return list(session.scalars(stmt))


def get_approval(session: Session, approval_id: int) -> Approval | None:
    return session.get(Approval, approval_id)


def approve(session: Session, registry: ToolRegistry, approval_id: int) -> ToolResult:
    """Approve a pending action and execute it.

    Raises ``KeyError`` if the approval does not exist and ``ValueError`` if
    it is not pending.
    """
    approval = session.get(Approval, approval_id)
    if approval is None:
        raise KeyError(f"No approval with id {approval_id}")
    if approval.status != ApprovalStatus.PENDING:
        raise ValueError(f"Approval {approval_id} is already {approval.status}")

    params = json.loads(approval.params_json)
    result = registry.execute_approved(approval.tool_name, params)

    approval.status = ApprovalStatus.APPROVED
    approval.resolved_at = datetime.now(timezone.utc)
    approval.result_json = json.dumps(result.data, default=str)
    session.add(approval)
    return result


def reject(session: Session, approval_id: int) -> Approval:
    """Reject a pending action without executing it."""
    approval = session.get(Approval, approval_id)
    if approval is None:
        raise KeyError(f"No approval with id {approval_id}")
    if approval.status != ApprovalStatus.PENDING:
        raise ValueError(f"Approval {approval_id} is already {approval.status}")
    approval.status = ApprovalStatus.REJECTED
    approval.resolved_at = datetime.now(timezone.utc)
    session.add(approval)
    return approval
