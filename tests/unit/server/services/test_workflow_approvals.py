from __future__ import annotations

from dataclasses import dataclass

from openhands.server.services.workflow_engine import WorkflowEngine


@dataclass
class FakeConnectorService:
    invoked: list

    def invoke_tool(self, tool_name, args, run_id):
        self.invoked.append(tool_name)
        return {"tool": tool_name, "status": "ok"}

    @staticmethod
    def hash_payload(payload):
        return str(payload)


class FakeNotifier:
    def notify_completion(self, run_id, model_presets):
        return None


def test_write_tools_require_approval(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ARTIFACTS_DIR", str(tmp_path / "artifacts"))
    engine = WorkflowEngine()
    fake_connector = FakeConnectorService(invoked=[])
    engine._connector_service = fake_connector
    engine._notifier = FakeNotifier()

    run = engine.create_run("secretary-default", {"recipient": "test"})
    assert fake_connector.invoked == []

    approvals = engine.get_run(run.id)["approvals"]
    engine.approve(run.id, approvals[0]["id"], "approved", "tester")

    assert fake_connector.invoked == []
