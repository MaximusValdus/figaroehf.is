"""Daily brief generation.

The brief is assembled entirely from READ tools, so generating it never
triggers the approval workflow. The result is rendered to Markdown and
persisted to memory (the ``briefs`` table).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from sqlalchemy.orm import Session

from ..models import ApprovalStatus, BriefRecord
from ..tools.registry import ToolRegistry
from .approvals import list_approvals


@dataclass
class Brief:
    """Structured daily brief, separate from its Markdown rendering."""

    brief_date: date
    owner_name: str
    events: list[dict] = field(default_factory=list)
    tasks: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)
    pending_approvals: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Daily Brief — {self.brief_date.isoformat()}")
        lines.append("")
        lines.append(f"Good morning, {self.owner_name}.")
        lines.append("")

        lines.append(f"## Schedule ({len(self.events)})")
        if self.events:
            for ev in self.events:
                start = ev.get("start", "")
                clock = start.split("T")[1][:5] if "T" in start else start
                lines.append(f"- {clock} — {ev.get('title', '')}")
        else:
            lines.append("- Nothing scheduled. A clear day.")
        lines.append("")

        lines.append(f"## Open tasks ({len(self.tasks)})")
        if self.tasks:
            for task in self.tasks:
                due = f" (due {task['due']})" if task.get("due") else ""
                lines.append(f"- [ ] {task.get('title', '')}{due}")
        else:
            lines.append("- No open tasks. ")
        lines.append("")

        lines.append(f"## Recent notes ({len(self.notes)})")
        if self.notes:
            for note in self.notes:
                lines.append(f"- {note.get('text', '')}")
        else:
            lines.append("- No notes.")
        lines.append("")

        if self.pending_approvals:
            lines.append(f"## Awaiting your approval ({len(self.pending_approvals)})")
            for summary in self.pending_approvals:
                lines.append(f"- {summary}")
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"


def build_brief(
    registry: ToolRegistry,
    *,
    owner_name: str,
    on: date | None = None,
    session: Session | None = None,
) -> Brief:
    """Assemble a :class:`Brief` from READ tools (and pending approvals)."""
    on = on or date.today()

    events = registry.execute("calendar.list_events", {"day": on.isoformat()}).data or []
    tasks = registry.execute("tasks.list_tasks", {"include_done": False}).data or []
    notes = registry.execute("notes.list_notes", {"limit": 3}).data or []

    pending: list[str] = []
    if session is not None:
        pending = [
            a.summary
            for a in list_approvals(session, status=ApprovalStatus.PENDING)
        ]

    return Brief(
        brief_date=on,
        owner_name=owner_name,
        events=events,
        tasks=tasks,
        notes=notes,
        pending_approvals=pending,
    )


def generate_and_store(
    registry: ToolRegistry,
    session: Session,
    *,
    owner_name: str,
    on: date | None = None,
) -> tuple[Brief, str]:
    """Build a brief, persist it to memory, and return (brief, markdown)."""
    brief = build_brief(registry, owner_name=owner_name, on=on, session=session)
    markdown = brief.to_markdown()
    session.add(BriefRecord(brief_date=brief.brief_date.isoformat(), content=markdown))
    return brief, markdown
