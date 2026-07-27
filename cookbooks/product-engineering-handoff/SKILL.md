---
name: product-engineering-handoff
description: "Turn an approved product direction into an evidence-grounded PRD, a repository-specific implementation plan, and a reviewed engineering handoff. Use when the user invokes /product-engineering-handoff or asks to prepare a product decision for engineering without implementing it."
---

# Product Engineering Handoff

Prepare the approved product direction described in $ARGUMENTS for engineering. Complete the phases in order and stop before implementation.

## Phase 1: Confirm The Direction

Confirm that the problem, target user, intended outcome, scope boundary, and decision owner are sufficiently stable to specify. If the core direction is still being explored, return `BLOCKED` with the unresolved decisions instead of inventing requirements.

## Phase 2: Write The Product Requirements

Invoke the `product-requirements` skill.

Produce the smallest PRD that defines:

- problem and evidence
- target users and current workaround
- goals, non-goals, and v1 exclusions
- primary flows and important failure, permission, cancellation, retry, and recovery states
- numbered behavioral requirements with acceptance checks
- success measures, constraints, dependencies, risks, and open decisions

Do not prescribe technical architecture unless an approved product constraint requires it.

## Phase 3: Build The Implementation Plan

Invoke the `implementation-planning` skill. Inspect the actual repository before proposing changes.

Translate the approved PRD into:

- current-state findings
- the smallest sufficient change
- ordered implementation steps tied to requirements
- affected files, integrations, consumers, persistence, permissions, and operational surfaces
- tests and verification evidence
- migration, rollout, compatibility, monitoring, and rollback work only when required

Do not leave material design choices for the implementer to discover.

## Phase 4: Review The Handoff

Invoke the `plan-review` skill against both the PRD and implementation plan.

The review must check:

- requirement-to-plan traceability
- missing user flows, dependencies, or integration work
- risky assumptions and unresolved decisions
- unnecessary scope or abstractions
- test, rollout, and verification gaps

Apply concrete corrections once. If a material decision still requires an owner, return `BLOCKED` rather than cycling indefinitely.

## Phase 5: Report

Return:

1. PRD
2. implementation plan
3. review verdict: `READY` or `BLOCKED`
4. unresolved decisions with owners
5. verification commands or checks
6. explicit statement that implementation has not started

## Requires

- `product-requirements` - Phase 2 product behavior and acceptance contract
- `implementation-planning` - Phase 3 repository-grounded technical plan
- `plan-review` - Phase 4 independent handoff-readiness review

Install everything:

```sh
npx skills add OWNER/REPOSITORY --skill product-engineering-handoff \
  product-requirements implementation-planning plan-review \
  --agent claude-code --yes
```

## Hard Gates

- Do not plan implementation without an approved direction and named decision owner.
- Do not mark the handoff ready while core behavior, scope, permissions, or acceptance criteria remain unresolved.
- Every behavioral requirement must map to an acceptance check and at least one implementation or verification step.
- The implementation plan must be grounded in the real repository and name supported verification commands or checks.
- `plan-review` must find no blocking readiness issue before the final verdict can be `READY`.

Back these gates with the consuming team's document approval or issue workflow. This cookbook does not implement code or create a mechanical CI gate by itself.
