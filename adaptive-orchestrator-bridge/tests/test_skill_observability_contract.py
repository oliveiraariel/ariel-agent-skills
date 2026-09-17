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
