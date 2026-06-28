"""Task tools."""

from __future__ import annotations

from typing import Any

from ..connectors.base import TasksConnector
from .base import Permission, Tool


class ListTasksTool(Tool):
    name = "tasks.list_tasks"
    description = "List open tasks (optionally include completed ones)."
    permission = Permission.READ

    def __init__(self, connector: TasksConnector) -> None:
        self.connector = connector

    def run(self, include_done: bool = False, **_: Any) -> list[dict]:
        return self.connector.list_tasks(include_done=include_done)


class CreateTaskTool(Tool):
    name = "tasks.create_task"
    description = "Create a new task. Requires approval."
    permission = Permission.WRITE

    def __init__(self, connector: TasksConnector) -> None:
        self.connector = connector

    def run(self, title: str, due: str | None = None, **_: Any) -> dict:
        return self.connector.create_task(title=title, due=due)

    def summarize(self, **params: Any) -> str:
        return f"Create task {params.get('title')!r}"


class CompleteTaskTool(Tool):
    name = "tasks.complete_task"
    description = "Mark a task complete. Requires approval."
    permission = Permission.WRITE

    def __init__(self, connector: TasksConnector) -> None:
        self.connector = connector

    def run(self, task_id: int, **_: Any) -> dict:
        return self.connector.complete_task(task_id=int(task_id))

    def summarize(self, **params: Any) -> str:
        return f"Complete task #{params.get('task_id')}"
