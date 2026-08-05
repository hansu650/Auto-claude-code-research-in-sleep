# Claim-Mirrored Section Blueprints

Use this reference whenever a task plans, drafts, rewrites, or audits a claim-bearing
Abstract, Introduction contribution list, Method/analysis section, or Conclusion. It is
canonical for section structure and cross-section mirroring; use
`writing-principles.md` for prose style.

These are semantic blueprints, not fill-in-the-blank prose. Adapt them to the paper type,
venue, and available evidence. Never invent an experiment, number, comparator, protocol,
or scope qualifier to complete a template.

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

Use the applicable subset of these semantic moves. They do not imply a fixed sentence
count or a requirement that every paper contain every move.

1. State the specific setting and why it matters.
2. Explain what existing approaches do and the unresolved limitation.
3. State the reframing insight or research question.
4. For a method paper, name the method and give its overall contract. For a theory,
   diagnostic, or position paper, name the corresponding analytical object or study
   design.
5. When useful, explain one to three component or argument roles in plain language.
6. State the evaluated scope/protocol and strongest supported evidence.
7. End with a scope-aware overall takeaway.

Rules:

- Obey the venue's explicit word limit. If no limit is known, target 150--200 words.
- Use long and short sentences as clarity requires; do not force one move per sentence.
- A reference paper may guide rhetorical order or cadence, never reusable prose, claims,
  terminology, or numbers.
- Do not force stock openers such as "Recent advances" or "Based on this insight."
- Prefer one canonical headline comparator and result unless the Claim Ledger requires
  more.
- Keep acronyms minimal and define any that are essential.
- Preserve the evaluated scope in the final takeaway.

## 3. Introduction Contribution Blueprint

Use two to four contribution bullets. For a three-bullet method paper, the default roles
are:

1. **Problem/formulation:** identify the neglected stage, failure mode, or requirement
   and formulate it precisely.
2. **Method/mechanism:** use the method name as the subject when natural; name the main
   modules and state each module's job.
3. **Evidence/scope:** state the evaluation protocol, evidence range, strongest supported
   result, and important transfer or generalization boundary.

Rules:

- Map every bullet to one or more Claim IDs and evidence entries.
- Do not begin every adjacent bullet with "We" merely out of habit.
- Do not force exactly three bullets when the claim structure needs two or four.
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

Follow the same claim order as the paper without copying the Introduction verbatim:

1. problem and reframing;
2. method or analytical object and component roles;
3. strongest supported evidence;
4. evaluated scope and limitations;
5. Future Work as a separate paragraph when venue space permits;
6. an optional final takeaway that does not broaden the claim.

Hard rules:

- No method, number, comparator, dataset, protocol, or claim may first appear in the
  Conclusion.
- Names and scope qualifiers must match the Claim Ledger.
- Future work must follow from a stated limitation; avoid generic promises.

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
- terminology is consistent while sentences are not copied verbatim across sections.
