---
name: lifecycle-retention
description: Design a customer lifecycle retention system with stage outcomes, onboarding, health signals, early warnings, intervention playbooks, and measurement. Use when churn is poorly understood, onboarding underperforms, or teams need proactive retention instrumentation rather than account-by-account sales actions. Not for account-specific commercial motions or for choosing a single top-level product health metric.
---

# Lifecycle Retention

## Boundary

Own system-level lifecycle instrumentation and intervention design. Account-specific commercial motions are out of scope. Do not prescribe universal health weights or churn thresholds, hide cancellation, coerce continued use, or replace account-specific expansion work.

## Required Inputs

- Business model, pricing cadence, customer segments, and expected value path
- Lifecycle events, product usage, support, billing, feedback, and churn evidence
- Current onboarding, renewal, cancellation, and recovery processes
- Data availability, consent, privacy, team capacity, and economic constraints

## Workflow

1. Define lifecycle stages from observable customer progress, not arbitrary day counts.
2. Set an outcome, entry evidence, exit evidence, owner, and failure mode for each stage.
3. Identify activation, adoption, value, relationship, billing, and risk signals available for each segment.
4. Build a simple health model from historically useful signals. Keep weights, missing data, and confidence visible.
5. Validate whether signals precede retention outcomes before automating interventions.
6. Design onboarding and early-warning playbooks with trigger, owner, action, suppression, and exit rules.
7. Separate product, service, billing, communication, and fit failures so the response addresses the cause.
8. Define cohort retention, gross and net revenue retention, activation, recovery, and intervention-effect measures with explicit formulas.
9. Phase instrumentation and playbooks according to current volume and team capacity, then set recalibration triggers.

## Output

1. **Lifecycle map and stage evidence**
2. **Health-signal model with confidence limits**
3. **Onboarding and intervention playbooks**
4. **Retention dashboard specification**
5. **Phased implementation and recalibration plan**

## Quality Gate

- Thresholds come from observed segment behavior or are labeled hypotheses.
- Health scores support diagnosis, not automatic punishment or pressure.
- Interventions respect consent, suppression, cancellation, and privacy choices.
- Incentives do not conceal unresolved product or service failures.
- Account-specific commercial action remains separate from system design.
