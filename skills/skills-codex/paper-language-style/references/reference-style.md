# Reference-Guided Narrative Grammar

Learn information hierarchy, argument cadence, and figure roles from exemplar papers. Never copy their prose, diagrams, claims, examples, or domain-specific content.

## Mechanism-first backbone pattern

This pattern, exemplified by strong mechanism-focused vision backbones such as DFormerv2, works well when the paper changes a familiar pipeline through one clear design insight.

Abstract the pattern as:

1. establish the task benefit or practical need;
2. describe the dominant implementation;
3. state why that implementation is mismatched to the underlying role of the input or signal;
4. introduce a different representation or prior;
5. show how the prior changes the core operator;
6. close with broad but measured experimental evidence.

Use it to make a mechanism feel inevitable. Do not reproduce the source paper's wording or scientific claim.

For Method:

- define the prior or representation first;
- show how it changes the operator;
- name the resulting module;
- show the full encoder or pipeline;
- validate the mechanism separately from the final benchmark.

For Conclusion:

- name the method;
- restate the mechanism in one or two sentences;
- summarize the strongest supported result and efficiency or practical value;
- stop without reopening the whole discussion.

## Problem-figure visual pipeline pattern

This pattern, exemplified by visual time-series methods such as ViT4TS, works well when a transformed representation creates both an opportunity and a failure mode.

Abstract the pattern as:

1. compare existing task paradigms with simple pipelines;
2. show why the transformed representation is useful;
3. show one concrete limitation of using it directly;
4. map each visible failure to a proposed mechanism;
5. use the full architecture to connect those mechanisms;
6. return to the same failure in ablation and qualitative evidence.

The motivation figure should let a novice answer:

- What is the input?
- What representation is created?
- Where does the failure occur?
- What observable error results?
- Which module repairs it?

## Figure hierarchy

Use this progression when the paper supports it:

1. **Paradigm figure:** existing routes and the paper's position.
2. **Failure figure:** concrete mechanism-level motivation.
3. **Architecture figure:** complete data flow.
4. **Module figures:** controlled zoom into each new operation.
5. **Evidence figures:** trade-off, sensitivity, or qualitative closure.

Do not include a figure solely because an exemplar has one. Every figure must answer a live reviewer question in the current paper.

## Experimental descent

Strong empirical narratives descend from outcome to mechanism:

`main comparison -> component ablation -> structural or diagnostic evidence -> efficiency -> qualitative behavior`

Use the main table to establish outcome. Use later evidence to explain why the outcome occurs. Avoid repeating the main table as a decorative plot.

## Sentence cadence

- Start a paragraph with its scientific job, not generic scene setting.
- Follow a longer explanatory sentence with a short consequence when clarity benefits.
- Use a transition to mark a real inference, not to decorate every sentence.
- Prefer explicit agents and operations.
- End a paragraph with a changed state: a narrowed gap, a derived requirement, a module output, or a supported finding.

## Safe adaptation checklist

- The current paper's facts, symbols, and evidence remain the only scientific source.
- No source sentence or caption has been paraphrased too closely.
- No source-specific figure geometry has been copied one-to-one.
- The number of sections, figures, and experiments follows current evidence, not exemplar density.
- Any missing evidence remains a declared gap; it is never filled by analogy.
