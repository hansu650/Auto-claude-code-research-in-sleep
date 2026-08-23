#!/usr/bin/env python3
"""Generate Claude-review overrides for the upstream Codex-native skills."""

from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "skills" / "skills-codex"
DEST_ROOT = REPO_ROOT / "skills" / "skills-codex-claude-review"

TARGET_SKILLS = [
    "research-review",
    "novelty-check",
    "research-refine",
    "auto-review-loop",
    "paper-plan",
    "paper-figure",
    "paper-write",
    "auto-paper-improvement-loop",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
SPAWN_BLOCK_RE = re.compile(r"```(?:yaml|text)?\nspawn_agent:\n([\s\S]*?)```")
FOLLOWUP_BLOCK_RE = re.compile(r"```(?:yaml|text)?\n(?:followup_task|send_input):\n([\s\S]*?)```")

OVERRIDE_NOTE = (
    "> Override for Codex users who want **Claude Code**, not a second Codex agent, "
    "to act as the reviewer. Install this package **after** `skills/skills-codex/*`.\n>\n"
    "> This reviewer is a different model family from the Codex executor. Only "
    "after complete artifact transport and a grounded external review response "
    "may the trace/audit record:\n>\n> ```yaml\n> review_independence: cross-family\n"
    "> acceptance_status: accepted\n> ```\n> A bridge or artifact-transport failure "
    "records `REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted."
)

REVIEWER_LINE = (
    "- **REVIEWER_MODEL = `claude-review`** — Claude reviewer invoked through the "
    "local `claude-review` MCP bridge. Set `CLAUDE_REVIEW_MODEL` if you need a "
    "specific Claude model override."
)

PREREQ_BLOCK = """## Prerequisites

- Install the base Codex-native skills first: copy `skills/skills-codex/*` into `~/.codex/skills/`.
- Then install this overlay package: copy `skills/skills-codex-claude-review/*` into `~/.codex/skills/` and allow it to overwrite the same skill names.
- Register the local reviewer bridge:
  ```bash
  codex mcp add claude-review -- python3 ~/.codex/mcp-servers/claude-review/server.py
  ```
- This gives Codex access to `mcp__claude-review__review_start`, `mcp__claude-review__review_reply_start`, and `mcp__claude-review__review_status`.
- If the bridge is unavailable, report `REVIEW_UNAVAILABLE` / `BLOCKED`;
  never substitute the executor's own judgment for an independent review.
- The default bridge receives prompt content, not arbitrary local-file access.
  Before **every** review call, expand every path-like placeholder in the
  templates below into a complete content-faithful artifact bundle with
  absolute path, source SHA-256, extraction method/version, and explicit
  `BEGIN/END ARTIFACT` boundaries. Paths are selectors for the executor to
  expand; paths alone are never reviewer evidence.
- Include text/code verbatim. For PDFs, include complete deterministically
  extracted text and the original PDF hash. Attach supported images with their
  hashes when the bridge supports them. If any required text, diff, result,
  PDF, or visual artifact cannot be transmitted faithfully within request and
  model limits, report `REVIEW_UNAVAILABLE` / `BLOCKED`; do not silently
  truncate it and do not record an `accepted` verdict.
""".strip()


def extract_field(frontmatter: str, field: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(frontmatter)
    if not match:
        return ""
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            value = value[1:-1]
    return value


def build_frontmatter(name: str, description: str) -> str:
    safe_desc = description.replace('"', '\\"')
    return f'---\nname: "{name}"\ndescription: "{safe_desc}"\n---\n\n'


def normalize_description(text: str) -> str:
    text = text or "Claude-review override for a Codex-native ARIS skill."
    text = text.replace("GPT using a secondary Codex agent", "Claude via claude-review MCP")
    text = text.replace("using a secondary Codex agent", "using Claude Code via claude-review MCP")
    text = text.replace("via GPT-5.6-Sol xhigh review", "via Claude review through claude-review MCP")
    text = text.replace("(Codex GPT-5.6-Sol ultra)", "(Claude via claude-review MCP)")
    text = text.replace("(Codex GPT-5.6-Sol xhigh)", "(Claude via claude-review MCP)")
    text = text.replace("iterative GPT-5.6-Sol review", "iterative Claude review")
    text = text.replace("GPT-5.6-Sol", "Claude")
    text = text.replace("via GPT-5.6-Sol ultra review", "via Claude review through claude-review MCP")
    text = text.replace("via GPT-5.5 xhigh review", "via Claude review through claude-review MCP")
    text = text.replace("GPT-5.5", "Claude through claude-review MCP")
    return text


def rewrite_spawn_block(match: re.Match[str]) -> str:
    lines = match.group(1).splitlines()
    out = ["```", "mcp__claude-review__review_start:"]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        if stripped.startswith("model:") or stripped.startswith("reasoning_effort:"):
            continue
        if stripped.startswith("message:"):
            out.append(line.replace("message:", "prompt:", 1))
            continue
        out.append(line)
    out.append("```")
    return "\n".join(out)


def rewrite_followup_block(match: re.Match[str]) -> str:
    lines = match.group(1).splitlines()
    out = ["```", "mcp__claude-review__review_reply_start:"]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        if stripped.startswith("model:") or stripped.startswith("reasoning_effort:"):
            continue
        if stripped.startswith("target:"):
            out.append(line.replace("target:", "threadId:", 1))
            continue
        if stripped.startswith("agent_id:"):
            out.append(line.replace("agent_id:", "threadId:", 1))
            continue
        if stripped.startswith("id:"):
            out.append(line.replace("id:", "threadId:", 1))
            continue
        if stripped.startswith("message:"):
            out.append(line.replace("message:", "prompt:", 1))
            continue
        out.append(line)
    out.append("```")
    return "\n".join(out)


def append_async_notes(text: str) -> str:
    note = (
        "After this review call, immediately save the returned `jobId` and poll "
        "`mcp__claude-review__review_status` with a bounded `waitSeconds` until "
        "`done=true`. A terminal payload is usable only when `status` is exactly "
        "`completed`, `error` is empty, and `response` is a non-empty string. Only "
        "then treat `response` as reviewer output and save the completed `threadId` "
        "for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, "
        "preserve the error in the trace, and do not record an `accepted` review."
    )

    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        if note in block:
            return block
        return f"{block}\n\n{note}"

    return re.sub(
        r"```(?:yaml|text)?\n(?:mcp__claude-review__review_start:|mcp__claude-review__review_reply_start:)[\s\S]*?```",
        repl,
        text,
    )


def rewrite_external_artifact_delivery(text: str) -> str:
    """Make path-based Codex review prompts self-contained for MCP bridges.

    A spawned Codex agent can read local absolute paths. The default Claude and
    Gemini review bridges cannot, so an external overlay must carry exact source
    content in the prompt instead of pretending the reviewer can open a path.
    """
    step_one = """### Step 1: Build a Content-Faithful Artifact Bundle

Resolve the user-named artifacts, but do not ask the external bridge to open
local paths. Its default reviewer receives prompt content, not filesystem
access. Build a deterministic bundle containing every required artifact:

- For text/code, include the complete content without summarizing, selecting
  passages, or inserting the executor's interpretation.
- For PDFs, record the original file SHA-256 plus the deterministic extractor
  and version, then include the complete extracted text.
- For a supported image input, attach the image and record its SHA-256; if a
  required non-text artifact cannot be transmitted faithfully, stop.
- Delimit every item with absolute path, SHA-256, extraction method, and
  `BEGIN/END ARTIFACT` boundaries.
- Carry the user's review objective, target venue, and requested output schema
  verbatim into the reviewer prompt; do not reinterpret or omit them.

If any required artifact cannot be included within the bridge/model limits,
ask the user to narrow the review scope or report `REVIEW_UNAVAILABLE` /
`BLOCKED`. Never silently truncate, send paths alone, or replace source
content with an executor-authored briefing."""
    text = re.sub(
        r"(?ms)^### Step 1: Resolve Primary Artifacts\n.*?(?=^### Step 2:)",
        step_one + "\n\n",
        text,
        count=1,
    )
    text = text.replace(
        "    Primary artifacts (read these directly):\n"
        "    - /absolute/path/to/paper-or-report\n"
        "    - /absolute/path/to/results-or-plan",
        "    Primary artifact bundle (complete source content, not a summary):\n"
        "    --- BEGIN ARTIFACT path=/absolute/path/to/paper-or-report "
        "sha256=<hex> extraction=<method+version> ---\n"
        "    [complete verbatim or deterministically extracted content]\n"
        "    --- END ARTIFACT path=/absolute/path/to/paper-or-report ---\n"
        "    --- BEGIN ARTIFACT path=/absolute/path/to/results-or-plan "
        "sha256=<hex> extraction=<method+version> ---\n"
        "    [complete verbatim content]\n"
        "    --- END ARTIFACT path=/absolute/path/to/results-or-plan ---",
    )
    text = text.replace(
        "    Target venue: [venue or unknown]\n"
        "    Primary artifact bundle",
        "    Target venue: [venue or unknown]\n"
        "    Requested output schema: [user's requested schema, verbatim]\n"
        "    Primary artifact bundle",
    )
    text = text.replace(
        "    Revised files:\n"
        "    - /absolute/path/to/file1\n"
        "    - /absolute/path/to/file2",
        "    Revised artifact bundle (same complete-content and SHA-256 rules):\n"
        "    --- BEGIN ARTIFACT path=/absolute/path/to/file1 sha256=<hex> "
        "extraction=<method+version> ---\n"
        "    [complete revised content]\n"
        "    --- END ARTIFACT path=/absolute/path/to/file1 ---\n"
        "    --- BEGIN ARTIFACT path=/absolute/path/to/file2 sha256=<hex> "
        "extraction=<method+version> ---\n"
        "    [complete revised content]\n"
        "    --- END ARTIFACT path=/absolute/path/to/file2 ---",
    )
    text = text.replace(
        "For each round, provide revised primary artifacts or request a focused\n"
        "re-check of issues raised by that reviewer. Do not inject the executor's\n"
        "interpretation of the prior verdict or coach the reviewer toward acceptance.",
        "For each round, provide a complete content-faithful bundle of every revised\n"
        "artifact or request a focused re-check using source content already present\n"
        "in that reviewer thread. Do not inject the executor's interpretation of the\n"
        "prior verdict or coach the reviewer toward acceptance.",
    )
    text = text.replace(
        "- Send absolute artifact paths in Round 1 and require the reviewer to read them directly",
        "- Send complete content-faithful artifact bundles with source SHA-256 values; paths alone are insufficient",
    )
    text = text.replace(
        "Send a detailed prompt with ultra reasoning:",
        "Send a detailed prompt for high-rigor review:",
    )
    text = text.replace(
        "In `nightmare`, launch an additional fresh adversarial reviewer with "
        "direct repository/file-reading instructions. It should read "
        "`NARRATIVE_REPORT.md` or `review-stage/AUTO_REVIEW.md` for the author's "
        "claims, then verify those claims against code, logs, result files, and "
        "paper drafts instead of trusting executor summaries.",
        "In `nightmare`, launch an additional fresh adversarial reviewer with an "
        "independently assembled, content-faithful artifact bundle. Include the "
        "complete claims, code, logs, result files, and paper drafts with source "
        "hashes; never substitute executor summaries or bare repository paths.",
    )
    text = text.replace(
        "    Review the work directly from its artifacts — executor notes are not\n"
        "    evidence, so read the files yourself rather than trusting my framing:\n"
        "    - Claims / paper draft: <path>\n"
        "    - Methods / code under review: <path(s)>\n"
        "    - Raw results (verbatim files, not a summary): <path(s)>\n"
        "    - Changed since last round: <changed-file paths> — read the diff, not my description",
        "    Review the complete transmitted artifact bundle below. Executor notes\n"
        "    and bare paths are not evidence; each item must contain its source hash\n"
        "    and complete content:\n"
        "    --- BEGIN ARTIFACT role=claims path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete paper draft or claims content]\n"
        "    --- END ARTIFACT role=claims ---\n"
        "    --- BEGIN ARTIFACT role=methods path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete methods or code content]\n"
        "    --- END ARTIFACT role=methods ---\n"
        "    --- BEGIN ARTIFACT role=results path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete raw result content]\n"
        "    --- END ARTIFACT role=results ---\n"
        "    --- BEGIN ARTIFACT role=changes path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete raw diff content]\n"
        "    --- END ARTIFACT role=changes ---",
    )
    text = text.replace(
        "Use everything in hard mode, then ask an additional fresh adversarial "
        "reviewer to verify claims against repository files, logs, result files, "
        "and paper drafts instead of trusting executor summaries. Preserve the "
        "fresh review as a separate raw response and trace.",
        "Use everything in hard mode, then give an additional fresh adversarial "
        "reviewer an independently assembled, complete content-faithful bundle of "
        "the claims, code, logs, result files, and paper drafts. Preserve the fresh "
        "review as a separate raw response and trace.",
    )
    text = text.replace(
        "    Since your last review these files changed — read them yourself; do not\n"
        "    take my word for what changed or whether it worked:\n"
        "    - Changed files: <paths>\n"
        "    - Raw diff: <path, or the `git diff` range>\n"
        "    - Updated raw results: <result-file paths> (verbatim files, not a pasted table)",
        "    Review this complete revised-artifact bundle; do not rely on my\n"
        "    description of what changed or whether it worked:\n"
        "    --- BEGIN ARTIFACT role=revised-files path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete revised file content]\n"
        "    --- END ARTIFACT role=revised-files ---\n"
        "    --- BEGIN ARTIFACT role=raw-diff path=<absolute-path-or-range> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete raw diff]\n"
        "    --- END ARTIFACT role=raw-diff ---\n"
        "    --- BEGIN ARTIFACT role=updated-results path=<absolute-path> sha256=<hex> extraction=<method+version> ---\n"
        "    [complete updated raw result content]\n"
        "    --- END ARTIFACT role=updated-results ---",
    )
    return text


def ensure_prerequisites(text: str) -> str:
    """Replace base prerequisites or insert the external-bridge contract."""
    pattern = re.compile(
        r"(?ms)^## Prerequisites\s*\n.*?(?=^## )"
    )
    if pattern.search(text):
        return pattern.sub(PREREQ_BLOCK + "\n\n", text, count=1)

    cold_start_end = "<!-- END ARIS NEUTRAL: COLD START -->"
    if cold_start_end in text:
        insert_at = text.index(cold_start_end) + len(cold_start_end)
        return text[:insert_at] + "\n\n" + PREREQ_BLOCK + text[insert_at:]

    first_section = re.search(r"(?m)^## ", text)
    if first_section:
        return text[:first_section.start()] + PREREQ_BLOCK + "\n\n" + text[first_section.start():]
    return text.rstrip() + "\n\n" + PREREQ_BLOCK + "\n"


def transform_body(text: str) -> str:
    text = re.sub(
        r"> \*\*Codex assurance:\*\*[\s\S]*?(?=\n\n)",
        "> **Claude overlay assurance:** this route is a different model family "
        "from the Codex executor. Record `review_independence: cross-family` and "
        "`acceptance_status: accepted` only after complete artifact transport and "
        "a grounded external review response. A bridge or transport failure records "
        "`REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted.",
        text,
        count=1,
    )
    text = text.replace("secondary Codex agent", "Claude reviewer via `claude-review` MCP")
    text = text.replace("via a Claude reviewer via `claude-review` MCP (xhigh reasoning)", "via `claude-review` MCP (high-rigor review)")
    text = text.replace("secondary Codex agent (xhigh reasoning)", "Claude reviewer via `claude-review` MCP")
    text = text.replace("GPT-5.6-Sol xhigh", "Claude review")
    text = text.replace("GPT-5.6-Sol ultra", "Claude review")
    text = text.replace("GPT-5.5 xhigh", "Claude review")
    text = text.replace("Send the full paper text to GPT-5.5 xhigh:", "Send the full paper text to Claude through `claude-review`:")
    text = text.replace("Send the complete outline to GPT-5.5 xhigh for feedback:", "Send the complete outline to Claude for feedback:")
    text = text.replace("Call REVIEWER_MODEL via `spawn_agent` (`spawn_agent`) with xhigh reasoning:", "Call REVIEWER_MODEL via `mcp__claude-review__review_start` with high-rigor review:")
    text = text.replace("Send a detailed prompt with xhigh reasoning:", "Send a detailed prompt with high-rigor review:")
    text = text.replace("Use `followup_task` with the returned agent id to continue the conversation:", "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` until `done=true` to continue the conversation:")
    text = text.replace("Use `send_input` with the returned agent id to continue the conversation:", "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` until `done=true` to continue the conversation:")
    text = text.replace("If this is round 2+, use `followup_task` with the saved agent id to maintain continuity.", "If this is round 2+, use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` until `done=true` to maintain continuity.")
    text = text.replace("If this is round 2+, use `send_input` with the saved agent id to maintain continuity.", "If this is round 2+, use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` until `done=true` to maintain continuity.")
    text = text.replace("Save the agent id for Round 2.", "Save the returned `jobId`, poll `mcp__claude-review__review_status` until `done=true`, then save the completed `threadId` for Round 2.")
    text = text.replace("Save agent id from first call, use `followup_task` for subsequent rounds", "Save the completed `threadId` from the first `mcp__claude-review__review_status` result, then use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for subsequent rounds")
    text = text.replace("Save agent id from first call, use `send_input` for subsequent rounds", "Save the completed `threadId` from the first `mcp__claude-review__review_status` result, then use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for subsequent rounds")
    text = text.replace("Document the agent id for potential future resumption", "Document the completed `threadId` for potential future resumption")
    text = text.replace("Use `followup_task` with the saved agent id:", "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`:")
    text = text.replace("Use `send_input` with the saved agent id:", "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`:")
    text = text.replace("use `followup_task` for Round 2 to maintain conversation context", "use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for Round 2 to maintain conversation context")
    text = text.replace("use `send_input` for Round 2 to maintain conversation context", "use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for Round 2 to maintain conversation context")
    text = text.replace("Save the agent id for Round 2.", "Save the completed `threadId` for Round 2.")
    text = text.replace("**CRITICAL: Save the `agent_id`** from this call for all later rounds.", "**CRITICAL: Save the returned `jobId`**, poll `mcp__claude-review__review_status` until `done=true`, then save the completed `threadId` from the status result for all later rounds.")
    text = text.replace("- **ALWAYS use `reasoning_effort: xhigh`** for all Codex review calls.", "- **Always ask the Claude reviewer for strict, high-rigor feedback** in every review round.")
    text = text.replace("- ALWAYS use `model: gpt-5.6-sol` + `reasoning_effort: ultra` for reviews (deep-audit tier; capability fallback per `reviewer-routing.md`, never below `xhigh`)", "- **Always ask the Claude reviewer for strict, high-rigor feedback** in every review round.")
    text = text.replace("- **Save `agent_id` from Phase 2** and use `followup_task` for later rounds.", "- **Save the completed `threadId` from Phase 2** and use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for later rounds.")
    text = text.replace("- **Save `agent_id` from Phase 2** and use `send_input` for later rounds.", "- **Save the completed `threadId` from Phase 2** and use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for later rounds.")
    text = text.replace("- **Use `followup_task`** for Round 2 to maintain conversation context", "- **Use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status`** for Round 2 to maintain conversation context")
    text = text.replace("- **Use `send_input`** for Round 2 to maintain conversation context", "- **Use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status`** for Round 2 to maintain conversation context")
    text = text.replace("GPT-5.5 responses", "Claude reviewer responses")
    text = text.replace("same-family provisional review", "cross-family accepted Claude review")
    text = text.replace("same-family provisional", "cross-family accepted")
    text = text.replace("A fresh Codex positive review", "A fresh Claude positive review")
    text = re.sub(
        r"^- \*\*REVIEWER_BACKEND = `codex`\*\*.*$",
        "- **REVIEWER_BACKEND = `claude-review`** — Cross-family Claude reviewer "
        "through the local bridge; positive verdicts record accepted.",
        text,
        flags=re.MULTILINE,
    )
    text = text.replace("`agent_id`", "`thread_id`")
    text = text.replace('"agent_id"', '"thread_id"')
    text = text.replace("ALWAYS use `reasoning_effort: xhigh` for reviews", "Always ask the Claude reviewer for strict, high-rigor feedback.")
    text = text.replace("ALWAYS use `reasoning_effort: xhigh` for maximum reasoning depth", "Always ask the Claude reviewer for strict, high-rigor feedback.")
    text = text.replace("mcp__codex__codex-reply", "mcp__claude-review__review_reply_start")
    text = text.replace("mcp__codex__codex", "mcp__claude-review__review_start")
    text = re.sub(r"^-\s+\*{0,2}REVIEWER_MODEL.*$", REVIEWER_LINE, text, flags=re.MULTILINE)
    text = re.sub(r"^-\s+\*{0,2}REVIEWER_BACKEND.*$",
                  "- **REVIEWER_BACKEND = `claude-review`** — reviews route through the claude-review MCP (Claude family; cross-family for a Codex executor).",
                  text, flags=re.MULTILINE)
    text = text.replace("GPT-5.6-Sol", "Claude")
    text = text.replace("gpt-5.6-sol", "the claude-review model")
    text = text.replace("uses normal Codex xhigh review through", "uses a normal high-rigor Claude review through")
    text = text.replace("Claude review Review (Round", "Claude Review (Round")
    text = text.replace("Never pass a prior agent_id into", "Never pass a prior threadId into")
    text = text.replace("store the returned agent_id for crash recovery only", "store the returned threadId for crash recovery only")
    text = text.replace("Save the agent_id for Round 2.", "Save the completed threadId for Round 2.")
    text = text.replace("Save the returned agent_id only for recovery bookkeeping.", "Save the returned threadId only for recovery bookkeeping.")
    text = text.replace("via a Claude reviewer via `claude-review` MCP (ultra reasoning)", "via `claude-review` MCP (high-rigor review)")
    text = text.replace("saved agent id", "saved threadId")
    text = text.replace("— Codex Review", "— Claude Review")
    # generic prose mop-up — AFTER all longer specific rows
    text = text.replace("`spawn_agent`", "`mcp__claude-review__review_start`")
    text = text.replace("`followup_task`", "`mcp__claude-review__review_reply_start`")
    text = text.replace("`send_input`", "`mcp__claude-review__review_reply_start`")
    text = ensure_prerequisites(text)
    text = SPAWN_BLOCK_RE.sub(rewrite_spawn_block, text)
    text = FOLLOWUP_BLOCK_RE.sub(rewrite_followup_block, text)
    text = text.replace(
        "```\nreasoning_effort: xhigh\n```",
        "```\nmcp__claude-review__review_start:\n  prompt: |\n    [Full novelty briefing + prior work list + specific novelty questions]\n```",
    )
    # New base-skill prose can mention Codex-native routes outside fenced tool
    # examples. Normalize those residual references after rewriting the blocks so
    # generated overlays never instruct users to mix Codex agents with Claude MCP.
    text = text.replace("Codex xhigh review", "Claude high-rigor review")
    text = text.replace("Codex Review", "Claude Review")
    text = text.replace("Codex/GPT-5.5", "Claude reviewer")
    text = text.replace("GPT-5.5", "the Claude reviewer")
    text = text.replace("spawn_agent", "mcp__claude-review__review_start")
    text = text.replace("followup_task", "mcp__claude-review__review_reply_start")
    text = text.replace("send_input", "mcp__claude-review__review_reply_start")
    text = text.replace("agent_id", "threadId")
    text = text.replace("thread_id", "threadId")
    text = text.replace("agent id", "completed threadId")
    text = text.replace("agent ID", "completed threadId")
    text = text.replace("same agent", "same completed threadId")
    return append_async_notes(rewrite_external_artifact_delivery(text))


def render_one(skill_name: str) -> str:
    skill_path = SRC_ROOT / skill_name / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"Missing frontmatter: {skill_path}")

    frontmatter = match.group(1)
    body = content[match.end():].lstrip("\n")
    name = extract_field(frontmatter, "name") or skill_name
    description = normalize_description(extract_field(frontmatter, "description"))

    output = build_frontmatter(name, description)
    output += OVERRIDE_NOTE + "\n\n"
    output += transform_body(body).rstrip() + "\n"
    return output


def generate_one(skill_name: str) -> None:
    output = render_one(skill_name)

    target_dir = DEST_ROOT / skill_name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "SKILL.md").write_text(output, encoding="utf-8", newline="\n")


def main() -> None:
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    for skill_name in TARGET_SKILLS:
        generate_one(skill_name)


if __name__ == "__main__":
    main()
