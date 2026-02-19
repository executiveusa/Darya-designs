from __future__ import annotations

import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from openhands.server.services.secrets_vault import SecretsVault, VaultError
from openhands.server.dependencies import get_dependencies

app = APIRouter(prefix="/api/vault", tags=["vault"], dependencies=get_dependencies())


class VaultSecretRequest(BaseModel):
    scope: str
    name: str
    value: str


@app.post("/secrets", response_model=dict)
def store_secret(payload: VaultSecretRequest):
    try:
        vault = SecretsVault(os.getenv("MASTER_KEY"))
        secret = vault.store_secret(payload.scope, payload.name, payload.value)
        return secret.__dict__
    except VaultError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/secrets", response_model=list[dict])
def list_secrets(scope: str | None = None):
    try:
        vault = SecretsVault(os.getenv("MASTER_KEY"))
        return [secret.__dict__ for secret in vault.list_secrets(scope)]
    except VaultError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
