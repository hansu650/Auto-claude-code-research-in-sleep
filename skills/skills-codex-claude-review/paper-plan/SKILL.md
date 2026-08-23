---
name: "paper-plan"
description: "Plan and structure a research paper from available project evidence. Use for paper outlines, claim-to-section plans, Abstract plans, Introduction contribution plans, Method organization, Conclusion plans, and figure/table plans; common requests include 写大纲, 论文规划, paper outline, and plan the paper. In a new or context-free folder, inspect local artifacts first and request only missing blocking input."
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

# Paper Plan: From Review Conclusions to Paper Outline

Generate a structured, section-by-section paper outline from: **$ARGUMENTS**

<!-- BEGIN ARIS NEUTRAL: COLD START -->
## Cold-start behavior

- Do not require prior conversation or a particular workspace. Treat the current request and discovered project artifacts as the source of truth.
- Inspect the current directory and any user-named paths first for relevant repository instructions, paper sources and PDFs, plans, claims, results, data, figures, tables, bibliography, and build files.
- If the request and discovered artifacts are sufficient, proceed without asking the user to repeat context.
- If required information is missing, ask only for the smallest blocking input. When safe, still provide the best useful scaffold, partial artifact, or diagnostic supported by the available evidence.
- Stay project-neutral: do not assume any paper, method, dataset, metric, filename, numbering, venue, build tool, or result that is not stated or discovered.
<!-- END ARIS NEUTRAL: COLD START -->

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

The constants and paths below are planning fallbacks, not facts about an existing
project. Do not impose them when the request or discovered artifacts establish a venue,
page rule, structure, or file layout.

## Constants

- **REVIEWER_MODEL = `claude-review`** — Claude reviewer invoked through the local `claude-review` MCP bridge. Set `CLAUDE_REVIEW_MODEL` if you need a specific Claude model override.
- **TARGET_VENUE = `ICLR`** — Default venue. User can override (e.g., `/paper-plan "topic" — venue: NeurIPS`). Supported: `ICLR`, `NeurIPS`, `ICML`, `CVPR`, `ACL`, `AAAI`, `ACM`, `IEEE_JOURNAL` (IEEE Transactions / Letters), `IEEE_CONF` (IEEE conferences).
- **MAX_PAGES** — Page limit. For ML conferences: main body to Conclusion end (excluding references, appendix). ICLR=9, NeurIPS=9, ICML=8, AAAI=7 technical-content pages plus references unless the current AAAI CFP says otherwise. **For IEEE venues: references ARE included in page count.** IEEE journal Transactions ≈ 12-14 pages total, Letters ≈ 4-5 pages total; IEEE conference ≈ 5-8 pages total (including references).

## Inputs

The skill expects one or more of these in the project directory:

1. **NARRATIVE_REPORT.md** or **STORY.md** — research narrative with claims and evidence
2. **review-stage/AUTO_REVIEW.md** — auto-review loop conclusions *(fall back to `./AUTO_REVIEW.md` if not found)*
3. **Experiment results** — JSON files in `figures/`, screen logs, tables
4. **idea-stage/IDEA_REPORT.md** — from idea-discovery pipeline (if applicable) *(fall back to `./IDEA_REPORT.md` if not found)*
5. **CLAIMS_FROM_RESULTS.md** — structured claim judgment from `/result-to-claim` (preferred if available)

Only after inspecting the current directory and user-named paths, if no usable evidence
or source material exists, ask for the smallest missing description needed to build a
defensible outline.

## Orchestra-Guided Writing Overlay

Keep the existing workflow and outputs, but use the shared references below to improve the quality of the story and outline:

- Read `../shared-references/writing-principles.md` when framing the Abstract, Introduction, Related Work, or hero figure
- Read `../shared-references/section-blueprints.md` **mandatorily** when planning a claim-bearing Abstract, Introduction contribution list, Method/analysis section, or Conclusion. Its Claim Ledger, fixed-count front-matter profile, and mirror contract are canonical.
- Read `../shared-references/publication-layout-gates.md` **mandatorily** when planning any figure or table.
- Read `../shared-references/venue-checklists.md` before freezing the outline for a specific venue
- Load these references only when they help; they are support material, not a new workflow phase

## Workflow

### Step 1: Extract Claims and Evidence

**First check for `CLAIMS_FROM_RESULTS.md`** — if its first line is `verdict: REVIEW_UNAVAILABLE`, treat the file as ABSENT for claim extraction (fall through to the narrative documents below) and then: under `— assurance: submission` (`shared-references/assurance-contract.md`; implied by `— effort: max|beast`) STOP — the claims were never adjudicated, rerun `/result-to-claim` first; under `assurance: draft` continue but tag every claim `[unadjudicated]`. Otherwise, if it exists, use it as the starting point for claims and merge it with any additional evidence from the narrative documents below.

Read all available narrative documents and extract:

1. **Core claims** (3-5 main contributions)
2. **Evidence** for each claim (which experiments, which metrics, which figures)
3. **Known weaknesses** (from reviewer feedback)
4. **Suggested framing** (from review conclusions)

Extend the existing matrix into one canonical **Claim Ledger**. Do not create a second
claim store:

```markdown
| Claim ID | Role | Exact claim | Comparator or N/A | Evidence (experiment/table/figure/theorem/proof) | Scope/data access | Selection/training/adaptation or N/A | Limitation | Forbidden expansion |
|---|---|---|---|---|---|---|---|---|
| C1 | formulation | ... | ... | ... | ... | ... | ... | ... |
```

Apply every disclosure distinction in `section-blueprints.md`; use `N/A` rather than
inventing a method-paper field for another paper type.

### Step 2: Determine Paper Type and Structure

Based on TARGET_VENUE and paper content, classify and select structure.

Before committing to a structure, apply the narrative principle from `../shared-references/writing-principles.md`:

- The paper should tell one coherent technical story
- By the end of the Introduction, the outline should make the **What**, **Why**, and **So What** explicit
- Front-load the most important material: title, abstract, introduction, and hero figure

**IMPORTANT**: The section count is FLEXIBLE (5-8 sections). Choose what fits the content best. The templates below are starting points, not rigid constraints.

**Empirical/Diagnostic paper:**
```
1. Introduction (1.5 pages)
2. Related Work (1 page)
3. Method / Setup (1.5 pages)
4. Experiments (3 pages)
5. Analysis / Discussion (1 page)
6. Conclusion (0.5 pages)
```

**Theory + Experiments paper:**
```
1. Introduction (1.5 pages)
2. Related Work (1 page)
3. Preliminaries & Modeling (1.5 pages)
4. Experiments (1.5 pages)
5. Theory Part A (1.5 pages)
6. Theory Part B (1.5 pages)
7. Conclusion (0.5 pages)
— Total: 9 pages
```
Theory papers often need 7 sections (splitting theory into estimation + optimization, or setup + analysis). The total page budget MUST sum to MAX_PAGES.

Theory papers should:
- Include **proof sketch** locations (not just theorem statements)
- Plan a **comparison table** of prior theoretical bounds vs. this paper's bounds
- Identify which proofs go in appendix vs. main body

**Method paper:**
```
1. Introduction (1.5 pages)
2. Related Work (1 page)
3. Method (2 pages)
4. Experiments (2.5 pages)
5. Ablation / Analysis (1 page)
6. Conclusion (0.5 pages)
```

### Step 2.5: Fix the Front-Matter Sentence Profile

Record the exact profile before planning individual sections. For an empirical AI method
paper, the default is: Abstract = 10 sentences; Introduction contributions = exactly 3
bullets with `2 / 3 / 3` sentences; Conclusion = 8 sentences. Use the sentence-role order
in `section-blueprints.md`. The roles and counts are fixed, while wording and technical
content remain specific to the paper's Claim Ledger.

An explicit user instruction or venue rule may replace this default. A theory,
diagnostic, position, or other non-method paper also needs a type-specific profile. In
either case, write the replacement exact counts and role sequence into `PAPER_PLAN.md`
before drafting; never leave the profile variable or silently change it later.

### Step 3: Section-by-Section Planning

For each section, specify:

```markdown
### §0 Abstract
- **Sentence profile**: [empirical AI method default = exactly 10 sentences; otherwise the recorded exact override]
- **Sentence roles**: [setting → limitation → reframing → method contract → mechanism 1 → mechanism 2 → design boundary → primary evidence → secondary evidence/boundary → takeaway]
- **Canonical claims**: [Claim IDs represented]
- **Headline evidence**: [canonical comparator/result/scope, if applicable]
- **Estimated length**: [venue limit; otherwise 150-200 words]
- **Self-contained check**: can a reader understand this without the paper?

### §1 Introduction
- **Opening hook**: [1-2 sentences that motivate the problem]
- **Gap**: [what's missing in prior work]
- **Key questions**: [the research questions this paper answers]
- **Contributions**: [empirical AI method default = exactly 3 role-based bullets with 2 / 3 / 3 sentences: problem/formulation, method/mechanism, evidence/scope; each mapped to Claim IDs and evidence]
- **Hero figure**: [describe what Figure 1 should show — MUST include clear comparison if applicable]
- **Estimated length**: 1.5 pages
- **Key citations**: [3-5 papers to cite here]

### §2 Related Work
- **Subtopics**: [2-4 categories of related work]
- **Positioning**: [how this paper differs from each category]
- **Minimum length**: 1 full page (at least 3-4 paragraphs with substantive synthesis)
- **Must NOT be just a list** — synthesize, compare, and position

### §3 Method / Setup / Preliminaries
- **Overview contract**: [input/output, frozen or unchanged parts, changed parts, end-to-end flow]
- **Representation/interface**: [objects handed to and from the method or analysis]
- **Modules/arguments**: [motivation → input/output → construction/equation → property/effect → hand-off]
- **Composition and access**: [selected/trained/adapted/fixed behavior plus online/offline/reference/full-sequence access]
- **Boundary cases**: [behavior required for reproduction]
- **Formal statements**: [theorems, propositions if applicable]
- **Proof sketch locations**: [which key steps appear here vs. appendix]
- **Estimated length**: 1.5-2 pages

### §4 Experiments / Main Results
- **Figures planned**:
  - Fig 1: [description, type: bar/line/table/architecture, WHAT COMPARISON it shows]
  - Fig 2: [description]
  - Table 1: [what it shows, which methods/baselines compared]
- **Data source**: [which JSON files / experiment results]

### §5 Conclusion
- **Sentence profile**: [empirical AI method default = exactly 8 sentences; otherwise the recorded exact override]
- **Sentence roles**: [answer → mechanism → primary evidence → secondary evidence/boundary → interpretation → limitation → practical takeaway → significance]
- **No-new-claim check**: [no new method, number, comparator, dataset, protocol, or claim]
- **Separate venue sections**: [Limitations/Future Work only when required, outside the eight-sentence Conclusion count]
- **Estimated length**: 0.5 pages
```

### Step 4: Figure Plan

List every figure and table:

```markdown
## Figure/Table Layout Contract

| Label | Kind | Width class | Preferred placement | Must preserve | Caption budget | Priority |
|---|---|---|---|---|---|---|
| fig:overview | figure* | double column | near first discussion | readable overview at final size | 2-3 lines | primary |
| tab:primary | table | single column | before secondary diagnostics | metric, protocol, grouping, units | 1-2 lines | primary |
```

Add the data source and intended claim/evidence link beneath each row. Caption budgets
are advisory and may not remove information required for self-contained interpretation.
Use exact-page placement only when the venue or user requires it.

**CRITICAL for Figure 1 / Hero Figure**: Describe in detail what the figure should contain, including:
- Which methods are being compared
- What the visual difference should demonstrate
- Caption draft that clearly states the comparison

### Step 5: Citation Scaffolding

For each section, list required citations:

```markdown
## Citation Plan
- §1 Intro: [paper1], [paper2], [paper3] (problem motivation)
- §2 Related: [paper4]-[paper10] (categorized by subtopic)
- §3 Method: [paper11] (baseline), [paper12] (technique we build on)
```

**Citation rules** (from claude-scholar + Imbad0202/academic-research-skills):
1. NEVER generate BibTeX from memory — always verify via search or existing .bib files
2. Every citation must be verified: correct authors, year, venue
3. Flag any citation you're unsure about with `[VERIFY]`
4. Prefer published versions over arXiv preprints when available

### Step 6: Cross-Review with REVIEWER_MODEL

Send the complete outline to Claude review for feedback:

```
mcp__claude-review__review_start:
  prompt: |
    Review this paper outline for a [VENUE] submission.
    [full outline including Canonical Claim Ledger and Front-Matter Coverage Index]

    Score 1-10 on:
    1. Logical flow — does the story build naturally?
    2. Claim-evidence alignment — every claim backed?
    3. Missing experiments or analysis
    4. Positioning relative to prior work
    5. Page budget feasibility (MAX_PAGES = main body to Conclusion end, excluding refs/appendix)
    6. Claim mirroring — do Abstract, contribution bullets, body, evidence, and Conclusion preserve the same comparator, result, protocol, and scope?
    7. Publication layout — does every figure/table have a width, placement, preservation, caption, and priority contract?
    8. Sentence-profile compliance — are the planned counts and roles exact (empirical AI method default: Abstract 10, contributions 2/3/3, Conclusion 8)?

    For each weakness, suggest the MINIMUM fix.
    Be specific and actionable — "add X" not "consider more experiments".
```

After this review call, immediately save the returned `jobId` and poll `mcp__claude-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

Apply feedback before finalizing.

### Step 7: Output

Save the final outline to `PAPER_PLAN.md` in the project root:

```markdown
# Paper Plan

**Title**: [working title]
**Venue**: [target venue]
**Type**: [empirical/theory/method]
**Front-matter sentence profile**: [empirical AI method default: Abstract 10; contributions 2 / 3 / 3; Conclusion 8, or an explicit exact override]
**Date**: [today]
**Page budget**: [MAX_PAGES] pages (main body to Conclusion end, excluding references & appendix)
**Section count**: [N] (must match the number of section files that will be created)

## Canonical Claim Ledger
[from Step 1]

## Front-Matter Coverage Index
| Claim ID | Abstract move | Intro bullet | Body subsection | Evidence location | Conclusion sentence |
|---|---|---|---|---|---|
[Claim IDs and locations only; do not duplicate claim text or evidence]

## Structure
[from Step 2-3, section by section]

## Figure/Table Layout Contract
[from Step 4, with detailed hero figure description and canonical contract columns]

## Citation Plan
[from Step 5]

## Reviewer Feedback
[from Step 6, summarized]

## Next Steps
- [ ] /paper-figure to generate all figures
- [ ] /paper-write to draft LaTeX
- [ ] /paper-compile to build PDF
```

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Do NOT generate author information** — leave author block as placeholder or anonymous
- **Be honest about evidence gaps** — mark claims as "needs experiment" rather than overclaiming
- **Page budget is hard** — if content exceeds MAX_PAGES, suggest what to move to appendix
- **MAX_PAGES counting differs by venue** — ML conferences: main body to Conclusion end, references/appendix NOT counted; AAAI main track is typically 7 technical-content pages plus references. **IEEE venues: references ARE counted toward the page limit.**
- **Venue-specific norms** — ML conferences (ICLR/NeurIPS/ICML) use `natbib` (`\citep`/`\citet`); **IEEE venues use `cite` package (`\cite{}`, numeric style)**
- **The Canonical Claim Ledger is the backbone** — every claim must map to evidence, every experiment must support a claim, and no duplicate claim store may drift from it
- **Freeze sentence logic before drafting** — counts and roles are fixed by the active profile; they never justify invented content
- **Figures need detailed descriptions** — especially the hero figure, which must clearly specify comparisons and visual expectations
- **Section count is flexible** — 5-8 sections depending on paper type. Don't force content into a rigid 5-section template.

## Acknowledgements

Outline methodology inspired by [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (claim-evidence mapping), [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) (citation verification), and [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (claim verification protocol).

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../../shared-references/output-manifest.md)** — maintain MANIFEST.md only when a run exceeds the protocol's >15-artifact threshold
> - **[Output Language Protocol](../../shared-references/output-language.md)** — respect the project's language setting
