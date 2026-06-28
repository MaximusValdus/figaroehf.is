"""Connectors integrate the assistant with external systems.

For the MVP every connector is a deterministic in-memory mock so the app
runs with no credentials and no outbound network calls. Swapping in a real
implementation means subclassing the base classes in ``base.py``.
"""

from .base import (
    CalendarConnector,
    Connectors,
    EmailConnector,
    NotesConnector,
    TasksConnector,
)
from .calendar import MockCalendarConnector
from .email import MockEmailConnector
from .notes import MockNotesConnector
from .tasks import MockTasksConnector


def build_mock_connectors() -> Connectors:
    """Return a bundle of seeded mock connectors."""
    return Connectors(
        calendar=MockCalendarConnector(),
        tasks=MockTasksConnector(),
        notes=MockNotesConnector(),
        email=MockEmailConnector(),
    )


__all__ = [
    "CalendarConnector",
    "TasksConnector",
    "NotesConnector",
    "EmailConnector",
    "Connectors",
    "MockCalendarConnector",
    "MockTasksConnector",
    "MockNotesConnector",
    "MockEmailConnector",
    "build_mock_connectors",
]
