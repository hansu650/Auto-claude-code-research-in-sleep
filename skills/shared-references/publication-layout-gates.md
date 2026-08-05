# Publication Layout Gates

Use this reference whenever planning, producing, or integrating a publication figure or table. It is the canonical source for width, caption, highlighting, compression, and visual-validation rules. Tables are first-class publication artifacts; they are not figures.

## Ownership

- `paper-plan` records the intended layout contract.
- `paper-figure` owns the **standalone artifact gate**: validate the rendered figure or table before manuscript integration. A paper draft is not required.
- `paper-compile` owns the **integrated-page gate**: validate the object at its final embedded size, its target page, and both neighboring pages.

Passing the standalone gate does not imply that the integrated page passes.

## Figure/Table Layout Contract

Record one row per planned object:

```markdown
| Label | Kind | Width class | Preferred placement | Must preserve | Caption budget | Priority |
|---|---|---|---|---|---|---|
| fig:overview | figure* | double column | near first discussion | readable core labels | 2–3 lines | primary |
| tab:primary | table | single column | before secondary diagnostics | three-line style | 1–2 lines | primary |
```

Use `\columnwidth` for single-column objects and `\textwidth` for double-column objects. Caption budgets are advisory: never remove a metric, essential protocol detail, abbreviation definition, or conditionality needed for self-contained interpretation. Specify an exact page only when the user or venue requires it; otherwise prefer proximity to the first reference and stable source order.

Do not infer displayed Figure or Table numbers from historical filenames. Use semantic `\label` keys and `\ref` references.

## Table Construction

- Default to venue-compatible `booktabs` three-line style: `\toprule`, `\midrule`, and `\bottomrule`. Do not add vertical rules or an outer box unless the venue requires them.
- Use `\multicolumn` for grouped headers and `\cmidrule(lr){a-b}` with the exact column span. A gap in a rule must represent intentional grouping, not accidental broken alignment.
- Align numeric columns by decimal point when practical. Keep signs, decimal precision, interval notation, and units consistent within a column.
- Keep captions compact and self-contained. Define the metric, essential protocol, abbreviations, and any conditional interpretation.
- Put primary evidence before legacy or secondary diagnostics unless the paper's argument requires another order.
- Inspect formulas inside cells for clipping, uneven baselines, and collisions with horizontal rules.

## Semantic Highlighting

- Declare each metric's optimization direction and the tie rule before highlighting results.
- Do not highlight a row merely because it is labeled as the proposed method or “Ours.”
- Prefer venue-compatible non-color cues such as bold or underline. Optional light grayscale shading may support them, but color must not be the only signal.
- Avoid red/green comparison coding. The result must remain understandable in grayscale and for readers with common color-vision deficiencies.
- Emphasize one primary conclusion or a small set of key cells per panel, not every favorable value.
- Check every highlighted cell against the source data and the declared tie rule.

## Width Compression Ladder

When a table is too wide, apply these fixes in order:

1. remove caption prose that belongs in the main text;
2. shorten repeated headers and define abbreviations;
3. remove low-priority columns or split a secondary panel;
4. reduce `\tabcolsep` conservatively;
5. use the smallest venue-permitted font;
6. change to a double-column table;
7. use `\resizebox` only as a last resort, then re-check the embedded text size.

If vertical density is the problem, adjust row padding or `\arraystretch` separately. `\arraystretch` is not a width fix. Do not shrink a user-locked core figure to solve an unrelated page-layout problem.

## Standalone Artifact Gate

Render and inspect the actual output artifact, not only its source or generation script.

For every figure:

- inspect it at the intended final physical size;
- verify that labels, legends, markers, line styles, and uncertainty indicators remain readable;
- check clipping, overlap, occlusion, unexpected rasterization, and truncated axes or nonzero baselines;
- ensure that color is not the only carrier of meaning and that the artifact remains legible in grayscale;
- confirm that caption terms and semantic labels match the plotted data.

For every table:

- inspect both the source and a standalone render when rendering is available;
- verify grouped-header spans and horizontal-rule continuity;
- check numeric alignment, signs, precision, intervals, units, and formula baselines;
- confirm that semantic emphasis matches the declared optimization direction and tie rule;
- verify readability at the intended final physical size, in grayscale, without relying on red/green distinctions.

Record the intended width class and the rendered dimensions used for the check. If no manuscript exists yet, stop after this gate and clearly state that integrated-page validation remains pending.

## Integrated-Page Gate

After compilation, inspect:

- the object at final embedded size;
- the full target page;
- both neighboring pages;
- all-page thumbnails for global reflow and accidental float movement.

Check for clipping, overlap, formula/table collisions, column drift, unreadable reduction, caption overflow, abnormal whitespace, and float reordering across important section boundaries. Re-run the standalone gate if integration required resizing or redesign.

## Completion Evidence

A layout check is complete only when it reports:

- the artifact path and source-data path;
- the intended width class and final inspected size;
- whether standalone rendering was inspected;
- whether grayscale and non-red/green checks passed;
- for tables, whether header spans, rule continuity, numeric alignment, and highlighting rules passed;
- whether integrated-page validation passed or remains pending.
