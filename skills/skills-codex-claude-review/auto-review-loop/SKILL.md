---
name: "auto-review-loop"
description: "Autonomous multi-round research review loop. Repeatedly reviews using Claude Code via claude-review MCP, implements fixes, and re-reviews until positive assessment or max rounds reached. Use when user says \"auto review loop\", \"review until it passes\", or wants autonomous iterative improvement."
---

> Override for Codex users who want **Claude Code**, not a second Codex agent, to act as the reviewer. Install this package **after** `skills/skills-codex/*`.
>
> This reviewer is a different model family from the Codex executor. Only after complete artifact transport and a grounded external review response may the trace/audit record:
>
> ```yaml
> review_independence: cross-family
> acceptance_status: accepted
> ```
> A bridge or artifact-transport failure records `REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted.

# Auto Review Loop: Autonomous Research Improvement

> **Claude overlay assurance:** this route is a different model family from the Codex executor. Record `review_independence: cross-family` and `acceptance_status: accepted` only after complete artifact transport and a grounded external review response. A bridge or transport failure records `REVIEW_UNAVAILABLE` / `BLOCKED` and is never accepted.

Autonomously iterate: review → implement fixes → re-review, until the external reviewer gives a positive assessment or MAX_ROUNDS is reached.

## Prerequisites

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

## Context: $ARGUMENTS

## Constants

- MAX_ROUNDS = 4
- POSITIVE_THRESHOLD: score >= 6/10 AND verdict ∈ {"ready", "almost"} — both must hold, matching the operative STOP CONDITION below. Verdict vocabulary is {"ready", "almost", "not ready"}. (Earlier wording used "or" + a stale verdict set; the AND form is authoritative.)
- REVIEW_DOC: `review-stage/AUTO_REVIEW.md` (cumulative log) *(fall back to `./AUTO_REVIEW.md` for legacy projects)*
- **OUTPUT_DIR = `review-stage/`** — All review-stage outputs go here. Create the directory if it doesn't exist.
- **REVIEWER_MODEL = `claude-review`** — Claude reviewer invoked through the local `claude-review` MCP bridge. Set `CLAUDE_REVIEW_MODEL` if you need a specific Claude model override.
- **REVIEWER_BACKEND = `claude-review`** — reviews route through the claude-review MCP (Claude family; cross-family for a Codex executor).
- **HUMAN_CHECKPOINT = false** — When `true`, pause after each round's review (Phase B) and present the score + weaknesses to the user. Wait for user input before proceeding to Phase C. The user can: approve the suggested fixes, provide custom modification instructions, skip specific fixes, or stop the loop early. When `false` (default), the loop runs fully autonomously.
- **COMPACT = false** — When `true`, (1) read `EXPERIMENT_LOG.md` and `findings.md` instead of parsing full logs on session recovery, (2) append key findings to `findings.md` after each round.
- **REVIEWER_DIFFICULTY = medium** — Controls adversarial depth: `medium` uses a normal high-rigor Claude review through `mcp__claude-review__review_start` / `mcp__claude-review__review_reply_start`; `hard` adds Reviewer Memory and Debate Protocol; `nightmare` adds direct repository-reading adversarial verification by an independent reviewer.
- **RENDER_HTML = true** — When `true` (default), auto-render `review-stage/AUTO_REVIEW.md` to HTML on loop termination via `/render-html`. Uses `--no-review` because the loop already performed a traced cross-family accepted Claude review. Set `false` to skip.

> 💡 Override: `/auto-review-loop "topic" — compact: true, human checkpoint: true, difficulty: hard`

## Claude-Aligned Reviewer Memory and Debate

For `difficulty: hard` and `difficulty: nightmare`, maintain `review-stage/REVIEWER_MEMORY.md`.

- Before each reviewer call, prepend the full `REVIEWER_MEMORY.md` contents under `## Your Reviewer Memory (persistent across rounds)`.
- Tell the reviewer to check whether prior suspicions were genuinely addressed or merely sidestepped.
- Require a `Memory update` section in the reviewer response.
- After Phase B, copy the `Memory update` into `REVIEWER_MEMORY.md` before writing `REVIEW_STATE.json`.
- In `nightmare`, launch an additional fresh adversarial reviewer with an independently assembled, content-faithful artifact bundle. Include the complete claims, code, logs, result files, and paper drafts with source hashes; never substitute executor summaries or bare repository paths.

## Instructions

In hard and nightmare modes, the reviewer must actively look for omissions, unsupported claims, cherry-picked evidence, metric mistakes, and weaknesses the executor may have downplayed.

For `difficulty: hard` and `nightmare`, use the **Debate Protocol** after a critical review:

1. Codex writes a concise rebuttal with evidence, not spin.
2. Send the rebuttal to the same reviewer via `mcp__claude-review__review_reply_start`.
3. The reviewer rules which objections are resolved, unresolved, or newly discovered.
4. Only mark a concern resolved when the reviewer accepts the rebuttal.

## State Persistence (Compact Recovery)

Long-running loops may hit the context window limit, triggering automatic compaction. To survive this, persist state to `review-stage/REVIEW_STATE.json` after each round:

```json
{
  "round": 2,
  "threadId": "019cd392-...",
  "status": "in_progress",
  "last_score": 5.0,
  "last_verdict": "not ready",
  "pending_experiments": ["screen_name_1"],
  "timestamp": "2026-03-13T21:00:00"
}
```

**Write this file at the end of every Phase E** (after documenting the round). Overwrite each time — only the latest state matters.

**On completion** (positive assessment or max rounds), set `"status": "completed"` so future invocations don't accidentally resume a finished loop.

## Workflow

### Initialization

1. **Check for `review-stage/REVIEW_STATE.json`** *(fall back to `./REVIEW_STATE.json` if not found — legacy path)*:
   - If neither path exists: **fresh start** (normal case, identical to behavior before this feature existed)
   - If it exists AND `status` is `"completed"`: **fresh start** (previous loop finished normally)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is older than 24 hours: **fresh start** (stale state from a killed/abandoned run — delete the file and start over)
   - If it exists AND `status` is `"in_progress"` AND `timestamp` is within 24 hours: **resume**
     - Read the state file to recover `round`, `threadId`, `last_score`, `pending_experiments`
     - Read `review-stage/AUTO_REVIEW.md` to restore full context of prior rounds *(fall back to `./AUTO_REVIEW.md`)*
     - If `pending_experiments` is non-empty, check if they have completed (e.g., check screen sessions)
     - Resume from the next round (round = saved round + 1)
     - Log: "Recovered from context compaction. Resuming at Round N."
2. Read project narrative documents, memory files, and any prior review documents. When `COMPACT = true` and compact files exist, prefer `findings.md` + `EXPERIMENT_LOG.md` over full raw logs.
3. Read recent experiment results (check output directories, logs)
4. Identify current weaknesses and open TODOs from prior reviews
5. Initialize round counter = 1 (unless recovered from state file)
6. Create/update `review-stage/AUTO_REVIEW.md` with header and timestamp

### Loop (repeat up to MAX_ROUNDS)

#### Phase A: Review

**Route by REVIEWER_DIFFICULTY:**

##### Medium (default) — Claude Review

Send comprehensive context to the external reviewer:

```
mcp__claude-review__review_start:
  prompt: |
    [Round N/MAX_ROUNDS of autonomous review loop]

    Review the complete transmitted artifact bundle below. Executor notes
    and bare paths are not evidence; each item must contain its source hash
    and complete content:
    --- BEGIN ARTIFACT role=claims path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete paper draft or claims content]
    --- END ARTIFACT role=claims ---
    --- BEGIN ARTIFACT role=methods path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete methods or code content]
    --- END ARTIFACT role=methods ---
    --- BEGIN ARTIFACT role=results path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete raw result content]
    --- END ARTIFACT role=results ---
    --- BEGIN ARTIFACT role=changes path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete raw diff content]
    --- END ARTIFACT role=changes ---

    Please act as a senior ML reviewer (NeurIPS/ICML level). Start from the
    assumption that the work is broken somewhere — your job is to find where.
    Be adversarial. Trust nothing the author tells you — verify everything
    yourself.

    1. Score this work 1-10 for a top venue
    2. List remaining critical weaknesses (ranked by severity)
    3. For each weakness, specify the MINIMUM fix (experiment, analysis, or reframing)
    4. State clearly: is this READY for submission? Yes/No/Almost

    Be brutally honest. If, after genuinely trying to break it, the work holds
    up and is ready, say so clearly.
```

After this review call, immediately save the returned `jobId` and poll `mcp__claude-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

If this is round 2+, use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` until `done=true` to maintain continuity.

##### Hard — Claude Review + Reviewer Memory

Use the same `mcp__claude-review__review_start` / `mcp__claude-review__review_reply_start` route as medium, but prepend the full `review-stage/REVIEWER_MEMORY.md` contents under `## Your Reviewer Memory (persistent across rounds)` and require a `Memory update` section in the reviewer response.

##### Nightmare — Independent Repository Review

Use everything in hard mode, then give an additional fresh adversarial reviewer an independently assembled, complete content-faithful bundle of the claims, code, logs, result files, and paper drafts. Preserve the fresh review as a separate raw response and trace.

#### Phase B: Parse Assessment

**CRITICAL: Save the FULL raw response** from the external reviewer verbatim (store in a variable for Phase E). Do NOT discard or summarize — the raw text is the primary record.

Then extract structured fields:
- **Score** (numeric 1-10)
- **Verdict** ("ready" / "almost" / "not ready")
- **Action items** (ranked list of fixes)

**STOP CONDITION**: If score >= 6 AND verdict ∈ {"ready", "almost"} (exact match — "not ready" does NOT qualify) → stop loop, document final state.

#### Phase B.5: Reviewer Memory Update (hard + nightmare only)

Skip entirely if `REVIEWER_DIFFICULTY = medium`.

After parsing the assessment, update `review-stage/REVIEWER_MEMORY.md`:

## Your Reviewer Memory (persistent across rounds)

Pass this file back to the reviewer in the next round so it can track its own suspicions.

```markdown
# Reviewer Memory

## Round 1 — Score: X/10
- **Suspicion**: [what the reviewer flagged]
- **Unresolved**: [concerns not yet addressed]
- **Patterns**: [recurring issues the reviewer noticed]

## Round 2 — Score: X/10
- **Previous suspicions addressed?**: [yes/no for each, with reviewer judgment]
- **New suspicions**: [...]
- **Unresolved**: [carried forward + new]
```

Rules:
- Append each round; never delete prior rounds.
- If the reviewer response includes a `Memory update` section, copy it verbatim.
- If the score REGRESSES round-to-round, don't just write a new memory line:
  diff the two rounds' raw `.response.md` files in `.aris/traces/` first and
  find the exact criterion that flipped (see `shared-references/review-tracing.md`
  § *Debugging With Traces*). The memory file is a summary; the trace is evidence.
- This file is passed back to the reviewer in the next round's Phase A.

#### Phase B.6: Debate Protocol (hard + nightmare only)

Skip entirely if `REVIEWER_DIFFICULTY = medium`.

After parsing the review, Codex writes a structured rebuttal for up to three high-impact weaknesses:

```markdown
### Rebuttal to Weakness #1: [title]
- **Accept / Partially Accept / Reject**
- **Argument**: [why this criticism is valid, invalid, already addressed, or out of scope]
- **Evidence**: [specific code, result file, log, prior-round fix, or paper section]
```

Send the rebuttal to the same reviewer via `mcp__claude-review__review_reply_start`:

```
mcp__claude-review__review_reply_start:
  threadId: [saved reviewer id]
  prompt: |
    Please rule on the author's rebuttal below.
    For each contested weakness, decide: accepted / partially accepted / rejected.
    If rejected, state the minimum evidence or change required.

    [paste rebuttal + evidence]
```

After this review call, immediately save the returned `jobId` and poll `mcp__claude-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

Record a `### Debate Transcript (hard + nightmare only)` section in `review-stage/AUTO_REVIEW.md`. Only mark a weakness resolved if the reviewer accepts the rebuttal.

### Debate Transcript (hard + nightmare only)

In the round log, preserve the rebuttal, reviewer ruling, accepted objections, rejected objections, and any required follow-up evidence.

#### Human Checkpoint (if enabled)

**Skip this step entirely if `HUMAN_CHECKPOINT = false`.**

When `HUMAN_CHECKPOINT = true`, present the review results and wait for user input:

```
📋 Round N/MAX_ROUNDS review complete.

Score: X/10 — [verdict]
Top weaknesses:
1. [weakness 1]
2. [weakness 2]
3. [weakness 3]

Suggested fixes:
1. [fix 1]
2. [fix 2]
3. [fix 3]

Options:
- Reply "go" or "continue" → implement all suggested fixes
- Reply with custom instructions → implement your modifications instead
- Reply "skip 2" → skip fix #2, implement the rest
- Reply "stop" → end the loop, document current state
```

Wait for the user's response. Parse their input:
- **Approval** ("go", "continue", "ok", "proceed"): proceed to Phase C with all suggested fixes
- **Custom instructions** (any other text): treat as additional/replacement guidance for Phase C. Merge with reviewer suggestions where appropriate
- **Skip specific fixes** ("skip 1,3"): remove those fixes from the action list
- **Stop** ("stop", "enough", "done"): terminate the loop, jump to Termination

#### Feishu Notification (if configured)

After parsing the score, check if `~/.codex/feishu.json` exists and mode is not `"off"`:
- Send a `review_scored` notification: "Round N: X/10 — [verdict]" with top 3 weaknesses
- If **interactive** mode and verdict is "almost": send as checkpoint, wait for user reply on whether to continue or stop
- If config absent or mode off: skip entirely (no-op)

#### Phase C: Implement Fixes (if not stopping)

For each action item (highest priority first):

1. **Code changes**: Write/modify experiment scripts, model code, analysis scripts
2. **Run experiments**: Deploy to GPU server via SSH + screen/tmux
3. **Analysis**: Run evaluation, collect results, update figures/tables
4. **Documentation**: Update project notes and review document

Prioritization rules:
- Skip fixes requiring excessive compute (flag for manual follow-up)
- Skip fixes requiring external data/models not available
- Prefer reframing/analysis over new experiments when both address the concern
- Always implement metric additions (cheap, high impact)

#### Phase D: Wait for Results

If experiments were launched:
- Monitor remote sessions for completion
- Collect results from output files and logs
- **Training quality check** — if W&B is configured, invoke `/training-check` to verify training was healthy (no NaN, no divergence, no plateau). If W&B is not available, skip silently.

#### Phase E: Document Round

Append to `review-stage/AUTO_REVIEW.md`:

```markdown
## Round N (timestamp)

### Assessment (Summary)
- Score: X/10
- Verdict: [ready/almost/not ready]
- Key criticisms: [bullet list]

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

[Paste the COMPLETE raw response from the external reviewer here — verbatim, unedited.
This is the authoritative record. Do NOT truncate or paraphrase.]

</details>

### Actions Taken
- [what was implemented/changed]

### Results
- [experiment outcomes, if any]

### Status
- [continuing to round N+1 / stopping]
```

**Write `review-stage/REVIEW_STATE.json`** with current round, completed threadId, score, verdict, and any pending experiments.

**Append to `findings.md`** (when `COMPACT = true`): one-line entry per key finding this round.

```markdown
- [Round N] [positive/negative/unexpected]: [one-sentence finding] (metric: X.XX → Y.YY)
```

Increment round counter → back to Phase A.

#### Review Tracing

## Review Tracing

After every `mcp__claude-review__review_start`, `mcp__claude-review__review_reply_start`, `oracle-pro`, or nightmare adversarial verification call, save a trace following `../shared-references/review-tracing.md`. Include prompt summary, reviewer route, saved threadId, raw response path, score/verdict, accepted fixes, rejected rebuttals, and the `Reviewer Memory` update if present.

### Termination

When loop ends (positive assessment or max rounds):

1. Update `review-stage/REVIEW_STATE.json` with `"status": "completed"`
2. Write final summary to `review-stage/AUTO_REVIEW.md`
3. Update project notes with conclusions
4. **Write method/pipeline description** to `review-stage/AUTO_REVIEW.md` under a `## Method Description` section — a concise 1-2 paragraph summary of the final method, architecture, and data flow. This serves as direct input for `/paper-illustration`.
5. **Generate claims from results** — invoke `/result-to-claim` to convert experiment results from `review-stage/AUTO_REVIEW.md` into structured paper claims. Output: `CLAIMS_FROM_RESULTS.md`. If `/result-to-claim` is not installed, skip this step (no `CLAIMS_FROM_RESULTS.md` is produced; `/paper-plan` extracts claims from the narrative as before) — but NEVER fabricate the file or its verdict. If it ran but its output starts with `verdict: REVIEW_UNAVAILABLE`, keep that file AS-IS (do not overwrite or paraphrase it) and record in `AUTO_REVIEW.md` that claims are UNADJUDICATED — downstream paper stages must not treat them as validated.
6. If stopped at max rounds without positive assessment:
   - List remaining blockers
   - Estimate effort needed for each
   - Suggest whether to continue manually or pivot
7. **Feishu notification** (if configured): Send `pipeline_done` with final score progression table
8. **Render HTML view** (if `RENDER_HTML = true`, default): invoke `/render-html` on the cumulative review log:
   ```
   /render-html "review-stage/AUTO_REVIEW.md" --no-review --state review-stage/REVIEW_STATE.json
   ```
   Pass `--state` explicitly when `REVIEW_STATE.json` exists (the helper does not auto-discover the sidecar). HTML lands at `review-stage/AUTO_REVIEW.html` with embedded source SHA256. **Non-blocking**: if `/render-html` fails, log the error and continue — the HTML is a convenience, not a termination prerequisite.

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../../shared-references/output-manifest.md)** — maintain MANIFEST.md only when a run exceeds the protocol's >15-artifact threshold
> - **[Output Language Protocol](../../shared-references/output-language.md)** — respect the project's language setting

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- Always ask the Claude reviewer for strict, high-rigor feedback.
- Save the completed `threadId` from the first `mcp__claude-review__review_status` result, then use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for subsequent rounds
- Be honest — include negative results and failed experiments
- Do NOT hide weaknesses to game a positive score
- Implement fixes BEFORE re-reviewing (don't just promise to fix)
- If an experiment takes > 30 minutes, launch it and continue with other fixes while waiting
- Document EVERYTHING — the review log should be self-contained
- Update project notes after each round, not just at the end

## Prompt Template for Round 2+

```
mcp__claude-review__review_reply_start:
  threadId: [saved from round 1]
  # inherits the agent's model/effort — do not re-send
  prompt: |
    [Round N update]

    Review this complete revised-artifact bundle; do not rely on my
    description of what changed or whether it worked:
    --- BEGIN ARTIFACT role=revised-files path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete revised file content]
    --- END ARTIFACT role=revised-files ---
    --- BEGIN ARTIFACT role=raw-diff path=<absolute-path-or-range> sha256=<hex> extraction=<method+version> ---
    [complete raw diff]
    --- END ARTIFACT role=raw-diff ---
    --- BEGIN ARTIFACT role=updated-results path=<absolute-path> sha256=<hex> extraction=<method+version> ---
    [complete updated raw result content]
    --- END ARTIFACT role=updated-results ---

    Please re-score and re-assess. Are the remaining concerns addressed?
    Same format: Score, Verdict, Remaining Weaknesses, Minimum Fixes.
```

After this review call, immediately save the returned `jobId` and poll `mcp__claude-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.
