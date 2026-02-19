from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from openhands.server.storage.sqlite_store import get_store


@dataclass
class ModelPreset:
    name: str
    model: str


@dataclass
class PresetState:
    active: str
    updated_at: str


class ModelPresetManager:
    def __init__(self) -> None:
        self._store = get_store()
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        presets = {
            "quality": os.getenv("MODEL_PRESET_QUALITY", "glm-quality"),
            "main": os.getenv("MODEL_PRESET_MAIN", "glm-main"),
            "fast": os.getenv("MODEL_PRESET_FAST", "glm-fast"),
            "long": os.getenv("MODEL_PRESET_LONG", "glm-long"),
        }
        with self._store.cursor() as cursor:
            for name, model in presets.items():
                cursor.execute(
                    "INSERT OR IGNORE INTO model_presets (name, model) VALUES (?, ?)",
                    (name, model),
                )

            active_default = os.getenv("DEFAULT_MODEL_PRESET", "quality")
            cursor.execute(
                "INSERT OR IGNORE INTO model_preset_state (id, active_preset) VALUES (1, ?)",
                (active_default,),
            )

    def list_presets(self) -> tuple[list[ModelPreset], PresetState]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT name, model FROM model_presets")
            presets = [ModelPreset(**row) for row in cursor.fetchall()]
            cursor.execute("SELECT active_preset FROM model_preset_state WHERE id = 1")
            active_row = cursor.fetchone()
            active = active_row[0] if active_row else "quality"
        return presets, PresetState(
            active=active,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    def set_active(self, preset_name: str) -> PresetState:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM model_presets WHERE name = ?",
                (preset_name,),
            )
            if not cursor.fetchone():
                raise ValueError("Unknown preset")
            cursor.execute(
                "UPDATE model_preset_state SET active_preset = ? WHERE id = 1",
                (preset_name,),
            )
        return PresetState(
            active=preset_name,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    def get_active_model(self) -> str:
        presets, state = self.list_presets()
        mapping = {preset.name: preset.model for preset in presets}
        return mapping.get(state.active, mapping.get("quality", "glm-quality"))
