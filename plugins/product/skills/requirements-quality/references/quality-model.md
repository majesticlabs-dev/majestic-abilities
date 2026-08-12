# Requirements Quality Model

Use this reference for a full audit or when a judgement is disputed. It separates statement quality, set quality, and governance evidence so that clean wording is not mistaken for correctness or approval.

## Classification Before Audit

Do not evaluate every actionable sentence as a requirement.

| Statement type | Meaning | Treatment |
| --- | --- | --- |
| Goal | Desired business or product outcome | Trace requirements to it; do not rewrite it as system behavior |
| Need | Stakeholder capability gap or problem without an asserted delivery obligation | Preserve intent and derive requirements only when requested |
| Requirement | Obligation on the organization, product, or solution established by explicit wording or source context | Audit at its abstraction level |
| Constraint | Externally imposed boundary or fixed decision | Record its authority and affected requirements |
| Assumption | Belief treated as true for now | Preserve uncertainty and define validation evidence |
| Decision | Choice already made by an authorized party | Record source, date, and implications when available |
| Risk | Uncertain event with possible consequence | Do not turn it into behavior without a mitigation decision |
| Question | Explicit request for unresolved information or a choice | Keep open and identify what it blocks |
| Proposal | Suggested behavior, idea, or preference that is not an approved obligation | Preserve it as an option; do not audit it as an approved requirement |

Use **Proposal** for hedged behavior such as "Maybe admins should revoke access." Use **Question** when the source explicitly asks whether or how access should be revoked. Use **Assumption** for a belief about what is already true.

Candidate is a lifecycle or approval status, not a statement type. When source authority is ambiguous, choose the nearest statement type and record its status as `Candidate` or `Unknown` rather than promoting it.

Distinguish a need from a stakeholder requirement by obligation status, not sentence shape. A need describes the capability gap. A stakeholder requirement states that the delivered outcome must satisfy that capability, either explicitly or because an authoritative requirements context makes the obligation clear. Do not infer approval from imperative wording alone.

## Abstraction Levels

| Level | Purpose | Pass evidence | Detail to defer |
| --- | --- | --- | --- |
| Business | Define an outcome or organizational obligation | Outcome, measure or observable condition, scope, and authorized validation | Product behavior and architecture |
| Stakeholder | Define a capability or quality needed by an affected group | Actor or stakeholder, intent, relevant boundaries, and a plausible validation scenario | Components, algorithms, fields, and low-level thresholds not yet decided |
| Solution | Define observable system behavior or an imposed solution constraint | Actor or trigger, behavior, result, boundaries, and concrete verification method | Internal design choices not required by the obligation |

A phrase such as "all channels" is not automatically clear or ambiguous. Pass it only when the intended audience shares a defined scope. Use `Unknown` when the glossary or scope evidence is absent.

### Applicability

Use **Not applicable** when the current lifecycle explicitly does not require the check. Use **Unknown** when the check applies but deciding evidence is absent.

Not applicable when, for example:

- concrete solution test details are requested from a business-level requirement
- downstream traceability to design or tests is reviewed before decomposition begins
- individual dates are requested when the governed baseline versions the set instead
- conformance is checked but no external or internal presentation standard exists

Do not use Not applicable merely because a check is inconvenient or evidence is missing.

## Individual Requirement Checks

### Abstraction fit

**Pass when:** wording, source label, and intended next consumer align at the business, stakeholder, or solution level.

**Fail when:** the statement is mislabeled, combines obligations from incompatible levels, or contains detail that contradicts its intended level.

**Unknown when:** the intended level or next consumer is not supplied and materially different readings remain possible.

Preserve the original statement for auditability. Propose relabeling when the obligation is valid at another level. Decompose only when the intended next phase requires it.

### Necessary and relevant

**Pass when:** the requirement traces to an in-scope goal, stakeholder need, obligation, or authorized constraint.

**Fail when:** available evidence shows it is out of scope, serves no stated purpose, or duplicates an obligation at the same level.

**Unknown when:** project purpose, scope, or source evidence is unavailable.

### Singular and cohesive

**Pass when:** the statement expresses one obligation that can be approved and verified as a unit.

**Fail when:** clauses can vary independently in priority, ownership, approval, delivery, or verification.

Words such as `and`, `or`, and semicolons are warning signals, not verdicts. Do not split one coherent outcome merely because it contains multiple verbs.

### Unambiguous

**Pass when:** intended readers would identify the same obligation, scope, and conditions from the available definitions.

**Fail when:** the text supports materially different obligations. Common evidence includes an undefined actor, hidden decision rule, unclear scope, conflicting quantifier, or unresolved optionality.

**Unknown when:** interpretation depends on a missing glossary, policy, external standard, or stakeholder decision.

### Clear and concise

**Pass when:** the intended audience can parse the obligation once, domain terms are defined or conventional, and each word contributes meaning.

**Fail when:** syntax obscures the obligation, terminology drifts, or removable prose hides the actor, behavior, or result.

Clarity is audience-specific. A regulator, operator, and engineer do not need identical terminology in every requirement.

### Verifiable

**Pass when:** the required evidence and pass condition are objective at the requirement's level.

- Business: a defined metric, observation, audit, or outcome review can validate it.
- Stakeholder: a credible scenario can demonstrate the capability once decomposition exists.
- Solution: a test, analysis, inspection, or demonstration has concrete inputs and expected results.

**Fail when:** compliance depends only on taste or undefined adjectives.

**Unknown when:** a measurable target or authoritative judgement is still pending. Do not invent a proxy metric merely because one is convenient.

### Implementation freedom

**Pass when:** the statement constrains behavior without fixing an unnecessary design choice, or supplied authority establishes that the named choice is required.

**Fail when:** supplied evidence establishes that a prescribed technology, architecture, data structure, vendor, or interface detail is unapproved, conflicts with the intended level, or unnecessarily restricts an approved outcome.

**Unknown when:** the requirement names an implementation choice but its authority is not supplied. Preserve the named choice, flag the evidence gap, and ask whether it is an approved constraint before removing it.

A named implementation can be justified by an approved constraint, interoperability need, regulation, contract, or interaction decision. Record that source.

### Feasibility

**Pass when:** delivery evidence supports feasibility within known technical, legal, schedule, budget, and organizational constraints.

**Fail when:** supplied evidence demonstrates a contradiction or known impossibility.

**Unknown when:** estimates, experiments, approvals, capacity, or constraints are missing. An agent's intuition is not feasibility evidence.

## Governance Evidence

Governance attributes are not properties of sentence wording.

### Ownership and validation

Accept an accountable individual, role, authority, or governance body when it can approve the requirement and resolve disputes. Require a named person only when the project's governance model does.

- `Pass`: approval authority and evidence are supplied.
- `Fail`: the required stage mandates an authority and the artifact explicitly leaves it unresolved.
- `Unknown`: no governance evidence is available.

Do not claim stakeholder validation from confident wording.

### Currency

Evaluate currency from the catalogue baseline, version history, source dates, change control, or review evidence. Individual dates are optional unless the governing process requires them.

Use `Unknown` rather than `Fail` when no history was supplied.

### Correctness

Do not use correctness as a circular summary of every other characteristic.

Report separately:

- **Well-formed:** applicable statement and set checks pass.
- **Validated:** authorized evidence confirms the requirement represents the intended need.
- **Correctness:** supported only when both are evidenced; otherwise `Unknown`.

## Requirement-Set Checks

### Consistency

Check for direct contradictions, incompatible conditions, terminology drift, mismatched quantities, and conflicting authority. Requirements at different levels may express the same intent without contradiction.

### Same-level uniqueness

Merge requirements only when they impose the same obligation at the same level and scope. Preserve distinct requirements when their actors, conditions, outcomes, authority, priority, or verification differ.

### Coverage and completeness

Judge coverage against the intended next phase, not against an imaginary final specification.

Sweep these categories in order. Mark each one `Covered`, `Gap`, or `Not applicable`:

1. goal and stakeholder trace
2. actor and journey coverage
3. happy, invalid, empty, denied, cancellation, retry, recovery, and offboarding states
4. entity lifecycle and create, read, update, archive, or delete behavior
5. feature interaction and concurrent or repeated execution
6. security, privacy, accessibility, regulatory, data, performance, reliability, and operational concerns
7. dependency and external-interface review

Report the marks only. Do not expand a `Gap` into a scenario table, a severity, or per-category commentary. A `Gap` becomes at most one open decision in the review output.

Missing categories are prompts for investigation, not requirements to invent. Report completeness as bounded by the supplied evidence.

### Traceability

Trace upstream to a source, goal, need, policy, regulation, or decision. Trace downstream only when the intended stage should already have design, delivery, or verification artifacts.

A missing downstream test is not a defect in an early stakeholder requirement. It may be deferred decomposition.

### Organization and modifiability

Check stable identifiers, logical grouping, canonical terminology, durable cross-references, baseline history, and whether a plausible scope change can be located without searching unrelated prose.

Do not require a particular template when the existing structure remains usable for its audience and lifecycle.

### Conformance

Apply a mandated template, contract, or regulatory form only when evidence identifies it. Otherwise assess internal consistency of presentation and record formatting improvements as minor.

## Heuristics, Not Automatic Failures

Investigate these signals:

- vague modifiers such as `appropriate`, `reasonable`, `fast`, `seamless`, or `scalable`
- optional terms such as `may`, `might`, `could`, `as needed`, or `where applicable`
- conjunctions, embedded lists, and multiple conditions
- passive constructions that hide the responsible actor
- named technologies, vendors, controls, schemas, or architectural components
- `TBD`, `TODO`, unstated defaults, and unresolved references
- inconsistent terms for the same actor, object, state, or event

A signal becomes a failure only when it creates an observable defect at the requirement's level.

## Repair Rules

1. Preserve the source identifier and record the original wording when auditability matters.
2. Preserve a valid requirement level. When an abstraction mismatch exists, retain the original and propose relabeling or decomposition separately.
3. Express the obligation with actor or subject, trigger or condition, behavior, and result when applicable.
4. Separate acceptance evidence from the requirement when combining them would obscure the obligation.
5. Split only independently variable obligations.
6. Remove an implementation choice only when evidence shows it is unnecessary or conflicts with the intended level. When authority is missing, preserve the choice and ask for the governing source.
7. Never invent thresholds, scope, actors, owners, dates, priorities, or failure behavior.
8. Label unsupported improvements as proposed and pair them with the decision needed.
9. Keep deferred design decisions distinct from current defects.
10. Re-run the applicable checks after rewriting.
