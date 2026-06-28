"""In-memory mock tasks connector with deterministic seed data."""

from __future__ import annotations

from .base import TasksConnector


class MockTasksConnector(TasksConnector):
    def __init__(self) -> None:
        self._tasks: list[dict] = [
            {"id": 1, "title": "Review Figaro contract draft", "due": None, "done": False},
            {"id": 2, "title": "Send Q3 numbers to accountant", "due": None, "done": False},
            {"id": 3, "title": "Book flights for conference", "due": None, "done": False},
            {"id": 4, "title": "File annual report", "due": None, "done": True},
        ]
        self._next_id = 5

    def list_tasks(self, include_done: bool = False) -> list[dict]:
        return [t for t in self._tasks if include_done or not t["done"]]

    def create_task(self, title: str, due: str | None = None) -> dict:
        task = {"id": self._next_id, "title": title, "due": due, "done": False}
        self._next_id += 1
        self._tasks.append(task)
        return task

    def complete_task(self, task_id: int) -> dict:
        for task in self._tasks:
            if task["id"] == task_id:
                task["done"] = True
                return task
        raise KeyError(f"No task with id {task_id}")
