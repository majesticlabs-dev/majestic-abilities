---
name: implementation-planning
description: Create an implementation plan grounded in the existing repository, with explicit scope, ordered changes, risks, and verification. Use when a feature, fix, migration, or refactor needs an executable technical plan before code changes begin.
---

# Implementation Planning

Turn an approved goal into the smallest executable technical plan supported by the real codebase.

## Boundary

Use this skill to author a plan. Use `plan-review` when an existing plan should be challenged for readiness, missing flows, or unnecessary scope.

Do not implement the plan unless the user explicitly asks for implementation.

## Required Inputs

Establish:

- goal and user-visible outcome
- scope, non-goals, and constraints
- acceptance criteria
- current repository state and relevant guidance
- rollout, compatibility, or deadline constraints

Ask only questions whose answers would materially change the plan. Record lesser uncertainty as assumptions.

## Workflow

1. Inspect the current code paths, tests, configuration, documentation, and existing abstractions related to the request.
2. Restate the problem and acceptance criteria in verifiable terms.
3. Identify the smallest change that satisfies the goal. Reuse existing patterns before proposing new layers or dependencies.
4. Trace affected callers, consumers, persistence, external integrations, permissions, background work, and operational surfaces.
5. Assess change risk from the proposed behavior, not from filenames. Trace affected contracts through static and dynamic dependents, registrations, shared state, and operational surfaces, then account for relevant criticality and cross-cutting failure modes. For each material risk, name the triggering step or path, plausible failure and consequence, evidence strength, and mitigation or verification. Omit generic risks with no concrete path. Mark evidence gaps rather than calling an area safe because it has few static references or existing tests.
6. Divide the work into ordered, independently understandable steps. Name the likely files or subsystems and the observable result of each step.
7. Include required tests with the behavior or regression each test proves.
8. Address migrations, compatibility, deployment ordering, feature flags, rollback, monitoring, and cleanup only when the change actually requires them.
9. Verify current third-party APIs, platform behavior, or standards when the plan depends on them.
10. End with exact verification commands or checks supported by the repository.

## Step Standard

Every implementation step should state:

- purpose
- files or subsystem affected
- concrete change
- dependencies on earlier steps
- verification or acceptance evidence

Do not leave material design choices as “figure out during implementation.”

## Output

1. **Goal and acceptance criteria**
2. **Scope and non-goals**
3. **Current-state findings**
4. **Assumptions and unresolved decisions**
5. **Ordered implementation steps**
6. **Change risk, evidence gaps, migration, and rollback notes**
7. **Verification plan**

## Quality Gate

Before returning the plan, confirm that:

- every step maps to the stated goal
- consuming code and integration points are covered
- change risk follows the proposed behavior through static and dynamic paths
- risky paths have verification
- no unnecessary abstraction or speculative scope was introduced
- a different engineer could execute the plan without inventing major decisions
