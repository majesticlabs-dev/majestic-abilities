# Document Readiness Reference

Use these checks according to the document's type and intended next phase. Early exploration may contain open questions. A handoff document must expose or resolve them.

## Readiness Dimensions

| Dimension | Question |
| --- | --- |
| Clarity | Can a reader explain the goal and decisions without interpretation? |
| Completeness | Does the document contain what its next consumer needs? |
| Specificity | Are behavior, boundaries, and evidence concrete? |
| Scope discipline | Does included work map to the stated objective? |
| Intent fidelity | Does the proposal still solve the original request? |

Use scores only when comparison is useful. Blocking findings matter more than an average score.

## Brainstorm Handoff

Expected:

- problem and affected user
- distinct approaches
- constraints and boundaries
- recommendation or explicit decision still needed
- concrete next step

Block handoff when the problem is only a symptom, approaches are cosmetic variations, or the next step is merely "think more."

## Implementation Plan

Expected:

- goal and testable acceptance criteria
- affected components or files with purpose
- ordered implementation steps
- dependencies and sequencing
- failure and rollback behavior
- verification strategy
- explicit scope boundary

Block implementation when a step says "figure out how," consuming code is unaccounted for, or behavior changes lack acceptance criteria.

## PRD or Feature Specification

Expected:

- problem and user impact
- target users or actors
- important flows and acceptance criteria
- priorities
- measurable success criteria
- explicit exclusions
- unresolved decisions and owners

Block handoff when required behavior is subjective, success cannot be measured, or scope boundaries remain implicit.

## Vague Language

Flag these when they hide a missing decision:

| Pattern | Missing information |
| --- | --- |
| appropriate or properly | The actual standard or behavior |
| as needed | Trigger and decision owner |
| various, some, or relevant | Named scope or quantity |
| handle errors appropriately | Error cases, response, and recovery |
| consider performance | Workload and measurable target |
| may need to | Decision, spike, owner, and deadline |
| TBD or TODO | Resolution or explicit tracked deferral |
| similar to X | Exact shared behavior and differences |
| good user experience | Observable usability criteria |
| scalable solution | Expected scale and resource constraints |
| clean architecture | Concrete boundaries and dependencies |

Do not flag responsible uncertainty in risk sections, explicit deferrals with owners, options analysis, or named spikes with a decision question.

## Blocking Versus Polish

Treat as blocking:

- missing information required by the next phase
- unresolved decisions disguised as implementation steps
- contradictions with the original request
- untestable acceptance criteria
- scope expansion without justification
- absent owner for a consequential decision

Treat wording and formatting improvements as polish when they do not change interpretation or execution.
