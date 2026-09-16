import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "invoke.py"
SPEC = importlib.util.spec_from_file_location("bridge_invoke", SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


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
    calls = []

    class Completed:
        def __init__(self, returncode):
            self.returncode = returncode

    def fake_run(args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return Completed(7)
        checkpoint_dir = project / ".adaptive" / "orchestrations"
        checkpoint_dir.mkdir(parents=True)
        (checkpoint_dir / "accepted.json").write_text("{}", encoding="utf-8")
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


def test_orchestrate_does_not_retry_after_checkpoint_exists(
    monkeypatch, tmp_path, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    calls = []

    class Completed:
        returncode = 9

    def fake_run(args, **kwargs):
        calls.append(args)
        checkpoint_dir = project / ".adaptive" / "orchestrations"
        checkpoint_dir.mkdir(parents=True)
        (checkpoint_dir / "admitted.json").write_text("{}", encoding="utf-8")
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
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise OSError("temporary exec failure")
        checkpoint_dir = project / ".adaptive" / "orchestrations"
        checkpoint_dir.mkdir(parents=True)
        (checkpoint_dir / "accepted.json").write_text("{}", encoding="utf-8")
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
    calls = 0

    class Completed:
        returncode = 0

    def fake_run(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            checkpoint_dir = project / ".adaptive" / "orchestrations"
            checkpoint_dir.mkdir(parents=True)
            (checkpoint_dir / "admitted.json").write_text("{}", encoding="utf-8")
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

