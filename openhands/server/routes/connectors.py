from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from openhands.server.services.connector_service import ConnectorService
from openhands.server.dependencies import get_dependencies

app = APIRouter(prefix="/api/connectors", tags=["connectors"], dependencies=get_dependencies())
service = ConnectorService()


class ConnectorConnectRequest(BaseModel):
    name: str
    payload: dict = Field(default_factory=dict)


@app.get("", response_model=list[dict])
def list_connectors():
    return [connector.__dict__ for connector in service.list_connectors()]


@app.post("/connect", response_model=dict)
def connect_connector(payload: ConnectorConnectRequest):
    try:
        connector = service.connect(payload.name, payload.payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return connector.__dict__


@app.get("/status", response_model=list[dict])
def connectors_status():
    return [connector.__dict__ for connector in service.status()]
