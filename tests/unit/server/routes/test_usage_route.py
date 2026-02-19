import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from pydantic import SecretStr

from openhands.server.app import app
from openhands.server.user_auth.user_auth import UserAuth
from openhands.storage.conversation.file_conversation_store import FileConversationStore
from openhands.storage.data_models.conversation_metadata import ConversationMetadata
from openhands.storage.data_models.settings import Settings
from openhands.storage.memory import InMemoryFileStore
from openhands.storage.settings.file_settings_store import FileSettingsStore
from openhands.storage.settings.settings_store import SettingsStore
from openhands.storage.secrets.secrets_store import SecretsStore
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.integrations.provider import ProviderToken, ProviderType


class MockUserAuth(UserAuth):
    def __init__(self, settings: Settings):
        self._settings = settings
        self._settings_store = MagicMock()
        self._settings_store.load = AsyncMock(return_value=settings)

    async def get_user_id(self) -> str | None:
        return "test-user"

    async def get_user_email(self) -> str | None:
        return "test@example.com"

    async def get_access_token(self) -> SecretStr | None:
        return SecretStr("token")

    async def get_provider_tokens(self) -> dict[ProviderType, ProviderToken] | None:
        return None

    async def get_user_settings_store(self) -> SettingsStore | None:
        return self._settings_store

    async def get_secrets_store(self) -> SecretsStore | None:
        return None

    async def get_user_secrets(self) -> UserSecrets | None:
        return None

    async def get_user_settings(self) -> Settings | None:
        return self._settings

    @classmethod
    async def get_instance(cls, request: Request) -> UserAuth:
        raise NotImplementedError

    @classmethod
    async def get_for_user(cls, user_id: str) -> UserAuth:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_usage_endpoint_returns_metrics():
    file_store = InMemoryFileStore()
    conversation_store = FileConversationStore(file_store)

    conversation_id = "abc123"
    metadata = ConversationMetadata(
        conversation_id=conversation_id,
        selected_repository=None,
        user_id="test-user",
        title="Test",
        last_updated_at=datetime.now(timezone.utc),
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        accumulated_cost=1.2345,
    )
    await conversation_store.save_metadata(metadata)

    settings = Settings(
        llm_model="glm-coding-main",
        llm_api_key=None,
        llm_base_url="http://litellm:4000/v1",
    )

    mock_auth = MockUserAuth(settings)

    with (
        patch.dict(os.environ, {"SESSION_API_KEY": ""}, clear=False),
        patch("openhands.server.dependencies._SESSION_API_KEY", None),
        patch(
            "openhands.server.user_auth.user_auth.UserAuth.get_instance",
            return_value=mock_auth,
        ),
        patch(
            "openhands.storage.settings.file_settings_store.FileSettingsStore.get_instance",
            AsyncMock(return_value=FileSettingsStore(file_store)),
        ),
        patch(
            "openhands.server.shared.ConversationStoreImpl.get_instance",
            AsyncMock(return_value=conversation_store),
        ),
    ):
        client = TestClient(app)
        response = client.get(
            f"/api/usage/current?session_id={conversation_id}"
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["model"] == "glm-coding-main"
    assert payload["prompt_tokens"] == 100
    assert payload["completion_tokens"] == 50
    assert payload["total_tokens"] == 150
    assert payload["accumulated_cost"] == 1.2345
