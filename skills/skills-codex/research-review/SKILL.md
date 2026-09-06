---
name: "research-review"
description: "Provide an independent, critical review of research ideas, manuscripts or experimental results using a secondary Codex agent. Use for research review, 审阅研究方案, or external feedback on a paper. General code review, configuration review and editing a Skill are outside this research workflow."
---

# Research Review via a secondary Codex agent (ultra reasoning)

> **Codex assurance:** the fresh base reviewer is same-family. Record
> `review_independence: same-family` and `acceptance_status: provisional` in
> traces and deliverables. A Claude/Gemini overlay may record cross-family
> accepted; an unavailable reviewer is BLOCKED, never a fabricated PASS.

Get a critical review of the requested research artifacts. A single complete review is the default; follow up only when revised evidence or a concrete unresolved question warrants it.

## Constants

- REVIEWER_MODEL = `gpt-5.6-sol` — Model used via a secondary Codex agent, reasoning effort `ultra` (deep-audit tier).
- **REVIEWER_BACKEND = `codex`** — Default: Codex ultra reviewer (deep-audit tier). Use `--reviewer: oracle-pro` only when explicitly requested; if Oracle is unavailable, warn and fall back to Codex at this skill's declared tier (`ultra`). **Same-family note:** this default reviewer is a second Codex/GPT agent — valid for Type-A completeness/drive review, but not a cross-family Type-B verdict; install a `skills-codex-claude-review` / `skills-codex-gemini-review` overlay for a cross-family acquittal (see `shared-references/reviewer-routing.md`).

## Context: $ARGUMENTS

## Prerequisites

- This independent-review workflow uses a secondary reviewer through `spawn_agent` and, when needed, `send_input`, subject to the host delegation policy and any user restriction. Do not require a separate magic phrase granting delegation when the requested workflow and applicable instructions already authorize it.
- If delegation is unavailable or not allowed, report `REVIEW_UNAVAILABLE` /
  `BLOCKED` for the independent review. Continue any authorized artifact preparation or clearly labeled executor feedback that remains useful; do not impersonate an independent reviewer. Follow `../shared-references/reviewer-routing.md` for supported routes and actual tool arguments.

## Workflow

### Step 1: Resolve Primary Artifacts

Resolve absolute paths to the user-named research artifacts and any directly
relevant project files, such as the paper, plan, result tables, experiment
records, and repository instructions. Pass the user's review objective, target
venue when known, and the requested output schema. Do **not** pre-digest the
files into a content briefing, extract key findings, or tell the reviewer what
conclusion to reach.

### Step 2: Initial Review (Round 1)
Send a detailed prompt with ultra reasoning:

```
spawn_agent:
  model: gpt-5.6-sol
  reasoning_effort: ultra
  message: |
    Review objective: [user's objective]
    Target venue: [venue or unknown]
    Primary artifacts (read these directly):
    - /absolute/path/to/paper-or-report
    - /absolute/path/to/results-or-plan

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

### Step 3: Focused Follow-Up (only when needed)
Use `send_input` with the returned agent id to continue the conversation:

```text
send_input:
  target: [saved reviewer id from Step 2]
  message: |
    Please continue the review using the revised materials below.

    Revised files:
    - /absolute/path/to/file1
    - /absolute/path/to/file2

    Focus on unresolved weaknesses and whether the revision actually fixed them.
```

For each round, provide revised primary artifacts or request a focused
re-check of issues raised by that reviewer. Do not inject the executor's
interpretation of the prior verdict or coach the reviewer toward acceptance.

Key follow-up patterns:
- "If we reframe X as Y, does that change your assessment?"
- "What's the minimum experiment to satisfy concern Z?"
- "Please design the minimal additional experiment package (highest acceptance lift per GPU week)"
- "Please write a mock NeurIPS/ICML review with scores"
- "Give me a results-to-claims matrix for possible experimental outcomes"

### Step 4: Convergence
Complete the review when it answers the requested questions with artifact-grounded findings, limitations and actionable next steps. Agreement or a positive score is not required. Do not keep reviewing unchanged material to obtain acceptance. Create an experiment plan, claims matrix or paper outline only when the request or findings call for one; record unresolved issues and the evidence needed to resolve them.

### Step 5: Document Everything
Save the full interaction and conclusions to a review document in the project root:
- Round-by-round summary of criticisms and responses
- Supported conclusions and unresolved disagreements on the reviewed scope
- Claims matrix when claims-to-results reasoning is part of the request
- Prioritized action list; estimate compute only when proposing experiments
- Paper outline if discussed

Update project memory/notes with key review conclusions.

If `— composed: <canonical-report-path>` is explicitly present, fold consensus,
claims matrix, TODOs, and trace links into that report instead of writing a
standalone review document. Without the directive, write the standalone review
as documented; never infer composed mode from an existing file. `— standalone`
always wins. See
[`output-composition.md`](../shared-references/output-composition.md).

### Step 6: Review Tracing

Save a trace for every `spawn_agent`, `send_input`, or `oracle-pro` review call following `../shared-references/review-tracing.md`. Record the reviewer route, saved agent id, prompt summary, raw response path, decisions, and action items. This preserves the Claude mainline Review Tracing semantics while using Codex-native reviewer calls.

## Key Rules

- Use the declared reviewer default and tier unless the user explicitly selects a supported route; apply `reviewer-routing.md` and record the actual model/effort.
- Send absolute artifact paths in Round 1 and require the reviewer to read them directly
- Be honest about weaknesses — hiding them leads to worse feedback
- Push back on criticisms you disagree with, but accept valid ones
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Document the agent id for potential future resumption
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
