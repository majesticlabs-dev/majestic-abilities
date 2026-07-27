---
name: data-pipeline-testing
description: Design tests and fixtures for data pipelines across transformation, contract, integration, incrementality, replay, and reconciliation behavior. Use when verifying ETL or ELT code, dbt models, schema changes, backfills, late data, idempotency, or failure recovery.
---

# Data Pipeline Testing

Test pipeline semantics, not only whether a job ran. Small readable fixtures and strong reconciliation oracles beat large opaque random datasets.

## Inputs

Establish:

1. Pipeline contract and stage grains.
2. Source and target schemas.
3. Incremental cursor and write strategy.
4. Validation and quarantine behavior.
5. Known incidents and edge cases.
6. External systems and available test substitutes.

## Workflow

### 1. Build a behavior matrix

Map each contract to a test layer:

| Behavior | Preferred test |
| --- | --- |
| Pure field transformation | Unit example or property test |
| Join and aggregation grain | Small table fixture with explicit expected output |
| Schema and semantic contract | Contract or validation test |
| Source and target integration | Integration test against realistic boundary |
| Incremental cursor and upsert | Multi-run stateful test |
| Backfill and replay | Historical range test plus reconciliation |
| Failure recovery | Fault injection and resume test |
| Published dataset | End-to-end consumer invariant |

Do not push every case into a slow end-to-end test.

### 2. Design fixtures from risks

Use [fixture-design.md](references/fixture-design.md). Include only rows needed to prove behavior:

- null and empty distinctions
- duplicate keys
- boundary values
- malformed records
- unknown categories
- one-to-many joins
- unmatched relationships
- timezone and period boundaries
- late updates and deletes
- repeated delivery
- out-of-order records

Keep identifiers and expected outputs readable.

### 3. Test transformation logic

Assert values, grain, and invariants. Cover:

- filters
- type and unit conversions
- join cardinality
- deduplication tie-breakers
- aggregations and rounding
- null propagation
- deterministic ordering when required

A row-count assertion cannot prove transformation correctness.

### 4. Test stateful behavior

Run the pipeline through sequences:

1. initial load
2. same input again
3. new records
4. update to an existing key
5. late-arriving record
6. delete or tombstone
7. failed partial attempt
8. retry
9. backfill overlapping live data

Verify target state and checkpoint after each run.

### 5. Test failures and quarantine

Inject:

- transient source failure
- target write failure
- malformed batch
- validation blocker
- individual bad record
- unavailable checkpoint store

Verify retry limits, atomicity, quarantine evidence, alerting, and safe resume.

### 6. Reconcile independently

Use an oracle independent of the implementation where possible. Compare:

- source and target key coverage
- accepted plus rejected totals
- sums or hashes by partition
- duplicate counts
- expected inserts, updates, and deletes
- checkpoint range and published partitions

### 7. Test schema evolution

Cover additive fields, missing required fields, type changes, renamed fields, semantic changes, and mixed-version inputs. Verify both compatibility and intended rejection.

### 8. Control generated data

Use generated or property-based fixtures for broad ranges and invariants, but fix seeds and preserve minimal failing examples. Do not let random fixtures replace named regression cases.

## Deliverable

Return:

1. Contract-to-test matrix
2. Fixture inventory
3. Unit, integration, and end-to-end boundaries
4. Multi-run incremental scenarios
5. Failure-injection scenarios
6. Reconciliation oracles
7. Schema-evolution coverage
8. Commands and environment requirements
9. Remaining untested risks

## Quality Gate

- Tests assert values and grain, not only execution or row count.
- Incremental tests span multiple runs.
- Idempotency, late data, deletes, and backfills are covered.
- Failures prove atomicity and recovery.
- Fixtures are deterministic and readable.
- Reconciliation uses an independent oracle where feasible.
