from __future__ import annotations

from openhands.server.services.model_presets import ModelPresetManager


def test_model_preset_switching(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("MODEL_PRESET_QUALITY", "glm-quality")
    monkeypatch.setenv("MODEL_PRESET_FAST", "glm-fast")
    monkeypatch.setenv("MODEL_PRESET_MAIN", "glm-main")
    monkeypatch.setenv("DEFAULT_MODEL_PRESET", "quality")

    manager = ModelPresetManager()
    presets, state = manager.list_presets()
    preset_names = {preset.name for preset in presets}

    assert "quality" in preset_names
    assert state.active == "quality"

    updated = manager.set_active("fast")
    assert updated.active == "fast"
    assert manager.get_active_model() == "glm-fast"
