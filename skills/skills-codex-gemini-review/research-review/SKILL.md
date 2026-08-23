---
name: "research-review"
description: "Get a deep critical review of research from Gemini via gemini-review MCP. Use when user says \"review my research\", \"help me review\", \"get external review\", or wants critical feedback on research ideas, papers, or experimental results."
---

> Override for Codex users who want **Gemini**, not a second Codex agent, to act as the reviewer. Install this package **after** `skills/skills-codex/*`.
>
> This reviewer is a different model family from the Codex executor. Only after complete artifact transport and a grounded external review response may the trace/audit record:
>
> ```yaml
> review_independence: cross-family
> acceptance_status: accepted
> ```
> A bridge or artifact-transport failure records `REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted.

# Research Review via `gemini-review` MCP (high-rigor review)

> **Gemini overlay assurance:** this route is a different model family from the Codex executor. Record `review_independence: cross-family` and `acceptance_status: accepted` only after complete artifact transport and a grounded external review response. A bridge or transport failure records `REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted.

Get a multi-round critical review of research work from an external LLM with maximum reasoning depth.

## Constants

- **REVIEWER_MODEL = `gemini-review`** — Gemini reviewer invoked through the local `gemini-review` MCP bridge. Set `GEMINI_REVIEW_MODEL` if you need a specific Gemini model override.
- **REVIEWER_BACKEND = `gemini-review`** — reviews route through the gemini-review MCP (Gemini family; cross-family for a Codex executor).

## Context: $ARGUMENTS

## Prerequisites

- Install the base Codex-native skills first: copy `skills/skills-codex/*` into `~/.codex/skills/`.
- Then install this overlay package: copy `skills/skills-codex-gemini-review/*` into `~/.codex/skills/` and allow it to overwrite the same skill names.
- Register the local reviewer bridge:
  ```bash
  codex mcp add gemini-review -- python3 ~/.codex/mcp-servers/gemini-review/server.py
  ```
- This gives Codex access to `mcp__gemini-review__review_start`, `mcp__gemini-review__review_reply_start`, and `mcp__gemini-review__review_status`.
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

## Workflow

### Step 1: Build a Content-Faithful Artifact Bundle

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
content with an executor-authored briefing.

### Step 2: Initial Review (Round 1)
Send a detailed prompt for high-rigor review:

```
mcp__gemini-review__review_start:
  prompt: |
    Review objective: [user's objective]
    Target venue: [venue or unknown]
    Requested output schema: [user's requested schema, verbatim]
    Primary artifact bundle (complete source content, not a summary):
    --- BEGIN ARTIFACT path=/absolute/path/to/paper-or-report sha256=<hex> extraction=<method+version> ---
    [complete verbatim or deterministically extracted content]
    --- END ARTIFACT path=/absolute/path/to/paper-or-report ---
    --- BEGIN ARTIFACT path=/absolute/path/to/results-or-plan sha256=<hex> extraction=<method+version> ---
    [complete verbatim content]
    --- END ARTIFACT path=/absolute/path/to/results-or-plan ---

    Please act as a senior ML reviewer (NeurIPS/ICML level). Start from the
    assumption that the work is broken somewhere — your job is to find where.
    Be adversarial. Trust nothing the author tells you — verify everything
    yourself. Identify:
    1. Logical gaps or unjustified claims
    2. Missing experiments that would strengthen the story
    3. Narrative weaknesses
    4. Whether the contribution is sufficient for a top venue
    Please be brutally honest.
```

After this review call, immediately save the returned `jobId` and poll `mcp__gemini-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

### Step 3: Iterative Dialogue (Rounds 2-N)
Use `mcp__gemini-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__gemini-review__review_status` with the returned `jobId` until `done=true` to continue the conversation:

```
mcp__gemini-review__review_reply_start:
  threadId: [saved reviewer id from Step 2]
  prompt: |
    Please continue the review using the revised materials below.

    Revised artifact bundle (same complete-content and SHA-256 rules):
    --- BEGIN ARTIFACT path=/absolute/path/to/file1 sha256=<hex> extraction=<method+version> ---
    [complete revised content]
    --- END ARTIFACT path=/absolute/path/to/file1 ---
    --- BEGIN ARTIFACT path=/absolute/path/to/file2 sha256=<hex> extraction=<method+version> ---
    [complete revised content]
    --- END ARTIFACT path=/absolute/path/to/file2 ---

    Focus on unresolved weaknesses and whether the revision actually fixed them.
```

After this review call, immediately save the returned `jobId` and poll `mcp__gemini-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

For each round, provide a complete content-faithful bundle of every revised
artifact or request a focused re-check using source content already present
in that reviewer thread. Do not inject the executor's interpretation of the
prior verdict or coach the reviewer toward acceptance.

Key follow-up patterns:
- "If we reframe X as Y, does that change your assessment?"
- "What's the minimum experiment to satisfy concern Z?"
- "Please design the minimal additional experiment package (highest acceptance lift per GPU week)"
- "Please write a mock NeurIPS/ICML review with scores"
- "Give me a results-to-claims matrix for possible experimental outcomes"

### Step 4: Convergence
Stop iterating when:
- Both sides agree on the core claims and their evidence requirements
- A concrete experiment plan is established
- The narrative structure is settled

### Step 5: Document Everything
Save the full interaction and conclusions to a review document in the project root:
- Round-by-round summary of criticisms and responses
- Final consensus on claims, narrative, and experiments
- Claims matrix (what claims are allowed under each possible outcome)
- Prioritized TODO list with estimated compute costs
- Paper outline if discussed

Update project memory/notes with key review conclusions.

If `— composed: <canonical-report-path>` is explicitly present, fold consensus,
claims matrix, TODOs, and trace links into that report instead of writing a
standalone review document. Without the directive, write the standalone review
as documented; never infer composed mode from an existing file. `— standalone`
always wins. See
[`output-composition.md`](../shared-references/output-composition.md).

### Step 6: Review Tracing

Save a trace for every `mcp__gemini-review__review_start`, `mcp__gemini-review__review_reply_start`, or `oracle-pro` review call following `../shared-references/review-tracing.md`. Record the reviewer route, saved threadId, prompt summary, raw response path, decisions, and action items. This preserves the ARIS mainline Review Tracing semantics while using Codex-native reviewer calls.

## Key Rules

- **Always ask the Gemini reviewer for strict, high-rigor feedback** in every review round.
- Send complete content-faithful artifact bundles with source SHA-256 values; paths alone are insufficient
- Be honest about weaknesses — hiding them leads to worse feedback
- Push back on criticisms you disagree with, but accept valid ones
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Document the completed `threadId` for potential future resumption
- The review document should be self-contained (readable without the conversation)

## Prompt Templates

### For initial review:
"I'm going to present a complete ML research project for your critical review. Please act as a senior ML reviewer (NeurIPS/ICML level)..."

### For experiment design:
"Please design the minimal additional experiment package that gives the highest acceptance lift per GPU week. Our compute: [describe]. Be very specific about configurations."

### For paper structure:
"Please turn this into a concrete paper outline with section-by-section claims and figure plan."

### For claims matrix:
"Please give me a results-to-claims matrix: what claim is allowed under each possible outcome of experiments X and Y?"

### For mock review:
"Please write a mock NeurIPS review with: Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."
