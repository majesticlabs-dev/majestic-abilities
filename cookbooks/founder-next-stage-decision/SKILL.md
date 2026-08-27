---
name: founder-next-stage-decision
description: "Decide how a founder of an existing product gets to the next growth stage: diagnose the ceiling, commit to one time-boxed discovery sprint, and decide with evidence instead of hope. Use when the user invokes founder-next-stage-decision by name or asks how to restart growth or get to the next stage."
---

# Founder Next Stage Decision

Run this workflow only for an existing product with revenue, customers, or churn data. For a pre-product commercial idea, invoke `brainstorm-product` directly in Mode B.

## Phase 1: Diagnose The Ceiling

Invoke the `brainstorm-product` skill in Mode A and run steps A1 through A9.

Establish:

- facts, the real goal, and the ceiling math against that goal
- customer segments and which one the metrics actually measure
- powers-of-10 tests for the forever use cases
- one agreed crux sentence
- four to six honest options, each with its gut reaction and leverage rank

Do not generate a sprint plan yet. Stop when the crux and the ranked options menu are written down.

## Phase 2: Commit To One Sprint

Pick the single most promising uncertain option from Phase 1. Invoke `brainstorm-product` step A10 to design a time-boxed sprint of about four weeks:

- one pass or fail question about the option, never "how do I scale it"
- concrete discovery actions: integrations, marketing passes, paid traffic to conversations, structured customer interviews
- the named comfort work to refuse during the sprint

Then invoke the `founder-priorities` skill to protect the sprint:

- cut, defer, or delegate everything that competes with it
- set the weekly execution cadence and the sprint-end revisit criteria
- state which tradeoffs the founder accepts for the sprint month

The sprint does not end with a product. It ends with evidence.

## Phase 3: Decide With Evidence

After the sprint deadline, invoke `brainstorm-product` step A11 for the closure audit, then invoke the `founder-plan-review` skill on the evidence and the resulting next-stage plan.

Return exactly one verdict:

- `PURSUE`: the evidence supports the option; the next-stage plan survives review
- `RESHAPE`: the evidence shows a narrower or adjacent path; restate the option and rerun a short sprint
- `DISCARD`: the crux stands or the option failed its question; return to the Phase 1 options menu

## Phase 4: Report

Return:

1. the agreed crux and the ceiling math
2. the option chosen for the sprint and the rejected alternatives
3. the sprint question, evidence collected, and the pass or fail result
4. verdict: `PURSUE`, `RESHAPE`, or `DISCARD`
5. the next-stage plan and the founder commitments that hold beyond the sprint
6. the next decision checkpoint

Do not produce a campaign, a full business plan, or a multi-year forecast.

## Requires

- `brainstorm-product` - Phase 1 diagnosis, options menu, sprint design, and closure audit
- `founder-priorities` - Phase 2 protected calendar and sprint cadence
- `founder-plan-review` - Phase 3 next-stage plan review and verdict

Install everything:

```sh
npx skills add majesticlabs-dev/majestic-abilities --skill founder-next-stage-decision \
  brainstorm-product founder-priorities founder-plan-review
```

## Hard Gates

- No sprint without a written, agreed crux.
- The sprint is time-boxed, has one pass or fail question, and names the comfort work to refuse.
- No `PURSUE` verdict without sprint evidence collected after the sprint design.
- Gut reactions are recorded verbatim and no option is discarded silently.
- `RESHAPE` requires a restated option, not a repeated sprint on the failed one.
