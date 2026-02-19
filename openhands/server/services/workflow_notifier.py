from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from typing import Any

import requests

from openhands.server.storage.sqlite_store import get_store


class WorkflowNotifier:
    def __init__(self) -> None:
        self._store = get_store()
        self._webhook_url = os.getenv("WEBHOOK_URL", "")
        self._webhook_secret = os.getenv("WEBHOOK_SECRET", "")
        self._notify_on_complete = os.getenv("NOTIFY_ON_COMPLETE", "true") == "true"
        self._tts_provider = os.getenv("TTS_PROVIDER", "none")
        self._tts_voice = os.getenv("TTS_VOICE", "")
        self._tts_api_key = os.getenv("TTS_API_KEY", "")

    def _hmac_signature(self, payload: str) -> str:
        if not self._webhook_secret:
            return ""
        signature = hmac.new(
            self._webhook_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _collect_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT path, type, created_at FROM artifacts WHERE run_id = ?",
                (run_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def _collect_run(self, run_id: str) -> dict[str, Any]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT id, workflow_id, status, updated_at FROM runs WHERE id = ?",
                (run_id,),
            )
            row = cursor.fetchone()
        if not row:
            raise ValueError("Run not found")
        return dict(row)

    def _generate_tts(self, message: str) -> str | None:
        if self._tts_provider == "none":
            return None
        if not self._tts_api_key:
            return None
        if self._tts_provider == "elevenlabs":
            response = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech",
                headers={"xi-api-key": self._tts_api_key},
                json={"text": message, "voice": self._tts_voice},
                timeout=30,
            )
            response.raise_for_status()
            audio = response.content
            return base64.b64encode(audio).decode("utf-8")
        if self._tts_provider == "openai":
            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers={"Authorization": f"Bearer {self._tts_api_key}"},
                json={"model": "gpt-4o-mini-tts", "voice": self._tts_voice, "input": message},
                timeout=30,
            )
            response.raise_for_status()
            return base64.b64encode(response.content).decode("utf-8")
        return None

    def notify_completion(self, run_id: str, model_presets) -> None:
        if not self._notify_on_complete or not self._webhook_url:
            return
        run = self._collect_run(run_id)
        artifacts = self._collect_artifacts(run_id)
        message = f"Run {run_id} completed"
        tts_audio = self._generate_tts(message)
        payload = {
            "run_id": run_id,
            "status": run.get("status"),
            "summary": message,
            "artifacts": artifacts,
            "model_preset": model_presets.list_presets()[1].active,
            "tokens_used": 0,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "tts_audio": tts_audio,
        }
        body = json.dumps(payload)
        signature = self._hmac_signature(body)
        headers = {"Content-Type": "application/json"}
        if signature:
            headers["X-Dara-Signature"] = signature
        response = requests.post(self._webhook_url, data=body, headers=headers, timeout=15)
        response.raise_for_status()
