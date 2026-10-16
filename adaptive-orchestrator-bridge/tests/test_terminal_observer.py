import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "terminal_observer", ROOT / "scripts" / "terminal_observer.py"
)
observer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["terminal_observer"] = observer
SPEC.loader.exec_module(observer)


def test_registration_persists_exact_source_and_gateway_job(monkeypatch, tmp_path):
    calls = []

    class Completed:
        returncode = 0
        stdout = json.dumps({"id": "cron-job-1"})

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return Completed()

    monkeypatch.setattr(observer.subprocess, "run", fake_run)
    registration = observer.register_terminal_observer(
        command=["/venv/bin/python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-1",
        environment={
            "OPENCLAW_SESSION_KEY": "agent:main:conversation-1",
            "OPENCLAW_CONVERSATION_REF": "webchat:conversation-1",
        },
    )

    assert registration.status == "REGISTERED"
    assert registration.job_id == "cron-job-1"
    assert registration.declaration_key == "adaptive-terminal:orch-1"
    stored = json.loads(
        observer.association_path(tmp_path, "orch-1").read_text(encoding="utf-8")
    )
    assert stored["session_key"] == "agent:main:conversation-1"
    assert stored["conversation_ref"] == "webchat:conversation-1"
    params = json.loads(calls[0][0][calls[0][0].index("--params") + 1])
    assert params["sessionTarget"] == "session:agent:main:conversation-1"
    assert params["agentId"] == "main"
    assert params["delivery"] == {"mode": "announce"}
    assert params["declarationKey"] == "adaptive-terminal:orch-1"
    assert params["trigger"]["once"] is True
    assert "project-status" in params["trigger"]["script"]
    assert "release_deliveries" in params["trigger"]["script"]
    assert "terminal" in params["trigger"]["script"]


def test_existing_registered_association_is_idempotent(monkeypatch, tmp_path):
    first = observer.ObserverRegistration(
        schema_version=1,
        orchestration_id="orch-2",
        project_root=str(tmp_path),
        session_key="agent:main:conversation-2",
        conversation_ref=None,
        declaration_key="adaptive-terminal:orch-2",
        status="REGISTERED",
        job_id="cron-job-2",
        created_at="2026-01-01T00:00:00+00:00",
    )
    observer._atomic_write(observer.association_path(tmp_path, "orch-2"), first)
    monkeypatch.setattr(
        observer.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("registered observer must not be recreated")
        ),
    )
    second = observer.register_terminal_observer(
        command=["python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-2",
        environment={},
    )
    assert second == first


def test_missing_source_session_is_recorded_without_claiming_delivery(tmp_path):
    registration = observer.register_terminal_observer(
        command=["python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-3",
        environment={},
    )
    assert registration.status == "UNBOUND"
    assert registration.job_id is None
    assert "OPENCLAW_SESSION_KEY" in (registration.error or "")


def test_terminal_payload_is_short_lived_and_terminal_only(tmp_path):
    payload = observer._cron_payload(
        command=["/venv/bin/python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-long",
        session_key="agent:main:conversation-long",
    )
    assert payload["schedule"] == {"kind": "every", "everyMs": 120_000}
    assert payload["trigger"]["once"] is True
    assert "timeoutSeconds: 20" in payload["trigger"]["script"]
    assert payload["payload"]["kind"] == "agentTurn"
    assert payload["delivery"] == {"mode": "announce"}
    assert "terminal=true" in payload["payload"]["message"]
    assert "project-status" in payload["trigger"]["script"]
    assert "canonical artifact" in payload["payload"]["message"]


def test_delivery_failure_remains_pending_and_retryable(monkeypatch, tmp_path):
    class Failed:
        returncode = 1
        stdout = ""

    monkeypatch.setattr(observer.subprocess, "run", lambda *a, **k: Failed())
    registration = observer.register_terminal_observer(
        command=["python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-failure",
        environment={"OPENCLAW_SESSION_KEY": "agent:main:conversation-failure"},
    )
    assert registration.status == "PENDING"
    assert registration.job_id is None
    assert observer._load(
        observer.association_path(tmp_path, "orch-failure")
    ).status == "PENDING"


def test_missing_add_id_is_reconciled_by_declaration_key(monkeypatch, tmp_path):
    calls = []

    class Completed:
        returncode = 0

        def __init__(self, stdout):
            self.stdout = stdout

    def fake_run(args, **kwargs):
        calls.append(args[3])
        if args[3] == "cron.add":
            return Completed(json.dumps({"ok": True}))
        return Completed(
            json.dumps(
                {
                    "jobs": [
                        {
                            "id": "reconciled-job",
                            "declarationKey": "adaptive-terminal:orch-reconcile",
                        }
                    ]
                }
            )
        )

    monkeypatch.setattr(observer.subprocess, "run", fake_run)
    registration = observer.register_terminal_observer(
        command=["python", "-m", "adaptive_orchestrator"],
        project_root=tmp_path,
        orchestration_id="orch-reconcile",
        environment={"OPENCLAW_SESSION_KEY": "agent:adaptive:main"},
    )
    assert registration.status == "REGISTERED"
    assert registration.job_id == "reconciled-job"
    assert calls == ["cron.add", "cron.list"]


def test_simultaneous_projects_keep_distinct_conversations(monkeypatch, tmp_path):
    calls = []

    class Completed:
        returncode = 0

        def __init__(self, job_id):
            self.stdout = json.dumps({"id": job_id})

    def fake_run(args, **kwargs):
        calls.append(json.loads(args[args.index("--params") + 1]))
        return Completed(f"job-{len(calls)}")

    monkeypatch.setattr(observer.subprocess, "run", fake_run)
    for orchestration_id, session_key in (
        ("orch-a", "agent:main:conversation-a"),
        ("orch-b", "agent:main:conversation-b"),
    ):
        observer.register_terminal_observer(
            command=["python", "-m", "adaptive_orchestrator"],
            project_root=tmp_path,
            orchestration_id=orchestration_id,
            environment={"OPENCLAW_SESSION_KEY": session_key},
        )
    assert [call["sessionTarget"] for call in calls] == [
        "session:agent:main:conversation-a",
        "session:agent:main:conversation-b",
    ]
    assert [call["declarationKey"] for call in calls] == [
        "adaptive-terminal:orch-a",
        "adaptive-terminal:orch-b",
    ]
