"""Note tools."""

from __future__ import annotations

from typing import Any

from ..connectors.base import NotesConnector
from .base import Permission, Tool


class ListNotesTool(Tool):
    name = "notes.list_notes"
    description = "List the most recent notes."
    permission = Permission.READ

    def __init__(self, connector: NotesConnector) -> None:
        self.connector = connector

    def run(self, limit: int = 5, **_: Any) -> list[dict]:
        return self.connector.list_notes(limit=int(limit))


class CreateNoteTool(Tool):
    name = "notes.create_note"
    description = "Save a new note. Requires approval."
    permission = Permission.WRITE

    def __init__(self, connector: NotesConnector) -> None:
        self.connector = connector

    def run(self, text: str, **_: Any) -> dict:
        return self.connector.create_note(text=text)

    def summarize(self, **params: Any) -> str:
        text = str(params.get("text", ""))
        preview = text if len(text) <= 40 else text[:37] + "..."
        return f"Save note {preview!r}"
