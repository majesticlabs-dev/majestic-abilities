# Data Quality Control Checklist

## Contract

- [ ] Data product and grain are explicit.
- [ ] Consumers and consequential decisions are named.
- [ ] Blocking, degraded, warning, and unknown states are distinct.
- [ ] Every critical rule has an owner.

## Completeness and Integrity

- [ ] Required fields have justified null thresholds.
- [ ] Primary or natural key expectations are enforced.
- [ ] Duplicate semantics are documented.
- [ ] Join cardinality is measured.
- [ ] Referential coverage is checked where material.
- [ ] Accepted plus rejected records reconcile to input.

## Validity and Consistency

- [ ] Types, units, ranges, and categories match the domain.
- [ ] Cross-field rules are executable.
- [ ] Timestamps have timezone and precision semantics.
- [ ] Derived fields reconcile with upstream values.
- [ ] Unknown categories or schema versions have a policy.

## Timeliness and Volume

- [ ] Freshness is measured from the correct event or arrival time.
- [ ] Delivery latency accounts for normal delay and seasonality.
- [ ] Volume thresholds use comparable periods.
- [ ] Missing partitions and duplicate deliveries are detectable.

## Drift

- [ ] Added, removed, and changed fields are surfaced.
- [ ] Null, category, and numeric distribution shifts are tracked where actionable.
- [ ] Sample size and normal calendar effects are considered.
- [ ] Statistical findings have operational thresholds and owners.

## Alerting

- [ ] Every alert identifies affected consumers.
- [ ] Severity maps to response expectations.
- [ ] Duplicate alerts are suppressed or grouped.
- [ ] Evidence and investigation links are attached.
- [ ] Maintenance, backfill, and known-event suppression is defined.
- [ ] Alert volume matches response capacity.

## Incident Response

- [ ] Affected partitions and consumers can be identified.
- [ ] Bad publications can be contained or replaced.
- [ ] Reprocessing is idempotent.
- [ ] Corrections are communicated.
- [ ] Root cause and prevention are recorded.

## Scorecards

- [ ] Critical failures are visible individually.
- [ ] Unknown checks are not counted as passes.
- [ ] Composite scores do not hide blockers.
- [ ] Threshold rationale and last review date are shown.
