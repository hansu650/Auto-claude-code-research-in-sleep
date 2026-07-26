---
name: paper-language-style
description: Apply a problem-driven, mechanism-clear, figure-coordinated, and evidence-grounded narrative layer to academic papers without changing scientific facts. Use when drafting or revising an Abstract, Introduction, Related Work, Method, Experiments, or Conclusion; aligning prose with figures and tables; reducing generic or AI-like writing; or adapting paper-write and paper-writing output for a novice reviewer.
---

# Paper Language Style

Write papers that a technically capable reviewer can understand on the first pass, even without prior knowledge of the exact subfield.

## Protect the factual envelope

Before revising prose, identify the fixed factual envelope:

- the research question and claimed scope;
- the method, module names, data flow, equations, and assumptions;
- the datasets, protocols, metrics, results, and uncertainty;
- the figure and table contents;
- the limitations established by the evidence.

Do not invent experiments, improve numbers, conceal contradictory evidence, change protocol descriptions, or broaden a claim beyond its support. Treat style references as structural inspiration only. Never copy their sentences, claims, examples, or scientific content.

## Build the narrative contract

Write a one-sentence paper story:

`task -> concrete failure -> proposed mechanism -> evidence -> value`

Then map every major element:

| Element | Required answer |
|---|---|
| Problem | What fails, where does it fail, and what is the consequence? |
| Method | What object is transformed, by which operation, into what output? |
| Modules | What does each module own, and how does one hand its output to the next? |
| Figures | What single reviewer question does each figure answer? |
| Experiments | Which claim does each table or plot test? |
| Conclusion | Which supported contribution should the reader retain? |

If any row lacks an answer, repair the argument before polishing sentences.

## Follow the drafting workflow

1. **Audit the current story.** Mark vague failures, missing handoffs, duplicated section roles, unsupported adjectives, and figure-text mismatches.
2. **Assign section jobs.** Use [references/section-patterns.md](references/section-patterns.md) for the Abstract, Introduction, Experiments, and Conclusion.
3. **Structure prior work.** Read [references/related-work-patterns.md](references/related-work-patterns.md) before drafting or materially revising Related Work.
4. **Expose the method data flow.** Read [references/method-patterns.md](references/method-patterns.md) before drafting or materially revising Method.
5. **Apply the reference grammar.** Read [references/reference-style.md](references/reference-style.md) when learning from exemplar papers or coordinating prose with figures.
6. **Run the cross-section checks.** Verify terminology, figures, evidence, numbers, and claim scope before delivery.

For a targeted sentence edit, load only the relevant reference. For a full-paper rewrite, read all four references.

## Use plain technical English

- Prefer familiar, precise verbs: `combine`, `map`, `restore`, `preserve`, `compare`, `reduce`, and `show`.
- Mix short and medium-length sentences. Give one major claim to each sentence.
- Give each paragraph one job. State that job early and end with a real state change.
- Use a transition only when the logic requires one. Useful transitions include `Based on this observation`, `To address this problem`, `Together`, and `Experiments show`.
- Avoid repeated `We ...` openings, especially in contribution lists.
- State a failure directly. Do not use a rhetorical question to manufacture motivation.
- Replace vague labels such as `implicit mapping` with the failed object, interface, and consequence.
- Avoid unsupported words such as `first`, `state-of-the-art`, `exceptional`, `comprehensive`, and `significant`.
- Keep technical terms stable. Do not vary terminology merely to avoid repetition.
- Prefer confident supported statements over defensive prose, but preserve material limitations and exceptions.

For example, replace:

> The return path is implicit.

with:

> The encoder can identify the correct abnormal patch, while the return mapping places its score on a neighboring grid cell or timestamp. This shifts the alarm and its interval boundary.

## Coordinate prose and figures

- Assign one primary question to every figure.
- Introduce a figure in the paragraph that needs its answer; do not batch unrelated figure references.
- Keep the order of objects in the prose, figure, caption, and equations consistent.
- Make every failure shown in a motivation figure correspond to a method operation and an experimental check.
- Use a full-system figure for the data flow and separate detail figures for module mechanisms.
- Keep overview figures light on equations. Put key equations beside the operation they explain in detail figures and in the Method text.
- Use LaTeX for mathematical variables. Route editable technical diagrams to `drawio-paper-diagram`.
- Place a figure after its first textual reference and within the section that explains it whenever the venue template permits.

## Enforce the evidence loop

Require this chain:

`Introduction problem -> Method mechanism -> Experiment test -> Conclusion takeaway`

Each contribution must have:

1. a concrete problem or requirement in the Introduction;
2. a named mechanism in Method;
3. a corresponding table, plot, audit, or analysis in Experiments;
4. a scope-correct takeaway in the Conclusion.

Do not treat a qualitative example as causal evidence. Do not repeat the same result in both a table and a chart unless the second view answers a different question.

## Run the final checks

Before returning revised text, verify:

- A novice reviewer can identify the task, failure, method, and result from the Abstract.
- The Introduction narrows from task to failure to design requirement.
- Related Work is organized by technical families rather than a citation list.
- Method exposes inputs, operations, outputs, and module handoffs in dependency order.
- Every figure has one role and appears near the text that uses it.
- Every experiment is tied to a paper claim.
- Abstract, body, tables, and Conclusion use the same metric names and numerical scope.
- No sequence of sentences repeatedly begins with `We`.
- No long sentence carries multiple independent claims.
- No rhetorical question, generic praise, or unsupported generalization remains.
- No stylistic edit changes a scientific fact.
