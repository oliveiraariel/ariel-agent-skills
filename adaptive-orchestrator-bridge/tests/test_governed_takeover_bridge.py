import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "invoke.py"
SPEC = importlib.util.spec_from_file_location("bridge_governed_invoke", SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


def test_bridge_forwards_owner_takeover_as_management_command(monkeypatch):
    args_seen = []
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/example")
    monkeypatch.setattr(
        bridge, "_resolve_explicit_root",
        lambda root: (["/usr/bin/python3", "-m", "adaptive_orchestrator"], {}),
    )
    monkeypatch.setattr(
        bridge, "_runtime_preflight",
        lambda *args, **kwargs: {"ok": True, "found": {}},
    )
    def fake_run(**kwargs):
        args_seen.append(kwargs)
        return 0
    monkeypatch.setattr(bridge, "_run_adaptive_with_admission_retry", fake_run)
    arguments = [
        "takeover-work-unit", "--project-root", "/project",
        "--orchestration-id", "orch", "--work-unit-id", "wu",
        "--mode", "direct", "--owner-agent", "main",
        "--actor", "operator", "--reason", "stalled", "--authorize",
    ]
    assert bridge.main(arguments) == 0
    assert len(args_seen) == 1
    assert args_seen[0]["adaptive_command"] == "takeover-work-unit"
    assert args_seen[0]["guarded_arguments"] == arguments[1:]
    assert "--constraint" not in args_seen[0]["guarded_arguments"]


def test_bridge_does_not_reinterpret_takeover_as_new_orchestration(monkeypatch):
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/example")
    monkeypatch.setattr(
        bridge, "_resolve_explicit_root",
        lambda root: (["/usr/bin/python3", "-m", "adaptive_orchestrator"], {}),
    )
    monkeypatch.setattr(
        bridge, "_runtime_preflight", lambda *a, **kw: {"ok": True, "found": {}}
    )
    monkeypatch.setattr(
        bridge, "_run_adaptive_with_admission_retry",
        lambda **kwargs: pytest.fail("Mode conflict must short-circuit before dispatch"),
    )
    assert bridge.main([
        "takeover-work-unit", "--multi-agent", "--orchestration-id", "orch"
    ]) == 2
