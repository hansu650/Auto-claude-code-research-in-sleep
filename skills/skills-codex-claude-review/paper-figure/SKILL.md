---
name: "paper-figure"
description: "Create or revise standalone publication-quality paper figures and tables from plans, data, or existing artifacts. Use for plots, comparison and ablation tables, multi-panel figures, diagrams, captions, table typography, and standalone figure/table layout; common requests include 画图, 画表, 改表格, paper figures, and redesign this table. In a new or context-free folder, inspect local artifacts first and request only missing blocking input."
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

# Paper Figure: Publication-Quality Plots from Experiment Data

<!-- BEGIN ARIS NEUTRAL: COLD START -->
## Cold-Start Behavior

Do not depend on prior chat or a pre-existing project narrative. First inspect the current directory for a paper plan, manuscript sources, result files, existing figures or tables, and venue instructions. If these artifacts are sufficient, proceed from them. If a required input is missing, ask only for the smallest blocking input and still provide a safe scaffold where possible. Keep all assumptions project-neutral; never import names, numbers, protocols, or design choices from another paper.
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

<!-- BEGIN ARIS NEUTRAL: PUBLICATION LAYOUT -->
## Publication Layout Gate

Read and follow [`publication-layout-gates.md`](../shared-references/publication-layout-gates.md) whenever planning, generating, revising, or validating a paper figure or table. This skill owns the standalone artifact gate: inspect the rendered figure or table at its intended final physical size without requiring a manuscript build. Record width class and dimensions; verify table header spans, three-line rule continuity, numeric alignment, declared metric direction and tie-aware highlighting, the ordered width-compression ladder, grayscale readability, and non-red/green semantics. Leave integrated-page validation to `paper-compile` and report it as pending when no compiled manuscript exists.
<!-- END ARIS NEUTRAL: PUBLICATION LAYOUT -->

Generate all figures and tables for a paper based on: **$ARGUMENTS**

## Scope: What This Skill Can and Cannot Do

| Category | Can auto-generate? | Examples |
|----------|-------------------|----------|
| **Data-driven plots** | ✅ Yes | Line plots (training curves), bar charts (method comparison), scatter plots, heatmaps, box/violin plots |
| **Comparison tables** | ✅ Yes | LaTeX tables comparing prior bounds, method features, ablation results |
| **Multi-panel figures** | ✅ Yes | Subfigure grids combining multiple plots (e.g., 3×3 dataset × method) |
| **Architecture/pipeline diagrams** | Route to a dedicated diagram skill | Use `drawio-paper-diagram`, `figure-spec`, or another available publication-diagram workflow; otherwise provide an editable skeleton and state the limitation |
| **Generated image grids** | ❌ No — manual | Grids of generated samples (e.g., GAN/diffusion outputs). These come from running your model, not from this skill |
| **Photographs / screenshots** | ❌ No — manual | Real-world images, UI screenshots, qualitative examples |

**In practice:** This skill owns data plots, tables, multi-panel assembly, and the standalone artifact gate. For architecture, pipeline, or illustrative figures, route to the available dedicated diagram/image skill and then validate the returned artifact here. Preserve existing user-created artifacts.
<!-- BEGIN ARIS NEUTRAL: DIAGRAM BACKENDS -->
### Diagram Backend Routing Contract

When the arguments include `diagram-backend: <value>`, use exactly one mapping
for the requested semantic label:

| Value | Delegate once to |
|---|---|
| `figurespec` | `figure-spec` |
| `drawio` | `drawio-paper-diagram` |
| `gemini` | `paper-illustration` |
| `codex-image2` | `paper-illustration-image2` |
| `mermaid` | `mermaid-diagram` |
| `manual` or `false` | do not generate; inspect the supplied artifact |

The handoff must include the semantic label, a locally grounded content brief, width
class, required preserved details, caption budget, and expected editable/rendered output
paths. A backend owns generation only. After it returns, resume this skill and run the
mandatory standalone artifact gate on the returned or manually supplied artifact. Backend
success alone is never completion.

Do not call multiple backends for the same label unless the user explicitly asks for
alternatives. If a requested backend is unavailable, use another mapping only with a
documented reason and no semantic change; otherwise request the smallest blocking input.
For `manual` or `false`, a missing artifact blocks only that label and requires
the smallest missing source; an existing artifact still must pass the same standalone
gate.
<!-- END ARIS NEUTRAL: DIAGRAM BACKENDS -->

## Constants

- **STYLE = `publication`** — Visual style preset. Options: `publication` (default, clean for print), `poster` (larger fonts), `slide` (bold colors)
- **DPI = 300** — Output resolution
- **FORMAT = `pdf`** — Output format. Options: `pdf` (vector, best for LaTeX), `png` (raster fallback)
- **COLOR_PALETTE = `tab10`** — Default matplotlib color cycle. Options: `tab10`, `Set2`, `colorblind` (deuteranopia-safe)
- **FONT_SIZE = 10** — Base font size (matches typical conference body text)
- **FIG_DIR = `figures/`** — Output directory for generated figures
- **REVIEWER_MODEL = `claude-review`** — Claude reviewer invoked through the local `claude-review` MCP bridge. Set `CLAUDE_REVIEW_MODEL` if you need a specific Claude model override.

## Inputs

1. **PAPER_PLAN.md** — Figure/Table Layout Contract (from `/paper-plan`)
2. **Experiment data** — JSON files, CSV files, or screen logs in `figures/` or project root
3. **Existing figures** — any manually created figures to preserve

If `PAPER_PLAN.md` is absent, inspect the request, manuscript, data, and existing artifacts.
Proceed when the intended figure or table can be inferred; ask only for the smallest
blocking target or data description when it cannot.

## Workflow

### Step 1: Read the Figure/Table Layout Contract

Parse the Figure/Table Layout Contract from PAPER_PLAN.md:

```markdown
| Label | Kind | Width class | Preferred placement | Must preserve | Caption budget | Priority |
|---|---|---|---|---|---|---|
| fig:overview | figure* | double column | near first discussion | readable overview at final size | 2-3 lines | primary |
| tab:primary | table | single column | before secondary diagnostics | metric, protocol, grouping, units | 1-2 lines | primary |
```

Read each row together with its data source and Claim ID/evidence link in the plan.

Identify:
- Which figures can be auto-generated from data
- Which require a dedicated diagram/image skill and return here for artifact validation
- Which are tables (generate as separate LaTeX publication artifacts, not figures)

### Step 2: Set Up Plotting Environment

Create a shared style configuration script:

```python
# paper_plot_style.py — shared across all figure scripts
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'font.size': FONT_SIZE,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE + 1,
    'xtick.labelsize': FONT_SIZE - 1,
    'ytick.labelsize': FONT_SIZE - 1,
    'legend.fontsize': FONT_SIZE - 1,
    'figure.dpi': DPI,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'text.usetex': False,  # set True if LaTeX is available
    'mathtext.fontset': 'stix',
})

# Color palette
COLORS = plt.cm.tab10.colors  # or Set2, or colorblind-safe

def save_fig(fig, name, fmt=FORMAT):
    """Save figure to FIG_DIR with consistent naming."""
    fig.savefig(f'{FIG_DIR}/{name}.{fmt}')
    print(f'Saved: {FIG_DIR}/{name}.{fmt}')
```

### Step 3: Auto-Select Figure Type

Use this decision tree for data-driven figures (inspired by Imbad0202/academic-research-skills):

| Data Pattern | Recommended Type | Default Width Class |
|-------------|-----------------|------|
| X=time/steps, Y=metric | Line plot | single column |
| Methods × 1 metric | Bar chart | single column |
| Methods × multiple metrics | Grouped bar / radar | double column |
| Two continuous variables | Scatter plot | single column |
| Matrix / grid values | Heatmap | single column |
| Distribution comparison | Box/violin plot | single column |
| Multi-dataset results | Multi-panel (subfigure) | double column |
| Prior work comparison | LaTeX table | choose from column count |

### Step 4: Generate Each Figure

For each figure in the plan, create a standalone Python script:

**Line plots** (training curves, scaling):
```python
# gen_fig2_training_curves.py
from paper_plot_style import *
import json

with open('figures/exp_results.json') as f:
    data = json.load(f)

fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))
ax.plot(data['steps'], data['fac_loss'], label='Factorized', color=COLORS[0])
ax.plot(data['steps'], data['crf_loss'], label='CRF-LR', color=COLORS[1])
ax.set_xlabel('Training Steps')
ax.set_ylabel('Cross-Entropy Loss')
ax.legend(frameon=False)
save_fig(fig, 'fig2_training_curves')
```

**Bar charts** (comparison, ablation):
```python
fig, ax = plt.subplots(1, 1, figsize=(5, 3))
methods = ['Baseline', 'Method A', 'Method B', 'Ours']
values = [82.3, 85.1, 86.7, 89.2]
bars = ax.bar(methods, values, color=[COLORS[i] for i in range(len(methods))])
ax.set_ylabel('Accuracy (%)')
# Add value labels on bars
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontsize=FONT_SIZE-1)
save_fig(fig, 'fig3_comparison')
```

**Comparison tables** (LaTeX, for theory papers; apply the canonical table-construction and highlighting rules):
```latex
\begin{table}[t]
\centering
\caption{Comparison of estimation error bounds. $n$: sample size, $D$: ambient dim, $d$: latent dim, $K$: subspaces, $n_k$: modes.}
\label{tab:bounds}
\begin{tabular}{lccc}
\toprule
Method & Rate & Depends on $D$? & Multi-modal? \\
\midrule
\citet{MinimaxOkoAS23} & $n^{-s'/D}$ & Yes (curse) & No \\
\citet{ScoreMatchingdistributionrecovery} & $n^{-2/d}$ & No & No \\
Proposed method & $\sqrt{\sum n_k d_k / n}$ & No & Yes \\
\bottomrule
\end{tabular}
\end{table}
```

**Architecture/pipeline diagrams** (delegated artifact path):
- Route to a dedicated publication-diagram skill when one is available; preserve its editable source plus rendered output
- If no such capability is available, provide an editable TikZ/Draw.io specification or skeleton and state what remains unresolved
- If the figure already exists, preserve it and validate the rendered output at its declared final size
- Return the completed artifact to this skill's standalone gate before generating the LaTeX include

### Step 5: Run All Scripts

```bash
# Run all figure generation scripts
for script in gen_fig*.py; do
    python "$script"
done
```

Verify all output files exist and are non-empty. Then **render-then-verify**:
re-open each RENDERED PDF/PNG (not the script) and self-check — no clipped
labels, no legend covering data, every number/label readable at final print
size. This self-check happens BEFORE the Step 7 review, so the reviewer's
budget goes to substance, not to catching clipped axes.

### Step 6: Generate LaTeX Include Snippets

For each figure, output the LaTeX code to include it:

```latex
% === Fig 2: Training Curves ===
\begin{figure}[t]
    \centering
    \includegraphics[width=\columnwidth]{figures/fig2_training_curves.pdf}
    \caption{Training curves comparing factorized and CRF-LR denoising.}
    \label{fig:training_curves}
\end{figure}
```

Save all snippets to `figures/latex_includes.tex` for easy copy-paste into the paper.

### Step 7: Figure Quality Review with REVIEWER_MODEL

Send figure descriptions and captions to Claude for review:

```
mcp__claude-review__review_start:
  prompt: |
    Review these figure/table plans for a [VENUE] submission.

    For each figure:
    1. Is the caption informative and self-contained?
    2. Does the figure type match the data being shown?
    3. Is the comparison fair and clear?
    4. Any missing baselines or ablations?
    5. Would a different visualization be more effective?

    [list all figures with captions and descriptions]
```

After this review call, immediately save the returned `jobId` and poll `mcp__claude-review__review_status` with a bounded `waitSeconds` until `done=true`. A terminal payload is usable only when `status` is exactly `completed`, `error` is empty, and `response` is a non-empty string. Only then treat `response` as reviewer output and save the completed `threadId` for a follow-up round. Otherwise record `REVIEW_UNAVAILABLE` / `BLOCKED`, preserve the error in the trace, and do not record an `accepted` review.

### Step 8: Quality Checklist

The checklist is PARTITIONED (pattern from Anthropic's Claude Science
`figure-style` skill, Apache-2.0): **correctness rules always bind** — they are
about whether the figure tells the truth, have no aesthetic content, and no
style choice may override them; **guidance rules are defaults** — they produce
a clean result, but a deliberate, stated alternative may override them.

**Correctness — always binds, verify against the DATA before the render:**

- [ ] **Excluded data never enters summaries** — a row excluded/flagged in the
      source either disappears entirely or is drawn visibly distinct (open /
      hatched marker, named in the key); it never feeds a mean/CI plotted
      alongside included rows
- [ ] **Captions and any claim-like title text are tested against EVERY plotted
      row** — if one category contradicts the claim, qualify it ("on 3 of 4
      benchmarks") or downgrade to a description; a figure that overclaims is
      wrong even if it renders beautifully
- [ ] **Comparable conditions only** — arms measured under different N / budget
      / protocol are not drawn as visual peers; separate them or mark the
      difference in the caption
- [ ] **State n and what was held fixed** — every panel with a summary mark
      says n and the unit of replication (panel or caption)
- [ ] **Render-then-verify** — the Step-5 self-check on the RENDERED PDF/PNG
      (not the script) actually happened: no clipped labels, no legend covering
      data, every number/label readable at final print size

**Guidance — strong defaults (from pedrohcgs/claude-code-my-workflow), a
deliberate stated alternative may override — EXCEPT items that Key Rules below
make hard (vector-PDF output and no-titles-inside-figures are Key Rules: treat
those two as binding, not overridable):**

- [ ] Font size readable at printed paper size (not too small)
- [ ] Colors distinguishable in grayscale (print-friendly)
- [ ] **No title inside figures** — titles go only in LaTeX `\caption{}` (from pedrohcgs)
- [ ] Legend does not overlap data
- [ ] Axis labels have units where applicable
- [ ] Axis labels are publication-quality (not variable names like `emp_rate`)
- [ ] Width matches the declared class: `\columnwidth` for single-column or `\textwidth` for double-column output
- [ ] PDF output is vector (not rasterized text)
- [ ] No matplotlib default title (remove `plt.title` for publications)
- [ ] Serif font matches paper body text (Times / Computer Modern)
- [ ] Colorblind-accessible (if using colorblind palette)

## Output

```
figures/
├── paper_plot_style.py          # shared style config
├── gen_fig1_architecture.py     # per-figure scripts
├── gen_fig2_training_curves.py
├── gen_fig3_comparison.py
├── fig1_architecture.pdf        # generated figures
├── fig2_training_curves.pdf
├── fig3_comparison.pdf
├── latex_includes.tex           # LaTeX snippets for all figures
└── TABLE_*.tex                  # standalone table LaTeX files
```

## Key Rules

- **Every figure must be reproducible** — save the generation script alongside the output
- **Do NOT hardcode data** — always read from JSON/CSV files
- **Use vector format (PDF)** for all plots — PNG only as fallback
- **No decorative elements** — no background colors, no 3D effects, no chart junk
- **Consistent style across all figures** — same fonts, colors, line widths
- **Colorblind-safe** — verify with https://davidmathlogic.com/colorblind/ if needed
- **One script per figure** — easy to re-run individual figures when data changes
- **No titles inside figures** — captions are in LaTeX only
- **Tables are first-class artifacts, not figures** — generate standalone `.tex` sources and validate their renders when available

## Figure Type Reference

| Type | When to Use | Default Width Class |
|------|------------|--------------|
| Line plot | Training curves, scaling trends | single column |
| Bar chart | Method comparison, ablation | single column |
| Grouped bar | Multi-metric comparison | double column |
| Scatter plot | Correlation analysis | single column |
| Heatmap | Attention, confusion matrix | single column |
| Box/violin | Distribution comparison | single column |
| Architecture | System overview | double column |
| Multi-panel | Combined results (subfigures) | double column |
| Comparison table | Prior bounds vs. ours (theory) | choose from column count |

## Acknowledgements

Design pattern (type × style matrix) inspired by [baoyu-skills](https://github.com/jimliu/baoyu-skills). Publication style defaults and figure rules from [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow). Visualization decision tree from [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills).
