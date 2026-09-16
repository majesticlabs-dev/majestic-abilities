---
name: first-customers
description: "Plan first B2B customer acquisition through audience, channel, offer, and pricing decisions."
metadata:
  requires: "icp-definition,go-to-market-motion,outbound-prospecting,pricing-strategy"
---

# First Customers

Run this user-invoked cookbook to prepare a plan for acquiring first B2B customers. Use evidence and stage to choose among warm, community, and cold routes, then keep a weekly record of what was learned. The default output is a plan and reviewable drafts. It does not send outreach, publish in a community, change live pricing, or spend money.

## Operating Contract

- Establish the product or offer, stage, target scope, capacity, cash constraints, owner, and permission boundary before choosing a route.
- Label evidence as observed, partial, stale, unavailable, or hypothesized. Do not invent customer counts, deadlines, conversion rates, or demand.
- Treat the workflow as B2B by default because its ICP work uses account fit and buyer roles. If the offer is consumer-facing, state which firmographic, account, or buyer-role fields do not apply and adapt only the applicable criteria with evidence. Do not silently turn consumer assumptions into account scorecards.
- Keep planning, preparation, and execution separate. Any external contact, posting, pricing change, or spend needs its own explicit authorization.

## Phase 1: Define The ICP

Invoke the `icp-definition` skill with the product, offer, customer evidence, delivery constraints, and available win, loss, retention, or expansion evidence.

Carry forward:

- an evidence-backed ICP statement and the unresolved hypotheses
- fit criteria, anti-ICP, buyer roles, and any applicable account tiers
- the smallest validation sample and pass, revise, or reject criteria

For a consumer adaptation, preserve the same evidence discipline while replacing only the fields that do not apply. Do not claim that a score predicts purchase.

## Phase 2: Price And Package The Offer

Invoke the `pricing-strategy` skill using the ICP, customer job, alternatives, sales motion, cost to serve, billing limits, and current pricing evidence.

Use its output to state the smallest offer that can be tested, the value metric, willingness-to-pay evidence, scenario assumptions, and rollback questions. Keep unknown willingness to pay and unit economics visible. Do not use a free or low price as a default or present an unsupported competitor price as evidence.

## Phase 3: Select The Motion And Route

Invoke the `go-to-market-motion` skill with the ICP and offer evidence plus stage, capacity, cash constraints, adoption path, and implementation burden. Choose one primary motion and at most two supporting channels. Map each selected channel to a route only when the evidence supports it.

Compare these route families:

- **Warm:** Use existing relationships, prior trust, referrals, or relevant past conversations when they reach the defined ICP. Record the risk that a friendly sample may not represent the market.
- **Community:** Use a community where the team participates, the target buyer discusses the problem, and the rules permit useful contribution. Record the evidence of problem discussion and the cost of earning trust.
- **Cold:** Use direct outreach only when the target list, claims, channel eligibility, jurisdiction, lawful contact basis, and follow-up capacity can be verified. Treat an unverified list or claim as a blocker.

Record the selected route, rejected routes, evidence for each rating, validation signal, scale prerequisites, and triggers to hold, narrow, or stop. If no route has sufficient evidence, return the gap and a validation step instead of forcing a channel.

## Phase 4: Prepare The Selected Route

- For a warm route, map relevant relationships and prepare a truthful conversation or introduction request. Do not send it.
- For a community route, identify eligible spaces, relevant questions, contribution boundaries, and feedback prompts. Follow the space rules and do not publish anything.
- For a cold route, invoke the `outbound-prospecting` skill. Pass the verified target, offer, proof, claims, channels, jurisdictions, list provenance, and permission boundary. Keep its sequence and response branches as drafts. If eligibility or legal basis is unknown, stop before an executable sequence and record the escalation.
- For every unselected route, record the missing evidence and the condition that would justify reconsidering it. Do not create irrelevant social or email work merely to fill the plan.

## Phase 5: Track Evidence Weekly

Maintain a dated weekly evidence log using the team's real review cadence. Do not add an arbitrary acquisition quota or deadline. Each entry should record:

- week or date, owner, route, permission state, and evidence source
- activity or prepared artifact, target segment, and the intended validation signal
- qualified conversation, activation, payment, objection, or no-data result
- missing evidence kept separate from a measured zero
- interpretation, confidence, next learning question, and keep, revise, narrow, or stop decision

At each weekly review, compare observations with the ICP, pricing, and motion criteria. Update hypotheses and route choice from the evidence. Activity alone is not customer demand, and one observation does not prove a causal effect.

## Report

Return:

1. scope, stage, constraints, owner, and permission boundary
2. ICP, anti-ICP, buyer roles, evidence status, and validation gaps
3. offer, value metric, pricing evidence, assumptions, and rollback questions
4. selected motion and route, rejected routes, rationale, and revisit triggers
5. route-specific drafts or preparation work, with unselected work omitted
6. weekly evidence tracker, decision criteria, blockers, and unresolved unknowns
7. status as planned or prepared, with no claim of external execution

## Installation

Install the cookbook and its dependencies:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill first-customers \
  icp-definition go-to-market-motion outbound-prospecting pricing-strategy
```

## Hard Gates

- Do not choose a route without stated stage, ICP evidence, offer constraints, and permission boundary.
- Do not force warm, community, or cold work when the evidence does not support it.
- Do not prepare executable cold outreach without verified eligibility, list provenance, claims, and response handling from `outbound-prospecting`.
- Do not present a price, customer target, response rate, deadline, or conversion promise without attributable evidence.
- Do not send, publish, change live pricing, or spend from this cookbook.
- Keep weekly observations, missing data, and decisions linked to the criteria that generated them.
