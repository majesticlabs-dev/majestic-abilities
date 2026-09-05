---
name: founder-plan-review
description: "Use when a founder asks to think bigger, rethink a plan, test whether it is ambitious enough, hold scope while increasing rigor, selectively consider expansion, or reduce an overbuilt plan. Not for authoring an implementation plan or checking engineering handoff readiness alone."
---

# Founder Plan Review

Review an existing plan as a consequential founder decision. Challenge both underreach and excess. Do not treat more scope as better by default.

## Boundary

This skill owns the plan's premise, scope posture, strategic leverage, user value, future direction, and executive execution risk. It can examine technical detail because technical failure can invalidate the plan.

Do not implement, edit the plan, write TODO files, or change repository files. Return proposed changes and scope decisions for the user to approve. Use an engineering implementation-readiness review when the question is only whether a handoff is complete and executable. Use a company-strategy workflow when the user needs to create medium- or long-term direction rather than review a concrete plan.

## Required Inputs

Establish:

- artifact under review and its decision owner
- intended user and business outcome
- current scope, exclusions, constraints, and deadline
- evidence behind the problem and proposed direction
- available people, money, capabilities, and operating capacity
- current system or company state relevant to the plan
- prior decisions, committed work, dependencies, and known risks
- desired review posture, when already chosen

Preserve supplied facts. Mark missing evidence `Unknown`. Ask only when the answer would change the scope posture, recommendation, or verdict.

## Review Postures

Choose the posture before posture-specific analysis. If the user did not choose one and the choice would materially change the review, ask.

1. **Expand:** Explore a materially more valuable version. Every addition requires explicit approval.
2. **Selectively expand:** Hold the current plan as the baseline, then offer separate additions for approval, deferral, or rejection.
3. **Hold scope:** Keep the scope fixed and review it with maximum rigor.
4. **Reduce:** Find the smallest version that still produces and proves the core outcome.

Do not change scope silently. Preserve the selected posture, but revise the recommendation when later evidence exposes a material contradiction or unacceptable risk.

## References

Load [review-sections.md](references/review-sections.md) after the premise, alternatives, posture, and proposed scope are clear. Evaluate every section for applicability. Mark a section `Not applicable` with a reason instead of inventing findings.

## Workflow

### 1. Audit the current state

Read the complete plan and the repository or source material it depends on. Inspect relevant guidance, code, tests, architecture documents, prior design decisions, current changes, known deferred work, and recurring problem areas. State evidence gaps when repository or operating context is unavailable.

If current market, platform, legal, or technical behavior materially affects the decision, verify it with current authoritative sources. Do not send confidential plan details to an external service without permission.

### 2. Challenge the premise

State:

- the real user and business outcome
- the problem the plan claims to solve
- the evidence that the problem is material
- what happens if nothing changes
- whether the plan solves the outcome or a proxy
- what existing capability already solves part of it

Separate supported facts, assumptions, and unknowns.

### 3. Map the future state

Describe:

```text
current state -> effect of this plan -> credible 12-month state
```

Identify whether the plan creates leverage, preserves options, or introduces path dependency. Do not substitute vivid language for evidence or commitments.

### 4. Compare alternatives

When meaningful alternatives exist, compare at least two distinct approaches. Include:

- the smallest approach that produces the core outcome
- the strongest durable approach supported by current evidence
- a lateral approach only when it uses a different mechanism or reframes the problem

For each, state outcome coverage, user value, effort, risk, reversibility, displaced work, existing leverage, and the evidence that could reject it. Do not use unsupported completeness scores or implementation-time claims.

### 5. Decide scope under the selected posture

For each proposed scope change, state:

- concrete user or business benefit
- evidence and assumption
- effort and operating burden
- dependencies and risks
- effect on the core outcome
- recommendation: accept, defer, or reject

Ask for approval only when a material scope decision blocks the rest of the review. Record lesser unresolved choices in the final report.

### 6. Resolve temporal decisions

Identify decisions that an implementer or operator would otherwise discover too late. Cover foundations, core behavior, integration, verification, rollout, support, and follow-up. Resolve material ambiguity now or assign an owner and deadline.

### 7. Run the full review

Use [review-sections.md](references/review-sections.md). Review applicable architecture, failure, security, data, maintainability, verification, performance, operations, deployment, trajectory, and design concerns. Findings must name evidence, consequence, and the smallest corrective action.

### 8. Issue the verdict

Return exactly one:

- `READY`: the selected scope and direction are defensible, with no unresolved material blocker.
- `REVISE`: the premise is sound, but material scope or risk corrections are required.
- `RETHINK`: the premise, outcome path, or accepted risk is not defensible.

## Output

Return:

1. **Verdict and review posture**
2. **Premise assessment:** outcome, evidence, assumptions, do-nothing case
3. **Current-to-future map**
4. **Alternatives and recommendation**
5. **Scope decision register:** accepted, deferred, rejected, pending
6. **What already exists:** reusable capabilities and prior decisions
7. **Review findings:** grouped by every review section, with non-applicable sections identified
8. **Failure and recovery registry:** when the plan introduces fallible paths
9. **Rollout and rollback assessment**
10. **Not in scope**
11. **Unresolved decisions:** owner and deadline where known
12. **Next decision or action**

## Standards

- Review the plan, not the founder's personality.
- More ambition must produce more value through a credible mechanism.
- Focus can require expansion, reduction, or no scope change.
- Every material finding needs evidence, consequence, and a correction or decision.
- Every failure must be visible to operators. Make it visible to users when it changes their result, latency, or state.
- Do not invent method names, exception classes, metrics, thresholds, effort estimates, or risks that the available plan cannot support.
- Diagrams and registries are required only when they clarify a non-trivial flow or decision.
- Scope remains under user control.
