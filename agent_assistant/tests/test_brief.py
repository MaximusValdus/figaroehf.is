"""Tests for daily brief generation."""

from __future__ import annotations

from datetime import date

from assistant.models import BriefRecord
from assistant.services import brief as brief_service


# A Monday — the mock calendar seeds two events on weekday 0.
MONDAY = date(2026, 6, 29)
SATURDAY = date(2026, 7, 4)  # weekday 5 -> no events


def test_brief_collects_events_tasks_and_notes(registry):
    brief = brief_service.build_brief(registry, owner_name="Valdimar", on=MONDAY)

    assert brief.brief_date == MONDAY
    # Seeded Monday events.
    titles = [e["title"] for e in brief.events]
    assert "Weekly planning" in titles
    assert "1:1 with Anna" in titles
    # Only open tasks are included (the seeded done task is excluded).
    assert brief.tasks, "expected open tasks"
    assert all(not t["done"] for t in brief.tasks)
    # Notes are present and capped at 3.
    assert 0 < len(brief.notes) <= 3


def test_brief_markdown_has_expected_sections(registry):
    brief = brief_service.build_brief(registry, owner_name="Valdimar", on=MONDAY)
    md = brief.to_markdown()

    assert "# Daily Brief — 2026-06-29" in md
    assert "Good morning, Valdimar." in md
    assert "## Schedule" in md
    assert "## Open tasks" in md
    assert "## Recent notes" in md
    # Event times are rendered as HH:MM.
    assert "09:00 — Weekly planning" in md


def test_brief_handles_empty_day(registry):
    brief = brief_service.build_brief(registry, owner_name="V", on=SATURDAY)
    md = brief.to_markdown()
    assert brief.events == []
    assert "Nothing scheduled" in md


def test_brief_surfaces_pending_approvals(registry, session):
    # Request a WRITE action so it lands in the pending-approval queue.
    result = registry.execute(
        "tasks.create_task", {"title": "Prepare board deck"}, session=session
    )
    session.commit()
    assert result.pending

    brief = brief_service.build_brief(
        registry, owner_name="V", on=MONDAY, session=session
    )
    assert any("Prepare board deck" in s for s in brief.pending_approvals)
    assert "## Awaiting your approval" in brief.to_markdown()


def test_generate_and_store_persists_brief(registry, session):
    _, markdown = brief_service.generate_and_store(
        registry, session, owner_name="Valdimar", on=MONDAY
    )
    session.commit()

    records = session.query(BriefRecord).all()
    assert len(records) == 1
    assert records[0].brief_date == "2026-06-29"
    assert records[0].content == markdown
