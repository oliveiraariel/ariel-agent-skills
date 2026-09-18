from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"


def test_delegated_project_scope_stays_inside_adaptive_execution() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "Once OpenClaw delegates an authorized project scope to Adaptive" in text
    assert "must not continue executing that same delegated scope" in text
    assert "Delegation is an execution boundary" in text


def test_control_room_is_not_expected_to_infer_out_of_band_project_execution() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "Control Room" in text
    assert "invisibly elsewhere" in text



def test_recovery_loop_is_proactive_after_durable_admission() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "detached per-orchestration supervisor guardian" in text
    assert "do not ask the user to authorize an out-of-band fallback" in text
    assert "`resume-project` and `supervise-projects`" in text



def test_async_project_finalization_uses_authoritative_project_state() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "never" in text and "tail --pid" in text
    assert "BRIDGE_FINAL" in text
    assert "project-status --orchestration-id" in text
    assert "checkpoint filename is only a storage key" in text
    assert "previous bounded `run` precheck is historical diagnostic evidence only" in text
    assert "stale precheck" in text



def test_project_requests_have_one_explicit_bridge_execution_mode() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "no implicit default execution mode" in text
    assert "exactly once" in text
    assert "--single-unit" in text
    assert "--multi-agent" in text
    assert "Do not split phases such as discovery, implementation, tests, packaging, or handoff" in text
