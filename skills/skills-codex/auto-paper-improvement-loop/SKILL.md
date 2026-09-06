---
name: auto-paper-improvement-loop
description: "Iteratively improve a compiled research paper through independent review, scoped fixes and recompilation. Use for a requested paper improvement loop or 论文润色循环. A single paragraph rewrite, citation fix or layout adjustment uses the relevant paper-write, citation or paper-compile workflow."
argument-hint: "[paper-directory] [— edit-whitelist <path>]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Auto Paper Improvement Loop: Review → Fix → Recompile

Autonomously improve the paper at: **$ARGUMENTS**

## Context

This skill is designed to run **after** Workflow 3 (`/paper-plan` → `/paper-figure` → `/paper-write` → `/paper-compile`). It takes a compiled paper and iteratively improves it through external LLM review.

Unlike `/auto-review-loop` (which iterates on **research** — running experiments, collecting data, rewriting narrative), this skill iterates on **paper writing quality** — fixing theoretical inconsistencies, softening overclaims, adding missing content, and improving presentation.

## Constants

- **MAX_ROUNDS = 2** — Default cap on review→fix→recompile cycles, not a minimum. Use the completion criteria below; do not run a second round solely to fill the quota or improve a score.
- **REVIEWER_MODEL = `gpt-5.6-sol`** — Model used via Codex MCP for paper review.
- **REVIEWER_BIAS_GUARD = true** — When `true`, every review round uses a fresh `spawn_agent` reviewer with no prior review context. Do not use stale self-reported context for review rounds. Set to `false` only for deliberate debugging of the legacy behavior. **Empirical evidence:** running the same paper with continuation replies plus "since last round we did X" prompts inflated scores from real 3/10 → fake 8/10 across multiple rounds; switching to fresh threads recovered the true 3/10 assessment.
- **REVIEW_LOG = `PAPER_IMPROVEMENT_LOG.md`** — Cumulative log of all rounds, stored in paper directory.
- **HUMAN_CHECKPOINT = false** — When `true`, pause after each round's review and present score + weaknesses to the user. The user can approve fixes, provide custom modification instructions, skip specific fixes, or stop early. When `false` (default), runs fully autonomously.
- **EDIT_WHITELIST = `null`** — Optional path to a YAML/JSON whitelist file constraining which paths and operations the fix-implementation step may touch. When `null` (default), edits remain constrained by the user's request, evidence and applicable project instructions. When set via `— edit-whitelist <path>` (also accepts `— edit_whitelist <path>`), the loop loads the file at startup and consults it before each edit; rejected edits are logged to `PAPER_IMPROVEMENT_LOG.md` rather than silently dropped. See "Optional: Edit Whitelist" below.

> 💡 Override: `/auto-paper-improvement-loop "paper/" — human checkpoint: true`

## Optional: Edit Whitelist (`— edit-whitelist <path>`, opt-in)

Lets the caller hard-constrain which files and operations the **fix-implementation** step (Step 3 / Step 6) is allowed to touch. **Default OFF — without an explicit whitelist, the user's requested scope and evidence boundaries still apply. Reviewer suggestions do not authorize new experiments, unsupported claims or unrelated changes.**

This is the parameter that upstream pipelines (e.g. `/resubmit-pipeline` Phase 2) use to enforce text-only resubmit microedits: no `.bib` mutations, no `.sty` / `.bst` mutations, no edits to prior-submission directories, no new `\cite{...}`, no new theorem environments, no new numerical claims.

### Schema

The whitelist file is YAML or JSON. All four sections are optional:

```yaml
allowed_paths:
  - sec/*.tex
  - main.tex
  - figures/*.tex
forbidden_paths:
  - "**/*.bib"
  - "**/*.sty"
  - "**/*.bst"
  - "../OldSubmission/**"
forbidden_operations:
  - new_cite              # blocks \cite{...}, \citep{...}, \citet{...}, \citeauthor{...} additions
  - new_bibitem           # blocks \bibitem{...} additions
  - new_theorem_env       # blocks \begin{theorem|lemma|proposition|corollary} additions
  - numerical_claim       # blocks adding new numbers / percentages / metrics
forbidden_deletions:      # operations that block REMOVALS, not additions
  - delete_existing_cite  # blocks removal of \cite{...} from the body (use citation-audit --soft-only instead)
  - delete_theorem_env    # blocks removal of an existing \begin{theorem|...} block
requires_user_approval_for:  # operations that don't auto-reject but pause for explicit user OK
  - rewrite_abstract
  - rewrite_intro_first_para
  - delete_section
max_edits_per_round: 30   # hard cap on accepted edits per round (rejections not counted)
rationale: "Resubmit mode: text-only microedits, paper structure frozen by user constraint."
```

### Resolution rules

- **`allowed_paths` empty AND `forbidden_paths` empty** → whitelist is a no-op (advisory: the file is loaded and `rationale` echoed to the log, but no path filtering is applied).
- **`allowed_paths` empty, `forbidden_paths` non-empty** → all paths NOT matched by `forbidden_paths` are mutable.
- **`allowed_paths` non-empty, `forbidden_paths` empty** → only paths matching `allowed_paths` are mutable.
- **Both non-empty** → an edit is allowed iff the target matches `allowed_paths` AND does NOT match `forbidden_paths`. `forbidden_paths` always wins on overlap.
- **`forbidden_operations` missing or empty** → no operation-level guard; only path-level filtering applies.

### Glob semantics

Use bash `extglob` / Python `fnmatch.fnmatch` semantics. `**` matches any depth (zero or more directory segments). Patterns are matched against the path **relative to the paper directory** (e.g. `paper/sec/intro.tex` matches `sec/*.tex` when paper-directory is `paper/`).

### Forbidden-operation detectors

For each candidate edit's diff (the new lines being added — deletions are exempt), the loop runs these regex checks and rejects if any forbidden operation matches:

| Operation | Detector (added lines only) |
|-----------|------------------------------|
| `new_cite` | `\\cite[a-zA-Z]*\{[^}]+\}` (catches `\cite`, `\citep`, `\citet`, `\citeauthor`, `\citeyear`, `\citealp`, etc.) |
| `new_bibitem` | `\\bibitem\{[^}]+\}` |
| `new_theorem_env` | `\\begin\{(theorem|lemma|proposition|corollary)\*?\}` |
| `numerical_claim` | New token matching `\b\d+(\.\d+)?%?\b` that did NOT appear in the deleted/replaced lines (i.e. genuinely new numbers, not edits to existing ones) |

### Behavior at loop start (before Round 1 fix-implementation)

1. If `— edit-whitelist <path>` is present in `$ARGUMENTS`, set `EDIT_WHITELIST = <path>`.
2. Load the file (`yaml.safe_load`; if it fails, fall back to `json.loads`). On load failure, abort the loop with a clear error — do NOT silently proceed unconstrained.
3. Echo `rationale` (if present) into `PAPER_IMPROVEMENT_LOG.md` under a new "Edit Whitelist" preamble section so the audit trail records why edits were constrained.

### Behavior during fix-implementation (Steps 3 and 6)

Before applying each proposed edit:

1. Resolve target file path relative to the paper directory.
2. Path check: if `allowed_paths` is non-empty, target must match at least one pattern. Then if `forbidden_paths` is non-empty, target must NOT match any pattern. If either fails → reject as `path` violation.
3. Operation check: build the unified diff (or just the set of newly-added lines) for the proposed edit. For each entry in `forbidden_operations`, run its detector on the added lines. If any detector matches → reject as `operation` violation.
4. If all checks pass, apply the edit normally.
5. If rejected, append an entry to `PAPER_IMPROVEMENT_LOG.md` under a `## Rejected by edit_whitelist (Round N)` heading with this schema:
   ```
   - file: <relative path>
     reason: path | operation
     pattern: <the offending forbidden_path glob, OR the offending forbidden_operation name + the matched substring>
     reviewer_concern: <the original Round-N weakness that motivated this edit>
   ```
6. Continue with the remaining edits in the round. Do NOT abort the whole round on a single rejection.

### End-of-round surfacing

At the end of each round (after the recompile, before moving to the next round), if any edits were rejected during that round's fix step:

- Print a one-line summary to the round's checkpoint output: `Edit whitelist rejected N edits this round (M path, K operation). See PAPER_IMPROVEMENT_LOG.md "Rejected by edit_whitelist (Round N)".`
- If `HUMAN_CHECKPOINT = true`, include the rejection list in the checkpoint shown to the user before they approve next-round fixes.

### Example invocations

```bash
# Resubmit-pipeline Phase 2 caller (text-only mode):
/auto-paper-improvement-loop "paper/" — edit-whitelist .resubmit/edit_whitelist.yaml

# Aliased form is accepted:
/auto-paper-improvement-loop "paper/" — edit_whitelist .resubmit/edit_whitelist.yaml

# Combined with other flags:
/auto-paper-improvement-loop "paper/" — human checkpoint: true — edit-whitelist constraints.yaml
```

### Rationale

Reviewer suggestions to add citations, theorem environments or numerical claims still require evidence and task authorization. A whitelist additionally makes frozen resubmit, camera-ready or rebuttal boundaries mechanically checkable and auditable through `PAPER_IMPROVEMENT_LOG.md`. Without a whitelist, the same user and project constraints still apply.

## Inputs

1. **Compiled paper** — `paper/main.pdf` + LaTeX source files
2. **Paper source entrypoint and included `.tex` files** — resolved in source order and passed as paths for direct review

## State Persistence (Compact Recovery)

If the context window is compacted mid-loop, recover from `PAPER_IMPROVEMENT_STATE.json`, which this skill writes after each round:

```json
{
  "current_round": 1,
  "agent_id": "019ce736-...",
  "last_score": 6,
  "status": "in_progress",
  "timestamp": "2026-03-13T21:00:00"
}
```

**On startup**: if `PAPER_IMPROVEMENT_STATE.json` exists with `"status": "in_progress"` AND `timestamp` is within 24 hours, read it + `PAPER_IMPROVEMENT_LOG.md` to recover context, then resume from the next round. Otherwise (file absent, `"status": "completed"`, or older than 24 hours), start fresh.

**After each round**: overwrite the state file. **On completion**: set `"status": "completed"`.

## Reviewer Independence Protocol

The reviewer must be context-naive on every round. Prior-round summaries, fix lists, and executor explanations are not evidence; they are a source of confirmation bias. If the reviewer is told what changed, scores tend to drift upward even when the manuscript itself has not materially improved.

Rules:
- Every round starts with a fresh `spawn_agent` reviewer call, not a stale continuation prompt.
- Never pass a prior agent_id into the next review prompt.
- Never include "since last round", "we fixed", "after applying", or any fix summary in the reviewer prompt.
- The only acceptable evidence of improvement is the current `.tex` source and compiled PDF.
- If a fix cannot be observed in the files, the reviewer should not be told it happened.
- If recovery metadata is needed, store the returned agent_id for crash recovery only; do not use it to preserve review context.

Set `REVIEWER_BIAS_GUARD = false` only if you explicitly want the legacy, context-carrying behavior for debugging.

## Workflow

### Step 0: Preserve Original

```bash
cp paper/main.pdf paper/main_round0_original.pdf
```

### Step 1: Resolve Paper Artifacts

Resolve the source entrypoint, included sections, compiled PDF and relevant figure paths. Pass primary paths to a fresh reviewer that can read them directly. Do not concatenate the whole paper into the prompt as a second copy. If a reviewer backend cannot read files, provide the required raw source content without executor summaries and state any omitted material.

### Step 2: Round 1 Review

Send the resolved source and compiled PDF paths to GPT-5.6-Sol xhigh using the current tool schema and `fork_turns: "none"`:

```text
spawn_agent:
  model: gpt-5.6-sol
  reasoning_effort: xhigh
  message: |
    You are reviewing a [VENUE] paper. Please provide a detailed, structured review.

    ## Paper Files:
    - LaTeX source: [list all section .tex files]
    - Compiled PDF: paper/main.pdf
    - Figures: [list figure files]

    Read BOTH the LaTeX source (for content/logic) AND the compiled PDF (for visual presentation).

    ## Review Instructions
    Please act as a senior ML reviewer ([VENUE] level). Provide:
    1. **Overall Score** (1-10, where 6 = weak accept, 7 = accept)
    2. **Summary** (2-3 sentences)
    3. **Strengths** (bullet list, ranked)
    4. **Weaknesses** (bullet list, ranked: CRITICAL > MAJOR > MINOR)
    5. **For each CRITICAL/MAJOR weakness**: A specific, actionable fix
    6. **Missing References** (if any)
    7. **Visual Review** (from the PDF):
       - Figure quality: readable? labels legible? colors distinguishable in grayscale?
       - Figure-caption alignment: does each caption match its figure?
       - Layout: orphaned headers, awkward page breaks, figures far from references?
       - Table formatting: aligned columns, consistent decimals, bold for best results?
       - Visual consistency: same color scheme across all figures?
    8. **Verdict**: Ready for submission? Yes / Almost / No

    Focus on: theoretical rigor, claims vs evidence alignment, writing clarity,
    self-containedness, notation consistency, AND visual presentation quality.
```

Save the agent_id for traceability and recovery; the next verdict-bearing round uses a fresh reviewer.

### Step 2b: Human Checkpoint (if enabled)

**Skip if `HUMAN_CHECKPOINT = false`.**

Present the review results and wait for user input:

```
📋 Round 1 review complete.

Score: X/10 — [verdict]
Key weaknesses (by severity):
1. [CRITICAL] ...
2. [MAJOR] ...
3. [MINOR] ...

Reply "go" to implement all fixes, give custom instructions, "skip 2" to skip specific fixes, or "stop" to end.
```

Parse user response same as `/auto-review-loop`: approve / custom instructions / skip / stop.

### Step 3: Implement Round 1 Fixes

Parse the review and implement fixes by severity:

**Priority order:**
1. CRITICAL fixes (assumption mismatches, internal contradictions)
2. MAJOR fixes (overclaims, missing content, notation issues)
3. MINOR fixes (if time permits)

**Edit-whitelist gate (if set):** If `EDIT_WHITELIST` is set, before applying each proposed edit, check the target path against `allowed_paths` / `forbidden_paths` and the new-lines diff against `forbidden_operations` per the "Optional: Edit Whitelist" section. Rejections are logged to `PAPER_IMPROVEMENT_LOG.md` under `## Rejected by edit_whitelist (Round 1)` with file, reason (`path` or `operation`), the offending pattern, and the original reviewer concern. The loop continues with remaining edits — a rejection never aborts the round. Surface a rejection summary at the end of the round.

**Common fix patterns:**

| Issue | Fix Pattern |
|-------|-------------|
| Assumption-model mismatch | Rewrite assumption to match the model, add formal proposition bridging the gap |
| Overclaims | Soften language: "validate" → "demonstrate practical relevance", "comparable" → "qualitatively competitive" |
| Missing metrics | Add quantitative table with honest parameter counts and caveats |
| Theorem not self-contained | Add "Interpretation" paragraph listing all dependencies |
| Notation confusion | Rename conflicting symbols globally, add Notation paragraph |
| Missing references | Add to `references.bib`, cite in appropriate locations |
| Theory-practice gap | Explicitly frame theory as idealized; add synthetic validation subsection |
| Proof gap (theory papers) | Run `/proof-checker` if PROOF_AUDIT.md doesn't exist yet; fix FATAL/CRITICAL issues |
| Writing clutter / passive voice | Apply sciwrite 5-pass audit: clutter extraction → active voice → sentence architecture → keyword consistency → numerical integrity. See `paper-write` Step 5 |
| Number mismatch (paper vs results) | Run `/paper-claim-audit` if PAPER_CLAIM_AUDIT.md doesn't exist; fix any `number_mismatch` or `aggregation_mismatch` claims |
| Keyword inconsistency | The "Banana Rule": if Methods says "obese group", Results must not say "heavier group". Extract key terms, verify consistency across all sections |

### Step 4: Recompile Round 1

```bash
cd paper && latexmk -C && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf main_round1.pdf
```

Verify: 0 undefined references, 0 undefined citations.

### Step 4.5: Restatement Regression Test

When the paper contains restated theorems/lemmas/propositions/corollaries, check main-body and appendix statement consistency. Reuse a recorded check only when all its statement and notation inputs are unchanged; rerun after edits that could affect them. Absence of restatements makes this check not applicable.

**Scope**
- Compare only theorem/lemma/proposition/corollary statements, not proof bodies.
- Classify files by `main.tex` input order: files before `\appendix` are main body; files after `\appendix` are appendix.

**Normalized comparison logic**
- Strip comments, `\label{...}`, `\ref{...}`, `\eqref{...}`, `\cite...{...}`, and whitespace-only differences.
- Collapse formatting-only macros such as `\emph{}`, `\textbf{}`, `\textit{}`, `\mathrm{}`, `\mathbf{}`, `\mathcal{}`, and `\operatorname{}` to their contents.
- Preserve quantifiers, case splits, assumptions, and the literal names of defined objects.
- Compare by theorem label when available; otherwise compare by theorem type and order.
- Flag any change in hypotheses, case splits, quantifier order, or terminology (`stationary` vs `terminal`) as regression drift.

The snippet below illustrates normalization only: it does not extract or compare theorem pairs, and a zero exit code is not a completed consistency check. Compare the actual statements and record discrepancies or use a complete project verifier.

```bash
python3 - <<'PY'
import re
def normalize(s):
    s = re.sub(r'%.*', '', s)
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    s = re.sub(r'\\(?:ref|eqref|cref|Cref|cite[a-zA-Z]*)\{[^}]*\}', '', s)
    s = re.sub(r'\\(?:emph|textbf|textit|mathrm|mathbf|mathsf|mathcal|operatorname)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\begin\{[^}]+\}|\\end\{[^}]+\}', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()
# Compare normalized theorem blocks from the current main-body files
# against their appendix restatements. Any mismatch blocks completion.
PY
```

**Empirical motivation:** in a real submission run, a key theorem had a multi-case split in the main text but a single-case statement in the appendix; a key variable was named one way in main and another in appendix. These drifted multiple times across fix rounds because no automated check caught regression.

### Step 5: Additional Review (only when needed)

Start an additional full review only when material revisions or unresolved review questions warrant it and the round cap allows it. If the requested scope and required checks are satisfied, skip to the final checks/report. Targeted verification of the last fixes is still required even when the full-review cap is reached.

If `REVIEWER_BIAS_GUARD = true` (default), use a **fresh** `spawn_agent` reviewer for Round 2. Do not ask the reviewer to reward the Round 1 fix summary for prompting. Save the returned agent_id only for recovery bookkeeping.

```text
spawn_agent:
  model: gpt-5.6-sol
  reasoning_effort: xhigh
  message: |
    You are reviewing a [VENUE] paper. This is a fresh, zero-context review.
    Ignore any prior review rounds, prior fix lists, or executor explanations.
    Judge the paper only from the current LaTeX source and compiled PDF.

    ## Paper Files:
    - LaTeX source: [list all section .tex files]
    - Compiled PDF: paper/main.pdf
    - Figures: [list figure files]

    Read BOTH the LaTeX source (for content/logic) AND the compiled PDF (for visual presentation).

    ## Review Instructions
    Please act as a senior ML reviewer ([VENUE] level). Provide:
    1. **Overall Score** (1-10, where 6 = weak accept, 7 = accept)
    2. **Summary** (2-3 sentences)
    3. **Strengths** (bullet list, ranked)
    4. **Weaknesses** (bullet list, ranked: CRITICAL > MAJOR > MINOR)
    5. **For each CRITICAL/MAJOR weakness**: A specific, actionable fix
    6. **Missing References** (if any)
    7. **Visual Review** (from the PDF):
       - Figure quality: readable? labels legible? colors distinguishable in grayscale?
       - Figure-caption alignment: does each caption match its figure?
       - Layout: orphaned headers, awkward page breaks, figures far from references?
       - Table formatting: aligned columns, consistent decimals, bold for best results?
       - Visual consistency: same color scheme across all figures?
    8. **Verdict**: Ready for submission? Yes / Almost / No

    Focus on: theoretical rigor, claims vs evidence alignment, writing clarity,
    self-containedness, notation consistency, and visual presentation quality.
```

If `REVIEWER_BIAS_GUARD = false` (legacy debugging only), use `send_input` with the saved reviewer id; this is **not** the recommended path.

### Step 5.5: Kill Argument Exercise (theory / scope-heavy papers only)

Run this only if the paper is theory-heavy (≥5 `\begin{theorem}|\begin{lemma}|\begin{proposition}|\begin{corollary}` environments in the source) or has explicit scope/generality claims in title/abstract, and only at finalization after the last actual revision round. Reuse a valid existing attack/adjudication only if its audited inputs are unchanged.

**Delegate to the `kill-argument` skill** (extracted in May 2026 as a standalone primitive). This step does NOT re-implement the Attack-and-Adjudication prompt template; instead, invoke the skill and read its output. The Codex-CLI form is to call the installed skill the same way you would call any other ARIS skill from the agent's tool list, then parse `KILL_ARGUMENT.json` from the paper directory.

**Merge rule** (auto-loop's responsibility — `kill-argument` itself is detect-only):

- Read `details.decomposed_points` from `KILL_ARGUMENT.json`.
- For each point with `verdict == "still_unresolved"` or `verdict == "partially_answered"` at `severity_if_unresolved == "critical"`:
  - Dedupe against the Round 2 weakness list by semantic overlap (~85% similarity threshold).
  - If novel, append it to the Step 6 fix list with the recommended_fix as the action description.
- If the adjudication shows the issue is `answered_by_current_text`, only downgrade an existing weakness item after verifying the cited file:line evidence yourself.
- Record both `KILL_ARGUMENT.md` and the merge decision in `PAPER_IMPROVEMENT_LOG.md`.
- If `HUMAN_CHECKPOINT = true`, include the merged findings in the checkpoint summary before asking the user to proceed.

This phase feeds directly into Step 6. The merged findings must land before the final recompile.

If kill-argument returns `verdict: NOT_APPLICABLE`, skip Step 5.5 entirely and proceed to Step 6. If it returns `BLOCKED` or `ERROR`, log the reason in `PAPER_IMPROVEMENT_LOG.md` and proceed without merging — the loop should not stall on an adversarial check that cannot run.

**Empirical motivation:** in a real submission run, after several rounds of standard improvement (score 7-8/10), the kill-argument exercise surfaced framing weaknesses that no prior review caught (e.g., a setting being mostly conditional rather than truly general, or a baseline being irrelevant to real systems). Author rebuttal forced explicit scope qualifications in abstract and discussion.

### Step 5b: Human Checkpoint (if enabled)

**Skip if `HUMAN_CHECKPOINT = false`.** Same as Step 2b — present Round 2 review, wait for user input.

### Step 6: Implement Round 2 Fixes

Same process as Step 3. Typical Round 2 fixes:
- Add controlled synthetic experiments validating theory
- Further soften any remaining overclaims
- Formalize informal arguments (e.g., truncation → formal proposition)
- Strengthen limitations section

**Edit-whitelist gate (if set):** Same as Step 3 — if `EDIT_WHITELIST` is set, run the path + forbidden-operation checks before applying each proposed edit. Rejections are logged to `PAPER_IMPROVEMENT_LOG.md` under `## Rejected by edit_whitelist (Round 2)` and the loop continues. Surface a rejection summary at the end of the round.

### Step 7: Recompile Round 2

```bash
cd paper && latexmk -C && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf main_round2.pdf
```

### Step 8: Format Check

After the final recompilation, run a **location-aware** format compliance check.

```bash
# If the log lacks file/line data, rerun the final compile once with -file-line-error.
cd paper && latexmk -pdf -file-line-error -interaction=nonstopmode -halt-on-error main.tex
```

```bash
# 1. Page count vs venue limit
PAGES=$(pdfinfo paper/main.pdf | grep Pages | awk '{print $2}')
echo "Pages: $PAGES (limit: 9 main body for ICLR/NeurIPS)"

# 2. Duplicate labels: HARD BLOCK
DUP_LABELS=$(grep -Rho "\\\\label{[^}]*}" paper/main.tex paper/sections 2>/dev/null | sort | uniq -d || true)
if [ -n "$DUP_LABELS" ]; then
    echo "Duplicate labels found (BLOCKING):"
    echo "$DUP_LABELS"
fi

# 3. Overfull warnings with location classification
OVERFULLS=$(grep -n "Overfull \\\\hbox" paper/main.log 2>/dev/null || true)

# Main body = source files before \appendix in main.tex.
# Appendix = source files after \appendix, or files whose path contains "appendix".
# Bibliography = paper.bbl, references.bib, or bibliography-generated output.
MAIN_BODY_OVERFULL=$(echo "$OVERFULLS" | grep -v -E 'appendix|paper\.bbl|references\.bib' || true)
APPENDIX_OVERFULL=$(echo "$OVERFULLS" | grep -E 'appendix' || true)
BIB_OVERFULL=$(echo "$OVERFULLS" | grep -E 'paper\.bbl|references\.bib' || true)

echo "Main-body overfulls (any size BLOCKS):"
echo "$MAIN_BODY_OVERFULL"
echo "Appendix overfulls (>10pt blocks):"
echo "$APPENDIX_OVERFULL"
echo "Bibliography overfulls (>20pt blocks):"
echo "$BIB_OVERFULL"
```

**Stop criteria:**
- Any duplicate label blocks completion.
- Any overfull in the main body blocks completion, regardless of size.
- Appendix overfulls block completion only if they exceed 10pt or are visibly clipping.
- Bibliography overfulls block completion only if they exceed 20pt or are visibly clipping.
- Underfull hboxes remain warnings unless they create obvious layout damage.

**Auto-fix patterns (location-aware):**

| Issue | Fix |
|-------|-----|
| Main-body overfull in equation | Split with `aligned` / `split` / `multline`, or shorten notation |
| Main-body overfull in table | Reduce font, resize table, or break table across rows |
| Main-body overfull in text | Rephrase; do not hide it with global `\sloppy` |
| Appendix overfull ≤ 10pt | Warn only unless visibly clipping |
| Appendix overfull > 10pt | Apply the same fix if the spill is visible |
| Bibliography overfull ≤ 20pt | Warn only unless caused by malformed entry or clipping |
| Bibliography overfull > 20pt | Fix malformed entry, URL, or DOI formatting |
| Over page limit | Move content to appendix, compress tables, reduce figure sizes |

**Location-aware interpretation:**
- Classify by the source file reported in the `-file-line-error` log.
- If a warning cannot be classified, treat it as main body and fix it.

**Empirical motivation:** in a real submission run, dozens of overfull hbox warnings (the largest well over 100pt in an appendix proof) survived multiple improvement rounds because the previous blanket "overfull > 10pt blocks" rule was too lax and treated all locations equally.

### Completion criteria

Complete when the requested paper scope is addressed, material fixes have been verified on the current artifacts, and applicable compilation, claim/evidence and visual gates are satisfied. Recompile after source changes; do not rebuild unchanged output solely because another numbered step contains a build command. Do not launch new experiments merely to satisfy a reviewer suggestion without task authorization.

At the round cap, lack of a useful next revision, or an unavailable required review, preserve the latest artifacts and report unresolved findings with their impact. A completed loop is not proof of acceptance. Run the applicable final checks and record the actual number of rounds; omit unused round rows/files from the report templates below.

### Step 9: Document Results

Create `PAPER_IMPROVEMENT_LOG.md` in the paper directory:

```markdown
# Paper Improvement Log

## Score Progression

| Round | Score | Verdict | Key Changes |
|-------|-------|---------|-------------|
| Round 0 (original) | X/10 | No/Almost/Yes | Baseline |
| Round 1 | Y/10 | No/Almost/Yes | [summary of fixes] |
| Round 2 | Z/10 | No/Almost/Yes | [summary of fixes] |

## Round 1 Review & Fixes

<details>
<summary>GPT-5.6-Sol xhigh Review (Round 1)</summary>

[Full raw review text, verbatim]

</details>

### Fixes Implemented
1. [Fix description]
2. [Fix description]
...

## Round 2 Review & Fixes

<details>
<summary>GPT-5.6-Sol xhigh Review (Round 2)</summary>

[Full raw review text, verbatim]

</details>

### Fixes Implemented
1. [Fix description]
2. [Fix description]
...

## PDFs
- `main_round0_original.pdf` — Original generated paper
- `main_roundN.pdf` — Snapshot after an actual revision round, only if produced
- `main.pdf` — Current validated deliverable; may be unchanged when no fixes were needed
```

### Step 9: Summary

Report to user:
- Score progression table
- Number of CRITICAL/MAJOR/MINOR issues fixed per round
- Final page count
- Remaining issues (if any)

### Feishu Notification (only if authorized and configured)

At review/completion events, first check whether the user explicitly authorized these Feishu notifications. If authorized and `~/.codex/feishu.json` is configured:
- **After each round**: Send `review_scored` — "Round N: X/10 — [key changes]"
- **After final round**: Send `pipeline_done` — score progression table + final page count
- If config absent or mode `"off"`: skip entirely (no-op)

## Output

```
paper/
├── main_round0_original.pdf    # Original
├── main_roundN.pdf             # Only snapshots of actual revision rounds, if any
├── main.pdf                    # Current validated deliverable, regardless of round count
└── PAPER_IMPROVEMENT_LOG.md    # Full review log with scores
```

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Preserve all PDF versions** — user needs to compare progression
- **Save FULL raw review text** — do not summarize or truncate GPT-5.6-Sol responses
- **Reviewer independence (Round 2+)**: when `REVIEWER_BIAS_GUARD = true` (default), use a **fresh** `spawn_agent` reviewer for every review round; never use stale reviewer continuation and never include "since last round" / fix summaries in the prompt. See the Reviewer Independence Protocol section above.
- **Always recompile after fixes** — verify 0 errors before proceeding
- **Do not fabricate experimental results** — synthetic validation must describe methodology, not invent numbers
- **Respect the paper's claims** — soften overclaims rather than adding unsupported new claims
- **Global consistency** — when renaming notation or softening claims, check ALL files (abstract, intro, method, experiments, theory sections, conclusion, tables, figure captions)
- **Edit-whitelist rejections are LOGGED, not silently dropped** — when `EDIT_WHITELIST` is set and an edit is rejected for a path or forbidden-operation violation, the rejection MUST be appended to `PAPER_IMPROVEMENT_LOG.md` with file, reason, offending pattern, and the original reviewer concern. The loop reports a rejection summary at the end of every round (and in the checkpoint, if `HUMAN_CHECKPOINT = true`). Never silently swallow a whitelist rejection — the audit trail is the whole point of the parameter.

## Historical Score Example (not an acceptance target)

Based on end-to-end testing on a real theory-paper run:

| Round | Score | Key Improvements |
|-------|-------|-----------------|
| Round 0 | 4/10 (content) | Baseline: assumption-model mismatch, overclaims, notation issues |
| Round 1 | 6/10 (content) | Fixed assumptions, softened claims, added interpretation, renamed notation |
| Round 2 | 7/10 (content) | Added synthetic validation, formal truncation proposition, stronger limitations |
| Round 3 | 5→8.5/10 (format) | Removed hero fig, appendix, compressed conclusion, fixed overfull hbox |

This inherited example is not an Astra benchmark or an expected score trajectory. Judge completion from current artifacts and applicable gates; do not coach a reviewer toward these scores.

## Review Tracing

After each `spawn_agent`, `send_input`, or adversarial reviewer call, save the trace following `../shared-references/review-tracing.md`. Write files directly to `.aris/traces/auto-paper-improvement-loop/<date>_run<NN>/`. Respect the `--- trace:` parameter when present (default: `full`).
