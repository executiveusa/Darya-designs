from __future__ import annotations

import re
from typing import Iterable

SECRET_PATTERNS = [
    re.compile(r"(Authorization: Bearer )([^\s]+)", re.IGNORECASE),
    re.compile(r"(api_key=)([^&\s]+)", re.IGNORECASE),
    re.compile(r"(token=)([^&\s]+)", re.IGNORECASE),
    re.compile(r"(x-api-key: )([^\s]+)", re.IGNORECASE),
]


def redact_text(text: str, secret_values: Iterable[str]) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(r"\1***", redacted)
    for secret in secret_values:
        if secret:
            redacted = redacted.replace(secret, "***")
    return redacted
