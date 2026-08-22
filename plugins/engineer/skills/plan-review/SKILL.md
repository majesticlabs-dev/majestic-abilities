---
name: plan-review
description: "Review implementation plans, PRDs, brainstorm handoffs, and feature specifications as whole delivery artifacts for implementation readiness. Use when flows, sequencing, dependencies, scope, operational risk, or verification should be challenged before handoff. Not for a dedicated requirement-statement or requirements-catalogue quality audit."
---

# Plan Review

Use this skill when a planning document exists but implementation has not started or whole-document handoff readiness needs review. Do not use it for a dedicated requirement-statement or requirements-catalogue quality audit when implementation flow, dependencies, and delivery risk are outside the request.

## Review Goals

- Confirm the goal and acceptance criteria are explicit and testable.
- Check that each implementation step maps to the goal.
- Identify missing dependencies, integrations, migrations, or operational work.
- Challenge unnecessary abstractions, extra files, or scope creep.
- Surface failure modes, rollback concerns, and verification gaps.
- Assess change risk from intended behavior and affected contracts, not file type or apparent isolation.
- Trace each user flow through success, invalid input, cancellation, retry, and permission boundaries.
- Apply the requested scope posture without changing scope silently.

## Scope Posture

Establish the review posture when scope is part of the question:

- **Hold:** Treat current scope as fixed and improve its delivery readiness.
- **Reduce:** Find the smallest version that still achieves and proves the stated outcome.
- **Consider expansion:** Keep current scope as the baseline, then present only additions with a clear user or operational benefit.

Infer the posture only from an explicit request such as "hold scope," "simplify this," or "think bigger." Otherwise default to Hold. Ask one question only when the choice would materially change the review.

For Reduce or Consider expansion, compare two or three materially different approaches when alternatives exist. Include the smallest sufficient approach and the strongest justified design, with concrete tradeoffs. Recommend one based on the stated outcome, not ambition or implementation volume.

Do not add or remove material scope without user approval. Separate proposed changes from readiness defects in the current plan. Reject speculative features, mandatory ceremony, and exhaustive artifacts that do not help satisfy or prove the outcome.

## Document Readiness

Identify the document type and intended next phase before judging it. Use [document-readiness.md](references/document-readiness.md) for type-specific requirements and vague language patterns.

Assess:

- clarity
- completeness for the next consumer
- specificity
- scope discipline
- intent fidelity to the original request

Separate blocking decisions from polish. Do not average away a blocker with a readiness score.

## Review Workflow

1. Read the document and the existing code or source material it depends on.
2. Identify its type, intended next phase, and document readiness requirements.
3. Restate the goal, scope boundaries, assumptions, and unresolved decisions in plain language.
4. Flag vague language when it hides behavior, thresholds, ownership, or acceptance criteria.
5. Break the plan into ordered steps and map each step to an acceptance criterion.
6. List distinct user flows, actors, triggers, expected outcomes, and failure paths.
7. Assess change risk from intended behavior, affected contracts, static and dynamic dependents, side effects, criticality, and the cross-cutting concerns below. For each material risk, require a triggering planned step or path, plausible failure and consequence, evidence strength, and mitigation or verification. Reject generic risk lists and keep missing evidence visible.
8. Check cross-cutting concerns:
   - auth and permissions
   - data shape, migrations, and rollback
   - external APIs and version-sensitive dependencies
   - observability, logging, and alerting
   - performance, caching, and background work
   - testing strategy and verification commands
9. Ask whether an existing flow already solves part of the problem.
10. Apply the selected scope posture:
   - Hold: recommend the smallest corrections needed to make the current plan ready.
   - Reduce: identify removable work and show that the reduced plan still satisfies each acceptance criterion.
   - Consider expansion: review the baseline first, then list optional additions separately with benefit, cost, risk, and effect on acceptance criteria.
11. Require explicit approval before incorporating a material scope change into the reviewed plan.

## Common Failure Modes

- A step says "figure out" instead of making a decision.
- The plan touches many files without explaining why each one is necessary.
- Data migrations or indexes are omitted even though behavior changes depend on them.
- New interfaces are introduced without describing consuming code changes.
- External services or library behavior are assumed without checking current docs.
- Testing covers the happy path only and ignores rollback, retries, or permission failures.

## Output

Return a concise markdown review with:

1. **Document readiness**: document type plus ready or needs revision.
2. **Viability**: ready, risky, or blocked.
3. **Critical issues**: items that should be fixed before implementation or handoff.
4. **Missing considerations**: important but non-blocking gaps.
5. **Scope recommendation**: hold, reduce, or optional expansions, with material scope changes still pending approval.
6. **Simpler path**: smaller solution if the plan is overbuilt.
7. **Recommended edits**: concrete plan changes.
8. **Verification**: what should prove the plan worked once implemented.

## Thorough Mode

For a high-risk or cross-cutting plan, also return:

- **Scope challenge:** what already exists, the smallest sufficient change, and work that can defer.
- **Path-to-test map:** each new user or data path, branches, failure mode, and planned coverage.
- **Change-risk map:** affected contracts, static and dynamic dependents, criticality, evidence gaps, controls, rollout, and rollback.
- **Deferred work:** explicitly out-of-scope follow-ups with rationale and prerequisites.
- **Unresolved decisions:** choices that still need an owner or would materially change implementation.

Use this mode only when risk justifies the extra surface. Do not impose mandatory interactive pauses
when a concise review is sufficient.

## Standards

- Only flag real risks.
- Prefer concrete fixes over generic advice.
- When the plan depends on unstable external behavior, check current primary documentation before finalizing the review.
