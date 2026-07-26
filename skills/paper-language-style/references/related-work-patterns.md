# Related Work Patterns

Organize Related Work as an argument about the remaining technical gap, not as a chronological bibliography.

## Choose a stable design axis

Group papers by a technical choice that remains meaningful across years, such as:

- native representation versus transformed representation;
- separate encoders versus shared or unified encoders;
- global prediction versus dense localization;
- learned alignment versus explicit coordinate recovery;
- direct modeling versus foundation-model transfer.

Use two to four families. Do not create one subsection per paper.

## Use the family paragraph unit

Build each family paragraph from five moves:

1. **Problem.** What need motivates this family?
2. **Mechanism.** What common technical choice defines it?
3. **Representatives.** Which works illustrate meaningful variants?
4. **Capability.** What does the family solve well?
5. **Residual gap.** What shared limitation remains relevant to this paper?

Generic structure:

> A first line of work addresses [problem] through [shared mechanism]. Representative methods use [variant A], [variant B], or [variant C] to obtain [capability]. These designs improve [resolved issue]. Their outputs, however, still leave [precise unresolved interface or requirement], which motivates the next family or the proposed method.

Do not reduce the paragraph to `A does X. B does Y. C does Z.`

## Use the three-stage funnel for transformed representations

When a paper moves evidence across representations or domains, use this order when supported:

1. **Same task in the native representation.**
2. **Same task with transformed or foundation representations.**
3. **Adjacent task with the same recovery, alignment, or dense-inference difficulty.**

Possible generic headings:

- `Task Modeling in the Native Representation`
- `Task Modeling with Transformed or Foundation Representations`
- `Dense Inference and Cross-Representation Recovery`

If a three-panel concept figure truly presents the same three paradigms, Related Work may mirror that order. Do not force three subsections merely to match the artwork.

## Treat the closest predecessor explicitly

Discuss the closest predecessor at the end of the most relevant subsection. Use an inheritance-gap-boundary contract:

1. State what upstream representation, encoder, or pipeline is inherited.
2. State the unresolved intermediate domain or interface.
3. State the minimal redesign boundary.

Generic pattern:

> The closest system already provides [upstream capability]. Its output is nevertheless defined in [intermediate representation], whereas the task requires [target-domain output]. The proposed method retains [unchanged component] and redesigns only [unresolved interface].

This is stronger than vague novelty language because it makes the delta inspectable.

## Add an adjacent mechanism subsection only when useful

If the method imports an idea from another field, explain:

`base mechanism -> known cost or limitation -> relevant improvements -> closest transferable capability -> remaining mismatch`

Do not cite an adjacent field merely to make the bibliography look broad.

## Make paragraph endings move the paper

Use one of four exit roles:

- **Scope ending:** delimit what the family covers.
- **Tension ending:** expose the cost of its design choice.
- **Residual-gap ending:** name the unresolved capability.
- **Method-bridge ending:** state the requirement that Method will implement.

The final Related Work paragraph should end with a capability requirement, not an experimental claim.

## Avoid duplication with the Introduction

- Let the Introduction explain why the problem matters and show one concrete failure.
- Let Related Work explain how method families reached the current boundary.
- Do not repeat the same citations, examples, and limitation sentences verbatim.
- Do not advertise numerical results in Related Work.

## Related Work checks

- `RW_CLASSIFY_BY_DESIGN_AXIS`: sections follow a technical axis, not time.
- `RW_FAMILY_UNIT`: each paragraph contains problem, mechanism, representatives, capability, and gap.
- `RW_CLOSEST_PREDECESSOR`: the nearest baseline receives an explicit delta contract.
- `RW_END_WITH_STATE_CHANGE`: every paragraph advances scope, tension, gap, or handoff.
- `RW_HANDOFF`: the last paragraph defines the capability Method must provide.
- `RW_NO_DUPLICATE_INTRO`: Related Work expands rather than repeats the Introduction.
