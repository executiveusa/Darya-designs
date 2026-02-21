from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from openhands.server.services.workflow_engine import WorkflowEngine
from openhands.server.dependencies import get_dependencies

app = APIRouter(prefix="/api/workflows", tags=["workflows"], dependencies=get_dependencies())
engine = WorkflowEngine()


class RunRequest(BaseModel):
    workflow_id: str
    input: dict = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    approval_id: str
    decision: str
    # Note: In a production system with user authentication, this should be
    # validated against the authenticated user to prevent impersonation
    decided_by: str  # Required field to track who made the decision


@app.get("", response_model=list[dict])
def list_workflows():
    return engine.list_workflows()


@app.post("/run", response_model=dict)
def run_workflow(payload: RunRequest):
    try:
        run = engine.create_run(payload.workflow_id, payload.input)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"run_id": run.id}


@app.get("/run/{run_id}", response_model=dict)
def get_run(run_id: str):
    try:
        return engine.get_run(run_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.get("/run/{run_id}/artifacts", response_model=list[dict])
def list_artifacts(run_id: str):
    return engine.list_artifacts(run_id)


@app.post("/run/{run_id}/approve", response_model=dict)
def approve_run(run_id: str, payload: ApprovalRequest):
    """Approve or reject a workflow run.
    
    Note: In a production system, this endpoint should verify that the
    decided_by field matches the authenticated user making the request.
    """
    # Validate decision value
    if payload.decision not in ("approved", "rejected"):
        raise HTTPException(
            status_code=400,
            detail="Decision must be 'approved' or 'rejected'"
        )
    
    try:
        return engine.approve(
            run_id,
            payload.approval_id,
            payload.decision,
            payload.decided_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
