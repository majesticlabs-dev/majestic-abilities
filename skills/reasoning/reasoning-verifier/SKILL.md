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

## Inputs

Require:

1. The original request, requirements, or decision criteria.
2. The completed analysis and conclusion.
3. Evidence or source material the analysis claims to use.
4. Known constraints on scope, time, cost, or risk.

When any input is missing, state what cannot be verified.

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

Include implicit premises required for the conclusion to follow.

### 3. Build a traceability matrix

For every original condition, record:

| Original condition | Treatment in analysis | Supporting evidence | Status |
| --- | --- | --- | --- |
| | | | addressed, omitted, contradicted, or unverifiable |

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

### 6. Test conclusion sensitivity

Ask whether correcting each major issue would:

- preserve the conclusion
- narrow or qualify it
- reverse it
- make the result unknown

Do not rewrite the analysis when the available evidence cannot support a corrected conclusion.

## Output

```markdown
# Verification Report

## Verdict
Sound | Sound with qualifications | Materially flawed | Unverifiable

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
[Corrected result, or Unknown with required evidence]
```

Classify findings as critical, major, or minor based on whether they change the conclusion.

## Quality Gate

- Every original condition appears in the traceability matrix.
- Evidence and assumptions are not conflated.
- Logical deductions are shown rather than asserted.
- Severity reflects effect on the conclusion.
- Unknowns remain unknown.
