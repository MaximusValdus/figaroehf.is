"""Smoke tests for the HTTP API."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from assistant import db as db_module
from assistant.api import deps
from assistant.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A TestClient backed by a temporary database and a fresh registry."""
    engine = db_module.make_engine(f"sqlite:///{tmp_path/'api.db'}")
    from sqlalchemy.orm import sessionmaker

    factory = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    monkeypatch.setattr(db_module, "engine", engine)
    monkeypatch.setattr(db_module, "SessionLocal", factory)
    deps.get_registry.cache_clear()
    db_module.init_db(engine)
    with TestClient(app) as c:
        yield c
    deps.get_registry.cache_clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_tools_reports_permissions(client):
    tools = {t["name"]: t for t in client.get("/tools").json()}
    assert tools["tasks.list_tasks"]["requires_approval"] is False
    assert tools["email.send_email"]["requires_approval"] is True


def test_brief_endpoint(client):
    body = client.get("/brief?on=2026-06-29").json()
    assert body["date"] == "2026-06-29"
    assert "# Daily Brief" in body["markdown"]


def test_write_tool_via_api_needs_approval_then_executes(client):
    resp = client.post(
        "/tools/execute",
        json={"name": "tasks.create_task", "params": {"title": "From API"}},
    ).json()
    assert resp["status"] == "pending_approval"
    approval_id = resp["approval_id"]

    pending = client.get("/approvals?status=pending").json()
    assert any(p["id"] == approval_id for p in pending)

    approved = client.post(f"/approvals/{approval_id}/approve").json()
    assert approved["status"] == "ok"
    assert approved["data"]["title"] == "From API"
