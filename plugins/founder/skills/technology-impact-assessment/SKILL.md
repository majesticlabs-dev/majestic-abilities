---
name: technology-impact-assessment
description: "Use when a founder asks what a technology announcement means for the business. Not for general market research, implementation planning, or trend summaries without a decision context."
---

# Technology Impact Assessment

Convert an external technology change into a bounded company decision. Novelty is not strategic value, and an announcement is not proof that a capability works for this business.

## Boundary

Use this skill when there is a specific external change and a named company, product, or strategic decision to evaluate.

Do not use announcement copy as verified capability evidence. Do not force an opportunity, competitive advantage, or urgent action. A valid conclusion is to monitor or take no material action.

This skill may identify experiments or strategic implications. It does not validate customer demand, produce an implementation plan, or replace specialist legal, security, or technical review.

## Required Inputs

Collect:

- announcement, release, or observed technology change
- company or product context and decision horizon
- current user workflow, architecture, economics, capabilities, and constraints
- strategic goals and committed work that could be displaced
- competitors, substitutes, dependencies, and switching constraints
- available primary and independent sources

## Evidence Labels

Use:

- **Verified:** directly established by observed behavior, reproducible evidence, or documentation limited to facts it can authoritatively establish, such as published terms, interfaces, or availability
- **Vendor claim:** a provider assertion about capability, performance, quality, adoption, suitability, or expected outcome that has not been independently observed or reproduced
- **Third-party report:** externally reported with named source and limitations
- **Inference:** reasoned implication from supported premises
- **Unknown:** material evidence is missing

## Workflow

### 1. Verify what changed

Start with a dated primary source. Check current documentation, availability, geography, eligibility, pricing, quotas, terms, security and data handling, deprecations, and stated limitations when relevant.

Use an independent source or direct probe for material performance or compatibility claims when feasible. Record what was not announced or cannot be verified.

### 2. Establish the baseline and delta

Describe the prior constraint and the actual change:

```text
previous capability or constraint -> new capability or constraint -> confidence
```

Separate a new technical possibility from a new economic, operational, or customer reality.

### 3. Map effects on this company

Assess only relevant dimensions:

- customer behavior and workflow
- product capability, quality, latency, or cost
- internal operating leverage
- distribution or market access
- competitor and substitute parity
- dependency, lock-in, and switching exposure
- security, privacy, legal, and trust implications
- skills, infrastructure, support, and maintenance burden
- committed roadmap opportunity cost

For every material implication, show the mechanism connecting the change to the effect.

### 4. Generate materially different responses

Consider a small set across distinct postures:

- adopt or integrate
- run a reversible experiment
- defend an exposed capability or margin
- change positioning, packaging, or distribution
- remove or defer planned work made obsolete
- monitor a named signal
- take no material action

Do not rank an option because it is unusual. Reject options that require imaginary customer behavior, unavailable capabilities, or unsupported competitor weakness.

### 5. Compare decision value

For each surviving option, assess:

- evidence strength
- strategic and user fit
- expected impact and causal mechanism
- required capability, cost, and displaced work
- timing and whether a real window exists
- reversibility and downside
- dependency and operational risk
- evidence that would invalidate the option

Use ranges or qualitative comparison when numeric estimates would be fabricated.

### 6. Define the sensing step

When a credible uncertain option survives screening, define the cheapest documentation check, prototype, benchmark, customer test, contract review, or operational trial. State the decision it will inform, pass and stop conditions, owner, and review date. If no option survives, omit the sensing step and state why.

### 7. Decide

Return one:

- **Act now:** evidence and timing justify a bounded commitment.
- **Experiment:** material potential exists, but a reversible test should precede commitment.
- **Monitor:** action is premature; name the signal and review date.
- **No material action:** the change does not currently alter the company’s best course.
- **Unverifiable:** missing evidence prevents a responsible assessment.

## Output

1. **Decision and verdict**
2. **Verified change summary** with evidence labels
3. **Baseline-to-delta map**
4. **Company-specific implications and mechanisms**
5. **Options, tradeoffs, and displaced work**
6. **Sensing step or monitoring trigger**
7. **Unknowns and conditions that would change the verdict**

Return up to five material implications and up to three materially different response options. Zero actionable implications or options is valid. Expand only when the decision scope or user request requires it.

## Quality Gate

- Every vendor claim remains labeled until verified.
- Current availability, terms, and limitations are checked when material.
- Implications are specific to the named company or product.
- Novelty is not used as a proxy for value.
- No competitive advantage is asserted without a mechanism and evidence.
- Reversibility, opportunity cost, and dependencies affect the verdict.
- No material action is accepted when the evidence supports it.
