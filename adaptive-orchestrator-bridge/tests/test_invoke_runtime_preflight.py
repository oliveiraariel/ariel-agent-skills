import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "invoke.py"
SPEC = importlib.util.spec_from_file_location("bridge_invoke", SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


def _write_project_checkpoint(project: Path, orchestration_id: str, *, terminal: bool = True) -> None:
    path = bridge._checkpoint_path(project, orchestration_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "orchestration_id": orchestration_id,
        "desired_state": "RUNNING",
        "phase": "EXECUTION",
        "work_unit_states": {"wu": "COMPLETED" if terminal else "RUNNING"},
        "active_executions": [] if terminal else [{"work_unit_id": "wu"}],
        "pending_replan": False,
        "replan_count": 0,
        "terminal": terminal,
    }
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "orchestration_id": orchestration_id,
                "state": state,
            }
        ),
        encoding="utf-8",
    )


def _status_payload(orchestration_id: str, *, terminal: bool = True) -> dict:
    return {
        "ok": True,
        "mode": "project-status",
        "orchestration_id": orchestration_id,
        "status": "COMPLETED" if terminal else "RUNNING",
        "terminal": terminal,
        "desired_state": "RUNNING",
        "work_unit_count": 1,
        "completed_work_unit_ids": ["wu"] if terminal else [],
        "blocked_work_unit_ids": [],
        "recovery_required_work_unit_ids": [],
        "unfinished_work_unit_ids": [] if terminal else ["wu"],
        "active_execution_count": 0 if terminal else 1,
        "pending_replan": False,
        "replan_count": 0,
    }


def test_runtime_preflight_passes_with_required_modules(monkeypatch):
    class Completed:
        returncode = 0
        stdout = json.dumps(
            {
                "executable": sys.executable,
                "prefix": sys.prefix,
                "base_prefix": sys.base_prefix,
                "site_packages": [],
                "found": {
                    name: f"/modules/{name}.py"
                    for name in bridge.RUNTIME_MODULES
                },
            }
        )

    monkeypatch.setattr(
        bridge.subprocess,
        "run",
        lambda *args, **kwargs: Completed(),
    )

    result = bridge._runtime_preflight(
        [sys.executable],
        {"PYTHONPATH": "/adaptive/src"},
    )

    assert result["ok"] is True
    assert set(result["found"]) == set(bridge.RUNTIME_MODULES)


def test_runtime_preflight_reports_missing_jsonschema(monkeypatch):
    class Completed:
        returncode = 0
        stdout = json.dumps({"executable": "/venv/bin/python", "prefix": "/venv", "found": {name: None if name == "jsonschema" else "/module.py" for name in bridge.RUNTIME_MODULES}})

    monkeypatch.setattr(bridge.subprocess, "run", lambda *args, **kwargs: Completed())
    result = bridge._runtime_preflight([sys.executable], {})
    assert result["ok"] is False
    assert result["missing"] == ["jsonschema"]


def test_main_does_not_start_adaptive_when_preflight_fails(monkeypatch, capsys):
    command = [sys.executable, "-m", "adaptive_orchestrator"]
    monkeypatch.setattr(bridge, "_resolve_explicit_root", lambda root: (command, {}))
    monkeypatch.setattr(bridge, "_runtime_preflight", lambda command, environment: {"ok": False, "missing": ["jsonschema"]})
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/root")
    adaptive_run = False

    def forbidden_run(*args, **kwargs):
        nonlocal adaptive_run
        adaptive_run = True

    monkeypatch.setattr(bridge.subprocess, "run", forbidden_run)
    assert bridge.main(["--objective", "read-only"]) != 0
    assert adaptive_run is False
    assert "BRIDGE_RUNTIME_PREFLIGHT_FAILED" in capsys.readouterr().err


def test_diagnose_does_not_print_secrets(monkeypatch, capsys):
    command = [sys.executable, "-m", "adaptive_orchestrator"]
    monkeypatch.setattr(
        bridge,
        "_resolve_explicit_root",
        lambda root: (command, {"PYTHONPATH": "/tmp/src"}),
    )
    monkeypatch.setattr(
        bridge,
        "_runtime_preflight",
        lambda command, environment: {
            "ok": True,
            "found": {name: "/module.py" for name in bridge.RUNTIME_MODULES},
        },
    )

    class Completed:
        returncode = 0
        stdout = json.dumps(
            {
                "adaptive_version": "test",
                "adaptive_module_path": "/tmp/src/adaptive_orchestrator/__init__.py",
                "python_prefix": "/tmp/venv",
                "python_base_prefix": "/usr",
                "venv_active": True,
                "gateway_dependencies_available": True,
                "worker_protocol_name": "adaptive-worker-protocol",
                "worker_protocol_version": 1,
            }
        )
        stderr = ""

    monkeypatch.setattr(
        bridge.subprocess,
        "run",
        lambda *args, **kwargs: Completed(),
    )
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/root")
    monkeypatch.setenv("OPENCLAW_GATEWAY_TOKEN", "secret-token")

    assert bridge.main(["--diagnose"]) == 0
    captured = capsys.readouterr()
    assert "secret-token" not in captured.out
    assert "secret-token" not in captured.err



def test_diagnose_resolves_code_root_without_pythonpath(monkeypatch, capsys, tmp_path):
    repo = tmp_path / "adaptive-ai-orchestrator"
    module = repo / "src" / "adaptive_orchestrator" / "__init__.py"
    module.parent.mkdir(parents=True)
    module.write_text("", encoding="utf-8")
    python = repo / ".venv" / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.write_text("", encoding="utf-8")

    command = [str(python), "-m", "adaptive_orchestrator"]
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", str(repo))
    monkeypatch.delenv("PYTHONPATH", raising=False)
    monkeypatch.setattr(
        bridge,
        "_resolve_explicit_root",
        lambda root: (command, {}),
    )
    monkeypatch.setattr(
        bridge,
        "_runtime_preflight",
        lambda command, environment: {
            "ok": True,
            "found": {
                name: (
                    str(module)
                    if name == "adaptive_orchestrator"
                    else f"/modules/{name}.py"
                )
                for name in bridge.RUNTIME_MODULES
            },
        },
    )

    class Completed:
        returncode = 0
        stdout = json.dumps(
            {
                "adaptive_version": "test",
                "adaptive_module_path": str(module),
                "python_prefix": str(repo / ".venv"),
                "python_base_prefix": "/usr",
                "venv_active": True,
                "gateway_dependencies_available": True,
                "worker_protocol_name": "adaptive-worker-protocol",
                "worker_protocol_version": 1,
            }
        )
        stderr = ""

    monkeypatch.setattr(bridge.subprocess, "run", lambda *args, **kwargs: Completed())

    assert bridge.main(["--diagnose"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["resolved_code_root"] == str(repo.resolve())


def test_preflight_uses_resolved_executable_and_environment(monkeypatch):
    calls = []
    class Completed:
        returncode = 0
        stdout = json.dumps({"found": {name: "/module.py" for name in bridge.RUNTIME_MODULES}})

    def capture(args, **kwargs):
        calls.append((args, kwargs))
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", capture)
    environment = {"PYTHONPATH": "/adaptive/src"}
    bridge._runtime_preflight([sys.executable, "-m", "adaptive_orchestrator"], environment)
    assert calls[0][0][0] == sys.executable
    assert calls[0][1]["env"] is environment

def test_orchestrate_retries_once_after_proven_pre_admission_failure(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = []

    class Completed:
        def __init__(self, returncode):
            self.returncode = returncode

    def fake_run(args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return Completed(7)
        orchestration_id = bridge._argument_value(args, "--orchestration-id")
        assert orchestration_id is not None
        _write_project_checkpoint(project, orchestration_id)
        return Completed(0)

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=["--project-root", str(project), "--objective", "test"],
        environment={},
    )

    assert result == 0
    assert len(calls) == 2
    events = capsys.readouterr().err
    assert "retrying-pre-admission-failure" in events
    assert '"checkpoint_created": false' in events
    assert '"checkpoint_created": true' in events
    assert "durable-admission-materialized" in events
    assert "BRIDGE_FINAL" in events
    assert '"authoritative_project_state": true' in events


def test_orchestrate_does_not_retry_after_checkpoint_exists(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = []

    class Completed:
        returncode = 9

    def fake_run(args, **kwargs):
        calls.append(args)
        orchestration_id = bridge._argument_value(args, "--orchestration-id")
        assert orchestration_id is not None
        _write_project_checkpoint(project, orchestration_id)
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=["--project-root", str(project), "--objective", "test"],
        environment={},
    )

    assert result == 9
    assert len(calls) == 1
    events = capsys.readouterr().err
    assert '"checkpoint_created": true' in events
    assert "retrying-pre-admission-failure" not in events


def test_orchestrate_retries_once_after_child_launch_oserror(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise OSError("temporary exec failure")
        orchestration_id = bridge._argument_value(args, "--orchestration-id")
        assert orchestration_id is not None
        _write_project_checkpoint(project, orchestration_id)
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=["--project-root", str(project), "--objective", "test"],
        environment={},
    )

    assert result == 0
    assert calls == 2
    events = capsys.readouterr().err
    assert "launch-error" in events
    assert "temporary exec failure" in events


def test_orchestrate_zero_exit_without_checkpoint_retries_once_then_succeeds(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            orchestration_id = bridge._argument_value(args, "--orchestration-id")
            assert orchestration_id is not None
            _write_project_checkpoint(project, orchestration_id)
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=["--project-root", str(project), "--objective", "test"],
        environment={},
    )

    assert result == 0
    assert calls == 2
    events = capsys.readouterr().err
    assert "retrying-pre-admission-failure" in events
    assert "exit-with-durable-admission" in events
    assert '"durable_admission_verified": true' in events


def test_orchestrate_zero_exit_without_checkpoint_twice_returns_deterministic_error(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=["--project-root", str(project), "--objective", "test"],
        environment={},
    )

    assert result == bridge.DURABLE_ADMISSION_NOT_MATERIALIZED
    assert calls == 2
    events = capsys.readouterr().err
    assert "durable-admission-not-materialized" in events
    assert '"durable_admission_verified": false' in events


def test_plan_only_zero_exit_without_checkpoint_is_valid(monkeypatch, tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=[
            "--project-root",
            str(project),
            "--plan-only",
            "--objective",
            "test",
        ],
        environment={},
    )

    assert result == 0
    assert calls == 1


def test_non_orchestrate_command_never_retries(monkeypatch, tmp_path):
    calls = 0

    class Completed:
        returncode = 4

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="wait",
        guarded_arguments=["--project-root", str(tmp_path)],
        environment={},
    )

    assert result == 4
    assert calls == 1



def test_bridge_routes_supported_supervisor_command_without_worker_constraint(
    monkeypatch, tmp_path
):
    command = [sys.executable, "-m", "adaptive_orchestrator"]
    captured = {}

    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/root")
    monkeypatch.setattr(
        bridge,
        "_resolve_explicit_root",
        lambda root: (command, {"PYTHONPATH": "/adaptive/src"}),
    )
    monkeypatch.setattr(
        bridge,
        "_runtime_preflight",
        lambda command, environment: {
            "ok": True,
            "found": {name: "/module.py" for name in bridge.RUNTIME_MODULES},
        },
    )

    def fake_run(**kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(
        bridge,
        "_run_adaptive_with_admission_retry",
        fake_run,
    )

    assert bridge.main(
        [
            "supervise-projects",
            "--watch",
            "--orchestration-id",
            "orch-1",
            "--project-root",
            str(tmp_path),
        ]
    ) == 0

    assert captured["adaptive_command"] == "supervise-projects"
    assert captured["guarded_arguments"][:2] == ["--watch", "--orchestration-id"]
    assert "--constraint" not in captured["guarded_arguments"]
    assert bridge.RECURSION_GUARD not in captured["guarded_arguments"]


def test_bridge_routes_resume_project_as_recovery_management_command(
    monkeypatch, tmp_path
):
    command = [sys.executable, "-m", "adaptive_orchestrator"]
    captured = {}

    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/root")
    monkeypatch.setattr(
        bridge,
        "_resolve_explicit_root",
        lambda root: (command, {"PYTHONPATH": "/adaptive/src"}),
    )
    monkeypatch.setattr(
        bridge,
        "_runtime_preflight",
        lambda command, environment: {
            "ok": True,
            "found": {name: "/module.py" for name in bridge.RUNTIME_MODULES},
        },
    )

    def fake_run(**kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(
        bridge,
        "_run_adaptive_with_admission_retry",
        fake_run,
    )

    assert bridge.main(
        [
            "resume-project",
            "--orchestration-id",
            "orch-1",
            "--project-root",
            str(tmp_path),
        ]
    ) == 0

    assert captured["adaptive_command"] == "resume-project"
    assert "--constraint" not in captured["guarded_arguments"]



def test_bridge_routes_project_status_without_worker_constraint(
    monkeypatch, tmp_path
):
    command = [sys.executable, "-m", "adaptive_orchestrator"]
    captured = {}

    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/root")
    monkeypatch.setattr(
        bridge,
        "_resolve_explicit_root",
        lambda root: (command, {"PYTHONPATH": "/adaptive/src"}),
    )
    monkeypatch.setattr(
        bridge,
        "_runtime_preflight",
        lambda command, environment: {
            "ok": True,
            "found": {name: "/module.py" for name in bridge.RUNTIME_MODULES},
        },
    )

    def fake_run(**kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(
        bridge,
        "_run_adaptive_with_admission_retry",
        fake_run,
    )

    assert bridge.main(
        [
            "project-status",
            "--orchestration-id",
            "orch-1",
            "--project-root",
            str(tmp_path),
        ]
    ) == 0

    assert captured["adaptive_command"] == "project-status"
    assert "--constraint" not in captured["guarded_arguments"]


def test_bridge_final_line_carries_authoritative_terminal_state(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        orchestration_id = bridge._argument_value(args, "--orchestration-id")
        assert orchestration_id is not None
        _write_project_checkpoint(project, orchestration_id)
        return Completed()

    monkeypatch.setattr(bridge.subprocess, "run", fake_run)
    monkeypatch.setattr(
        bridge,
        "_project_status",
        lambda **kwargs: (_status_payload(kwargs["orchestration_id"]), None),
    )

    result = bridge._run_adaptive_with_admission_retry(
        command=[sys.executable, "-m", "adaptive_orchestrator"],
        adaptive_command="orchestrate",
        guarded_arguments=[
            "--project-root",
            str(project),
            "--objective",
            "test",
        ],
        environment={},
    )

    assert result == 0
    lines = [line for line in capsys.readouterr().err.splitlines() if line]
    assert lines[-1].startswith("BRIDGE_FINAL ")
    payload = json.loads(lines[-1].split(" ", 1)[1])
    assert payload["authoritative_project_state"] is True
    assert payload["terminal"] is True
    assert payload["status"] == "COMPLETED"
    assert payload["returncode"] == 0
    assert payload["orchestration_id"]
