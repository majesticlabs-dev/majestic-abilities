---
name: data-quality
description: Define and operate data quality controls, service levels, scorecards, drift monitoring, and incident response for a data product. Use when establishing trust requirements, freshness or volume alerts, quality gates, ownership, or ongoing monitoring across pipelines and datasets.
---

# Data Quality

Define whether a data product is fit for a specific consumer and keep that judgment observable over time. Quality is contextual, not a universal percentage.

## Boundary

- Use `data-source-assessment` to establish the initial source baseline.
- Use `data-validation` to implement executable schema and business-rule checks.
- Use `anomaly-detection` for context-dependent unusual observations.
- Use `data-pipeline-testing` to verify transformation behavior before deployment.

## Inputs

Establish:

1. Data product, grain, owner, and consumers.
2. Decisions or systems that depend on it.
3. Freshness, completeness, and correctness expectations.
4. Existing incidents and known exceptions.
5. Source and downstream service levels.
6. Alert recipients and response capacity.

A metric without an owner or response is telemetry, not a control.

## Workflow

### 1. Define fitness for use

For each consumer, state what failure makes the data unusable, degraded, or merely imperfect. Separate blocking invariants from warning indicators.

### 2. Choose relevant dimensions

Use only dimensions tied to consumer impact:

- **Completeness:** required records and fields are present
- **Uniqueness:** declared keys do not duplicate
- **Validity:** values satisfy contracts
- **Consistency:** related fields and datasets agree
- **Accuracy:** values reconcile to an authoritative source
- **Timeliness:** freshness and delivery latency meet need
- **Integrity:** relationships and grain remain intact

Do not claim accuracy when no source of truth exists.

### 3. Define checks at the right boundary

Place checks where failures can be diagnosed and contained:

- source arrival
- raw ingestion
- staging contract
- transformation
- published data product
- cross-system reconciliation

Avoid duplicating the same rule in several tools without one owner.

### 4. Set evidence-based thresholds

Derive thresholds from:

- explicit business requirements
- observed normal ranges
- seasonality and calendar effects
- downstream tolerance
- historical incidents

Document warning, blocking, and unknown states. Do not hard-code conventional values such as 95 percent completeness without justification.

### 5. Monitor change

Track relevant trends:

- schema changes
- row or partition volume
- missingness
- category appearance and disappearance
- numeric distribution
- freshness and latency
- failed validation counts
- reconciliation differences

Account for sample size and multiple comparisons before treating statistical significance as operational drift.

### 6. Design alerting

Every alert must define:

- condition and evaluation window
- severity
- affected consumers
- owner and escalation path
- deduplication or suppression
- investigation link or evidence
- recovery and backfill expectation

Prefer a small actionable alert set over a noisy comprehensive dashboard.

### 7. Report without hiding blockers

Do not let a composite score average away a failed critical invariant. Report:

- critical checks individually
- dimension-level status
- trends and exceptions
- unknown or unevaluable checks
- overall status based on explicit gating logic

### 8. Close the incident loop

For failures, capture cause, affected partitions, consumer impact, containment, correction, replay or backfill, and prevention. Update thresholds only when evidence shows the contract changed.

## Reference

Use [quality-control-checklist.md](references/quality-control-checklist.md) to design and review controls.

## Deliverable

Return:

1. Data product and consumer contract
2. Quality dimensions and checks
3. Threshold rationale
4. Gate logic
5. Monitoring and alert ownership
6. Scorecard layout
7. Incident and backfill procedure
8. Known exceptions and unknowns

## Quality Gate

- Every check maps to consumer impact.
- Critical invariants cannot be hidden by averaging.
- Thresholds have evidence and owners.
- Unknown checks remain visible.
- Alerts are actionable and rate-controlled.
- Incidents include correction and prevention paths.
