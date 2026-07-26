# Method Patterns

Write Method in the order required to understand the computation. Keep the figure hierarchy and prose dependency chain consistent.

## Use dual navigation

Let figures provide top-down navigation:

`system -> module -> operator`

Let prose provide dependency-driven navigation:

`representation -> operation -> handoff -> composition -> output`

The reader should be able to enter through either path and reach the same method.

## Recommended subsection order

Adapt this topology to the actual method:

1. **Problem Setup and Design Requirements**
2. **Overall Pipeline or End-to-End Overview**
3. **Representation or Module I**
4. **Operator or Module II**
5. **End-to-End Composition**, when aggregation across windows, scales, boundaries, or stages is nontrivial

Do not add subsections without a distinct dependency or reviewer question.

## State the change boundary

In the overview, distinguish:

- inherited or frozen components;
- reused representations or cached evidence;
- modified interfaces;
- new modules;
- final outputs.

This prevents the reader from attributing the whole upstream system to the paper.

## Use the module contract

Explain every module through five answers:

1. **Why:** Which concrete failure or requirement makes it necessary?
2. **Input:** What tensor, set, field, sequence, or graph enters?
3. **Operation:** What transformation is applied?
4. **Output:** What object leaves, including shape and meaning?
5. **Handoff:** Which next module consumes that exact object?

An equivalent compact contract is:

`input domain -> operation -> structural property -> output domain -> consumer`

The final noun of one module should match the first noun of the next. If the terms differ, explain the conversion explicitly.

## Explain corrective methods as invariants

When a method repairs an existing operation, use:

`old operator -> violated invariant -> new operator -> restored invariant`

Separate implementation correction, structural verification, and new algorithmic contribution. Do not inflate a local correction into a broader theory.

## Define the representation before the operator

Before presenting an operator, define:

- the object it acts on;
- its indices and coordinate system;
- its dimensions or domain;
- the meaning of each axis;
- boundary and empty-set behavior when relevant.

Only then introduce the transformation.

## Present the baseline before the delta

When modifying a predecessor:

1. give the baseline equation or operation;
2. identify the exact term or interface that fails;
3. present the minimal change;
4. explain the behavioral consequence.

This makes novelty and correctness easier to evaluate.

## Explain equations behaviorally

After every important equation, state:

- what the equation selects, combines, normalizes, or preserves;
- what happens at boundaries or special cases;
- why the output satisfies the next module's requirement.

Use generic symbols before substituting experimental constants. Put implementation values such as image size, window length, or grid dimensions in a later instantiation sentence unless the value is intrinsic to the method.

Keep notation identical across text, equations, figures, and captions.

## Coordinate method figures and subsections

- Use the overall figure to show the end-to-end data flow and change boundary.
- Use one detail figure per complex module.
- Give a detail figure two levels when helpful:
  - `(a)` the module's macro position and input/output;
  - `(b)` one element's or one index's computation.
- Pair each panel with one subsection. Avoid a figure whose panels are discussed out of order.
- Keep overview figures light on equations; place detail equations beside visible objects or in the text.
- Show concrete inputs and outputs whenever the representation is otherwise abstract.

## Expose composition

Do not hide the final composition in one sentence. If outputs are fused across scales, windows, paths, or modules, define:

- what is combined;
- the weighting or reduction rule;
- the shared coordinate system;
- the final output domain.

Explain why composition preserves the properties established by the modules.

## Method checks

- `METHOD_DUAL_NAVIGATION`: figure and prose lead to the same computation.
- `METHOD_ROADMAP_FIRST`: the reader sees the overall route before operator detail.
- `REPRESENTATION_BEFORE_OPERATOR`: every operator has a defined input domain.
- `BASELINE_THEN_DELTA`: modifications are expressed against the predecessor.
- `EXPLAIN_MATH_BEHAVIOR`: equations are followed by a behavioral explanation.
- `GENERIC_SYMBOLS_BEFORE_INSTANTIATION`: method definitions are not tied prematurely to one experiment.
- `MODULE_CONTRACT`: every module has why, input, operation, output, and handoff.
- `EXPLICIT_MODULE_HANDOFF`: adjacent modules name the same transferred object.
- `COMPOSITION_IS_NOT_HIDDEN`: final fusion or aggregation is explicit.
- `PANEL_SECTION_BIJECTION`: each detail panel has one textual home.
- `SECTION_LOCAL_FLOATS`: figures remain near the subsections that explain them.
