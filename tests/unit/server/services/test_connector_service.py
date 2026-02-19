from __future__ import annotations

from dataclasses import dataclass

from openhands.server.services.connector_service import ConnectorService


@dataclass
class FakeResponse:
    payload: list[dict]

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_connector_catalog(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("MCP_RUBE_URL", "http://mcp.local")

    def fake_get(url, headers, timeout):
        return FakeResponse(
            payload=[{"id": "c1", "name": "email", "status": "available"}]
        )

    monkeypatch.setattr("requests.get", fake_get)

    service = ConnectorService()
    connectors = service.list_connectors()

    assert connectors[0].name == "email"
