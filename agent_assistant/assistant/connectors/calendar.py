"""In-memory mock calendar connector with deterministic seed data."""

from __future__ import annotations

from datetime import date

from .base import CalendarConnector

# Seed events keyed by weekday (0 = Monday) so any test date is populated.
_SEED_BY_WEEKDAY: dict[int, list[dict]] = {
    0: [
        {"title": "Weekly planning", "start": "09:00", "end": "09:30"},
        {"title": "1:1 with Anna", "start": "14:00", "end": "14:30"},
    ],
    1: [{"title": "Client call — Figaro", "start": "11:00", "end": "12:00"}],
    2: [
        {"title": "Deep work block", "start": "09:00", "end": "11:00"},
        {"title": "Lunch with investor", "start": "12:30", "end": "13:30"},
    ],
    3: [{"title": "Product review", "start": "15:00", "end": "16:00"}],
    4: [{"title": "Demo & retro", "start": "10:00", "end": "11:00"}],
    5: [],
    6: [],
}


class MockCalendarConnector(CalendarConnector):
    def __init__(self) -> None:
        self._created: list[dict] = []
        self._next_id = 1000

    def list_events(self, day: date) -> list[dict]:
        events: list[dict] = []
        for ev in _SEED_BY_WEEKDAY.get(day.weekday(), []):
            events.append(
                {
                    "title": ev["title"],
                    "start": f"{day.isoformat()}T{ev['start']}:00",
                    "end": f"{day.isoformat()}T{ev['end']}:00",
                }
            )
        # Include any events created (and approved) for this day.
        events.extend(e for e in self._created if e["start"].startswith(day.isoformat()))
        return sorted(events, key=lambda e: e["start"])

    def create_event(self, title: str, start: str, end: str | None = None) -> dict:
        event = {"id": self._next_id, "title": title, "start": start, "end": end}
        self._next_id += 1
        self._created.append(event)
        return event
