from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from openhands.server.dependencies import get_dependencies
from openhands.server.shared import config
from openhands.server.user_auth import get_user_settings
from openhands.server.utils import get_conversation_store, validate_conversation_id
from openhands.storage.conversation.conversation_store import ConversationStore
from openhands.storage.data_models.conversation_metadata import ConversationMetadata
from openhands.storage.data_models.settings import Settings

app = APIRouter(prefix='/api', dependencies=get_dependencies())


class UsageResponse(BaseModel):
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    accumulated_cost: float
    updated_at: str


async def _get_usage_metadata(
    session_id: str = Query(..., description='Conversation/session ID'),
    conversation_store: ConversationStore = Depends(get_conversation_store),
) -> ConversationMetadata:
    validate_conversation_id(session_id)
    try:
        return await conversation_store.get_metadata(session_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Conversation {session_id} not found',
        )


@app.get('/usage/current', response_model=UsageResponse)
async def get_current_usage(
    settings: Settings | None = Depends(get_user_settings),
    metadata: ConversationMetadata = Depends(_get_usage_metadata),
) -> UsageResponse:
    model = (
        settings.llm_model
        if settings and settings.llm_model
        else config.get_llm_config().model
    )

    updated_at = metadata.last_updated_at or datetime.now(timezone.utc)

    return UsageResponse(
        model=model,
        prompt_tokens=metadata.prompt_tokens,
        completion_tokens=metadata.completion_tokens,
        total_tokens=metadata.total_tokens,
        accumulated_cost=metadata.accumulated_cost,
        updated_at=updated_at.isoformat(),
    )
