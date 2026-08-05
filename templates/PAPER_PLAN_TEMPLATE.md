# Paper Plan

> **Template for Workflow 3 — skip planning phase.** Fill in, then run `/paper-writing "PAPER_PLAN.md"`. An existing plan may skip Phase 1 only after it satisfies the canonical Claim Ledger, Front-Matter Coverage Index, and Figure/Table Layout Contract below. Migrate a legacy plan into these contracts before treating it as complete.

## Metadata
- **Title**: [Title]
- **Venue**: [ICLR / NeurIPS / ICML]
- **One-sentence contribution**: [Core takeaway]

## Canonical Claim Ledger
| Claim ID | Role | Exact claim | Comparator or N/A | Evidence (experiment/table/figure/theorem/proof) | Scope/data access | Selection/training/adaptation or N/A | Limitation | Forbidden expansion |
|---|---|---|---|---|---|---|---|---|
| C1 | [primary] | [Exact sentence-level claim] | [Comparator or N/A] | [semantic figure/table label, result file, or analysis] | [dataset, split, population, and what data the method may access] | [what is trained, development-selected, calibrated, adapted, or N/A] | [boundary of the supported claim] | [stronger wording that the evidence does not support] |
| C2 | [supporting] | [Exact sentence-level claim] | [Comparator or N/A] | [semantic evidence link] | [scope and data-access boundary] | [selection/training/adaptation boundary or N/A] | [known limitation] | [forbidden extrapolation] |

## Front-Matter Coverage Index
| Claim ID | Abstract move | Intro bullet | Body subsection | Evidence location | Conclusion sentence |
|---|---|---|---|---|---|
| C1 | [problem/method/evidence/takeaway] | [bullet number] | [section/subsection] | [tab:primary or fig:overview] | [mirrored, scope-aware sentence] |
| C2 | [move or N/A] | [bullet number] | [section/subsection] | [semantic evidence label] | [mirrored sentence or N/A] |

## Section Plan

### 1. Introduction (~1.5 pages)
- **What**: [contribution]
- **Why**: [importance]
- **How**: [approach]
- **Result**: [strongest number]

### 2. Related Work (~1 page)
- [Group 1]: [papers, gap]
- [Group 2]: [papers, gap]

### 3. Method (~2 pages)
- [Problem formulation]
- [Proposed approach]

### 4. Experiments (~3 pages)
- [Setup, main results, ablation]

### 5. Conclusion (~0.5 pages)
- [Summary, limitations, future]

## Figure/Table Layout Contract
| Label | Kind | Width class | Preferred placement | Must preserve | Caption budget | Priority |
|---|---|---|---|---|---|---|
| fig:overview | figure* | double column | near first method discussion | [module order and readable labels at final size] | 2–3 lines | primary |
| fig:main_results | figure | single column | near the claim it supports | [metric direction, uncertainty, and comparator identity] | 1–2 lines | secondary |
| tab:primary | table | single column | before secondary diagnostics | [metric, protocol, grouping, units, and tie-aware emphasis] | 1–2 lines | primary |

## Key References
1. [Author et al., "Title", Venue Year]
2. [...]
