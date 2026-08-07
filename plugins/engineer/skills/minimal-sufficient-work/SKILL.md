---
name: minimal-sufficient-work
description: Apply the MSW deletion rule to keep plans, implementation, tests, remediation, reviews, artifacts, and process limited to work necessary to satisfy or prove the requested outcome. Use when the user invokes MSW or the deletion rule, when work risks expanding beyond scope, or before adding code, tests, files, abstractions, limits, review findings, or follow-up work.
---

# Minimal Sufficient Work (MSW)

Use the MSW kernel to complete the requested outcome without speculative work, extra process, or proof beyond what the outcome requires.

## Program

```
contract ← the requested outcome + the smallest criteria that prove it

while ∃ claim c : deleting c leaves contract unmet ∨ unproven
      do c ; prove c

halt ; report
```

## Definitions

### Contract

Establish the requested outcome and the smallest set of acceptance criteria that would prove it before doing work. Treat the contract as both the floor and the ceiling.

When the request is ambiguous:

- In attended work, ask only when the answer would materially change the contract.
- In unattended work, bind the smallest reading consistent with the stated intent and record the assumption.

Do not silently expand the contract with inferred improvements, generic best practices, or unrelated cleanup.

### Claim

Treat anything petitioning to become work as a claim, including:

- a plan step or implementation change
- a test, check, investigation, or proof step
- a new file, abstraction, dependency, artifact, or process
- a review finding or discovered edge case
- a migration, rollout control, monitoring change, or cleanup task
- an instinct that another pass would be useful

A claim is a proposal, not a verdict. Its source or stated severity does not make it necessary.

### Deletion Rule

For every claim `c`, ask:

> If `c` is deleted, does the contract remain met and proven for the task's actual inputs, environment, and applicable constraints?

- If yes, reject the claim. Do not implement, investigate, defer, or create follow-up work for it.
- If no, accept the claim and perform the smallest reliable act that closes the specific gap.

A claim passes only when deleting it leaves the contract unmet or unproven. Useful, thorough, conventional, and possible are not synonyms for necessary. Derive severity from impact on the contract, not from the person or tool that raised the claim.

### Do and Prove

For each accepted claim:

1. Perform the smallest reliable act that closes the gap.
2. Produce evidence sized to that claim.
3. Close the claim when the evidence proves it.

An unproven act leaves its claim open. Re-proving a closed claim is a new claim and must pass the deletion rule.

Use evidence appropriate to the gap, such as a focused test, command output, direct inspection, reproduced behavior, type check, build result, or authoritative documentation. Do not add a broader test or review pass unless deleting it would leave the contract unproven.

### Halt

Stop when the contract is proven and no remaining claim passes the deletion rule. Reviewer silence and exhausted imagination are not stopping conditions. Continuing after the fixed point is as incorrect as stopping before it.

## Fuses

Use these fuses when claim evaluation fails to converge:

```text
rounds = 3 -> halt and report open items; do not chase them
claim born in round n+1 that was visible in round n -> reject
```

A round is one complete evaluation, action, and proof pass over the claims then visible. The three-round limit is defined by this skill, not inferred from task size.

## No Unauthoritative Limits

Never invent a cap, threshold, quota, budget, timeout, retry count, round count, file count, line count, acceptance-criterion count, agent count, or similar limit.

A limit is admissible only when its exact value is:

- explicitly required by the requester
- imposed by an applicable technical or platform contract
- defined by authoritative project policy
- derived from measured evidence necessary to meet or prove the contract

State the authority or derivation whenever proposing or applying a limit. If no authority exists, omit the limit and apply the deletion rule. Metrics may be evidence, but must not become gates, defaults, targets, or recommendations through agent intuition. Examples and representative proportions do not become defaults.

If a necessary limit requires an unresolved owner choice, ask rather than manufacture a value. The fuse above is already authorized by this skill.

## Report

Report only:

1. the outcome against the contract
2. the evidence that proves it
3. necessary open items remaining because a fuse fired or the work is blocked
4. rejected claims worth the user's attention, at most one line each

Do not turn rejected claims into recommendations, investigations, or deferred tasks.

## Quality Gate

Before reporting, confirm:

- the requested outcome and proof criteria formed the contract
- every performed action passed the deletion rule
- every accepted claim has evidence or remains explicitly open
- no invented limit shaped the work
- no closed claim was re-proven without necessity
- work stopped at the fixed point or an authorized fuse
