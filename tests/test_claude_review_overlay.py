#!/usr/bin/env python3
"""
Forbidden-token scan for the generated claude-review overlay pack.

The overlay replaces the codex-mirror's same-family reviewer with Claude via
the claude-review MCP. A leftover Codex token means the generator's rules went
stale against the mirror source (the failure mode that shipped half-converted
overlays before): a user following the overlay would call a tool that doesn't
exist or pin an OpenAI model on a Claude server.

Run: python3 tests/test_claude_review_overlay.py   (also pytest-compatible)
"""
import importlib.util
import os
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PACK = os.path.join(REPO, "skills", "skills-codex-claude-review")
GENERATOR = os.path.join(REPO, "tools", "generate_codex_claude_review_overrides.py")

FORBIDDEN = [
    "mcp__codex__",           # codex MCP tools
    "spawn_agent",            # codex-native reviewer spawn
    "followup_task",          # current codex-native follow-up
    "send_input",             # legacy codex-native follow-up
    "gpt-5.6-sol",            # OpenAI model pin (any case)
    "gpt-5.5",                # incl. old default; gpt-5.5-pro Oracle refs are fine -> checked below
    "model_reasoning_effort", # OpenAI effort knob
    "reasoning_effort",       # spawn-form effort knob
]
# Oracle Pro is a legitimate cross-reference in overlay prose
ALLOWED_SUBSTRINGS = ["gpt-5.5-pro", "GPT-5.5 Pro"]


def check_pack(pack=PACK):
    problems = []
    if not os.path.isdir(pack):
        return problems
    for dirpath, _dirnames, filenames in os.walk(pack):
        for fn in filenames:
            if fn != "SKILL.md":   # pack READMEs legitimately describe the upstream mechanics
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, REPO)
            for i, line in enumerate(open(path, encoding="utf-8"), 1):
                probe = line
                for ok in ALLOWED_SUBSTRINGS:
                    probe = probe.replace(ok, "")
                low = probe.lower()
                for tok in FORBIDDEN:
                    if tok.lower() in low:
                        problems.append(f"{rel}:{i}: forbidden token {tok!r}: {line.strip()[:100]}")
    return problems


def test_overlay_has_no_codex_tokens():
    problems = check_pack()
    assert not problems, "\n".join(problems)


def test_overlay_is_exact_generator_output_with_lf_endings():
    spec = importlib.util.spec_from_file_location("claude_overlay_generator", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for skill_name in module.TARGET_SKILLS:
        path = os.path.join(PACK, skill_name, "SKILL.md")
        data = open(path, "rb").read()
        assert b"\r" not in data, f"{skill_name} overlay must use repository LF endings"
        assert data.decode("utf-8") == module.render_one(skill_name), \
            f"{skill_name} overlay is stale; regenerate it from the Codex mirror"


def test_every_generated_overlay_is_fail_closed_and_self_contained():
    spec = importlib.util.spec_from_file_location("claude_overlay_generator", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for skill_name in module.TARGET_SKILLS:
        path = os.path.join(PACK, skill_name, "SKILL.md")
        text = open(path, encoding="utf-8").read()
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
        assert "preserve the error in the trace" in text


def test_auto_review_loop_transmits_content_instead_of_bare_paths():
    text = open(
        os.path.join(PACK, "auto-review-loop", "SKILL.md"),
        encoding="utf-8",
    ).read()
    for stale_instruction in (
        "direct repository/file-reading instructions",
        "read the files yourself",
        "Methods / code under review: <path(s)>",
        "Changed files: <paths>",
        "Updated raw results: <result-file paths>",
        "verify claims against repository files",
    ):
        assert stale_instruction not in text
    assert "Review the complete transmitted artifact bundle" in text
    assert "BEGIN ARTIFACT role=claims" in text
    assert "BEGIN ARTIFACT role=raw-diff" in text
    assert "complete content-faithful bundle" in text


def test_research_review_preserves_all_revised_evidence_and_output_schema():
    text = open(
        os.path.join(PACK, "research-review", "SKILL.md"),
        encoding="utf-8",
    ).read()
    assert "requested output schema" in text
    assert "Requested output schema: [user's requested schema, verbatim]" in text
    assert "BEGIN ARTIFACT path=/absolute/path/to/file1" in text
    assert "BEGIN ARTIFACT path=/absolute/path/to/file2" in text


if __name__ == "__main__":
    ps = check_pack()
    if ps:
        print("\n".join(ps))
        print(f"\n{len(ps)} forbidden tokens in the overlay pack")
        sys.exit(1)
    print("ok: overlay pack is fully converted")
