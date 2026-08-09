#!/usr/bin/env python3
"""Generate parity-critical Gemini overlays from the Codex-native source.

The Claude generator already performs the structural Codex-reviewer to async
MCP transformation. Reusing that deterministic rendering here keeps the
paper-writing and research-review semantics identical across reviewer families
instead of maintaining hand-copied, progressively stale overlays.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_GENERATOR = Path(__file__).with_name(
    "generate_codex_claude_review_overrides.py"
)
DEST_ROOT = REPO_ROOT / "skills" / "skills-codex-gemini-review"
TARGET_SKILLS = ["paper-write", "research-review"]


def _load_claude_generator():
    spec = importlib.util.spec_from_file_location(
        "aris_claude_overlay_generator", CLAUDE_GENERATOR
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator: {CLAUDE_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLAUDE = _load_claude_generator()


def render_one(skill_name: str) -> str:
    if skill_name not in TARGET_SKILLS:
        raise ValueError(f"Unsupported Gemini parity target: {skill_name}")

    text = CLAUDE.render_one(skill_name)
    # Preserve references to the repository's historical mainline while
    # replacing only reviewer-family and bridge identities.
    text = text.replace("Claude mainline", "ARIS mainline")
    replacements = (
        ("CLAUDE_REVIEW_MODEL", "GEMINI_REVIEW_MODEL"),
        ("claude-review", "gemini-review"),
        ("Claude Code", "Gemini"),
        ("Claude", "Gemini"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def generate_one(skill_name: str) -> None:
    target_dir = DEST_ROOT / skill_name
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "SKILL.md").write_text(
        render_one(skill_name), encoding="utf-8", newline="\n"
    )


def main() -> None:
    for skill_name in TARGET_SKILLS:
        generate_one(skill_name)


if __name__ == "__main__":
    main()
