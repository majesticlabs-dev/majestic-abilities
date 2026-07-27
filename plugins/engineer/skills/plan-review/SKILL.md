---
name: plan-review
description: "Review implementation plans, PRDs, brainstorm handoffs, and feature specifications for readiness, missing flows, risky assumptions, unnecessary scope, and verification gaps. Use when a planning document should be challenged before implementation or handoff."
---

# Plan Review

Use this skill when a planning document exists but implementation has not started or handoff readiness needs review.

## Review Goals

- Confirm the goal and acceptance criteria are explicit and testable.
- Check that each implementation step maps to the goal.
- Identify missing dependencies, integrations, migrations, or operational work.
- Challenge unnecessary abstractions, extra files, or scope creep.
- Surface failure modes, rollback concerns, and verification gaps.
- Trace each user flow through success, invalid input, cancellation, retry, and permission boundaries.

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
7. Check cross-cutting concerns:
   - auth and permissions
   - data shape, migrations, and rollback
   - external APIs and version-sensitive dependencies
   - observability, logging, and alerting
   - performance, caching, and background work
   - testing strategy and verification commands
8. Ask whether an existing flow already solves part of the problem.
9. Recommend the smallest change set that still satisfies the goal.

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
5. **Simpler path**: smaller solution if the plan is overbuilt.
6. **Recommended edits**: concrete plan changes.
7. **Verification**: what should prove the plan worked once implemented.

## Thorough Mode

For a high-risk or cross-cutting plan, also return:

- **Scope challenge:** what already exists, the smallest sufficient change, and work that can defer.
- **Path-to-test map:** each new user or data path, branches, failure mode, and planned coverage.
- **Deferred work:** explicitly out-of-scope follow-ups with rationale and prerequisites.
- **Unresolved decisions:** choices that still need an owner or would materially change implementation.

Use this mode only when risk justifies the extra surface. Do not impose mandatory interactive pauses
when a concise review is sufficient.

## Standards

- Only flag real risks.
- Prefer concrete fixes over generic advice.
- When the plan depends on unstable external behavior, check current primary documentation before finalizing the review.
