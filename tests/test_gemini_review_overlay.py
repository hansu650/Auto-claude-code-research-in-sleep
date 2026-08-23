from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPO_ROOT / "tools" / "generate_codex_gemini_review_overrides.py"
PACK = REPO_ROOT / "skills" / "skills-codex-gemini-review"


def load_generator():
    spec = importlib.util.spec_from_file_location("gemini_overlay_generator", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parity_critical_overlays_are_exact_lf_generator_output() -> None:
    module = load_generator()
    for skill_name in module.TARGET_SKILLS:
        path = PACK / skill_name / "SKILL.md"
        data = path.read_bytes()
        assert b"\r" not in data, f"{skill_name} Gemini overlay must use LF"
        assert data.decode("utf-8") == module.render_one(skill_name), \
            f"{skill_name} Gemini overlay is stale; regenerate it"


def test_gemini_research_review_is_fail_closed() -> None:
    text = (PACK / "research-review" / "SKILL.md").read_text(encoding="utf-8")
    assert "REVIEW_UNAVAILABLE" in text and "`BLOCKED`" in text
    assert "never substitute the executor's own judgment" in text


def test_generated_gemini_overlays_are_fail_closed_and_self_contained() -> None:
    module = load_generator()
    for skill_name in module.TARGET_SKILLS:
        text = (PACK / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "REVIEW_UNAVAILABLE" in text and "`BLOCKED`" in text
        assert "Before **every** review call" in text
        assert "Paths are selectors for the executor" in text
        assert "do not record an `accepted` verdict" in text
        assert "Only after complete artifact transport" in text
        assert "is never accepted" in text
        assert "Every overlay trace/audit records" not in text
        assert "`status` is exactly `completed`" in text
        assert "`error` is empty" in text
        assert "`response` is a non-empty string" in text


def test_gemini_research_review_preserves_revised_evidence_and_output_schema() -> None:
    text = (PACK / "research-review" / "SKILL.md").read_text(encoding="utf-8")
    assert "Requested output schema: [user's requested schema, verbatim]" in text
    assert "BEGIN ARTIFACT path=/absolute/path/to/file1" in text
    assert "BEGIN ARTIFACT path=/absolute/path/to/file2" in text
