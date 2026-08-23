# Claim-Mirrored Section Blueprints

Use this reference whenever a task plans, drafts, rewrites, or audits a claim-bearing
Abstract, Introduction contribution list, Method/analysis section, or Conclusion. It is
canonical for section structure and cross-section mirroring; use
`writing-principles.md` for prose style.

These are claim-grounded structural blueprints, not fill-in-the-blank prose. For an
empirical AI method paper, use the fixed-count profile below unless the user or venue
explicitly requires a different one. The sentence roles and counts are fixed; the wording
and technical content remain paper-specific. Never copy exemplar phrasing or invent an
experiment, number, comparator, protocol, or scope qualifier to fill a sentence.

If the paper is theory, diagnostic, position, or another non-method type, record a
type-specific profile with exact counts in `PAPER_PLAN.md` before drafting. Likewise, if a
venue word limit or an explicit user instruction conflicts with the default profile,
record the replacement counts and roles before writing; do not silently drift into a
variable-length structure.

## 1. One Canonical Claim Ledger

Use a single canonical Claim Ledger. If an older plan contains a legacy claim/evidence
store, migrate its grounded content into this ledger and replace the old references. Do not
maintain a second store containing duplicated claim text or evidence.

```markdown
| Claim ID | Role | Exact claim | Comparator or N/A | Evidence (experiment/table/figure/theorem/proof) | Scope/data access | Selection/training/adaptation or N/A | Limitation | Forbidden expansion |
|---|---|---|---|---|---|---|---|---|
| C1 | formulation | ... | ... | ... | ... | ... | ... | ... |
```

Use `N/A` when a field genuinely does not apply. When applicable, keep the following
concepts separate:

- gradient-trained or otherwise fitted parameters;
- development-time selection, tuning, or model choice;
- target-time adaptation, calibration, or memory instantiation;
- inference-time access, including prefix, reference-set, or complete-sequence access;
- a fixed numerical threshold versus a transferred operating fraction or rule;
- intervals conditional on realized selections versus intervals that repeat the full
  selection pipeline.

The ledger is the source of truth for wording, comparators, headline numbers, protocol
names, scope qualifiers, and limitations everywhere else in the paper.

## 2. Abstract Blueprint

### Empirical AI method default: exactly 10 sentences

1. **Setting:** state the specific task or setting and why it matters.
2. **Limitation:** explain what existing approaches do and the unresolved limitation.
3. **Reframing:** state the paper's key insight or research question.
4. **Method contract:** name the method and state its overall input-to-output role.
5. **Mechanism 1:** explain the first main module or operation and its job.
6. **Mechanism 2:** explain the second module, composition step, or complementary job.
7. **Design boundary:** state the intended behavior and what remains fixed, excluded, or
   deliberately unchanged.
8. **Primary evidence:** give the evaluated scope/protocol and strongest supported result.
9. **Secondary evidence:** give transfer, robustness, ablation, or independent
   confirmation; when none exists, state the evidence boundary instead of inventing one.
10. **Takeaway:** end with the strongest scope-aware conclusion supported by the ledger.

Rules:

- Obey the venue's explicit word limit. If no limit is known, target 150--200 words.
- Keep one numbered role per surface sentence. Vary sentence length and syntax for
  readability; do not create fragments or semicolon chains to game the count.
- A reference paper may guide rhetorical order or cadence, never reusable prose, claims,
  terminology, or numbers.
- Do not force stock openers such as "Recent advances" or "Based on this insight."
- Prefer one canonical headline comparator and result unless the Claim Ledger requires
  more.
- Keep acronyms minimal and define any that are essential.
- Preserve the evaluated scope in the final takeaway.

## 3. Introduction Contribution Blueprint

### Empirical AI method default: exactly 3 bullets with 2 / 3 / 3 sentences

1. **Problem/formulation — 2 sentences:** sentence 1 identifies the neglected stage,
   failure mode, or requirement; sentence 2 formulates the paper's reframing and scope.
2. **Method/mechanism — 3 sentences:** sentence 1 states the method's overall contract;
   sentence 2 states the first module's job; sentence 3 states the complementary module
   or composition mechanism and its job.
3. **Evidence/scope — 3 sentences:** sentence 1 states the evaluation protocol and scope;
   sentence 2 reports the canonical headline result; sentence 3 reports independent or
   secondary evidence and its transfer/generalization boundary. If no secondary evidence
   exists, sentence 3 states that evidence boundary without implying a missing result.

Rules:

- Map every bullet to one or more Claim IDs and evidence entries.
- Do not begin every adjacent bullet with "We" merely out of habit.
- Preserve the `2 / 3 / 3` sentence allocation unless an explicit replacement profile is
  recorded before drafting.
- Make bullets specific and falsifiable; "we conduct extensive experiments" is not a
  contribution.
- Do not promote descriptive, oracle, conditional, or selected-case evidence into a
  general causal claim.

## 4. Method or Analysis Blueprint

For a method or system paper, use the applicable subset below. Theory and diagnostic
papers should preserve the same contract logic with their corresponding objects.

1. **Overview and contract:** input, output, unchanged or frozen components, changed
   components, and end-to-end data flow.
2. **Representation/interface:** objects passed between the existing system and the new
   method.
3. **Module 1..N:** failure or motivation -> input/output -> construction or equation ->
   direct property or intuitive effect -> hand-off to the next module.
4. **Composition and inference:** how modules combine and what is selected, trained,
   adapted, calibrated, or fixed.
5. **Access and deployment assumptions:** online/offline status, full-sequence access,
   target-prefix/reference access, and the scope of any latency measurement.
6. **Complexity and implementation:** include only when relevant to a stated claim.
7. **Boundary cases:** ties, constant inputs, empty predictions, padding, invalid support,
   or other behavior needed for reproduction.

For each important equation, use this local order:

```text
why the equation is needed -> equation with every symbol defined -> direct property,
effect, and relevant boundary case
```

Do not present a naked equation and postpone its purpose until a later paragraph.

## 5. Conclusion Blueprint

### Empirical AI method default: exactly 8 sentences

Follow the same claim order as the paper without copying the Introduction verbatim:

1. **Answer:** name the method and state the paper's direct answer to the problem.
2. **Mechanism:** summarize the main modules and their complementary roles.
3. **Primary evidence:** restate the strongest supported evaluation result at the proper
   scope.
4. **Secondary evidence:** state transfer, robustness, ablation, or independent
   confirmation; if unavailable, state the evidence boundary.
5. **Interpretation:** say what the supported evidence attributes to the main components
   or design choices without claiming causality beyond the experiments.
6. **Limitation:** state the most important scope or deployment limitation.
7. **Practical takeaway:** state what the method enables within the evaluated setting.
8. **Significance:** close with the broader technical meaning without expanding the claim.

Hard rules:

- No method, number, comparator, dataset, protocol, or claim may first appear in the
  Conclusion.
- Names and scope qualifiers must match the Claim Ledger.
- Do not append generic Future Work to the eight-sentence Conclusion. If the venue
  mandates a separate Limitations or Future Work section, keep it outside this count and
  derive it from sentence 6.

## 6. Front-Matter Coverage Index

Add this lightweight index to `PAPER_PLAN.md`. It points to Claim IDs and locations and
must not duplicate claim text or evidence from the Claim Ledger.

```markdown
| Claim ID | Abstract move | Intro bullet | Body subsection | Evidence location | Conclusion sentence |
|---|---|---|---|---|---|
```

## 7. Mirror Gate

Before considering the front matter and conclusion complete, verify:

- every Introduction contribution has a method, analysis, theory, or diagnostic
  implementation and an evidence location;
- every supported contribution is reflected in the Conclusion;
- Abstract and Conclusion use the same canonical comparator, number, and scope qualifier;
- the Conclusion introduces no new claim;
- the active sentence profile is recorded and satisfied exactly: for the empirical AI
  method default, Abstract = 10 sentences, contribution bullets = 2 / 3 / 3 sentences,
  and Conclusion = 8 sentences;
- terminology is consistent while sentences are not copied verbatim across sections.
