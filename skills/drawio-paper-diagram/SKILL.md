---
name: drawio-paper-diagram
description: Create or patch editable publication-quality Draw.io method, architecture, workflow, motivation, and module-detail diagrams with true MathJax labels, vector-only assets, reference-guided visual storytelling, and source-level validation. Use when a user requests a .drawio file, asks to modify an existing Draw.io paper figure, requires LaTeX mathematics inside Draw.io, or needs an editable academic diagram. Do not use for empirical plots, ablation charts, or LaTeX tables; route those to paper-figure.
---

# Draw.io Paper Diagram

Create editable academic diagrams whose scientific story remains understandable to a reader without prior knowledge of the method.

## Route the task

- Use this skill for `.drawio` architecture, method, motivation, workflow, and module-detail figures.
- Use `figure-spec` when deterministic JSON-to-SVG output is preferred over Draw.io editing.
- Use `paper-figure` for empirical plots, ablation charts, measured heatmaps, and LaTeX tables. Schematic score-field heatmaps inside a method diagram remain in this skill.
- Use `paper-illustration` for natural or conceptual artwork that is not a structured technical diagram.

## Establish the figure contract

Before creating a new figure or materially restructuring one, determine:

1. The user-confirmed source `.drawio` file, if one exists.
2. Whether the figure is an evidence figure or a schematic illustration.
3. Its paper role: context, problem motivation, full architecture, or module detail.
4. Its intended paper width and required output files.
5. A one-sentence story in the form `input -> problem/operation -> proposed mechanism -> output`.

Do not draw until the one-sentence story is coherent. Preserve the aspect ratio unless the user explicitly requests a redesign. For a small targeted patch such as changing a color, moving one label, or repairing one connector, apply the patch directly and retain the existing contract.

## Preserve the editable source

- Treat the user-confirmed `.drawio` as the source of truth.
- Patch existing cells when the user has manually arranged the figure; do not regenerate or overwrite the composition.
- Keep stable, descriptive cell IDs and explicit geometries.
- Version the source before material restructuring only when the user requests a version or overwrite risk is material; do not create unsolicited duplicate files for a small patch.
- Modify or export only the artifacts requested by the user.
- Name imported SVG assets by figure and purpose, such as `fig3_encoder_large_scale_waveform.svg`.

## Design for a novice reader

Read [references/visual-grammar.md](references/visual-grammar.md) before creating or materially restructuring a figure.

Require all three comprehension gates:

- **5 seconds:** identify the input, output, and proposed module.
- **30 seconds:** trace the primary data flow and state what each proposed module does.
- **2 minutes:** connect each visual example to its nearby equation or operation.

Use domain objects before generic boxes: curves for time series, grids for spatial support, bands for intervals, columns for ownership, and heatmaps for score fields. Show concrete input and output visuals whenever possible. Give each panel one question to answer. Keep one dominant reading direction and move auxiliary paths above or below it.

Write a method acronym with a short functional gloss on first appearance, for example `IHP` with `recover base-grid support`. Use only the acronym thereafter.

## Use true LaTeX mathematics

Read [references/drawio-math.md](references/drawio-math.md) whenever the figure contains variables, dimensions, sets, or equations.

- Set `math="1"` on every relevant `mxGraphModel`.
- Put mathematical content in `\(...\)` or `\[...\]`.
- Keep method names, ordinary prose, and subfigure labels as normal text.
- Do not fake mathematics with HTML `<sub>`/`<sup>`, plain Unicode operators, or upright Arial variables.
- Place an equation beside the operation it explains; do not collect unrelated equations at the bottom.
- Use at most one core equation in an overview panel. Use additional equations only in the detailed panel and pair them with visible objects.

## Build semantically

- Make every box, grid, arrow, color, and equation correspond to an actual operation or representation.
- Remove decorative matrices, token bars, and arrows that lack a defined meaning.
- Keep the primary flow visually stronger than auxiliary paths.
- Use thin connectors and small arrowheads.
- Avoid crossings and never run a connector through a label, equation, or module.
- Verify exact grid dimensions and scale relationships; never infer `3x3` when the method requires `4x4`.
- Keep repeated inputs, waveforms, and score fields visually consistent across the figure.
- Use color to encode meaning, not decoration. Inherit the current figure or reference palette instead of imposing a fixed palette.

## Protect evidence integrity

- In **evidence mode**, reproduce values and geometry from result artifacts exactly. Never improve, suppress, or fabricate results for visual appeal.
- In **schematic mode**, simplify shapes or curves only to explain the mechanism. Do not present schematic values as measured evidence.
- Learn composition and visual grammar from references, but do not copy their scientific content, embedded screenshots, or plotted values.

## Keep assets vector

- Prefer Draw.io primitives and SVG assets.
- Do not use PNG/JPEG screenshots as final paper objects.
- Reject SVG files that embed raster images.
- Preserve SVG aspect ratios.
- Move mathematical labels out of imported SVGs into Draw.io MathJax labels when practical.

## Validate and review

Run the bundled source-level audit after each material edit:

```bash
python "$CLAUDE_SKILL_DIR/scripts/audit_drawio.py" path/to/figure.drawio --require-math
```

If `CLAUDE_SKILL_DIR` is unavailable, resolve the script from the absolute directory of the selected `SKILL.md`. Common fallbacks are `skills/drawio-paper-diagram/scripts/audit_drawio.py`, `skills/skills-codex/drawio-paper-diagram/scripts/audit_drawio.py`, and `~/.codex/skills/drawio-paper-diagram/scripts/audit_drawio.py`. Do not assume that the current working directory is the skill directory.

Omit `--require-math` only when the figure truly contains no mathematical content. Add `--strict` before final delivery to make warnings fail the audit.

The source audit does not render MathJax or prove final page bounds. Render one preview when a Draw.io exporter is available. Otherwise ask the user to open the source and provide a screenshot for visual review. Check:

- clipping, overlaps, unexpected wrapping, and excessive empty space;
- connector direction, crossings, and arrowhead size;
- exact grid dimensions and consistent repeated assets;
- readable labels at final paper scale;
- formulas placed beside their corresponding objects;
- no unintended edits to the user's manual arrangement.

Do not impose a multi-round audit on a small targeted correction; one source audit and one focused visual check are sufficient.

## Deliver cleanly

- Deliver only the requested `.drawio`, SVG, or PDF files.
- Keep previews, logs, and temporary renders outside the final figure directory or under `_work/`.
- Do not create placement READMEs unless requested.
- Do not compile the paper or combine PDFs unless requested.
- Before removing an asset, confirm that no current Draw.io file references it.
