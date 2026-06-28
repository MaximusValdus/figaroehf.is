"""SQLAlchemy models that make up the assistant's memory."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class ApprovalStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Approval(Base):
    """A WRITE action awaiting (or having received) a human decision."""

    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tool_name: Mapped[str] = mapped_column(String(128), nullable=False)
    # JSON-encoded parameters captured at request time.
    params_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    summary: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default=ApprovalStatus.PENDING
    )
    # JSON-encoded result once executed.
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class BriefRecord(Base):
    """A historical record of a generated daily brief (memory)."""

    __tablename__ = "briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brief_date: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


class MemoryEntry(Base):
    """A simple key/value fact the assistant remembers across sessions."""

    __tablename__ = "memory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow
    )
