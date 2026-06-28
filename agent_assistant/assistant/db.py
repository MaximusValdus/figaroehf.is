"""Database engine and session management (SQLite)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings
from .models import Base


def make_engine(database_url: str | None = None):
    """Create a SQLAlchemy engine for the given (or configured) URL."""
    url = database_url or get_settings().database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args, future=True)


# Default engine/sessionmaker used by the app & CLI.
engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db(target_engine=None) -> None:
    """Create all tables if they do not yet exist."""
    Base.metadata.create_all(bind=target_engine or engine)


@contextmanager
def session_scope(factory: sessionmaker | None = None) -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    factory = factory or SessionLocal
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    """FastAPI dependency that yields a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
