---
name: marketing-plan
disable-model-invocation: true
description: "Create an organic marketing plan and assess paid-spend readiness."
metadata:
  requires: "editorial-planning,social-content,newsletter-editorial,growth-experimentation"
---

# Marketing Plan

Run this user-invoked cookbook to prepare an organic marketing plan and decide whether a bounded paid test is justified. Select channels from audience evidence, stage, capacity, and economics. Organic traction is useful evidence but is not a universal prerequisite for paid work. The default output is planning, drafts, and measurement design. It does not publish, send, configure campaigns, or spend.

## Operating Contract

- Establish the business outcome, target audience, offer, stage, current evidence, channel access, production capacity, budget constraints, owner, and permission boundary.
- Keep observed results, partial or stale data, hypotheses, and unavailable inputs separate. Do not invent reach, engagement, subscriber, conversion, or revenue results.
- Choose only channels that the target audience uses or where the team has credible access and capacity. Social and newsletter work is conditional; do not add either to fill a calendar.
- Keep editorial value, promotion, and paid acquisition separate. Every material claim needs a source or an explicit evidence label.
- Treat paid spend as a decision with a bounded learning purpose, measurement plan, budget authority, and stop or review conditions. This cookbook never grants spending authority.

## Phase 1: Set The Audience And Content Decision

Invoke the `editorial-planning` skill with the business outcome, audience questions, offer, available channels, planning horizon, content pillars, source material, proof, capacity, and recent performance signals.

Constrain its output to:

- a signal log linked to the audience behavior the plan may influence
- a ranked organic idea backlog with evidence, strategic role, effort, and shelf life
- killed or deferred ideas with reasons
- a production plan that fits the stated capacity and has a review trigger

Do not turn a topic score into a forecast of reach, demand, or revenue.

## Phase 2: Add Only Relevant Channel Work

If a professional social platform is a supported channel for the audience and goal, invoke the `social-content` skill. Pass the platform, account, audience, source material, proof, voice, capacity, desired action, and permission boundary. Verify current platform limits and policy constraints, and keep posts or threads as drafts unless publishing is separately authorized.

If a recurring newsletter is an appropriate channel and an owned audience, editorial promise, sources, and sending owner exist, invoke the `newsletter-editorial` skill. Keep its edition, links, source notes, and feedback loop as drafts. Do not invent a subscriber list, deliverability result, sending configuration, or compliance completion.

If either channel is not supported by evidence or capacity, record it as unselected with the missing condition. Use the editorial plan for other organic formats that fit the request instead of forcing social or email output.

## Phase 3: Design The Learning Loop

Invoke the `growth-experimentation` skill for the selected organic test and, when useful, the proposed paid test. Define one decision, one primary variable per experiment, a control or comparison, instrumentation, primary metric, guardrails, contamination risks, cost, and decision rules. Use the user's measurement window or leave timing unresolved. Low-volume results remain provisional, and no winner is declared from inadequate evidence.

## Phase 4: Make The Paid-Spend Decision

Evaluate paid work against:

- clarity of the target audience, problem, offer, and conversion path
- evidence of activation, retention, payment, or another business outcome
- unit economics, allowable acquisition cost, margin, and available budget
- targeting access, platform constraints, attribution quality, and operational capacity
- the purpose of the test, what would change the decision, and who owns approval

Return one of these planning decisions, with evidence and unknowns:

- **Run a bounded paid test:** the learning question is clear, the offer and measurement path are usable, the budget boundary is supplied or approved, and guardrails and stop conditions are explicit.
- **Defer paid:** a material readiness, economics, targeting, measurement, or capacity gap should be resolved first.
- **Insufficient evidence:** the request does not support either decision; list the smallest evidence-gathering step.

Do not require a fixed customer count, a fixed period of organic traction, or a universal organic-before-paid sequence. If paid is recommended before organic traction, state why the bounded test is justified. Preserve an explicitly approved budget and its limits; mark only an unapproved budget or a proposed increase as awaiting approval. The recommendation does not execute the test.

## Report

Return:

1. objective, audience, stage, constraints, owner, and permission boundary
2. evidence baseline and coverage limits
3. organic signal log, ranked ideas, killed ideas, selected channels, and production plan
4. social or newsletter output only when its channel conditions are met
5. experiment specifications, instrumentation, metrics, guardrails, and decision rules
6. paid-spend decision, evidence, assumptions, budget boundary and approval status, stop conditions, and approval owner
7. status as planned or prepared, with no claim of publication, sending, configuration, or spend

## Installation

Install the cookbook and its dependencies:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill marketing-plan \
  editorial-planning social-content newsletter-editorial growth-experimentation
```

## Hard Gates

- Do not select a channel without audience, goal, evidence, and capacity support.
- Do not force social or newsletter work when its channel conditions are absent.
- Do not recommend paid spend without a bounded learning purpose, measurement path, economics or explicit unknowns, budget boundary, and approval owner.
- Do not make organic traction a universal paid gate, and do not use paid spend to hide an undefined audience or offer.
- Do not claim causal lift, a winning variant, or a business result from inadequate or unfinalized evidence.
- Do not publish, send, configure, or spend from this cookbook.
