from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import requests
import logging
from openhands.server.storage.sqlite_store import get_store, json_dump, json_load

logger = logging.getLogger(__name__)


@dataclass
class Connector:
    id: str
    name: str
    status: str
    metadata: dict[str, Any]
    created_at: str


class ConnectorService:
    def __init__(self) -> None:
        self._store = get_store()
        self._base_url = os.getenv("MCP_RUBE_URL", "").rstrip("/")
        self._api_key = os.getenv("MCP_RUBE_API_KEY", "")

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def list_connectors(self) -> list[Connector]:
        if not self._base_url:
            return []
        response = requests.get(f"{self._base_url}/connectors", headers=self._headers(), timeout=15)
        response.raise_for_status()
        connectors = response.json()
        result = []
        for item in connectors:
            result.append(
                Connector(
                    id=item.get("id", uuid4().hex),
                    name=item.get("name", "unknown"),
                    status=item.get("status", "available"),
                    metadata=item,
                    created_at=item.get("created_at", datetime.now(timezone.utc).isoformat()),
                )
            )
        return result

    def connect(self, name: str, payload: dict[str, Any]) -> Connector:
        if not self._base_url:
            raise RuntimeError("MCP_RUBE_URL not configured")
        response = requests.post(
            f"{self._base_url}/connectors/connect",
            headers=self._headers(),
            json={"name": name, "payload": payload},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        connector_id = data.get("id", uuid4().hex)
        created_at = datetime.now(timezone.utc).isoformat()
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT OR REPLACE INTO connectors (id, name, status, metadata, created_at) VALUES (?, ?, ?, ?, ?)",
                (connector_id, name, data.get("status", "connected"), json_dump(data), created_at),
            )
        return Connector(
            id=connector_id,
            name=name,
            status=data.get("status", "connected"),
            metadata=data,
            created_at=created_at,
        )

    def status(self) -> list[Connector]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT id, name, status, metadata, created_at FROM connectors")
            rows = cursor.fetchall()
        return [
            Connector(
                id=row["id"],
                name=row["name"],
                status=row["status"],
                metadata=json_load(row["metadata"]) or {},
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def invoke_tool(self, tool_name: str, args: dict[str, Any], run_id: str) -> dict[str, Any]:
        if not self._base_url:
            raise RuntimeError("MCP_RUBE_URL not configured")
        response = requests.post(
            f"{self._base_url}/tools/invoke",
            headers=self._headers(),
            json={"tool_name": tool_name, "args": args, "run_id": run_id},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def hash_payload(payload: dict[str, Any]) -> str:
        encoded = json_dump(payload).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
