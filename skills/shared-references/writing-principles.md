# Orchestra-Adapted Writing Principles

Use this reference when `paper-plan` needs help shaping the paper's story or when `paper-write` needs stronger drafting and revision guidance.

This is the expanded English counterpart to the detailed Chinese version. It is not a new workflow phase. Its purpose is to provide a stronger writing model on top of the existing `insleep` pipeline.

Use the active-profile precedence in `section-blueprints.md`. Counts below are
new-draft fallbacks, not instructions to reshape author-approved text. Preserve
the project's selected profile and any declared text locks.

## Contents

- [When to Read](#when-to-read)
- [The Narrative Principle](#the-narrative-principle)
- [Time Allocation and Reviewer Reading Order](#time-allocation-and-reviewer-reading-order)
- [How to Write the Abstract](#how-to-write-the-abstract)
- [Introduction Structure](#introduction-structure)
- [How to Write the Conclusion](#how-to-write-the-conclusion)
- [Sentence-Level Clarity](#sentence-level-clarity)
- [Micro-Level Writing Tactics](#micro-level-writing-tactics)
- [Evidence-led Revision](#evidence-led-revision)
- [Word Choice and Precision](#word-choice-and-precision)
- [Mathematical Writing](#mathematical-writing)
- [Figure Design](#figure-design)
- [Common Mistakes](#common-mistakes)
- [Pre-Submission Checklist](#pre-submission-checklist)

## When to Read

- Read before locking the framing of the paper.
- Read before drafting the Abstract and Introduction.
- Read when Related Work feels like a literature dump.
- Read when the prose feels generic, templated, or overly AI-shaped.
- Read when the structure looks fine on paper but the draft still feels unconvincing.

## The Narrative Principle

### Neel Nanda's Core View

A paper should be a **short, rigorous, evidence-backed technical story**, not a pile of experiments.

By the end of the Introduction, the reader should clearly understand:

- **The What**: the 1-3 specific claims the paper makes,
- **The Why**: the evidence that supports those claims,
- **The So What**: why the community should care.

### Andrej Karpathy's Complement

A strong paper “sells” **one thing** that was previously absent or non-obvious. The full paper should be organized around that single contribution.

### Practical Rules

- If the core contribution cannot be stated in one sentence, the framing has not converged.
- Every section should serve the same story instead of launching a second one.
- Experiments, related work, and discussion are there to support the main claim, not to operate as independent mini-papers.

### One-Sentence Contribution Test

If you cannot write something like the following, the framing is still too loose:

- “We prove that X converges under assumption Y.”
- “We show that method A improves B by 15% on benchmark C.”
- “We identify failure mode D and propose mechanism E that removes it.”

If the one-sentence contribution is hard to write, the usual causes are:

- the contribution is still too vague,
- the evidence is not yet tightly coupled to the claims,
- or the paper does not yet know what story it is telling.

## Time Allocation and Reviewer Reading Order

### Where Effort Should Go

A useful rule of thumb is to spend roughly the same amount of time on:

1. the Abstract,
2. the Introduction,
3. the Figures,
4. everything else combined.

This is not an exaggeration. Many reviewers form a preliminary judgment before they read the full methods section carefully.

### Common Reviewer Reading Order

Most reviewers encounter the paper in this order:

1. Title
2. Abstract
3. Introduction
4. Figures, especially Figure 1
5. The rest

### Writing Implications

- Put disproportionate effort into the title, abstract, introduction, and hero figure.
- Do not bury the main contribution after Section 3.
- Make the value of the paper legible before the reader reaches the full method.
- If the first two pages are unclear, later brilliance may never be seen.

## How to Write the Abstract

Use the semantic moves and evidence rules in
[`section-blueprints.md`](section-blueprints.md). For an empirical AI method paper, use
its **exact 10-sentence profile**: setting, limitation, reframing, method contract, two
mechanism sentences, design boundary, primary evidence, secondary evidence or its
boundary, and a scope-aware takeaway. This fixes the rhetorical logic, not the prose:
every sentence must still be written from the paper's own Claim Ledger. Obey the venue's
explicit word limit; when none is known, 150--200 words is a useful default target.

At the prose level, a good abstract should:

- enter the paper's specific setting and unresolved limitation quickly;
- explain the method, analytical object, or study design in plain language;
- report only evidence and scope qualifiers supported by the canonical Claim Ledger;
- remain understandable without citations or undefined acronyms; and
- end with a scope-aware takeaway rather than a broader promise.

### Openings to Delete

If the first sentence could fit almost any ML paper, delete it.

For example:

- “Large language models have achieved remarkable success...”
- “In recent years, deep learning has...”
- “Neural networks have revolutionized...”

The problem is not just that these openings sound stale. They carry **too little information** to help a reviewer judge the paper's specific contribution.

## Introduction Structure

### Basic Requirements

In two-column conference papers, the Introduction is usually best at about 1-1.5 pages.

It should satisfy the following:

- the method should start appearing by page 2-3 at the latest,
- an empirical AI method paper should include exactly three contribution bullets with
  `2 / 3 / 3` sentences,
- the central story should already make sense before technical detail arrives.

### Recommended Rhetorical Flow

1. **Opening hook**
   - What problem does the paper address?
   - Why does it matter now?

2. **Background / challenge**
   - Why is the problem hard?
   - What has prior work tried, and why is it insufficient?

3. **Approach overview**
   - What does this paper do differently?
   - What is the key insight?

4. **Contribution bullets**
   - exactly three for the empirical AI method default, each mapped to a Claim ID and
     evidence location
   - 2 sentences for problem/formulation, 3 for method/mechanism, and 3 for evidence/scope
   - specific and falsifiable
   - role-based rather than forced into identical "We ..." openings

5. **Results preview**
   - surface the strongest result early
   - tell the reader what is worth remembering

6. **Optional roadmap**
   - briefly describe the remaining sections

Use [`section-blueprints.md`](section-blueprints.md) for the contribution-role patterns,
Method contract, Conclusion mirror, and front-matter coverage index. The problem with a
bullet such as “we perform extensive experiments” is not grammar; it is that a reviewer
cannot cleanly agree, disagree, or challenge it.

## How to Write the Conclusion

For an empirical AI method paper, use the **exact 8-sentence profile** in
[`section-blueprints.md`](section-blueprints.md): answer, mechanism, primary evidence,
secondary evidence or its boundary, supported interpretation, limitation, practical
takeaway, and broader technical significance. Follow the active profile, which
may use the compact alternative. Keep the Claim Ledger order and preserve precise
headline wording when useful; avoid copying whole paragraphs. Existing or required
separate Limitations/Future Work sections sit outside the Conclusion count; do not
append generic future work merely to make the ending longer.

## Sentence-Level Clarity

### The Core Insight from Gopen and Swan

Readers have strong structural expectations about prose. If you repeatedly violate those expectations, readers spend effort decoding the sentence instead of understanding the idea.

### Seven Key Principles

#### 1. Keep Subject and Verb Close

Weak:

```text
The model, which was trained on 100M tokens and then fine-tuned with several domain-specific modifications, achieves strong results.
```

Strong:

```text
The model achieves strong results after training on 100M tokens and fine-tuning with domain-specific modifications.
```

#### 2. Put Important Information Near the End

Weak:

```text
Accuracy improves by 15% when using attention.
```

Strong:

```text
When using attention, accuracy improves by 15%.
```

#### 3. Put Context at the Start

Weak:

```text
A new attention mechanism is introduced to solve the alignment problem.
```

Strong:

```text
To address the alignment problem, we introduce a new attention mechanism.
```

#### 4. Move from Old to New

Readers track arguments more easily when the sentence begins with what is already familiar and ends with what is newly important.

#### 5. One Unit, One Function

- A paragraph should ideally do one main job.
- If a sentence is carrying two layers of logic at once, it probably wants to become two sentences.

#### 6. Put Actions in Verbs

Weak:

```text
We performed an analysis of the results.
```

Strong:

```text
We analyzed the results.
```

#### 7. Set the Stage Before New Material

Before presenting an equation, theorem, or experimental result, tell the reader why it matters.

### Fast Revision Questions

When revising a paragraph, ask:

- Is the subject separated from the verb by too much material?
- Does the sentence begin with context?
- Does the sentence end on the point that matters most?
- Is this paragraph trying to do two jobs at once?

## Micro-Level Writing Tactics

### Reduce Ambiguous Pronouns

When `this`, `it`, or `these` could be unclear, replace them with a specific noun.

Weak:

```text
This shows the method is robust.
```

Strong:

```text
These ablation results show that the method is robust to label noise.
```

### Move Verbs Earlier

Readers parse sentences faster when the main verb arrives early.

### Remove Low-Information Fillers

These words can usually be deleted:

- actually
- very
- really
- quite
- basically
- essentially
- Importantly,
- Notably,
- It is worth noting that

### Paragraph Shape

A useful paragraph skeleton is:

- first sentence: the point,
- middle: support,
- last sentence: reinforcement or transition.

Do not bury the key sentence in the middle.

## Evidence-led Revision

### Revise the reasoning before polishing the sentence

For the requested paragraph, identify its job, the evidence it uses, and the
specific point the reader should retain. Repair unclear comparisons, missing
definitions, or unsupported causal language before swapping vocabulary.
Split a sentence when it mixes distinct reasoning steps; keep necessary scope
qualifiers attached to the claim. Do not turn every sentence into the same
length or force repeated "We" / "This demonstrates" openings.

When the user requests sentence-by-sentence review, show the complete original
and proposed replacement with a brief reason. Explain in the user's language
while preserving the manuscript's language. When direct editing is authorized,
make the scoped revision and report it without inventing an approval loop.

### Method paragraphs

- Name the error or failure a component addresses before describing its steps.
  Use concrete objects and verbs: what enters, what changes, what is retained,
  and what is passed onward. Avoid repeating "effective" or "powerful" as a
  substitute for the operation.
- Separate algebraic properties from empirical effects. Orthogonality of
  outputs, an exact loss decomposition, independent parameters, and independent
  optimization are different claims. Check shared inputs, parameters, and
  objectives before inferring one from another.
- Keep the overall data flow in Overview, the operation in the module section,
  and experimental settings in Setup. Remove duplicated explanation only after
  checking that a reader still has the information needed at first use.

### Results paragraphs and tables

Lead with the strongest supported finding, then the evidence and the exception
that changes its interpretation. Let the table carry most cell values. Repeat
numbers in prose when they carry the headline result or make a comparison
unambiguous. If both metrics move together, a defined "error" may suffice;
name the metrics when they diverge or when defining the measurement.

State shared settings once in Setup; keep local exceptions beside the relevant
comparison. Table headers and row labels should identify the compared systems.
Explain an unfamiliar abbreviation at first use, without making readers chase
several sections to understand a panel. Preserve essential conditions when
shortening captions or merging protocol prose.

Keep the comparator and aggregation explicit: an average across baselines is
not the strongest baseline, a mean of relative improvements is not a relative
improvement of means, and one-seed results are not multi-seed estimates. Use
"lower mean error" for an observed mean difference; "statistically significant"
requires an appropriate test or interval. A few same-direction seed results do
not establish significance. Describe rounded ties according to the declared
table rule, not as a strict win inferred from bold text.

Distinguish **supported**, **suggestive but insufficient**, and **not ascertainable
from the available artifact**. Missing reporting does not prove an experiment
was never run. A mathematical identity does not itself establish empirical
novelty, and selected examples illustrate behavior rather than its prevalence.

### Related work and section consistency

Compare methods along a concrete axis such as the object corrected, accessible
inputs, objective, or trainable parts. State the paper's difference without
claiming all prior work lacks an ability that was not checked. Place a model's
citation with its name when consistent with the venue style; place broader
evidence with the claim it supports. Natural contrasts are useful when they
express a real difference, not merely vary the wording.

Recheck Abstract, contribution bullets, results, and Conclusion after a factual
change: comparator, scope, aggregation, and caveats must still match. For locked
sections, flag the affected exact sentences for the agreed review process.
Stop once the requested prose is clear, faithful, and consistent; do not run
another full-paper rewrite merely to pursue a higher stylistic score.

## Word Choice and Precision

### Zachary Lipton Style: Remove Needless Hedging

Unless uncertainty is genuine, avoid overusing:

- may
- can
- might
- potentially

Excessive hedging often reads less like rigor and more like self-doubt.

### Replace Vague Terms with Specific Ones

| Vague Term | Better Alternative |
|-----------|--------------------|
| performance | accuracy / F1 / latency / throughput |
| improves | increases by X% / reduces by Y |
| large | 1B parameters / 100M tokens |
| fast | 3x faster / 50ms latency |
| good results | 92% accuracy / 0.85 F1 |

### Terminology Consistency

Do not rename the same concept across the paper.

For example, avoid mixing:

- model / network / architecture
- training / learning / optimization
- sample / instance / example

Choose the best term and keep it stable.

### Describe the Actual Contribution

Choose verbs for what the method does. Use "combine", "modify", or "extend"
when accurate; do not replace them with "develop" or "introduce" to imply
greater novelty. Explain the substantive difference through the changed
operation, information access, objective, or guarantee and its evidence.

## Mathematical Writing

### Core Principle

The goal of mathematical writing is not to sound sophisticated. It is to let the reader **follow** the argument.

Prefer the following:

1. state assumptions formally before the theorem,
2. pair proofs and derivations with intuition,
3. keep notation consistent,
4. define symbols at first use.

### Recommended Notation Habits

```latex
% Scalars: lowercase italic
$x$, $y$, $\alpha$, $\beta$

% Vectors: lowercase bold
$\mathbf{x}$, $\mathbf{v}$

% Matrices: uppercase bold
$\mathbf{W}$, $\mathbf{X}$

% Sets: uppercase calligraphic
$\mathcal{X}$, $\mathcal{D}$

% Named functions: roman
$\mathrm{softmax}$, $\mathrm{ReLU}$
```

### Common Mathematical Writing Mistakes

- presenting equations without telling the reader why they matter,
- introducing assumptions too late,
- reusing symbols with different meanings across sections,
- moving all proof intuition to the appendix and leaving only bare statements in the main text.

For theory papers especially, **intuition and rigor** should coexist.

## Figure Design

### Why Figure 1 Matters

Figure 1 is often one of the first artifacts a reviewer studies after the abstract.

It should usually do at least one of the following:

- explain the core system or method idea,
- show the strongest comparison that justifies the paper,
- or provide the simplest visual summary of the main claim.

The canonical rules for figures, tables, captions, width, highlighting, compression, and
standalone versus integrated rendering live in
[`publication-layout-gates.md`](publication-layout-gates.md). At the prose level, make
captions self-contained and tell the reader what is compared and what conclusion the
artifact supports. Prefer vector plots and avoid decorative titles inside figures.

## Common Mistakes

### Structural Mistakes

| Mistake | Fix |
|--------|-----|
| Introduction longer than 1.5 pages | Move background to Related Work |
| Method buried too late | Front-load the contribution and compress the intro |
| Contribution structure drifts | Restore the empirical method default of 3 bullets with 2 / 3 / 3 sentences, or record an explicit override profile |
| Experiments not tied to claims | State what each experiment tests |

### Writing Mistakes

| Mistake | Fix |
|--------|-----|
| Generic abstract opening | Start from the paper's actual contribution |
| Inconsistent terminology | Keep one name per concept |
| Too much passive voice | Prefer active constructions |
| Hedging everywhere | Keep hedging only where uncertainty is real |

### Figure Mistakes

| Mistake | Fix |
|--------|-----|
| Raster plots | Use PDF / EPS or other vector output |
| Red-green color schemes | Switch to colorblind-safe palettes |
| Titles inside figures | Move the title into the caption |
| Captions that require the main text | Rewrite them to be self-contained |

### Citation Mistakes

| Mistake | Fix |
|--------|-----|
| Related Work as paper-by-paper summary | Reorganize by method family or research question |
| Missing important references | Proactively expand the search |
| AI-generated citations | Use a verification workflow |
| Inconsistent key or style format | Normalize the bibliography |

## Pre-Submission Checklist

### Narrative

- [ ] The contribution can be stated in one sentence.
- [ ] The Introduction makes the What / Why / So What clear.
- [ ] Every major experiment supports a clear claim.

### Structure

- [ ] For an empirical AI method paper, the Abstract has exactly 10 sentences in the
      role order defined by `section-blueprints.md` and obeys the venue word limit.
- [ ] The Introduction stays within about 1-1.5 pages.
- [ ] The method starts by page 2-3.
- [ ] There are exactly 3 concrete contribution bullets with 2 / 3 / 3 sentences.
- [ ] The Conclusion has exactly 8 sentences in the defined role order and introduces
      no new claim.
- [ ] Limitations are clearly stated.

### Writing

- [ ] Terminology is consistent.
- [ ] There are no generic field-background openings.
- [ ] Unnecessary hedging has been removed.
- [ ] All key figures have self-contained captions.

### Technical

- [ ] Citations are verified.
- [ ] Error bars and statistical reporting are clear.
- [ ] Compute resources are documented.
- [ ] Code / data availability is stated.

## Final Sentence

**A paper is not just a written record of experiments. It is a technical conclusion organized into a story that a reviewer is willing to believe.**
