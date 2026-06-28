# Personal Agent Assistant

A small, modular **FastAPI** service for a personal agent assistant. It
generates a **daily brief**, keeps **memory** in SQLite, and exposes
calendar / tasks / notes / email capabilities through a uniform, **permission-aware
tool interface**. Every action that changes state or reaches the outside world is
**gated behind explicit human approval**.

This is an MVP: all connectors are **deterministic mocks**, so it runs with no
credentials and makes **no outbound network calls**. In particular, the email
connector **never sends mail** — "sent" messages are captured in a local outbox.

## Features

- 🗞️ **Daily brief** — schedule, open tasks, recent notes, and anything awaiting
  approval, rendered to Markdown.
- 🧠 **SQLite memory** — approvals, brief history, and key/value facts persist
  across sessions.
- 🔌 **Tool interface** — calendar, tasks, notes, and email exposed as tools with
  declared permissions (`READ` / `WRITE`).
- 🧪 **Mock connectors** — seeded, deterministic, offline.
- ✅ **Approval-required actions** — `WRITE` tools create a pending approval and
  do **not** execute until a human approves.
- 🧰 **CLI + HTTP API** — drive everything from the terminal or over HTTP.

## Project structure

```
agent_assistant/
├── assistant/
│   ├── config.py            # env-based settings
│   ├── db.py                # SQLite engine / session
│   ├── models.py            # ORM models (memory: approvals, briefs, facts)
│   ├── schemas.py           # Pydantic API models
│   ├── main.py              # FastAPI app factory
│   ├── cli.py               # Typer CLI (brief, tool, approvals, serve, ...)
│   ├── connectors/          # external systems — mocks for the MVP
│   │   ├── base.py          #   abstract interfaces + Connectors bundle
│   │   ├── calendar.py  tasks.py  notes.py  email.py
│   ├── tools/               # permission-aware tool layer
│   │   ├── base.py          #   Tool, Permission, ToolResult
│   │   ├── registry.py      #   dispatch + approval gating
│   │   └── *_tool.py        #   calendar/tasks/notes/email tools
│   ├── services/
│   │   ├── brief.py         # daily brief assembly + persistence
│   │   └── approvals.py     # approve / reject / list workflow
│   └── api/
│       ├── routes.py        # HTTP endpoints
│       └── deps.py          # shared dependencies
└── tests/
    ├── test_brief.py        # brief generation
    ├── test_permissions.py  # tool permissions + approval workflow
    └── test_api.py          # HTTP smoke tests
```

## Setup

Requires **Python 3.10+**.

```bash
cd agent_assistant

# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt   # runtime + test deps
# or, for runtime only:  pip install -r requirements.txt
# or, editable install:  pip install -e ".[dev]"

# 3. (optional) configure
cp .env.example .env               # adjust ASSISTANT_* settings

# 4. Initialise the database
python -m assistant.cli init-db
```

## Usage

### CLI

```bash
# Generate today's brief (also stored to memory)
python -m assistant.cli brief

# A specific day
python -m assistant.cli brief --on 2026-06-29

# Invoke a READ tool (runs immediately)
python -m assistant.cli tool tasks.list_tasks

# Invoke a WRITE tool (creates a pending approval — does NOT run yet)
python -m assistant.cli tool tasks.create_task -p title="Call the bank"

# Review and act on approvals
python -m assistant.cli approvals
python -m assistant.cli approve 1     # executes the action
python -m assistant.cli reject 1      # discards it

# Run the HTTP server
python -m assistant.cli serve         # http://127.0.0.1:8000
```

> Installing the package (`pip install -e .`) also exposes an `assistant`
> console script, so `assistant brief` works without the `python -m` prefix.

### HTTP API

Start the server (`assistant serve`) and open the interactive docs at
`http://127.0.0.1:8000/docs`.

| Method & path                          | Description                                  |
| -------------------------------------- | -------------------------------------------- |
| `GET  /health`                         | Liveness check                               |
| `GET  /tools`                          | List tools and their permission level        |
| `POST /tools/execute`                  | Run a tool (WRITE → returns a pending approval) |
| `GET  /brief?on=YYYY-MM-DD`            | Generate & store the daily brief             |
| `GET  /approvals?status=pending`       | List approval requests                       |
| `POST /approvals/{id}/approve`         | Approve and execute an action                |
| `POST /approvals/{id}/reject`          | Reject an action                             |

Example:

```bash
curl -s http://127.0.0.1:8000/brief | python -m json.tool

curl -s -X POST http://127.0.0.1:8000/tools/execute \
  -H 'content-type: application/json' \
  -d '{"name":"email.send_email","params":{"to":"a@b.com","subject":"Hi","body":"..."}}'
# -> {"status":"pending_approval","approval_id":1,...}   (nothing is sent)
```

## How the approval model works

Each tool declares a permission:

- **`READ`** (e.g. `calendar.list_events`, `tasks.list_tasks`) — side-effect free,
  executes immediately.
- **`WRITE`** (e.g. `tasks.create_task`, `calendar.create_event`,
  `email.send_email`) — `ToolRegistry.execute()` records a **pending `Approval`**
  in SQLite and returns `status="pending_approval"` **without running the tool**.
  The action only runs when `approve()` is called, which then marks the approval
  resolved and stores the result.

Set `ASSISTANT_AUTO_APPROVE=true` to bypass the gate (not recommended outside of
local experimentation).

## Configuration

Settings come from environment variables (prefix `ASSISTANT_`) or a `.env` file:

| Variable                   | Default                      | Purpose                                  |
| -------------------------- | ---------------------------- | ---------------------------------------- |
| `ASSISTANT_DATABASE_URL`   | `sqlite:///./assistant.db`   | Memory store location                    |
| `ASSISTANT_OWNER_NAME`     | `Valdimar`                   | Name used to personalise the brief       |
| `ASSISTANT_AUTO_APPROVE`   | `false`                      | Execute WRITE tools without approval      |

## Testing

```bash
python -m pytest          # or: make test
```

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the suite on
Python 3.10–3.12. It is inert while this project lives in a subdirectory and
activates automatically once the directory becomes a repository root.
Common tasks are also wrapped in a `Makefile` (`make help`).

The suite covers brief generation (`test_brief.py`), the permission model and
approval workflow (`test_permissions.py`), and the HTTP API (`test_api.py`).

## Extending with real connectors

Replace a mock by subclassing the matching interface in
`assistant/connectors/base.py` (e.g. `CalendarConnector`) and wiring it into
`build_registry()` instead of `build_mock_connectors()`. The tool and approval
layers are unchanged — a real `send_email` is still `WRITE`, so it remains
approval-gated by construction.

## Roadmap (post-MVP)

- Real connectors (Google Calendar, a task manager, email) behind the same interfaces
- LLM-authored brief narration and task prioritisation
- Scheduled/automated brief delivery
- Richer memory (semantic recall) beyond key/value facts
