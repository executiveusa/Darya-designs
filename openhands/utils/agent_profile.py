from __future__ import annotations

import os
import re
from pathlib import Path

from openhands.core.logger import openhands_logger as logger

DEFAULT_AGENT_PROFILE = "dara"
PROFILE_ENV_VAR = "DEFAULT_AGENT_PROFILE"
PROFILE_DIR = "agents"
PROFILE_EXTENSION = ".md"


def _get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _normalize_profile_name(profile_name: str | None) -> str | None:
    if not profile_name:
        return None
    lowered = profile_name.strip().lower()
    if lowered in {"none", "off", "disabled"}:
        return None
    if not re.fullmatch(r"[a-z0-9_-]+", lowered):
        logger.warning(
            "Agent profile name contains invalid characters; skipping profile load.",
            extra={"profile": profile_name},
        )
        return None
    return lowered


def load_agent_profile(profile_name: str | None = None) -> str | None:
    normalized = _normalize_profile_name(profile_name)
    if normalized is None:
        return None

    repo_root = _get_repo_root()
    profile_path = repo_root / PROFILE_DIR / f"{normalized}{PROFILE_EXTENSION}"

    if not profile_path.exists():
        logger.warning(
            "Agent profile not found.",
            extra={"profile": normalized, "path": str(profile_path)},
        )
        return None

    try:
        return profile_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        logger.error(
            "Failed to read agent profile.",
            extra={"profile": normalized, "error": str(exc)},
        )
        return None


def get_default_agent_profile() -> str | None:
    env_profile = _normalize_profile_name(os.getenv(PROFILE_ENV_VAR))
    return load_agent_profile(env_profile or DEFAULT_AGENT_PROFILE)


def merge_profile_with_instructions(
    profile_content: str | None, conversation_instructions: str | None
) -> str | None:
    if profile_content and conversation_instructions:
        return f"{profile_content}\n\n{conversation_instructions}".strip()
    return profile_content or conversation_instructions
