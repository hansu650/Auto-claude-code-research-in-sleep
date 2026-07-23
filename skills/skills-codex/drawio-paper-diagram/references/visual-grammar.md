# Visual Grammar for Academic Draw.io Figures

Use these principles as a reference-derived visual grammar. Do not bind the figure to a particular paper, palette, or copied layout.

## Start from the scientific story

Write one sentence before drawing:

`input -> problem or operation -> proposed mechanism -> output`

If this sentence is unclear, refine the scientific narrative before arranging shapes.

## Prefer explanatory objects

Represent the domain directly:

- time series as curves;
- spatial support as grids or highlighted cells;
- anomaly intervals as bands;
- token membership as cells and incidence links;
- temporal ownership as columns or timestamp markers;
- score fields as heatmaps;
- aggregation as a visible merge or a nearby equation.

Avoid replacing every concept with an identical rounded rectangle.

## Keep one primary route

Use a single dominant left-to-right or top-to-bottom flow. Place auxiliary paths above or below it, draw them more lightly, and merge them cleanly. Avoid crossings and backward jumps.

Every connector must have an interpretable source, target, direction, and operation.

## Give each panel one job

Useful panel roles include:

- prior paradigm;
- concrete limitation;
- proposed conceptual change;
- full system overview;
- one-module overview;
- one worked local example.

Do not make one panel explain the literature, full architecture, derivation, and results simultaneously.

## Separate overview from detail

For a module-detail figure:

1. Show `visual input -> module -> visual output` in the overview.
2. Select one target position in the detail panel.
3. Show the relevant membership or ownership objects.
4. Place the key equation beside the operation.
5. Show the value written or projected to the output.

Use no more than one core equation in the overview. Keep only equations that advance the worked example in the detail panel.

## Establish hierarchy without decoration

- Make the primary flow darkest or most prominent.
- Distinguish input, intermediate representation, proposed operation, and output.
- Use the same style for the same semantic role throughout the figure.
- Use two to four accent roles when possible, but inherit the project's palette.
- Avoid gradients, glow, large shadows, decorative icons, and excessive rounding.
- Keep labels short and preferably on one line.

## Preserve continuity

Repeated visual objects must remain recognizable. If the input is a particular waveform, rolling windows and encoder examples should look derived from it. If a target cell is orange, use that target color consistently through lookup, aggregation, and write-back.

## Pass the novice-reader gate

At final paper scale, verify:

1. A reader can find input, output, and the proposed module in five seconds.
2. A reader can trace the main flow in thirty seconds.
3. A reader can explain the purpose of each proposed module without reading the full method section.
4. A reader can point from every equation to the visual object it describes.
5. Removing a label would not make an unlabeled decorative object scientifically ambiguous.

If the gate fails, simplify the layout or replace prose with a concrete visual example.
