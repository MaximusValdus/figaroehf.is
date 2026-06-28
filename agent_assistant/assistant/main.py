"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import router
from .db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Personal Agent Assistant",
        version="0.1.0",
        description=(
            "Daily briefs, SQLite-backed memory, and approval-gated tools "
            "over mock calendar/tasks/notes/email connectors."
        ),
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


app = create_app()
