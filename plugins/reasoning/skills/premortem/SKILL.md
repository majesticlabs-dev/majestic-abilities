---
name: premortem
description: Run a prospective-hindsight premortem on a concrete plan or costly decision and convert plausible failure stories into safeguards. Use before launches, hires, partnerships, product bets, migrations, or other commitments with meaningful downside.
---

# Premortem

Assume a concrete plan has already failed, then work backward to identify how it happened and what should change before commitment.

## Boundary

Use this skill when the plan is specific enough to name its owner, affected people, intended outcome, and time horizon.

- Use `devils-advocate` when choosing among competing approaches.
- Use `reasoning-verifier` to trace a completed analysis back to its original conditions.
- Use ordinary plan review for low-cost implementation gaps.
- Skip premortems for vague ideas, factual questions, or decisions that can no longer change.

## Context Threshold

Before starting, establish:

1. What is being attempted?
2. Who owns it and who is affected?
3. What does success mean?
4. What is the relevant time horizon?
5. What costs, trust, safety, or reversibility constraints matter?

Ask only for missing context that would materially change the analysis.

## Workflow

### 1. Set the frame

State the premise using the plan's actual horizon:

```text
It is [time horizon] from now. [Plan] failed. We are explaining how it happened.
```

Keep the frame fixed throughout the analysis.

### 2. Generate specific failure stories

List plausible reasons the plan failed. Consider only relevant dimensions:

- demand, adoption, or behavior
- execution capacity and ownership
- technical reliability and data integrity
- operations, support, and incident response
- economics and cash exposure
- vendors, partners, and external dependencies
- security, privacy, legal, or reputation risk
- incentives, communication, and decision latency

A useful failure mode names a mechanism and consequence. Reject generic entries such as "poor execution."

### 3. Deepen each material failure

For each material failure mode, record:

- **Failure story:** how events unfolded
- **Underlying assumption:** what had to be false
- **Early warning signs:** observable leading indicators
- **Impact:** what was lost or damaged
- **Current control:** what already reduces the risk

Keep failure stories independent before synthesis so one narrative does not crowd out the others.

### 4. Prioritize

Classify each failure mode by:

- likelihood
- impact
- detectability before severe damage
- reversibility

Do not multiply ordinal scores into fake precision. Use the dimensions to identify:

- most likely failure
- most damaging failure
- hardest failure to detect
- shared hidden assumption

### 5. Revise the plan

Map every material failure mode to one of:

- prevention
- early detection
- containment
- rollback or exit
- explicit acceptance

Prefer small, testable safeguards. Name an owner, timing, and evidence for each plan revision.

### 6. Define commitment checks

Create three to seven checks that must pass before commitment. Include stop conditions for risks that cannot be eliminated.

## Output

```markdown
# Premortem

## Frame
It is [time horizon] from now. [Plan] failed.

## Failure Modes
### [Failure mode]
- Story: ...
- Assumption: ...
- Warning signs: ...
- Impact: ...
- Current control: ...

## Synthesis
- Most likely failure: ...
- Most damaging failure: ...
- Hardest to detect: ...
- Shared hidden assumption: ...

## Revised Plan
| Failure mode | Revision | Owner | Timing | Evidence |
| --- | --- | --- | --- | --- |

## Commitment Checks
- [ ] ...

## Stop Conditions
- ...
```

Persist the report only when requested or when the user supplied an output path.

## Quality Gate

- Every failure story is specific to the actual plan.
- Assumptions and warning signs are observable.
- Recommendations map directly to failure modes.
- Safeguards include owners and evidence.
- The analysis changes the plan rather than merely describing risk.
