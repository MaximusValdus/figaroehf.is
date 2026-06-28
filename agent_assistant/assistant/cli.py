"""Command-line interface for the agent assistant.

Examples::

    assistant init-db
    assistant brief
    assistant brief --on 2026-06-29
    assistant tool tasks.create_task --param title="Call the bank"
    assistant approvals
    assistant approve 1
    assistant serve
"""

from __future__ import annotations

import json
from datetime import date
from typing import Optional

import typer

from .config import get_settings
from .connectors import build_mock_connectors
from .db import SessionLocal, init_db, session_scope
from .services import approvals as approvals_service
from .services import brief as brief_service
from .tools.registry import build_registry

app = typer.Typer(help="Personal agent assistant.", no_args_is_help=True)


def _registry():
    settings = get_settings()
    return build_registry(build_mock_connectors(), auto_approve=settings.auto_approve)


@app.command("init-db")
def init_db_command() -> None:
    """Create the SQLite tables."""
    init_db()
    typer.echo("Database initialised.")


@app.command()
def brief(on: Optional[str] = typer.Option(None, help="Date as YYYY-MM-DD.")) -> None:
    """Generate (and store) the daily brief, printed as Markdown."""
    init_db()
    settings = get_settings()
    target = date.fromisoformat(on) if on else date.today()
    registry = _registry()
    with session_scope() as session:
        _, markdown = brief_service.generate_and_store(
            registry, session, owner_name=settings.owner_name, on=target
        )
    typer.echo(markdown)


@app.command()
def tool(
    name: str = typer.Argument(..., help="Tool name, e.g. tasks.create_task."),
    param: list[str] = typer.Option(
        None, "--param", "-p", help="key=value pair (repeatable)."
    ),
) -> None:
    """Invoke a tool. WRITE tools create a pending approval instead of running."""
    init_db()
    params = {}
    for item in param or []:
        key, _, value = item.partition("=")
        params[key] = value
    registry = _registry()
    with session_scope() as session:
        result = registry.execute(name, params, session=session)
    if result.pending:
        typer.echo(f"Pending approval #{result.approval_id}: {result.message}")
    elif result.ok:
        typer.echo(json.dumps(result.data, indent=2, default=str))
    else:
        typer.echo(f"Error: {result.message}", err=True)
        raise typer.Exit(code=1)


@app.command()
def approvals(
    status: Optional[str] = typer.Option(None, help="Filter: pending/approved/rejected.")
) -> None:
    """List approval requests."""
    init_db()
    with session_scope() as session:
        items = approvals_service.list_approvals(session, status=status)
        if not items:
            typer.echo("No approvals.")
            return
        for a in items:
            typer.echo(f"#{a.id}  [{a.status:>8}]  {a.summary}")


@app.command()
def approve(approval_id: int = typer.Argument(...)) -> None:
    """Approve and execute a pending action."""
    init_db()
    registry = _registry()
    with session_scope() as session:
        try:
            result = approvals_service.approve(session, registry, approval_id)
        except (KeyError, ValueError) as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(code=1)
    typer.echo("Approved and executed:")
    typer.echo(json.dumps(result.data, indent=2, default=str))


@app.command()
def reject(approval_id: int = typer.Argument(...)) -> None:
    """Reject a pending action without executing it."""
    init_db()
    with session_scope() as session:
        try:
            approvals_service.reject(session, approval_id)
        except (KeyError, ValueError) as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(code=1)
    typer.echo(f"Rejected approval #{approval_id}.")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000),
    reload: bool = typer.Option(False),
) -> None:
    """Run the FastAPI server with uvicorn."""
    import uvicorn

    uvicorn.run("assistant.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
