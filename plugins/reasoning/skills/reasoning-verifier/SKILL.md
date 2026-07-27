---
name: reasoning-verifier
description: Verify a completed analysis by tracing original requirements, evidence, and assumptions into its conclusion. Use when reviewing a consequential recommendation, diagnosis, comparison, or decision for omitted constraints, invented premises, or unsupported logical steps.
---

# Reasoning Verifier

Check whether a completed analysis answers the original problem using supported conditions and a valid chain from evidence to conclusion.

## Boundary

Use this skill after an analysis or recommendation exists.

- Use `devils-advocate` before choosing among competing options.
- Use `premortem` to expose how a concrete plan could fail.
- Do not replace domain verification, tests, or primary-source research with reasoning review.
- Skip this workflow for low-stakes conclusions or ones that are cheap to reverse.

Scale the depth of the matrix and the assumption audit to the cost of being wrong.

## Inputs

Gather:

1. The original request, requirements, or decision criteria.
2. The completed analysis and conclusion.
3. Evidence or source material the analysis claims to use.
4. Known constraints on scope, time, cost, or risk.

Missing inputs narrow the verification rather than block it. State what cannot be verified.

Source material is frequently unavailable. Without it, still check internal consistency, traceability, and premise classification, and record every citation that cannot be opened as **Unknown** in step 4.

## Workflow

### 1. Extract original conditions

List separately:

- explicit requirements
- explicit facts
- constraints and exclusions
- success criteria
- user preferences
- unresolved questions

Do not convert preferences into hard requirements or inferred context into fact.

### 2. Reconstruct the proposed reasoning

Write the chain as:

```text
Evidence and premises -> intermediate claims -> conclusion
```

Reconstruct the strongest version the text supports. When a step admits a valid reading, use it. Include implicit premises required for the conclusion to follow.

### 3. Build a traceability matrix

For every original condition, record its treatment, supporting evidence, and status.

| Original condition | Treatment in analysis | Supporting evidence | Status |
| --- | --- | --- | --- |

Status is `addressed`, `omitted`, `contradicted`, or `unverifiable`.

A condition is not addressed merely because the analysis repeats its wording.

### 4. Audit assumptions

Classify each premise as:

- **Given:** explicit in the original material
- **Verified:** supported by cited evidence
- **Deduced:** follows logically from supported premises
- **Invented:** required by the solution but unsupported
- **Unknown:** cannot be checked from available evidence

Call out assumptions that materially affect the conclusion.

### 5. Test the logical chain

Check for:

- conclusion drift from the original question
- missing alternatives
- correlation treated as causation
- universal claims from narrow evidence
- inconsistent standards between options
- circular support
- hidden value judgments
- certainty stronger than the evidence
- recommendations that do not solve the diagnosed problem

Report only gaps the text actually contains. An empty finding list is a valid result. Do not promote wording or presentation issues to logical gaps in order to fill a section.

### 6. Test conclusion sensitivity

Ask whether correcting each major issue would:

- preserve the conclusion
- narrow or qualify it
- reverse it
- make the result unknown

Do not rewrite the analysis when the available evidence cannot support a corrected conclusion.

## Severity

Assign severity from the sensitivity outcome:

- **Critical:** reverses the conclusion or makes the result unknown
- **Major:** narrows or qualifies the conclusion, or removes its support
- **Minor:** affects rigor or presentation while the conclusion holds

## Output

```markdown
# Verification Report

## Verdict
Sound | Sound with qualifications | Sound conclusion from unsound reasoning | Materially flawed | Unverifiable

## Original Conditions
- ...

## Reasoning Chain
...

## Traceability Matrix
| Condition | Treatment | Evidence | Status |
| --- | --- | --- | --- |

## Unsupported or Missing Premises
- [Severity]: ...

## Logical Gaps
- [Severity]: ...

## Conclusion Sensitivity
- ...

## Corrected Conclusion
[Restated result, `Unchanged` when nothing material was found, or `Unknown` with the evidence required]
```

A corrected conclusion restates the result within the evidence already present. It is not fresh analysis.

When the conclusion survives but the chain supporting it does not, report the broken reasoning as a finding. It will not hold on the next case.

Persist the report only when requested or when the user supplied an output path.

## Quality Gate

- Every original condition appears in the traceability matrix.
- The reconstruction uses the strongest reading the text supports.
- Evidence and assumptions are not conflated.
- Logical deductions are shown rather than asserted.
- Status and severity use the defined vocabularies.
- Findings are real rather than manufactured to fill a section.
- Unknowns remain unknown.
