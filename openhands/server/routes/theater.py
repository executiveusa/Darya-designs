from __future__ import annotations

from fastapi import APIRouter

from openhands.server.dependencies import get_dependencies

app = APIRouter(prefix="/api/theater", tags=["theater"], dependencies=get_dependencies())


# Placeholder theater router
# TODO: Implement theater-specific endpoints
