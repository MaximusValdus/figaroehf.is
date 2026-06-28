"""Tests for the tool permission model and approval workflow."""

from __future__ import annotations

import pytest

from assistant.connectors import build_mock_connectors
from assistant.models import Approval, ApprovalStatus
from assistant.services import approvals as approvals_service
from assistant.tools.base import Permission
from assistant.tools.registry import build_registry


def test_read_tool_executes_immediately(registry):
    result = registry.execute("tasks.list_tasks", {})
    assert result.ok
    assert isinstance(result.data, list)
    assert result.approval_id is None


def test_write_tool_requires_approval_and_does_not_execute(registry, session, connectors):
    before = len(connectors.tasks.list_tasks(include_done=True))

    result = registry.execute(
        "tasks.create_task", {"title": "Call the bank"}, session=session
    )
    session.commit()

    assert result.pending
    assert result.approval_id is not None
    # The action has NOT run yet — no new task created.
    after = len(connectors.tasks.list_tasks(include_done=True))
    assert after == before
    # A pending approval was recorded.
    approval = session.get(Approval, result.approval_id)
    assert approval.status == ApprovalStatus.PENDING
    assert "Call the bank" in approval.summary


def test_write_tool_requires_session(registry):
    with pytest.raises(ValueError):
        registry.execute("tasks.create_task", {"title": "x"}, session=None)


def test_approving_executes_the_action(registry, session, connectors):
    result = registry.execute(
        "tasks.create_task", {"title": "Call the bank"}, session=session
    )
    session.commit()

    exec_result = approvals_service.approve(session, registry, result.approval_id)
    session.commit()

    assert exec_result.ok
    titles = [t["title"] for t in connectors.tasks.list_tasks(include_done=True)]
    assert "Call the bank" in titles

    approval = session.get(Approval, result.approval_id)
    assert approval.status == ApprovalStatus.APPROVED
    assert approval.resolved_at is not None


def test_rejecting_does_not_execute(registry, session, connectors):
    before = len(connectors.tasks.list_tasks(include_done=True))
    result = registry.execute(
        "tasks.create_task", {"title": "Should not run"}, session=session
    )
    session.commit()

    approvals_service.reject(session, result.approval_id)
    session.commit()

    after = len(connectors.tasks.list_tasks(include_done=True))
    assert after == before
    approval = session.get(Approval, result.approval_id)
    assert approval.status == ApprovalStatus.REJECTED


def test_cannot_approve_twice(registry, session):
    result = registry.execute(
        "tasks.create_task", {"title": "Once"}, session=session
    )
    session.commit()
    approvals_service.approve(session, registry, result.approval_id)
    session.commit()
    with pytest.raises(ValueError):
        approvals_service.approve(session, registry, result.approval_id)


def test_email_is_write_and_never_delivers(registry, session, connectors):
    result = registry.execute(
        "email.send_email",
        {"to": "ceo@example.com", "subject": "Hi", "body": "Test"},
        session=session,
    )
    session.commit()
    assert result.pending  # email always needs approval

    approvals_service.approve(session, registry, result.approval_id)
    session.commit()

    outbox = connectors.email.outbox()
    assert len(outbox) == 1
    # Mock connector captures the message but never delivers it.
    assert outbox[0]["delivered"] is False


def test_auto_approve_executes_write_without_approval():
    connectors = build_mock_connectors()
    registry = build_registry(connectors, auto_approve=True)
    before = len(connectors.tasks.list_tasks(include_done=True))

    result = registry.execute("tasks.create_task", {"title": "Auto task"})
    assert result.ok
    assert len(connectors.tasks.list_tasks(include_done=True)) == before + 1
    assert registry.requires_approval("tasks.create_task") is False


def test_permission_metadata_is_correct(registry):
    assert registry.get("tasks.list_tasks").permission is Permission.READ
    assert registry.get("tasks.create_task").permission is Permission.WRITE
    assert registry.get("email.send_email").permission is Permission.WRITE
    assert registry.requires_approval("calendar.create_event") is True
    assert registry.requires_approval("calendar.list_events") is False


def test_unknown_tool_returns_error(registry):
    result = registry.execute("does.not_exist", {})
    assert result.status == "error"
