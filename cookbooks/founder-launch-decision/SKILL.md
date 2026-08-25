---
name: founder-launch-decision
description: "Turn a founder-led launch proposal into a defensible audience, go-to-market motion, legal-unknown inventory, and final GO, NARROW, or DELAY decision. Use when the user invokes founder-launch-decision by name or needs a launch decision before execution."
---

# Founder Launch Decision

Evaluate the launch described in the user's request. Produce a decision, not a campaign, legal clearance, or implementation plan.

## Phase 1: Define The Audience

Invoke the `icp-definition` skill.

Establish:

- observed customer evidence versus hypotheses
- fit criteria and anti-ICP
- economic buyer, champion, user, and blocker
- account or audience tiers
- the smallest validation step for material unknowns

Keep provisional claims visible. A scoring model is a decision aid, not proof.

## Phase 2: Choose The Motion

Invoke the `go-to-market-motion` skill using the ICP evidence.

Choose one primary motion and at most two supporting channels based on buying behavior, trust, deal economics, stage, capacity, and cash constraints. Define validation signals, scale prerequisites, and triggers to hold, narrow, or stop.

Do not choose outbound, product-led, inbound, partner, or enterprise motion merely because it is familiar.

## Phase 3: Inventory Legal Unknowns

Invoke the `launch-legal-checklist` skill.

Record:

- scope, jurisdictions, customer type, claims, payments, and material transactions
- data collection, processing, retention, and user-rights questions
- contracts, refunds, intellectual property, workers, accessibility, insurance, and regulated exposure
- general administrative tasks versus counsel-required or specialist-required decisions
- missing evidence and prioritized next actions

The checklist provides general information only. It never grants legal clearance or replaces qualified counsel.

## Phase 4: Issue The Launch Verdict

Invoke the `launch-readiness` skill using all prior outputs.

Return exactly one verdict:

- `GO`: no unresolved material blocker for the stated scope
- `NARROW`: a concrete, reversible scope reduction removes every current blocker
- `DELAY`: material legal, privacy, safety, fulfillment, ownership, support, or follow-up risk remains

For each blocker, state the evidence, impact, owner, and minimum corrective action.

## Phase 5: Report

Return:

1. ICP and evidence status
2. selected motion and rejected alternatives
3. legal and specialist escalation inventory
4. verdict: `GO`, `NARROW`, or `DELAY`
5. blockers, material unknowns, owners, and minimum fixes
6. the next decision checkpoint

Do not produce campaign copy, a launch calendar, forecasts, legal documents, or an assertion of legal readiness.

## Requires

- `icp-definition` - Phase 1 audience fit, buyer roles, and validation evidence
- `go-to-market-motion` - Phase 2 route-to-market decision
- `launch-legal-checklist` - Phase 3 legal and compliance unknown inventory
- `launch-readiness` - Phase 4 final launch verdict

Install everything:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill founder-launch-decision \
  icp-definition go-to-market-motion launch-legal-checklist launch-readiness
```

## Hard Gates

- Do not issue a launch verdict without a defined scope, audience, offer, reversibility, and named owners.
- Unknown evidence must remain visible and cannot be treated as clearance.
- Counsel-required or specialist-required material issues remain blockers until resolved by the appropriate owner.
- `NARROW` is valid only when the stated scope reduction demonstrably removes every blocker.
- `GO` requires no unresolved material blocker and a workable fulfillment, support, refund, follow-up, and incident path for the stated scope.

Back final approval in the consuming team's decision record. This cookbook informs the decision but cannot provide legal clearance or enforce operational readiness.
