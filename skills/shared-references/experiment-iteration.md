# Evidence-driven Experiment Iteration

Read only the sections needed for baseline selection, experimental design,
authorized research iteration, or handoff. Use the project's existing plan,
tracker, and result registry; do not create a parallel bookkeeping system.
Examples below are conditional controls, not a mandatory benchmark suite.
This is also the experiment-driven mode of `research-refine`; no separate skill
or per-round proposal review is needed to use it. User/project preferences govern
GPU scheduling and independent reviews. Keep actual submission review gates
distinct from exploratory decisions.

## Choose a question that could change the next decision

State a concrete observation with its task, metric, parent model and selection
conditions. Inspect what the code can observe and what it forces: missing
cross-variable dependencies, compressed features, normalization invariances,
and restricted output spaces can suggest useful hypotheses. A structural
limitation is a mathematical fact only when checked; its responsibility for the
observed error remains a separate empirical question.

Compare the main hypothesis with only the alternatives needed to choose a test:
insufficient optimization, excessive step size, drift of the inherited model,
missing input information, or a harmful part of an update. Prefer the cheapest
probe that can distinguish them, such as a fixed-feature affine head, calibration,
branch subtraction, frozen/joint comparison, or decomposition of an existing
checkpoint's update. Do not require another probe when current evidence already
answers the question, and do not mistake a diagnostic evaluation for retraining.

Let contrary evidence change the design. If a prespecified decomposition finds
that the component suspected to help actually hurts validation, retain that
result, revise the explanation, and test the resulting constraint in a new fit.
A post-hoc decomposition motivates that fit; it does not prove its outcome or
establish the universal choice of a subspace. If a safeguard rarely activates,
measure its interventions before crediting it for the result.

Preserving a strong inherited model through a zero-output correction, frozen
reference and selectable epoch 0 can make a test interpretable. Keep the
unchanged predictor as a real option when that is the comparison being made.
This is not a permanent restriction to add-on heads: a justified backbone change
is possible when it lies within the user's scope.

## Search failure history without banning a whole direction

Compare the parent, code/configuration, data/features, objective, training budget,
selection rule and seed before calling a candidate an exact repeat. Reuse an
already completed identical failure unless reproduction or a specific integrity
question justifies another run. A renamed candidate is not a new hypothesis.

Related negative evidence is narrower: failing on compressed statistics does
not rule out a materially different information source or representation. State
which condition changed, why the earlier failure does not settle the question,
and what limited experiment can distinguish it. Intentional additional seeds for
confirmation are not accidental duplicates.

Use the existing failure log to record conditions, observation, the explanation
weakened, what remains open, and the next decision. Do not turn a negative result
into a global prohibition or build another logging system.

## Choose the research anchor and the comparison set separately

A research anchor is the system whose concrete weakness motivates the work.
Choose it by task/venue relevance, the user's domain familiarity, an inspectable
failure, available data and official implementation, and feasible training and
evaluation cost. Recency or a prestigious venue alone is insufficient. Verify
paper claims and code availability before calling them verified; an LLM suggestion
is a candidate source, not evidence. Seek recent primary sources when recency
matters, without copying a past project's fixed year cutoff.

The paper comparison set answers a different question: how does the final method
compare with credible alternatives? Keep strong relevant baselines and simple
alternatives that can explain the gain. Record whether every result is published,
reproduced, or newly measured. A published table can establish context; it does
not by itself establish matched training, tuning, splits, or compute fairness.

## Recover the experiment state before proposing a new run

Start with the latest verified state, then inspect history only to resolve gaps:

- code/config version and exact checkpoint identity, including architecture,
  trained auxiliary modules, buffers, dtype, and preprocessing;
- dataset/version, column order, splits, scaler fitting, evaluation windows,
  metric reduction, seeds, and checkpoint-selection rule;
- completed and running jobs, current retained candidates, failed hypotheses,
  and evidence paths linking each number to its run and checkpoint.

Reuse a result only when its relevant protocol and artifact identities still
match the proposed comparison. When a base, input, objective, data split, or
training recipe changes, identify the affected evidence and rerun those controls
if needed. Do not relabel old ablations as tests of the new method, or rebuild
unchanged valid results merely because another machine takes over.

## Diagnose, hypothesize, and make a discriminating comparison

1. **Diagnose:** locate the observed gap using learning curves, retained epoch,
   error structure, gradients, or a focused example. Separate measured behavior
   from its possible explanation. Falling training loss with an unchanged best
   validation checkpoint suggests several hypotheses; it does not identify a
   learning-rate failure by itself.
2. **Hypothesize:** state one falsifiable explanation, the smallest useful change,
   what stays fixed, the expected observation, and what would reject it. Ground
   the change in a checked mechanism, derivation, or relevant primary source.
   Avoid another module simply because the previous run lost. Fix the development
   panel, primary metric or multi-metric tradeoff, protected incumbent cases, and
   expand/stop rule before reading candidate results. Include representative hard
   cases and existing strengths when regressions matter; no universal panel size
   or gain threshold applies. Use training/validation for candidate decisions.
3. **Check the implementation:** verify the intended initial function, trainable
   and frozen parts, loss, gradient path, legal data access, and metric counting.
   If an added residual is meant to preserve the base initially, test output
   equality within a declared numerical tolerance. A zero-initialized output
   layer may delay upstream gradients; test the intended behavior across updates.
4. **Run the planned block:** preserve positive, null, and negative outcomes.
   Complete its prespecified scope unless a recorded sequential rule, technical
   failure, budget, or user stop applies. Do not silently drop tasks because
   early scores are poor. Recover failed jobs from a verifiable state.
5. **Decide:** record the observation, remaining confounds, retain/reject reason,
   and next discriminating test. Continue within the authorized scope and budget.
   Repeated null findings should lead to a different hypothesis, a simpler method,
   or a narrower claim, not an identical rerun without new evidence. Finish when
   the requested evidence is sufficient, the agreed budget/stop condition is reached,
   or no informative in-scope test remains. Report any unresolved gap explicitly.
   When metrics disagree, apply the declared objective and record all of them;
   do not choose a new primary metric after seeing the result.

When budgets and the next action are already clear, keep checks proportional to
data validity, loading, gradients, evaluation coverage, duplicate prevention and
recoverability. Reuse unchanged evidence and same-task environments. Ready
independent jobs may continue while the active executor analyzes results or
reads relevant literature on CPU; dependent scientific changes wait for evidence.
A deterministic queue resumes jobs, but it does not invent the next hypothesis.
Use actual continuation capabilities and do not promise an unattended research
loop merely because a script or skill file exists.

Keep earlier checkpoints immutable and update a new registry for retained models.
If development allows task-specific winners, retain their exact selection unit
and rule. Do not mix horizons, seeds, or checkpoints into a supposedly uniform
model after inspecting test results. Such an exploratory collection must be
labeled as selected development results.

## Controls that separate plausible explanations

Select the control that addresses the actual claim:

| Question | Useful comparison | What must stay explicit |
|---|---|---|
| Do two components each help? | Base, Base+A, Base+B, Base+A+B | Same base identity, legal inputs, selection rule, and relevant training conditions |
| Is the gain due to more training or tuning? | Matched selection opportunity and a justified budget comparison | Equal epochs, updates, and wall time are different protocols; include all training stages and explain hardware/tuning budgets |
| Does a constraint/projection cause the gain? | Constraint on/off with other interfaces fixed | If disabling it changes another module's input, hold that input fixed in a separate control |
| Does the chosen subspace matter? | Equal-dimensional plausible alternative subspaces | Match dimension, selection process, and applicable model/training budget |
| Does fitting order or the objective matter? | Independent/sequential fitting or alternate losses | Shared base, target definitions, inputs, checkpoint selection, and objective scaling |
| Is the correction more than a simple alternative? | Credible simple calibration/correction on the same predictor | Same training data and predictor; transfer claims need genuinely external predictors |

Do not call an inherited base "unmodified" when it includes a previously trained
branch. Define the comparison anchor precisely. When matching every budget is
impossible, say which fairness question the chosen protocol answers rather than
calling it universally fair.

## Evidence boundaries before paper claims

Freeze the final recipe and selection rule before confirmatory evaluation.
Separate single-seed screening, repeated benchmark development, and confirmation.
Additional seeds estimate training variation; they do not make a repeatedly used
test set untouched. Use genuinely held-out evaluation when available, or disclose
the remaining selection limitation and narrow the claim.

Report the aggregation and its denominator, seed count, and uncertainty measure
(for example, sample standard deviation rather than a confidence interval).
Never infer statistical significance from a few consistent signs or overlapping/
nonoverlapping error bars alone. Observed mean improvements, evidence suggesting
a mechanism, and an established causal explanation have different strength.

Keep three states visible: supported at the tested scope, suggestive but
insufficient, and not ascertainable from available artifacts. Do not turn missing
reporting into proof of missing work. After a method pivot, update the claim map
and evidence links before drafting the new story; record provenance of external
ideas without claiming an unobserved skill invocation or review occurred.

## Server handoff for authorized autonomous research

A useful handoff gives the receiving executor decisions to make, not merely
commands to launch. Adapt the following to the already authorized task. Preparing
the handoff does not itself authorize sending it to another person or service.

```text
Objective and boundary: solve [specific problem] on [authorized environment],
within [existing compute/time/scope limits]. Current verified state: [paths].
Read [latest plan, result registry, failed hypotheses] first. Preserve ongoing
jobs and existing evidence; do not rerun [verified completed blocks] without a
specific invalidation reason.

Verify data/protocol/checkpoint identity and a local forward/evaluation witness.
CPU loading alone does not verify GPU benchmark equivalence. Preserve trained
auxiliary modules and buffers; investigate cross-device differences with a paired
check rather than silently changing the protocol.

Diagnose the remaining gap. Propose a small falsifiable change grounded in the
observed results and checked technical evidence. Record what stays fixed, the
planned task block, selection rule, success/rejection criteria, and budget.
Implement and verify it, run the block, retain all outcomes, then decide the next
step within authorization. Ordinary reversible work needs no repeated approval.
Stop or request input when the scope/cost boundary changes or required access is
missing; report a technical blocker rather than inventing success.

Return: actual completed/planned counts and missing/failed task identities;
results, logs, code/config and checkpoint identities; relevant epoch-0, update or
mechanism-activation diagnostics; retained/rejected candidates with reasons;
development/confirmation status; remaining uncertainty; and the next test with
its estimated cost (unknown costs remain unknown).
```

Do not hard-code a prior project's datasets, seed IDs, metric thresholds, module
names, device types, or polling interval into a general handoff. Keep skills,
human decisions, external suggestions, and actual run evidence distinguishable.
