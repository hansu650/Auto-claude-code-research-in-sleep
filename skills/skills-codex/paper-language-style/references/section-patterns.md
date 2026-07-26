# Section Patterns

Use these patterns as functional templates. Adapt their length to the venue and evidence.

## Abstract

Write one compact paragraph with five moves:

1. **Background and value.** Name the task and why it matters.
2. **Concrete failure.** State what object is misplaced, lost, blurred, conflated, or misestimated; locate the failing interface; state the practical consequence.
3. **Whole method.** Introduce the complete method before its modules.
4. **Division of labor and collaboration.** Explain what each module does and why their order matters.
5. **Evidence and value.** Give one core result or compact evidence statement, then state the supported value.

Use this dependency:

`background -> failure -> method -> sequential collaboration -> result and value`

Keep only one or two decisive numbers. Do not list the whole experimental suite.

### Collaboration sentence

Use a domain-specific version of:

> Module A first restores or constructs \(X\). Module B then consumes \(X\) to produce \(Y\). Their sequence preserves or guarantees \(Z\) across the complete path.

Do not merely list two module descriptions. State the transferred object and why the order is necessary.

## Introduction

Use a narrowing sequence:

1. Establish the task and its practical importance.
2. Describe the dominant technical route.
3. Identify a concrete failure in that route.
4. Show the failure or paradigm gap in a concept figure.
5. Convert the failure into a design requirement.
6. Introduce the method with a real transition such as `Based on this observation, we propose ...`.
7. Preview the data flow and module collaboration.
8. Summarize contributions at three levels:
   - problem formulation or perspective;
   - method and mechanisms;
   - evidence and practical value.

Vary contribution openings. Suitable forms include:

- `This work formulates ...`
- `The proposed framework combines ...`
- `Experiments across ... demonstrate ...`

Do not make every bullet begin with `We`.

### Figure roles in the Introduction

- Use the first concept figure to place the work among existing paradigms.
- Use a separate motivation figure to show the concrete failure that produces the design requirement.
- Introduce the two figures in separate paragraphs when they answer different questions.
- Do not cite both figures in one generic sentence.

End the Introduction with a stable paper roadmap only when the venue convention benefits from one.

## Experiments

Establish a claim-to-evidence map before writing:

| Claim | Typical evidence |
|---|---|
| Main predictive quality | complete comparison table |
| Component contribution | controlled ablation |
| Structural correctness | invariant or coverage audit |
| Statistical stability | confidence intervals or repeated trials |
| Efficiency | scoped runtime, memory, or parameter analysis |
| Mechanism behavior | diagnostic or sensitivity study |
| Interpretability | representative qualitative cases |
| Scope or robustness | alternate settings or failure cases |

Write each result paragraph in this order:

1. overall finding;
2. one decisive number or comparison;
3. mechanism-based interpretation;
4. brief scope, exception, or boundary when material.

Keep the final sentence positive and scope-correct. Acknowledge an exception without letting the entire paragraph revolve around the paper's weakness.

Give each table one primary question. Avoid a table and a chart that repeat the same values unless the chart exposes an additional relationship such as a trade-off, trend, or uncertainty.

## Conclusion

Use a concise five-part recovery:

1. State the complete method.
2. Restate the concrete failure it addresses.
3. Explain how the modules work in sequence.
4. Summarize the strongest supported experimental finding.
5. State the final value within the demonstrated scope.

The Conclusion should echo the Introduction's problem in resolved form. It should not reproduce the entire data flow, introduce a new mechanism, add a new number, or make a broader claim than the experiments support.

### Compact conclusion skeleton

> We propose [method], a [defining property] framework for [task]. Existing [pipeline] can [recognize or estimate correctly] while [specific interface failure and consequence]. [Module A] [operation and output], after which [Module B] [operation and final output]. Experiments on [scope] show [one supported result or evidence summary]. These results establish [scope-correct value].
