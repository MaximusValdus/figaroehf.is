"""In-memory mock notes connector with deterministic seed data."""

from __future__ import annotations

from .base import NotesConnector


class MockNotesConnector(NotesConnector):
    def __init__(self) -> None:
        self._notes: list[dict] = [
            {"id": 1, "text": "Figaro valuation hinges on recurring revenue share."},
            {"id": 2, "text": "Ask legal about the non-compete clause."},
            {"id": 3, "text": "Investor prefers a phased earn-out structure."},
        ]
        self._next_id = 4

    def list_notes(self, limit: int = 5) -> list[dict]:
        # Most recent first.
        return list(reversed(self._notes))[:limit]

    def create_note(self, text: str) -> dict:
        note = {"id": self._next_id, "text": text}
        self._next_id += 1
        self._notes.append(note)
        return note
