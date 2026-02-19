from __future__ import annotations

from openhands.server.services.secrets_vault import SecretsVault


def test_secrets_vault_roundtrip(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    vault = SecretsVault("master-key")
    secret = vault.store_secret("connector", "token", "super-secret")

    stored = vault.get_secret_value(secret.id)
    assert stored == "super-secret"

    secrets = list(vault.list_secrets("connector"))
    assert secrets[0].name == "token"
