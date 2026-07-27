---
name: data-pipeline-design
description: Design reliable batch or incremental data pipelines with explicit grain, load strategy, idempotency, checkpoints, late-data handling, backfills, storage layout, and reconciliation. Use when planning ETL, ELT, CDC, file-based, or PostgreSQL-backed data movement before implementation.
---

# Data Pipeline Design

Choose the smallest pipeline shape that can be rerun, recovered, observed, and reconciled safely.

## Boundary

Use this skill after the source has a credible assessment. Use `dbt-development` for dbt project implementation and `data-pipeline-testing` for executable verification strategy.

## Inputs

Establish:

1. Source and target systems.
2. Source and target grain.
3. Natural, primary, and deduplication keys.
4. Volume, cadence, latency, and retention.
5. Insert, update, delete, and late-arrival behavior.
6. Backfill and replay requirements.
7. Failure, cost, security, and compliance constraints.

## Workflow

### 1. Write the pipeline contract

Define:

- source object and target object
- grain at every stage
- field mapping and semantic transformations
- cursor or change token
- target write behavior
- delete handling
- validation boundaries
- publication condition
- ownership and service level

Do not implement incrementality before identifying reliable change semantics.

### 2. Choose a load strategy

| Source behavior | Initial strategy |
| --- | --- |
| Small, stable, safely replaceable dataset | Full refresh with atomic publication |
| Reliable ordered cursor with updates | Incremental extraction with overlap and idempotent upsert |
| Durable ordered change log | CDC with offset management and delete handling |
| Immutable events | Append with deduplication and reconciliation |
| No trustworthy change signal | Full refresh or snapshot comparison |

Treat row-count thresholds as workload-specific, not universal constants.

### 3. Design reliability

Use [reliability-patterns.md](references/reliability-patterns.md). Specify:

- idempotency key
- checkpoint location and commit point
- transaction or atomic publication boundary
- retryable error classes
- bad-record path
- duplicate-delivery behavior
- partial-failure recovery
- structured run metadata

Never advance the checkpoint before durable target publication and required validation succeed.

### 4. Design incrementality and backfills

Use [incremental-loads.md](references/incremental-loads.md). Cover:

- overlap window
- timestamp tie-breaker
- late updates
- deletes and tombstones
- initial history load
- historical correction
- concurrent live loads
- replay isolation
- reconciliation after backfill

Build backfill behavior before relying on the ongoing schedule.

### 5. Choose storage layout

For file-backed stages, use [parquet-storage.md](references/parquet-storage.md). Define schema, partition keys, file sizing, compression, publication, and evolution.

Avoid high-cardinality partitioning and uncontrolled small files. A file format does not provide transaction semantics by itself.

### 6. Define transformation boundaries

Keep raw ingestion reproducible. Separate:

- raw preservation
- parsing and normalization
- validation and quarantine
- business transformation
- publication

Name each stage and its grain. Avoid destructive cleanup before raw evidence is retained.

### 7. Design PostgreSQL operations when relevant

Use [postgresql-patterns.md](references/postgresql-patterns.md) only for PostgreSQL targets or sources. Keep dialect-specific behavior out of the generic pipeline contract.

### 8. Add observability and reconciliation

Record per run:

- run and batch identifiers
- source cursor range
- extracted, accepted, rejected, inserted, updated, and deleted counts
- validation result
- checkpoint before and after
- duration, retries, and error class
- output partition or version

Define reconciliation equations and control totals. Row counts alone are rarely sufficient.

### 9. Plan rollback and recovery

State how to:

- retry a failed batch
- replay a cursor range
- replace a bad publication
- pause live loads during repair
- restore or compensate destructive writes
- resume without duplication

## Deliverable

Return:

1. Pipeline contract
2. Load-strategy decision
3. Stage and grain diagram
4. Checkpoint and idempotency design
5. Late-data, delete, and backfill behavior
6. Storage and schema-evolution plan
7. Validation and reconciliation controls
8. Failure, rollback, and replay plan
9. Observability fields
10. Implementation slices

## Quality Gate

- Grain and keys are explicit at every stage.
- Reruns cannot silently duplicate or corrupt data.
- Checkpoints follow durable validated publication.
- Deletes, late data, and backfills are designed.
- Counts and control totals reconcile.
- Recovery is described before scheduling.
