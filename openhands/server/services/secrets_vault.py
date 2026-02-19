from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from uuid import uuid4

from cryptography.fernet import Fernet, InvalidToken

from openhands.server.storage.sqlite_store import get_store


class VaultError(RuntimeError):
    pass


@dataclass
class VaultSecret:
    id: str
    scope: str
    name: str
    created_at: str


class SecretsVault:
    def __init__(self, master_key: str | None) -> None:
        if not master_key:
            raise VaultError("MASTER_KEY is required for secrets vault")
        self._fernet = Fernet(self._derive_key(master_key))
        self._store = get_store()

    @staticmethod
    def _derive_key(master_key: str) -> bytes:
        digest = hashlib.sha256(master_key.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest)

    def store_secret(self, scope: str, name: str, value: str) -> VaultSecret:
        encrypted = self._fernet.encrypt(value.encode("utf-8")).decode("utf-8")
        secret_id = uuid4().hex
        created_at = datetime.now(timezone.utc).isoformat()
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT INTO secrets (id, scope, name, value, created_at) VALUES (?, ?, ?, ?, ?)",
                (secret_id, scope, name, encrypted, created_at),
            )
        return VaultSecret(id=secret_id, scope=scope, name=name, created_at=created_at)

    def list_secrets(self, scope: str | None = None) -> list[VaultSecret]:
        with self._store.cursor() as cursor:
            if scope:
                cursor.execute(
                    "SELECT id, scope, name, created_at FROM secrets WHERE scope = ?",
                    (scope,),
                )
            else:
                cursor.execute("SELECT id, scope, name, created_at FROM secrets")
            return [VaultSecret(**row) for row in cursor.fetchall()]

    def get_secret_value(self, secret_id: str) -> str:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT value FROM secrets WHERE id = ?",
                (secret_id,),
            )
            row = cursor.fetchone()
        if not row:
            raise VaultError("Secret not found")
        try:
            return self._fernet.decrypt(row[0].encode("utf-8")).decode("utf-8")
        except InvalidToken as exc:
            raise VaultError("Failed to decrypt secret") from exc

    def list_secret_values(self) -> Iterable[str]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT value FROM secrets")
            rows = cursor.fetchall()
        for row in rows:
            try:
                yield self._fernet.decrypt(row[0].encode("utf-8")).decode("utf-8")
            except InvalidToken:
                continue
