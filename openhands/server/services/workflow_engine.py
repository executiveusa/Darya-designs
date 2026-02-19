from __future__ import annotations

import json
import os
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
from openhands.server.redaction import redact_text
from openhands.server.services.connector_service import ConnectorService
from openhands.server.services.model_presets import ModelPresetManager
from openhands.server.services.secrets_vault import SecretsVault
from openhands.server.storage.sqlite_store import get_store, json_dump, json_load
from openhands.server.services.workflow_notifier import WorkflowNotifier

logger = logging.getLogger(__name__)


@dataclass
class WorkflowRun:
    id: str
    workflow_id: str
    status: str
    current_step: int
    created_at: str
    updated_at: str


@dataclass
class Approval:
    id: str
    run_id: str
    action_type: str
    payload_hash: str
    status: str
    decided_by: str | None
    decided_at: str | None


@dataclass
class Artifact:
    id: str
    run_id: str
    path: str
    type: str
    created_at: str


class WorkflowEngine:
    def __init__(self) -> None:
        self._store = get_store()
        self._artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "/data/artifacts"))
        self._connector_service = ConnectorService()
        self._model_presets = ModelPresetManager()
        self._notifier = WorkflowNotifier()
        master_key = os.getenv("MASTER_KEY")
        self._vault = SecretsVault(master_key) if master_key else None
        self._ensure_default_workflow()

    def _ensure_default_workflow(self) -> None:
        workflow_id = "secretary-default"
        schema = {
            "name": "Draft Email + Schedule Follow-up",
            "steps": [
                {
                    "type": "agent_step",
                    "name": "draft_email",
                    "artifact": "draft_email.txt",
                },
                {
                    "type": "approval_gate",
                    "action_type": "approve_email_send",
                },
                {
                    "type": "tool_step",
                    "tool_name": "send_email",
                    "write": True,
                    "artifact": "email_payload.json",
                },
                {
                    "type": "tool_step",
                    "tool_name": "create_calendar_event",
                    "write": True,
                    "artifact": "calendar_payload.json",
                },
            ],
        }
        created_at = datetime.now(timezone.utc).isoformat()
        smoke_id = "agent0-smoke"
        smoke_schema = {
            "name": "Agent 0 Smoke Test",
            "steps": [
                {"type": "tool_step", "tool_name": "shell_command", "command": "node -v", "write": False, "artifact": "node_version.txt"},
                {"type": "tool_step", "tool_name": "shell_command", "command": "python --version", "write": False, "artifact": "python_version.txt"},
                {"type": "tool_step", "tool_name": "shell_command", "command": "echo 'smoke ok' > smoke.txt", "write": False, "artifact": "smoke.txt"},
            ],
        }
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT OR IGNORE INTO workflows (id, name, schema, created_at) VALUES (?, ?, ?, ?)",
                (workflow_id, schema["name"], json_dump(schema), created_at),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO workflows (id, name, schema, created_at) VALUES (?, ?, ?, ?)",
                (smoke_id, smoke_schema["name"], json_dump(smoke_schema), created_at),
            )

    def list_workflows(self) -> list[dict[str, Any]]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT id, name, schema, created_at FROM workflows")
            rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "schema": json_load(row["schema"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def _store_run(self, run: WorkflowRun) -> None:
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT INTO runs (id, workflow_id, status, current_step, input, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    run.id,
                    run.workflow_id,
                    run.status,
                    run.current_step,
                    None,
                    run.created_at,
                    run.updated_at,
                ),
            )

    def _update_run(self, run_id: str, status: str, current_step: int) -> None:
        with self._store.cursor() as cursor:
            cursor.execute(
                "UPDATE runs SET status = ?, current_step = ?, updated_at = ? WHERE id = ?",
                (status, current_step, datetime.now(timezone.utc).isoformat(), run_id),
            )

    def create_run(self, workflow_id: str, input_payload: dict[str, Any]) -> WorkflowRun:
        run_id = uuid4().hex
        now = datetime.now(timezone.utc).isoformat()
        run = WorkflowRun(
            id=run_id,
            workflow_id=workflow_id,
            status="running",
            current_step=0,
            created_at=now,
            updated_at=now,
        )
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT INTO runs (id, workflow_id, status, current_step, input, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    run.id,
                    run.workflow_id,
                    run.status,
                    run.current_step,
                    json_dump(input_payload),
                    run.created_at,
                    run.updated_at,
                ),
            )
        self._execute_run(run_id)
        return run

    def _load_workflow(self, workflow_id: str) -> dict[str, Any]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT schema FROM workflows WHERE id = ?", (workflow_id,))
            row = cursor.fetchone()
        if not row:
            raise ValueError("Workflow not found")
        return json_load(row[0])

    def _load_run_input(self, run_id: str) -> dict[str, Any]:
        with self._store.cursor() as cursor:
            cursor.execute("SELECT input FROM runs WHERE id = ?", (run_id,))
            row = cursor.fetchone()
        return json_load(row[0]) or {}

    def _create_approval(self, run_id: str, action_type: str, payload_hash: str) -> Approval:
        approval_id = uuid4().hex
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT INTO approvals (id, run_id, action_type, payload_hash, status, decided_by, decided_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (approval_id, run_id, action_type, payload_hash, "pending", None, None),
            )
        return Approval(
            id=approval_id,
            run_id=run_id,
            action_type=action_type,
            payload_hash=payload_hash,
            status="pending",
            decided_by=None,
            decided_at=None,
        )

    def _has_approved(self, run_id: str, payload_hash: str) -> bool:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT status FROM approvals WHERE run_id = ? AND payload_hash = ? ORDER BY decided_at DESC LIMIT 1",
                (run_id, payload_hash),
            )
            row = cursor.fetchone()
        return bool(row and row[0] == "approved")

    def _record_artifact(self, run_id: str, path: Path, artifact_type: str) -> Artifact:
        artifact_id = uuid4().hex
        created_at = datetime.now(timezone.utc).isoformat()
        with self._store.cursor() as cursor:
            cursor.execute(
                "INSERT INTO artifacts (id, run_id, path, type, created_at) VALUES (?, ?, ?, ?, ?)",
                (artifact_id, run_id, str(path), artifact_type, created_at),
            )
        return Artifact(
            id=artifact_id,
            run_id=run_id,
            path=str(path),
            type=artifact_type,
            created_at=created_at,
        )

    def _write_artifact(self, run_id: str, filename: str, content: str) -> Path:
        target_dir = self._artifacts_dir / "runs" / run_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filename
        secrets = list(self._vault.list_secret_values()) if self._vault else []
        redacted = redact_text(content, secrets)
        target_path.write_text(redacted, encoding="utf-8")
        self._record_artifact(run_id, target_path, "text")
        return target_path

    def _execute_run(self, run_id: str) -> None:
        workflow_id, current_step, status = self._get_run_state(run_id)
        if status not in {"running", "waiting_approval"}:
            return
        workflow = self._load_workflow(workflow_id)
        steps = workflow.get("steps", [])
        payload = self._load_run_input(run_id)

        for index in range(current_step, len(steps)):
            step = steps[index]
            step_type = step.get("type")
            if step_type == "agent_step":
                content = (
                    f"Draft for workflow {workflow.get('name')}.\n"
                    f"Input: {json.dumps(payload, ensure_ascii=False)}"
                )
                self._write_artifact(run_id, step.get("artifact", "draft.txt"), content)
                self._update_run(run_id, "running", index + 1)
                continue

            if step_type == "approval_gate":
                action_type = step.get("action_type", "approval")
                payload_hash = self._connector_service.hash_payload(step)
                if not self._has_approved(run_id, payload_hash):
                    self._create_approval(run_id, action_type, payload_hash)
                    self._update_run(run_id, "waiting_approval", index)
                    return
                self._update_run(run_id, "running", index + 1)
                continue

            if step_type == "tool_step":
                write_flag = bool(step.get("write"))
                payload_hash = self._connector_service.hash_payload(step)
                if write_flag and not self._has_approved(run_id, payload_hash):
                    self._create_approval(run_id, step.get("tool_name", "tool"), payload_hash)
                    self._update_run(run_id, "waiting_approval", index)
                    return
                if step.get("tool_name") == "shell_command":
                    result = self._run_shell_command(step.get("command", ""))
                else:
                    result = self._connector_service.invoke_tool(
                        step.get("tool_name", "tool"),
                        {"input": payload},
                        run_id,
                    )
                self._write_artifact(
                    run_id,
                    step.get("artifact", "tool_output.json"),
                    json_dump(result),
                )
                self._update_run(run_id, "running", index + 1)
                continue

            if step_type == "http_step":
                self._write_artifact(
                    run_id,
                    step.get("artifact", "http_response.txt"),
                    "HTTP step executed",
                )
                self._update_run(run_id, "running", index + 1)
                continue

        self._update_run(run_id, "completed", len(steps))
        try:
            self._notifier.notify_completion(run_id, self._model_presets)
        except Exception as exc:
            logger.warning("Webhook notification failed: %s", exc)

    @staticmethod
    def _run_shell_command(command: str) -> dict[str, str]:
        if not command:
            return {"status": "skipped", "output": "no command provided"}
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "output": (result.stdout + result.stderr).strip(),
            "command": command,
        }

    def _get_run_state(self, run_id: str) -> tuple[str, int, str]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT workflow_id, current_step, status FROM runs WHERE id = ?",
                (run_id,),
            )
            row = cursor.fetchone()
        if not row:
            raise ValueError("Run not found")
        return row["workflow_id"], row["current_step"], row["status"]

    def get_run(self, run_id: str) -> dict[str, Any]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT id, workflow_id, status, current_step, created_at, updated_at FROM runs WHERE id = ?",
                (run_id,),
            )
            row = cursor.fetchone()
        if not row:
            raise ValueError("Run not found")
        return {
            "id": row["id"],
            "workflow_id": row["workflow_id"],
            "status": row["status"],
            "current_step": row["current_step"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "approvals": self.list_approvals(run_id),
        }

    def list_approvals(self, run_id: str) -> list[dict[str, Any]]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT id, action_type, payload_hash, status, decided_by, decided_at FROM approvals WHERE run_id = ?",
                (run_id,),
            )
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def list_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        with self._store.cursor() as cursor:
            cursor.execute(
                "SELECT id, path, type, created_at FROM artifacts WHERE run_id = ?",
                (run_id,),
            )
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def approve(self, run_id: str, approval_id: str, decision: str, decided_by: str | None) -> dict[str, Any]:
        decided_at = datetime.now(timezone.utc).isoformat()
        with self._store.cursor() as cursor:
            cursor.execute(
                "UPDATE approvals SET status = ?, decided_by = ?, decided_at = ? WHERE id = ?",
                (decision, decided_by, decided_at, approval_id),
            )
        if decision == "approved":
            workflow_id, current_step, _ = self._get_run_state(run_id)
            self._update_run(run_id, "running", current_step)
            self._execute_run(run_id)
        else:
            self._update_run(run_id, "rejected", 0)
        return self.get_run(run_id)
