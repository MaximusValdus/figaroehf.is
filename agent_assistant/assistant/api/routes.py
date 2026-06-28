"""HTTP routes for the assistant."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_session
from ..models import ApprovalStatus
from ..schemas import (
    ApprovalOut,
    BriefOut,
    ToolInvocation,
    ToolResultOut,
)
from ..services import approvals as approvals_service
from ..services import brief as brief_service
from .deps import get_registry

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/tools")
def list_tools(registry=Depends(get_registry)) -> list[dict]:
    return [
        {
            "name": t.name,
            "description": t.description,
            "permission": t.permission.value,
            "requires_approval": registry.requires_approval(t.name),
        }
        for t in registry.list_tools()
    ]


@router.post("/tools/execute", response_model=ToolResultOut)
def execute_tool(
    invocation: ToolInvocation,
    session: Session = Depends(get_session),
    registry=Depends(get_registry),
) -> ToolResultOut:
    result = registry.execute(invocation.name, invocation.params, session=session)
    if result.status == "error":
        session.rollback()
        raise HTTPException(status_code=400, detail=result.message)
    session.commit()
    return ToolResultOut(
        status=result.status,
        data=result.data,
        message=result.message,
        approval_id=result.approval_id,
    )


@router.get("/brief", response_model=BriefOut)
def get_brief(
    on: str | None = None,
    session: Session = Depends(get_session),
    registry=Depends(get_registry),
) -> BriefOut:
    settings = get_settings()
    target = date.fromisoformat(on) if on else date.today()
    brief, markdown = brief_service.generate_and_store(
        registry, session, owner_name=settings.owner_name, on=target
    )
    session.commit()
    return BriefOut(
        date=brief.brief_date.isoformat(),
        markdown=markdown,
        events=brief.events,
        tasks=brief.tasks,
        notes=brief.notes,
        pending_approvals=brief.pending_approvals,
    )


@router.get("/approvals", response_model=list[ApprovalOut])
def get_approvals(
    status: str | None = None, session: Session = Depends(get_session)
) -> list[ApprovalOut]:
    items = approvals_service.list_approvals(session, status=status)
    return [ApprovalOut.from_model(a) for a in items]


@router.post("/approvals/{approval_id}/approve", response_model=ToolResultOut)
def approve_action(
    approval_id: int,
    session: Session = Depends(get_session),
    registry=Depends(get_registry),
) -> ToolResultOut:
    try:
        result = approvals_service.approve(session, registry, approval_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    session.commit()
    return ToolResultOut(
        status=result.status,
        data=result.data,
        message=result.message,
        approval_id=approval_id,
    )


@router.post("/approvals/{approval_id}/reject", response_model=ApprovalOut)
def reject_action(
    approval_id: int, session: Session = Depends(get_session)
) -> ApprovalOut:
    try:
        approval = approvals_service.reject(session, approval_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    session.commit()
    return ApprovalOut.from_model(approval)
