"""Durable OpenClaw completion observer registration for Adaptive projects.

This module only registers a short trigger with the Gateway. It never waits for
Adaptive, resumes a checkpoint, or dispatches a Work Unit. The Gateway owns the
schedule, trigger execution, announcement delivery, and retry semantics.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OBSERVER_DIR = ".adaptive/openclaw-terminal-observers"
OBSERVER_SCHEMA_VERSION = 1
_SAFE_ID = re.compile(r"^[A-Za-z0-9._:-]+$")
_SESSION_AGENT = re.compile(r"^agent:([^:]+):")


@dataclass(frozen=True)
class ObserverRegistration:
    schema_version: int
    orchestration_id: str
    project_root: str
    session_key: str | None
    conversation_ref: str | None
    declaration_key: str
    status: str
    job_id: str | None = None
    error: str | None = None
    created_at: str | None = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def association_path(project_root: Path, orchestration_id: str) -> Path:
    if not _SAFE_ID.fullmatch(orchestration_id):
        raise ValueError("invalid orchestration id for observer association")
    return project_root / OBSERVER_DIR / f"{orchestration_id}.json"


def declaration_key(orchestration_id: str) -> str:
    return f"adaptive-terminal:{orchestration_id}"


def _agent_id_from_session_key(session_key: str) -> str | None:
    match = _SESSION_AGENT.match(session_key)
    return match.group(1) if match else None


def _load(path: Path) -> ObserverRegistration | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    try:
        return ObserverRegistration(**payload)
    except TypeError:
        return None


def _atomic_write(path: Path, registration: ObserverRegistration) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(asdict(registration), ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _trigger_script(
    *,
    command: list[str],
    project_root: Path,
    orchestration_id: str,
    environment: dict[str, str] | None = None,
) -> str:
    status_command = [
        *command,
        "project-status",
        "--orchestration-id",
        orchestration_id,
        "--project-root",
        str(project_root),
    ]
    shell_command = " ".join(shlex.quote(part) for part in status_command)
    pythonpath = (environment or {}).get("PYTHONPATH")
    if pythonpath:
        shell_command = f"PYTHONPATH={shlex.quote(pythonpath)} {shell_command}"
    message = (
        "Adaptive orchestration {id} reached terminal=true. Reconcile the "
        "authoritative project-status and Result Store for project-root {root}; "
        "then reconcile release_deliveries and deliver exactly one final report "
        "to the originating conversation. Include canonical artifact, report, "
        "version, size, and SHA-256 fields when present. Keep artifact validation "
        "separate from notification delivery. Do not resume, redispatch, or "
        "create another orchestration."
    ).format(id=orchestration_id, root=project_root)
    # This is OpenClaw Code Mode JavaScript, persisted inside cron.add. The
    # command is bounded and the trigger is once=true, so it is not a long wait.
    return (
        "const result = await exec({command: "
        + json.dumps(shell_command)
        + ", timeoutSeconds: 20}); "
        "const text = typeof result === 'string' ? result : JSON.stringify(result); "
        "const terminal = /\\\"terminal\\\"\\s*:\\s*true/.test(text); "
        "return json({fire: terminal, message: terminal ? "
        + json.dumps(message)
        + " : '', state: {terminal}});"
    )


def _cron_payload(
    *,
    command: list[str],
    project_root: Path,
    orchestration_id: str,
    session_key: str,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": f"Adaptive terminal — {orchestration_id[:12]}",
        "declarationKey": declaration_key(orchestration_id),
        "description": "Durable terminal observer for one Adaptive orchestration.",
        "sessionTarget": f"session:{session_key}",
        "sessionKey": session_key,
        "schedule": {"kind": "every", "everyMs": 120_000},
        "trigger": {
            "script": _trigger_script(
                command=command,
                project_root=project_root,
                orchestration_id=orchestration_id,
                environment=environment,
            ),
            "once": True,
        },
        "payload": {
            "kind": "agentTurn",
            "message": (
                f"Reconcile Adaptive orchestration {orchestration_id} after "
                "terminal=true using authoritative project-status and the Result "
                f"Store from {project_root}. Reconcile release_deliveries and announce its final status, completed, "
                "pending and blocked Work Units, canonical artifact/report paths, version, size, SHA-256, and any "
                "interruption reason. Do not execute, resume, redispatch, or "
                "create another orchestration."
            ),
            "timeoutSeconds": 300,
        },
        "delivery": {"mode": "announce"},
        "enabled": True,
    }
    agent_id = _agent_id_from_session_key(session_key)
    if agent_id:
        payload["agentId"] = agent_id
    return payload


def _find_gateway_job_id(
    *, declaration: str, environment: dict[str, str], timeout_seconds: int
) -> str | None:
    """Reconcile a successful cron.add whose CLI response omitted its id."""
    completed = subprocess.run(
        [
            "openclaw",
            "gateway",
            "call",
            "cron.list",
            "--params",
            json.dumps({"includeDisabled": True, "limit": 200}),
            "--json",
        ],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
        timeout=timeout_seconds,
    )
    if completed.returncode != 0:
        return None
    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    jobs = response.get("jobs", []) if isinstance(response, dict) else []
    if not isinstance(jobs, list):
        return None
    for job in jobs:
        if isinstance(job, dict) and job.get("declarationKey") == declaration:
            job_id = job.get("id")
            if isinstance(job_id, str) and job_id:
                return job_id
    return None


def register_terminal_observer(
    *,
    command: list[str],
    project_root: Path,
    orchestration_id: str,
    environment: dict[str, str],
    timeout_seconds: int = 20,
) -> ObserverRegistration:
    """Persist and idempotently register one Gateway-owned observer."""
    path = association_path(project_root, orchestration_id)
    existing = _load(path)
    if existing is not None and existing.status == "REGISTERED":
        return existing

    session_key = (
        environment.get("OPENCLAW_SESSION_KEY")
        or environment.get("OPENCLAW_SOURCE_SESSION_KEY")
    )
    conversation_ref = environment.get("OPENCLAW_CONVERSATION_REF")
    base = dict(
        schema_version=OBSERVER_SCHEMA_VERSION,
        orchestration_id=orchestration_id,
        project_root=str(project_root),
        session_key=session_key,
        conversation_ref=conversation_ref,
        declaration_key=declaration_key(orchestration_id),
        status="PENDING",
        created_at=existing.created_at if existing else _now(),
    )
    if not session_key:
        unbound = {**base, "status": "UNBOUND"}
        registration = ObserverRegistration(
            **unbound,
            error=(
                "OpenClaw source session is unavailable; set "
                "OPENCLAW_SESSION_KEY in the trusted Bridge execution context."
            ),
        )
        _atomic_write(path, registration)
        return registration

    payload = _cron_payload(
        command=command,
        project_root=project_root,
        orchestration_id=orchestration_id,
        session_key=session_key,
        environment=environment,
    )
    try:
        completed = subprocess.run(
            [
                "openclaw",
                "gateway",
                "call",
                "cron.add",
                "--params",
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
            timeout=timeout_seconds,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"cron.add exited {completed.returncode}")
        response = json.loads(completed.stdout)
        job_id = response.get("id") if isinstance(response, dict) else None
        if not isinstance(job_id, str) or not job_id:
            job_id = _find_gateway_job_id(
                declaration=base["declaration_key"],
                environment=environment,
                timeout_seconds=timeout_seconds,
            )
        if not isinstance(job_id, str) or not job_id:
            raise RuntimeError("cron.add returned no durable job id")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, RuntimeError) as exc:
        pending = {**base, "status": "PENDING"}
        registration = ObserverRegistration(
            **pending,
            error=" ".join(str(exc).split())[:500],
        )
        _atomic_write(path, registration)
        return registration

    registered = {**base, "status": "REGISTERED", "job_id": job_id}
    registration = ObserverRegistration(**registered)
    _atomic_write(path, registration)
    return registration
