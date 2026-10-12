"""Bridge forwards named profile and governed fallback commands without owning logic."""
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "invoke.py"
SPEC = importlib.util.spec_from_file_location("bridge_profile_invoke", SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


@pytest.fixture
def mocked_bridge(monkeypatch):
    seen = []
    monkeypatch.setenv("ADAPTIVE_ORCHESTRATOR_ROOT", "/example")
    monkeypatch.setattr(
        bridge, "_resolve_explicit_root",
        lambda root: (["/usr/bin/python3", "-m", "adaptive_orchestrator"], {}),
    )
    monkeypatch.setattr(
        bridge, "_runtime_preflight",
        lambda *args, **kwargs: {"ok": True, "found": {}},
    )
    monkeypatch.setattr(
        bridge, "_run_adaptive_with_admission_retry",
        lambda **kwargs: seen.append(kwargs) or 0,
    )
    return seen


@pytest.mark.parametrize("management,expected", [
    (["execution-profile", "list"], "execution-profile"),
    (["execution-profile", "show", "gpt-terra-medium-low"], "execution-profile"),
    (["fallback-direto", "--orchestration-id", "id", "--all-pending",
      "--owner-agent", "adaptive", "--actor", "user",
      "--reason", "takeover", "--authorize"], "fallback-direto"),
    (["switch-execution-profile", "--orchestration-id", "id",
      "--execution-profile", "gpt-luna-medium-low",
      "--actor", "user", "--reason", "quota", "--authorize"], "switch-execution-profile"),
])
def test_management_commands_are_forwarded_unchanged(mocked_bridge, management, expected):
    assert bridge.main(management) == 0
    assert len(mocked_bridge) == 1
    assert mocked_bridge[0]["adaptive_command"] == expected
    assert mocked_bridge[0]["guarded_arguments"] == management[1:]


def test_execution_profile_is_forwarded_with_existing_orchestration(monkeypatch, tmp_path, mocked_bridge):
    assert bridge.main([
        "--multi-agent", "--project-root", str(tmp_path),
        "--agent", "sgfp", "--planner-agent", "adaptive",
        "--execution-profile", "gpt-terra-medium-low",
        "--objective", "Approved work",
    ]) == 0
    call = mocked_bridge[0]
    assert call["adaptive_command"] == "orchestrate"
    assert "--execution-profile" in call["guarded_arguments"]
    assert "gpt-terra-medium-low" in call["guarded_arguments"]
    assert "--constraint" in call["guarded_arguments"]


def test_management_cannot_be_combined_with_new_orchestration(mocked_bridge):
    assert bridge.main([
        "fallback-direto", "--durable-single-worker", "--all-pending"
    ]) == 2
    assert mocked_bridge == []
