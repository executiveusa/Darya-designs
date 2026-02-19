from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from openhands.server.services.model_presets import ModelPresetManager
from openhands.server.dependencies import get_dependencies

app = APIRouter(prefix="/api/models", tags=["models"], dependencies=get_dependencies())
manager = ModelPresetManager()


class PresetResponse(BaseModel):
    name: str
    model: str


class PresetStateResponse(BaseModel):
    active: str
    updated_at: str


class PresetListResponse(BaseModel):
    presets: list[PresetResponse]
    state: PresetStateResponse


class PresetActivateRequest(BaseModel):
    preset: str


@app.get("/presets", response_model=PresetListResponse)
def list_presets():
    presets, state = manager.list_presets()
    return PresetListResponse(
        presets=[PresetResponse(name=p.name, model=p.model) for p in presets],
        state=PresetStateResponse(active=state.active, updated_at=state.updated_at),
    )


@app.post("/presets/active", response_model=PresetStateResponse)
def set_active_preset(payload: PresetActivateRequest):
    try:
        state = manager.set_active(payload.preset)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    try:
        from openhands.server.shared import config as shared_config

        shared_config.get_llm_config().model = manager.get_active_model()
    except Exception:
        pass
    return PresetStateResponse(active=state.active, updated_at=state.updated_at)
