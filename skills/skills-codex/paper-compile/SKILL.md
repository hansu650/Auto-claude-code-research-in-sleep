---
name: "paper-compile"
description: "Compile, repair, format, and visually verify integrated LaTeX papers and PDFs. Use for building a PDF, fixing LaTeX errors or warnings, layout-only changes, typography, page limits, and integrated figure/table placement; common requests include 编译论文, 排版论文, build PDF, fix LaTeX, and move this figure or table. In a new or context-free folder, inspect local build instructions and sources first and request only missing blocking input."
---

# Paper Compile: LaTeX to Submission-Ready PDF

<!-- BEGIN ARIS NEUTRAL: COLD START -->
## Cold-Start Behavior

- Do not depend on prior chat history, a particular workspace, or unstated project context.
- Inspect the current directory first for repository instructions, build scripts/configuration, LaTeX sources, existing PDFs/logs, figures, tables, and venue files.
- If the available files establish the task and build contract, proceed from that evidence.
- If a required input is missing, ask only for the minimum blocking information and still provide the safest useful scaffold or diagnosis available.
- Never assume a specific paper, method, dataset, filename, venue, page number, figure number, or table number.
<!-- END ARIS NEUTRAL: COLD START -->

Compile the LaTeX paper and fix any issues: **$ARGUMENTS**

## Build Contract and Precedence

Resolve how this repository is built before running a compiler. Apply this precedence exactly:

1. The user's explicit instructions for this task.
2. Applicable repository instruction files, including scoped `AGENTS.md`, `CLAUDE.md`, or equivalent files.
3. Repository-owned build scripts and configuration such as `Makefile`, `latexmkrc`, CI workflows, or documented commands.
4. The conservative fallbacks below, only for details that remain unresolved.

Never replace a higher-precedence contract with a familiar local command. Record the resolved paper directory, main source, compiler/engine, command, output path, and venue limit before compiling.

## Fallbacks

- **COMPILER = `latexmk`** — fallback build orchestrator when the repository does not specify one.
- **ENGINE = `pdflatex`** — fallback engine; use `xelatex` or `lualatex` only when the source, fonts, or repository contract requires it.
- **MAX_COMPILE_ATTEMPTS = 3** — Maximum attempts to fix errors and recompile.
- **PAPER_DIR = `paper/`** — fallback source directory; otherwise use the discovered directory.
- **MAIN_TEX = `main.tex`** — fallback entry point; otherwise use the target named by the build contract.
- **OUTPUT_PDF = main source stem + `.pdf`** — fallback output; otherwise use the configured output path.
- **MAX_PAGES** — Page limit. ML conferences: main body to Conclusion end (excluding references & appendix). ICLR=9, NeurIPS=9, ICML=8. **IEEE venues: references ARE included in page count.** IEEE journal ≈ 12-14 pages, IEEE conference ≈ 5-8 pages (all inclusive).
- **RESCUE_ON_REPEAT_FAILURE = true** — If the same compile class fails after two attempts, preserve `compile.log` and ask for a focused rescue / second opinion before further edits.

## Mandatory Publication-Layout Gate

Before changing or accepting figure/table placement, sizing, captions, or integrated page layout, read [`../shared-references/publication-layout-gates.md`](../shared-references/publication-layout-gates.md). Its integrated-page checks are mandatory. `paper-compile` owns this final page-level gate even when another skill created the standalone artifact.

## Workflow

### Step 0: Snapshot the Task and Existing Work

Before any edit or build:

1. Record the current directory, repository root, branch/commit when available, and the resolved build contract.
2. If the directory is a Git worktree, capture `git status --short` and retain it as the baseline. Treat every pre-existing modification and untracked file as user-owned; never stage, restore, overwrite, or discard unrelated work.
3. Record the source files, bibliography, figures/tables, existing PDF/log, and venue files that are in scope. If Git is unavailable, use a file inventory with sizes/timestamps and hashes for protected files.
4. Record which repository instruction files and build scripts/configuration were consulted.

For a **layout-only** request, establish a content-preservation gate before editing:

- Define the authorized files and allowed layout transformations.
- Compute cryptographic hashes for files outside the authorized set that must remain byte-identical.
- Preserve manuscript wording, numbers, citations, equations, labels, and experimental content unless the user explicitly expands the scope.
- After editing, inspect the source diff manually, recheck protected hashes, and run a numeric/string audit over the affected manuscript scope.
- State the exact extraction/comparison method and coverage. Never call an underspecified or spot-checked comparison deterministic.
- If a layout fix appears to require rephrasing prose, stop and request authorization rather than silently changing it.

If the user or project designates a SHA-256/text lock manifest, treat it as an
additional binding gate:

- verify every protected section before editing and again after the final build;
- protect the lock manifest itself, and never regenerate it merely to make a
  failed check pass;
- rebuild a lock only after the user explicitly authorizes the corresponding
  content change, and record the reason and reviewed diff;
- when protected prose shares a file with authorized layout markup, use a
  documented deterministic text extraction instead of claiming that a whole-file
  hash proves preservation;
- expect pagination and float flow to change after a first-page or layout edit.
  The invariant is protected text/content, not pixel-identical downstream pages.

### Step 1: Verify Prerequisites Portably

Detect the host shell and use its native commands. Do not assume that Bash syntax works in PowerShell or that PowerShell syntax works in Bash.

- Bash-like shells: use `command -v`, `test`, and shell-native path quoting.
- PowerShell: use `Get-Command`, `Test-Path`, and `Get-ChildItem -LiteralPath`.
- Prefer repository scripts when they exist; adapt diagnostic commands to the current shell without changing build semantics.

Verify the resolved compiler/engine, main source, bibliography inputs, section inputs, and figure/table assets. If a required tool is missing, report it and give host-appropriate installation guidance; do not silently switch engines or build systems.

### Step 2: First Compilation Attempt

Run the resolved repository command from the resolved paper directory. If no repository command exists, use the fallback equivalent of:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error MAIN_TEX
```

Use an incremental build first. **Do not run `latexmk -C` by default.** Clean only when stale generated artifacts are shown to cause the failure, record the reason, and verify that the clean target cannot remove source or user-authored assets. Capture output with host-native logging while preserving the compiler's real exit code.

### Step 3: Error Diagnosis and Auto-Fix

If compilation fails, read `compile.log` and fix common errors:

**Missing packages:**
```
! LaTeX Error: File `somepackage.sty' not found.
```
→ Follow the repository's selected TeX distribution and package policy. Use its package
manager only when installation is authorized; otherwise report the missing package. Do
not assume TeX Live/`tlmgr`, switch distributions, or remove a required package merely to
make the build pass.

**Undefined references:**
```
LaTeX Warning: Reference `fig:xyz' on page 3 undefined
```
→ Check `\label{fig:xyz}` exists in the correct figure environment.

**Missing figures:**
```
! LaTeX Error: File `figures/fig1.pdf' not found.
```
→ Check if the file exists with a different extension (.png vs .pdf). Update the `\includegraphics` path.

**Citation undefined:**
```
LaTeX Warning: Citation `smith2024' undefined
```
→ Add the missing entry to `references.bib` or fix the citation key.

**`[VERIFY]` markers in text:**
→ Search for `[VERIFY]` markers left by `/paper-write`. These indicate unverified citations or facts. Search for the correct information or flag to the user.

**Overfull hbox:**
```
Overfull \hbox (12.5pt too wide) in paragraph at lines 42--45
```
→ Diagnose the rendered effect and source cause. Rephrase only when content edits are authorized; for layout-only work, preserve prose and use the repair ladder below or report the unresolved constraint.

**BibTeX errors:**
```
I was expecting a `,' or a `}'---line 15 of references.bib
```
→ Fix BibTeX syntax (missing comma, unmatched braces, special characters in title).

**`\crefname` undefined for custom theorem types:**
→ Ensure `\crefname{assumption}{Assumption}{Assumptions}` and similar are in the preamble after `\newtheorem{assumption}`.

**Float and layout repair ladder:** use the least invasive successful step, rebuild after each step, and stop once the constraint is satisfied.

1. Confirm the actual problem in both the log and rendered page; check the float's width class against `\columnwidth` or `\textwidth` as required by the template.
2. Correct a mismatched float environment, width, or asset bounding box without changing manuscript content.
3. Adjust template-supported placement specifiers and keep the float near its first reference.
4. Move the float source within the surrounding section when this preserves reading order and references.
5. Improve the standalone table/figure geometry under the mandatory publication-layout gate; change caption wording only when explicitly authorized.
6. Use a template-compatible float barrier only when section leakage is the demonstrated cause.
7. Treat manual page breaks, forced placement, negative vertical spacing, and geometry overrides as last resorts requiring a stated reason and neighbor-page verification.

Do not force a float to an exact page unless the user or venue explicitly requires that placement.

### Step 4: Iterative Fix Loop

```
for attempt in 1..MAX_COMPILE_ATTEMPTS:
    compile()
    if success:
        break
    parse_errors()
    auto_fix()
```

For each error:
1. Read the error message from `compile.log`
2. Locate the source file and line number
3. Apply the fix
4. Recompile

### Step 5: Post-Compilation Checks

After successful compilation, verify that the resolved output PDF exists, is nonempty, opens successfully, and has the expected page count. Use host-native file inspection plus `pdfinfo` or an equivalent PDF inspector.

**Integrated visual review (mandatory):**

1. Render every page and inspect an all-page thumbnail/contact sheet for global flow, blank or duplicated pages, float drift, inconsistent density, and reference placement.
2. Render every changed page at readable resolution and inspect it in detail.
3. Also inspect the immediate preceding and following page for each changed page; at document boundaries, inspect the one available neighbor.
4. Check figure labels, table alignment and precision, caption fit, grayscale legibility, margins, headers/footers, section starts, orphaned headings, and visible overfull content.
5. Rebuild and repeat this gate after every layout repair. A successful compiler exit alone is not layout verification.

**Automated checks:**

- [ ] PDF file exists and is > 100KB (not empty/corrupt)
- [ ] Total page count is reasonable (MAX_PAGES + appendix + references)
- [ ] No "??" in the PDF (undefined references — grep the log)
- [ ] No "[?]" in the PDF (undefined citations — grep the log)
- [ ] Figures are rendered (not missing image placeholders)

Search the resolved log with shell-native text search for undefined references, undefined citations, missing assets, and fatal errors. Preserve and report the actual compiler exit code.

### Step 6: Page Count Verification

**CRITICAL**: Verify paper fits within MAX_PAGES.

**For ML conferences (ICLR/NeurIPS/ICML/CVPR/ACL/AAAI):** Main body = first page through end of Conclusion section (not necessarily §5 — could be §6, §7, or §8 depending on structure). References and appendix are NOT counted.

**For IEEE venues:** The TOTAL page count (including references) must fit within the limit. There is no separate "main body" counting — everything up to and including the references counts.

**Precise check:** use `pdftotext` or an equivalent extractor to preserve page boundaries, then locate the actual end of Conclusion and start of References/Bibliography. Run the extraction with host-native piping or temporary-file handling; do not assume a Bash pipeline. Confirm ambiguous headings against the rendered pages.

If Conclusion ends mid-page and References start on the same page, the main body is that page number (e.g., if both are on page 9, main body = ~8.5 pages, which is fine for a 9-page limit since it leaves room for the References header).

If over limit:
- Identify which sections are longest
- Suggest specific cuts (move proofs to appendix, compress tables, tighten writing)
- Report: "Main body is X pages (limit: MAX_PAGES). Suggestion: move [specific content] to appendix."

### Step 6.5: Stale File Detection

Enumerate `.tex` files with host-native file discovery and trace `\input`, `\include`, and repository-defined inclusion macros from the resolved main source. Report unreferenced files as candidates only. Do not delete or rewrite them automatically; they may be intentional alternates or pre-existing user work.

### Step 7: Submission Readiness

For conference submission, additional checks:

- [ ] **Anonymous**: no author names, affiliations, or self-citations that reveal identity
- [ ] **Page limit**: main body within MAX_PAGES (to end of Conclusion)
- [ ] **Font embedding**: inspect the resolved PDF with `pdffonts` or an equivalent tool and confirm every required font is embedded
- [ ] **No supplementary mixed in**: appendix clearly after `\newpage\appendix`
- [ ] **File size**: reasonable (< 50MB for most venues, < 10MB preferred)
- [ ] **No `[VERIFY]` markers**: search the PDF text for leftover markers

### Step 7.5: Deliver the Verified Artifact

The verified build output is the source of truth. If the final PDF is copied or renamed for delivery, compute a cryptographic hash (prefer SHA-256) for both the verified output and delivered file and require exact equality. A successful copy command or equal file size is not sufficient. Report both resolved paths and hashes; if they differ, do not present the delivered file as verified.

### Step 7.6: Mirror Submission Metadata When Applicable

Run this gate only when the user is preparing a portal submission and provides,
or the project explicitly designates, a local submission-fields artifact.

- Compare title, abstract, keywords, track, and author order against the
  canonical source using documented whitespace/line-break normalization. Do not
  silently normalize punctuation, wording, or keyword order.
- Keep personal portal metadata local unless the user explicitly authorizes
  publishing it.
- If the portal offers the uploaded PDF for download, hash the downloaded copy
  against the verified local delivery. A submission ID or timestamp proves that
  an event occurred; it does not prove which bytes or metadata were accepted.
- If the portal cannot be read back, report that limitation instead of claiming
  an end-to-end mirror check.

### Step 8: Output Summary

```markdown
## Compilation Report

- **Status**: SUCCESS / FAILED
- **Resolved build command**: [repository command or fallback]
- **Verified PDF**: [resolved output path]
- **Delivered PDF**: [same path or copied/renamed path]
- **Verified/delivered SHA-256**: [hash] / [hash; must match]
- **Pages**: X (main body to Conclusion) + Y (references) + Z (appendix)
- **Within page limit**: YES/NO (MAX_PAGES = N)
- **Errors fixed**: [list of auto-fixed issues]
- **Warnings remaining**: [list of non-critical warnings]
- **Undefined references**: 0
- **Undefined citations**: 0
- **Layout pages inspected**: all-page thumbnails + changed pages [list] + neighbors [list]
- **Content-preservation audit**: NOT APPLICABLE / PASSED / FAILED [method and scope]

### Next Steps
- [ ] Review any explicitly reported visual or content-preservation exceptions
- [ ] Run `/paper-write` to fix any content issues
- [ ] Submit to [venue] via OpenReview / CMT / HotCRP
```

## Key Rules

- **Never delete the user's source files** — only modify authorized files to fix errors or requested layout
- **Never rephrase manuscript text during layout-only work** — request explicit scope expansion first
- **Keep compile.log** — useful for debugging
- **Don't suppress warnings** — report them, let the user decide
- **If LaTeX is not installed**, provide clear installation instructions rather than failing silently
- **Font embedding is critical** — some venues reject PDFs with non-embedded fonts
- **Page count rules differ by venue** — ML conferences: main body to Conclusion (refs excluded). **IEEE venues: total pages including references.**

## Common Venue Requirements

| Venue | Style File | Citation | Page Limit | Refs in limit? | Submission |
|-------|-----------|----------|------------|----------------|------------|
| ICLR 2026 | `iclr2026_conference.sty` | `natbib` (`\citep`/`\citet`) | 9 pages (to Conclusion end) | No | OpenReview |
| NeurIPS 2026 | `neurips_2026.sty` | `natbib` (`\citep`/`\citet`) | 9 pages (to Conclusion end) | No | OpenReview |
| ICML 2026 | `icml2026.sty` | `natbib` (`\citep`/`\citet`) | 8 pages (to Conclusion end) | No | OpenReview |
| IEEE Journal | `IEEEtran.cls` [journal] | `cite` (`\cite{}`, numeric) | ~12-14 pages (Transactions) / ~4-5 (Letters) | **Yes** | IEEE Author Portal / ScholarOne |
| IEEE Conference | `IEEEtran.cls` [conference] | `cite` (`\cite{}`, numeric) | 5-8 pages (varies by conf) | **Yes** | EDAS / IEEE Author Portal |
