---
name: product-requirements
description: Write an evidence-grounded product requirements document with users, scope, requirements, acceptance checks, success measures, risks, and unresolved decisions. Use when an approved product direction needs a PRD for implementation, stakeholder review, or delivery handoff.
---

# Product Requirements

Create the smallest PRD that makes the product decision, expected behavior, and success criteria unambiguous.

## Boundary

Use `feature-brief` when the problem, options, or recommendation are still being explored. Use this skill when the direction is sufficiently stable to define implementation-ready product requirements.

A PRD defines the product outcome and behavioral contract. It should not prescribe technical architecture unless a technical constraint is part of the approved product decision.

## Required Inputs

Establish:

- problem, evidence, and why it matters now
- target users and current workaround
- approved direction and decision owner
- scope constraints, dependencies, and required date if any
- baseline and intended product or business outcome

Ask only for missing decisions that materially change scope or behavior. Mark unsupported claims and unknowns instead of inventing them.

## Workflow

1. Separate the observed user problem from the proposed solution.
2. Define target users, relevant segments, non-users, and the current journey or workaround.
3. State goals, non-goals, v1 scope, and explicit exclusions.
4. Describe the primary user flows and important invalid, empty, permission, cancellation, retry, and recovery states.
5. Write numbered requirements as observable behavior. Give each requirement a concrete acceptance check.
6. Identify data, privacy, accessibility, legal, operational, support, and dependency constraints that materially affect the product behavior.
7. Define success measures with a baseline, target rationale, measurement window, owner, and guardrails.
8. Record risks, assumptions, unresolved decisions, and what evidence would resolve them.
9. Remove speculative future scope and implementation detail that does not constrain the product decision.

## Requirement Standard

Each requirement should be:

- necessary for a stated goal
- specific about actor, trigger, behavior, and result
- testable through an acceptance check
- clear about permissions and failure behavior when relevant
- independent of an unapproved implementation choice

Use `must`, `should`, and `may` consistently when priority distinctions are needed.

## Output

1. **Problem and evidence**
2. **Target users and current workaround**
3. **Goals and non-goals**
4. **V1 scope and exclusions**
5. **User flows and edge states**
6. **Numbered requirements with acceptance checks**
7. **Success measures and guardrails**
8. **Constraints and dependencies**
9. **Risks, assumptions, and open decisions**
10. **Decision owner and next handoff**

## Quality Gate

The PRD is ready when:

- every requirement traces to a user need or explicit constraint
- v1 exclusions prevent obvious scope ambiguity
- critical failure and permission states are defined
- success can be measured without inventing a future baseline
- unresolved decisions are visible and assigned
- implementation can begin without guessing core product behavior
