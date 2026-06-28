"""Calendar tools."""

from __future__ import annotations

from datetime import date
from typing import Any

from ..connectors.base import CalendarConnector
from .base import Permission, Tool


class ListEventsTool(Tool):
    name = "calendar.list_events"
    description = "List calendar events for a given day (YYYY-MM-DD)."
    permission = Permission.READ

    def __init__(self, connector: CalendarConnector) -> None:
        self.connector = connector

    def run(self, day: str | None = None, **_: Any) -> list[dict]:
        target = date.fromisoformat(day) if day else date.today()
        return self.connector.list_events(target)


class CreateEventTool(Tool):
    name = "calendar.create_event"
    description = "Create a calendar event. Requires approval."
    permission = Permission.WRITE

    def __init__(self, connector: CalendarConnector) -> None:
        self.connector = connector

    def run(self, title: str, start: str, end: str | None = None, **_: Any) -> dict:
        return self.connector.create_event(title=title, start=start, end=end)

    def summarize(self, **params: Any) -> str:
        return f"Create calendar event {params.get('title')!r} at {params.get('start')}"
