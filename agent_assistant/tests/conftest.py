"""Shared test fixtures: an isolated in-memory database and registry."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assistant.connectors import build_mock_connectors
from assistant.db import init_db
from assistant.tools.registry import build_registry


@pytest.fixture
def session_factory():
    """A fresh in-memory SQLite database per test."""
    engine = create_engine("sqlite:///:memory:", future=True)
    init_db(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


@pytest.fixture
def session(session_factory):
    sess = session_factory()
    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture
def connectors():
    return build_mock_connectors()


@pytest.fixture
def registry(connectors):
    """Registry with the approval workflow enabled (auto_approve off)."""
    return build_registry(connectors, auto_approve=False)
