from __future__ import annotations

from dataclasses import dataclass

from openhands.server.services.model_presets import ModelPresetManager
from openhands.server.services.workflow_notifier import WorkflowNotifier
from openhands.server.storage.sqlite_store import get_store


@dataclass
class FakeResponse:
    status_code: int = 200

    def raise_for_status(self):
        return None


def test_webhook_signature(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("WEBHOOK_URL", "http://localhost/webhook")
    monkeypatch.setenv("WEBHOOK_SECRET", "secret")

    store = get_store()
    with store.cursor() as cursor:
        cursor.execute(
            "INSERT INTO runs (id, workflow_id, status, current_step, input, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("run1", "wf1", "completed", 0, "{}", "now", "now"),
        )

    def fake_post(url, data, headers, timeout):
        assert headers.get("X-Dara-Signature")
        return FakeResponse()

    monkeypatch.setattr("requests.post", fake_post)
    notifier = WorkflowNotifier()
    notifier.notify_completion("run1", ModelPresetManager())
