---
name: plan-review
description: "Review implementation plans and feature specifications for missing flows, risky assumptions, unnecessary complexity, and verification gaps. Use when a plan exists and should be challenged before implementation starts."
---

# Plan Review

Use this skill when a plan exists but implementation has not started.

## Review Goals

- Confirm the goal and acceptance criteria are explicit and testable.
- Check that each implementation step maps to the goal.
- Identify missing dependencies, integrations, migrations, or operational work.
- Challenge unnecessary abstractions, extra files, or scope creep.
- Surface failure modes, rollback concerns, and verification gaps.
- Trace each user flow through success, invalid input, cancellation, retry, and permission boundaries.

## Review Workflow

1. Read the plan and the existing code or docs it depends on.
2. Restate the goal, scope boundaries, and assumptions in plain language.
3. Break the plan into ordered steps and map each step to an acceptance criterion.
4. List distinct user flows, actors, triggers, expected outcomes, and failure paths.
5. Check cross-cutting concerns:
   - auth and permissions
   - data shape, migrations, and rollback
   - external APIs and version-sensitive dependencies
   - observability, logging, and alerting
   - performance, caching, and background work
   - testing strategy and verification commands
6. Ask whether an existing flow already solves part of the problem.
7. Recommend the smallest change set that still satisfies the goal.

## Common Failure Modes

- A step says "figure out" instead of making a decision.
- The plan touches many files without explaining why each one is necessary.
- Data migrations or indexes are omitted even though behavior changes depend on them.
- New interfaces are introduced without describing consuming code changes.
- External services or library behavior are assumed without checking current docs.
- Testing covers the happy path only and ignores rollback, retries, or permission failures.

## Output

Return a concise markdown review with:

1. **Viability**: ready, risky, or blocked.
2. **Critical issues**: items that should be fixed before implementation.
3. **Missing considerations**: important but non-blocking gaps.
4. **Simpler path**: smaller solution if the plan is overbuilt.
5. **Recommended edits**: concrete plan changes.
6. **Verification**: what should prove the plan worked once implemented.

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
