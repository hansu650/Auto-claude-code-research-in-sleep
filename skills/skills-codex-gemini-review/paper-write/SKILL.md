---
name: "paper-write"
description: "Write, rewrite, or polish research-paper prose and LaTeX from available project evidence. Use for a full draft or individual sections, especially the Abstract, Introduction and contribution bullets, Method, Conclusion, limitations, and future work; common requests include 写论文, 改摘要, write paper, rewrite abstract, and polish conclusion. In a new or context-free folder, inspect local artifacts first and request only missing blocking input."
---

> Override for Codex users who want **Gemini**, not a second Codex agent, to act as the reviewer. Install this package **after** `skills/skills-codex/*`.

# Paper Write: Section-by-Section LaTeX Generation

> **Gemini overlay assurance:** `review_independence: cross-family` and `acceptance_status: accepted`.

Draft a LaTeX paper based on: **$ARGUMENTS**

<!-- BEGIN ARIS NEUTRAL: COLD START -->
## Cold-start behavior

- Do not require prior conversation or a particular workspace. Treat the current request and discovered project artifacts as the source of truth.
- Inspect the current directory and any user-named paths first for relevant repository instructions, paper sources and PDFs, plans, claims, results, data, figures, tables, bibliography, and build files.
- If the request and discovered artifacts are sufficient, proceed without asking the user to repeat context.
- If required information is missing, ask only for the smallest blocking input. When safe, still provide the best useful scaffold, partial artifact, or diagnostic supported by the available evidence.
- Stay project-neutral: do not assume any paper, method, dataset, metric, filename, numbering, venue, build tool, or result that is not stated or discovered.
<!-- END ARIS NEUTRAL: COLD START -->

The constants and template paths below are full-draft initialization fallbacks, not facts
about an existing manuscript. Do not apply them to a section-only rewrite or when local
files establish another venue, anonymity setting, page rule, or directory layout.

## Constants

- **REVIEWER_MODEL = `gemini-review`** — Gemini reviewer invoked through the local `gemini-review` MCP bridge. Set `GEMINI_REVIEW_MODEL` if you need a specific Gemini model override.
- **TARGET_VENUE = `ICLR`** — Default venue. Supported: `ICLR`, `NeurIPS`, `ICML`. Determines style file and formatting.
- **ANONYMOUS = true** — If true, use anonymous author block. Set `false` for camera-ready.
- **MAX_PAGES = 9** — Main body page limit. Counts from first page to end of Conclusion section. References and appendix are NOT counted.
- **DBLP_BIBTEX = true** — Fetch real BibTeX from DBLP/CrossRef instead of LLM-generated entries. Eliminates hallucinated citations. Zero install required. Set `false` to use legacy behavior (LLM search + `[VERIFY]` markers).

## Inputs

1. **PAPER_PLAN.md** — outline with canonical Claim Ledger, coverage index, section plan, and figure/table layout plan (from `/paper-plan`)
2. **NARRATIVE_REPORT.md** — the research narrative (primary source of content)
3. **Generated figures** — PDF/PNG files in `figures/` (from `/paper-figure`)
4. **LaTeX includes** — `figures/latex_includes.tex` (from `/paper-figure`)
5. **Bibliography** — existing `.bib` file, or will create one

If `PAPER_PLAN.md` is absent, inspect existing LaTeX, PDFs, narrative/claim files, results,
figures, tables, and the user's requested section. Proceed when those artifacts are
sufficient; otherwise ask only for the smallest missing outline or evidence.

## Orchestra-Guided Writing Overlay

- Read `../shared-references/writing-principles.md` before drafting prose or when it feels generic.
- Read `../shared-references/section-blueprints.md` **mandatorily** before drafting or rewriting a claim-bearing Abstract, Introduction contribution list, Method/analysis section, or Conclusion.
- Read `../shared-references/venue-checklists.md` during final write-up and submission checks.
- Read `../shared-references/citation-discipline.md` only when the built-in verified bibliography path is insufficient.

## Templates

### Venue-Specific Setup

The skill includes conference templates in `templates/`. Select based on TARGET_VENUE:

**ICLR:**
```latex
\documentclass{article}
\usepackage{iclr2026_conference,times}
% \iclrfinalcopy  % Uncomment for camera-ready
```

**NeurIPS:**
```latex
\documentclass{article}
\usepackage[preprint]{neurips_2025}
% \usepackage[final]{neurips_2025}  % Camera-ready
```

**ICML:**
```latex
\documentclass[accepted]{icml2025}
% Use [accepted] for camera-ready
```

### Project Structure

Generate this file structure:

```
paper/
├── main.tex                    # master file (includes sections)
├── iclr2026_conference.sty     # or neurips_2025.sty / icml2025.sty
├── math_commands.tex           # shared math macros
├── references.bib              # bibliography (filtered — only cited entries)
├── sections/
│   ├── 0_abstract.tex
│   ├── 1_introduction.tex
│   ├── 2_related_work.tex
│   ├── 3_method.tex            # or preliminaries, setup, etc.
│   ├── 4_experiments.tex
│   ├── 5_conclusion.tex
│   └── A_appendix.tex          # proof details, extra experiments
└── figures/                    # symlink or copy from project figures/
```

**Section files are FLEXIBLE**: If the paper plan has 6-8 sections, create corresponding files (e.g., `4_theory.tex`, `5_experiments.tex`, `6_analysis.tex`, `7_conclusion.tex`).

## Workflow

### Step 0: Backup and Clean

If `paper/` already exists, back up to `paper-backup-{timestamp}/` before overwriting. Never silently destroy existing work.

**CRITICAL: Clean stale files.** When changing section structure (e.g., 5 sections → 7 sections), delete section files that are no longer referenced by `main.tex`. Stale files (e.g., old `5_conclusion.tex` left behind when conclusion moved to `7_conclusion.tex`) cause confusion and waste space.

### Step 1: Initialize Project

1. Create `paper/` directory
2. Copy venue template from `templates/` — the template already includes:
   - All standard packages (amsmath, hyperref, cleveref, booktabs, etc.)
   - Theorem environments with `\crefname{assumption}` fix
   - Anonymous author block
3. Generate `math_commands.tex` with paper-specific notation
4. Create section files matching PAPER_PLAN structure

**Author block (anonymous mode):**
```latex
\author{Anonymous Authors}
```

### Step 2: Generate math_commands.tex

Create shared math macros based on the paper's notation:

```latex
% math_commands.tex — shared notation
\newcommand{\R}{\mathbb{R}}
\newcommand{\E}{\mathbb{E}}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
% Add paper-specific notation here
```

### Step 3: Write Each Section

Process sections in order. For each section:

1. **Read the plan** — what claims, evidence, citations belong here
2. **Read NARRATIVE_REPORT.md** — extract relevant content, findings, and quantitative results
3. **Draft content** — write complete LaTeX (not placeholders)
4. **Insert figures/tables** — use snippets from `figures/latex_includes.tex`
5. **Add citations** — use `\citep{}` / `\citet{}` (all three venues use `natbib`)

#### Section-Specific Guidelines

**§0 Abstract:**
- Use the applicable semantic moves from `section-blueprints.md`; do not force a fixed sentence count
- Must be self-contained (understandable without reading the paper)
- Start with the paper's specific contribution, not generic field-level background
- Use only the canonical comparator, evidence, and scope from the Claim Ledger
- Obey the venue word limit; if unknown, target 150-200 words
- No citations, no undefined acronyms
- No `\begin{abstract}` — that's in main.tex

**§1 Introduction:**
- Open with a compelling hook (1-2 sentences, problem motivation)
- State the gap clearly ("However, ...")
- List 2-4 role-based, falsifiable contributions; map each to Claim IDs and evidence and do not force every bullet to begin with "We"
- End with a brief roadmap ("The rest of this paper is organized as...")
- Include the main result figure if space allows
- Target: 1.5 pages

**§2 Related Work:**
- **MINIMUM 1 full page** (3-4 substantive paragraphs). Short related work sections are a common reviewer complaint.
- Organize by category using `\paragraph{Category Name.}`
- Each category: 1 paragraph summarizing the line of work + 1-2 sentences positioning this paper
- Do NOT just list papers — synthesize and compare
- End each paragraph with how this paper relates/differs

**§3 Method / Preliminaries / Setup:**
- Define notation early (reference math_commands.tex)
- State the input/output contract, frozen or unchanged components, changed components, and end-to-end flow before module detail
- For each module or argument use motivation → input/output → construction/equation → property/effect → hand-off
- Disclose what is selected, trained, adapted, calibrated, or fixed and what target/reference/full-sequence access is required
- Introduce each important equation with its purpose, define every symbol, and follow it with the direct effect and relevant boundary case
- Use `\begin{definition}`, `\begin{theorem}` environments for formal statements
- For theory papers: include proof sketches of key results in main body, full proofs in appendix
- For theory papers: include a **comparison table** of prior bounds vs. this paper
- Include algorithm pseudocode if applicable (`algorithm2e` or `algorithmic`)
- Target: 1.5-2 pages

**§4 Experiments:**
- Start with experimental setup (datasets, baselines, metrics, implementation details)
- Main results table/figure first
- Then ablations and analysis
- Every claim from the introduction must have supporting evidence here
- Target: 2.5-3 pages

**§5 Conclusion:**
- Mirror the paper's claim order without copying the Introduction
- Repeat only canonical evidence, comparators, protocols, and scope qualifiers
- Introduce no new method, number, comparator, dataset, protocol, or claim
- State limitations honestly; put Future Work in a separate paragraph derived from those limitations when space permits
- Ethics statement and reproducibility statement (if venue requires)
- Target: 0.5 pages

**Appendix:**
- Proof details (full proofs of main-body theorems)
- Additional experiments, ablations
- Implementation details, hyperparameter tables
- Additional visualizations

### Step 4: Build Bibliography

**CRITICAL: Only include entries that are actually cited in the paper.**

1. Scan all `\citep{}` and `\citet{}` references in the drafted sections
2. Build a citation key list
3. For each citation key:
   - Check existing `.bib` files in the project/narrative docs
   - If not found and **DBLP_BIBTEX = true**, use the verified fetch chain below
   - If not found and **DBLP_BIBTEX = false**, search arXiv/Scholar for correct BibTeX
   - **NEVER fabricate BibTeX entries** — mark unknown ones with `[VERIFY]` comment
4. Write `references.bib` containing ONLY cited entries (no bloat)

#### Verified BibTeX Fetch (when DBLP_BIBTEX = true)

Three-step fallback chain — zero install, zero auth, all real BibTeX:

**Step A: DBLP (best quality — full venue, pages, editors)**
```bash
# 1. Search by title + first author
curl -s "https://dblp.org/search/publ/api?q=TITLE+AUTHOR&format=json&h=3"
# 2. Extract DBLP key from result (e.g., conf/nips/VaswaniSPUJGKP17)
# 3. Fetch real BibTeX
curl -s "https://dblp.org/rec/{key}.bib"
```

**Step B: CrossRef DOI (fallback — works for arXiv preprints)**
```bash
# If paper has a DOI or arXiv ID (arXiv DOI = 10.48550/arXiv.{id})
curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"
```

**Step C: Mark `[VERIFY]` (last resort)**
If both DBLP and CrossRef return nothing, mark the entry with `% [VERIFY]` comment. Do NOT fabricate.

**Why this matters:** LLM-generated BibTeX frequently hallucinates venue names, page numbers, or even co-authors. DBLP and CrossRef return publisher-verified metadata. Upstream skills (`/research-lit`, `/novelty-check`) may mention papers from LLM memory — this fetch chain is the gate that prevents hallucinated citations from entering the final `.bib`.

**Automated bib cleaning** — use this Python pattern to extract only cited entries:

```python
import re
# 1. Grep all \citep{...} and \citet{...} from all .tex files
# 2. Extract unique keys (handle multi-cite like \citep{a,b,c})
# 3. Parse the full .bib file, keep only entries whose key is in the cited set
# 4. Write the filtered bib
```

This prevents bib bloat (e.g., 948 lines → 215 lines in testing).

**Citation verification rules (from claude-scholar + Imbad0202):**
1. Every BibTeX entry must have: author, title, year, venue/journal
2. Prefer published venue versions over arXiv preprints (if published)
3. Use consistent key format: `{firstauthor}{year}{keyword}` (e.g., `ho2020denoising`)
4. Double-check year and venue for every entry
5. Remove duplicate entries (same paper with different keys)

### Step 5: De-AI Polish (from kgraph57/paper-writer-skill)

After drafting all sections, scan for common AI writing patterns and fix them:

**Content patterns to fix:**
- Significance inflation ("groundbreaking", "revolutionary" → use measured language)
- Formulaic transitions ("In this section, we..." → remove or vary)
- Generic conclusions ("This work opens exciting new avenues" → be specific)

**Language patterns to fix (watch words):**
- Replace: delve, pivotal, landscape, tapestry, underscore, noteworthy, intriguingly
- Remove filler: "It is worth noting that", "Importantly,", "Notably,"
- Avoid rule-of-three lists ("X, Y, and Z" appearing repeatedly)
- Don't start consecutive sentences with "This" or "We"

### Step 6: Cross-Review with REVIEWER_MODEL

Send the complete draft to Gemini review:

```
mcp__gemini-review__review_start:
  prompt: |
    Review this [VENUE] paper draft (main body, excluding appendix).

    Focus on:
    1. Does each claim from the intro have supporting evidence?
    2. Is the writing clear, concise, and free of AI-isms?
    3. Any logical gaps or unclear explanations?
    4. Does it fit within [MAX_PAGES] pages (to end of Conclusion)?
    5. Is related work sufficiently comprehensive (≥1 page)?
    6. For theory papers: are proof sketches adequate?
    7. Are figures/tables clearly described and properly referenced?
    8. Do Abstract, contribution bullets, body, evidence, and Conclusion mirror the Claim Ledger without comparator, number, protocol, or scope drift?
    9. Does the Conclusion introduce any new claim or unsupported expansion?

    For each issue, specify: severity (CRITICAL/MAJOR/MINOR), location, and fix.

    [paste full draft text]
```

After this start call, immediately save the returned `jobId` and poll `mcp__gemini-review__review_status` with a bounded `waitSeconds` until `done=true`. Treat the completed status payload's `response` as the reviewer output, and save the completed `threadId` for any follow-up round.

Apply CRITICAL and MAJOR fixes. Document MINOR issues for the user.

### Step 7: Reverse Outline Test (from Research-Paper-Writing-Skills)

After drafting all sections:

1. **Extract topic sentences** — pull the first sentence of every paragraph
2. **Read them in sequence** — they should form a coherent narrative on their own
3. **Check claim coverage** — every supported Claim ID from the canonical Claim Ledger must appear in its planned locations
4. **Check evidence mapping** — every experiment/figure must support a stated claim
5. **Fix gaps** — if a topic sentence doesn't advance the story, rewrite the paragraph

### Step 8: Final Checks

Before declaring done:

- [ ] All `\ref{}` and `\label{}` match (no undefined references)
- [ ] All `\citep{}` / `\citet{}` have corresponding BibTeX entries
- [ ] No author information in anonymous mode
- [ ] Figure/table numbering is correct
- [ ] Page count within MAX_PAGES (main body to Conclusion end)
- [ ] No TODO/FIXME/XXX markers left in the text
- [ ] No `[VERIFY]` markers left unchecked
- [ ] Abstract is self-contained (understandable without reading the paper)
- [ ] Front-Matter Coverage Index is complete and matches the canonical Claim Ledger
- [ ] Abstract and Conclusion use the same canonical comparator, headline evidence, protocol, and scope qualifiers
- [ ] Conclusion introduces no new method, number, comparator, dataset, protocol, or claim
- [ ] Title is specific and informative (not generic)
- [ ] Related work is ≥1 full page
- [ ] references.bib contains ONLY cited entries (no bloat)
- [ ] **No stale section files** — every .tex in `sections/` is `\input`ed by `main.tex`
- [ ] **Section files match main.tex** — file numbering and `\input` paths are consistent

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../../shared-references/output-manifest.md)** — log every output to MANIFEST.md
> - **[Output Language Protocol](../../shared-references/output-language.md)** — respect the project's language setting

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.

- **Do NOT generate author names, emails, or affiliations** — use anonymous block or placeholder
- **Write complete sections, not outlines** — the output should be compilable LaTeX
- **One file per section** — modular structure for easy editing
- **Every claim must cite evidence** — cross-reference the Canonical Claim Ledger
- **Compile-ready** — the output should compile with `latexmk` without errors (modulo missing figures)
- **No over-claiming** — use hedging language ("suggests", "indicates") for weak evidence
- **Venue style matters** — all three venues (ICLR/NeurIPS/ICML) use `natbib` (`\citep`/`\citet`)
- **Page limit = main body to Conclusion** — references and appendix do NOT count
- **Clean bib** — references.bib must only contain entries that are actually `\cite`d
- **Section count is flexible** — match PAPER_PLAN structure, don't force into 5 sections
- **Backup before overwrite** — never destroy existing `paper/` directory without backing up

## Writing Quality Reference

Principles from [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills):

1. **One message per paragraph** — each paragraph makes exactly one point
2. **Topic sentence first** — the first sentence states the paragraph's message
3. **Explicit transitions** — connect paragraphs with logical connectors
4. **Reverse outline test** — extract topic sentences; they should form a coherent narrative

De-AI patterns from [kgraph57/paper-writer-skill](https://github.com/kgraph57/paper-writer-skill):

5. **No AI watch words** — delve, pivotal, landscape, tapestry, underscore
6. **No significance inflation** — groundbreaking, revolutionary, paradigm shift
7. **No formulaic structures** — vary sentence openings and transitions

## Acknowledgements

Writing methodology adapted from [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (CCF award-winning methodology). Citation verification from [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) and [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills). De-AI polish from [kgraph57/paper-writer-skill](https://github.com/kgraph57/paper-writer-skill). Backup mechanism from [baoyu-skills](https://github.com/jimliu/baoyu-skills).
