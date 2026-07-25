---
name: devils-advocate
description: Pressure-test a preferred approach by exposing hidden assumptions, opportunity costs, confidence gaps, and conditions that favor alternatives. Use when choosing an architecture, tool, strategy, or costly commitment before the decision is locked in.
---

# Devil's Advocate

Challenge the preferred option honestly before commitment. The goal is a stronger decision, not performative disagreement.

## Boundary

Use this skill when multiple approaches remain possible and choosing poorly has meaningful cost or lock-in.

- Use `premortem` when a concrete plan needs prospective failure analysis.
- Use `reasoning-verifier` after a completed recommendation needs traceability checking.
- Skip this workflow for mechanical work or decisions the user has explicitly closed.

## Inputs

Identify:

1. The decision being made.
2. The currently preferred option and why it is attractive.
3. Credible alternatives.
4. Constraints, evidence, and irreversible costs.
5. The decision deadline and ability to reverse course.

Mark missing facts rather than silently filling them in.

## Workflow

### 1. State the commitment

Restate the preferred option, intended outcome, and strongest evidence supporting it.

### 2. Steel-man the opposition

Build the strongest case against the preferred option. Examine:

- unsupported assumptions
- edge cases and adoption failure
- operational and maintenance burden
- security, privacy, legal, or trust exposure
- opportunity cost
- incentives that could distort behavior
- dependency and lock-in risk
- conditions that make another option better

Include at least one non-obvious failure mode. Do not invent remote objections merely to lengthen the list.

### 3. Separate evidence from uncertainty

Classify each objection as:

- **Verified:** supported by available evidence
- **Plausible:** credible but not yet verified
- **Speculative:** possible but too weak to drive the decision

State what evidence would confirm or refute every material plausible objection.

### 4. Resolve the objections

For each verified or material plausible objection:

- defend the preferred option with evidence
- modify the approach
- add a reversible experiment, safeguard, monitor, or exit condition
- change the recommendation when the objection holds

Every mitigation must map to a specific objection.

### 5. Reassess the choice

Compare the revised preferred option with credible alternatives using the original constraints. Do not preserve the initial recommendation merely for consistency.

## Confidence Requests

Do not promise literal certainty for open-world decisions. When asked for complete confidence or every loophole:

1. Define what must be true for the decision to be acceptable.
2. List which conditions were verified.
3. Identify unresolved uncertainty.
4. Add monitoring or kill conditions where uncertainty cannot be removed.
5. Return `High`, `Medium`, or `Low` confidence with reasons.

## Output

```markdown
## Decision Pressure Test

### Preferred Option
[Option, intended outcome, and supporting evidence]

### Strongest Case Against It
| Objection | Status | Evidence needed | Consequence |
| --- | --- | --- | --- |

### Alternatives Favored Under These Conditions
- [Alternative]: [conditions]

### Resolution
- [Defended, modified, tested, or rejected objection]

### Verdict
[Keep, modify, test first, or reject]

### Assumptions and Exit Signals
- Assumption: ...
  Exit signal: ...

### Confidence
High | Medium | Low: [reason]
```

## Quality Gate

- The critique attacks the strongest version of the option.
- Material objections are evidence-labeled.
- Opportunity cost and reversibility are explicit.
- Mitigations map to objections.
- The final recommendation is allowed to change.
