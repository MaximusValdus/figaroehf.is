"""Abstract connector interfaces and the connector bundle."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


class CalendarConnector(ABC):
    @abstractmethod
    def list_events(self, day: date) -> list[dict]:
        """Return events occurring on ``day``."""

    @abstractmethod
    def create_event(self, title: str, start: str, end: str | None = None) -> dict:
        """Create a calendar event and return it."""


class TasksConnector(ABC):
    @abstractmethod
    def list_tasks(self, include_done: bool = False) -> list[dict]:
        """Return tasks, optionally including completed ones."""

    @abstractmethod
    def create_task(self, title: str, due: str | None = None) -> dict:
        """Create a task and return it."""

    @abstractmethod
    def complete_task(self, task_id: int) -> dict:
        """Mark a task complete and return it."""


class NotesConnector(ABC):
    @abstractmethod
    def list_notes(self, limit: int = 5) -> list[dict]:
        """Return the most recent notes."""

    @abstractmethod
    def create_note(self, text: str) -> dict:
        """Create a note and return it."""


class EmailConnector(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send an email. Mock implementations MUST NOT deliver anything."""

    @abstractmethod
    def outbox(self) -> list[dict]:
        """Return messages that were 'sent' (captured locally)."""


@dataclass
class Connectors:
    """A bundle of the connectors the tools depend on."""

    calendar: CalendarConnector
    tasks: TasksConnector
    notes: NotesConnector
    email: EmailConnector
