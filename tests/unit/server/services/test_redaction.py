from __future__ import annotations

from openhands.server.redaction import redact_text


def test_redaction_masks_secrets():
    text = "Authorization: Bearer secret-token api_key=abc123"
    result = redact_text(text, ["secret-token", "abc123"])
    assert "secret-token" not in result
    assert "abc123" not in result
    assert "***" in result
