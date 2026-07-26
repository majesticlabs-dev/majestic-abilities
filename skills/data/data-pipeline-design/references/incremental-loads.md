# Incremental Loads and Backfills

## Strategy Selection

Use full refresh when the dataset is small enough to replace safely or no trustworthy change signal exists.

Use incrementality only when the source exposes one of:

- immutable ordered event identifier
- durable log offset
- monotonically advancing cursor
- reliable update timestamp plus deterministic tie-breaker
- source-supported change data capture

## Composite Watermarks

A timestamp alone can repeat. Pair it with a stable tie-breaker and order by both:

```text
(updated_at, source_id) > (last_updated_at, last_source_id)
ORDER BY updated_at, source_id
```

This does not solve late updates whose timestamp falls behind the committed watermark. Use an overlap window and idempotent target writes when that is possible.

## Checkpoint Commit

For each cursor range:

1. Read the checkpoint.
2. Extract a bounded range.
3. Normalize and validate.
4. Write idempotently.
5. Reconcile counts and control totals.
6. Publish output.
7. Commit the new checkpoint.

Never commit step 7 before durable completion of the required earlier steps.

## Late and Corrected Data

Define:

- expected lateness distribution
- overlap duration
- mutable history window
- correction precedence
- deduplication version or tie-breaker
- behavior beyond the correction window

Monitor how many accepted changes arrive through the overlap. That evidence should tune the window.

## Deletes

Choose explicitly:

- source tombstone applied to target
- soft delete with source deletion timestamp
- periodic anti-join reconciliation
- snapshot replacement
- append-only retention with current-state view

A pipeline that copies inserts and updates but ignores source deletes is not a complete mirror.

## CDC

For change data capture, record:

- source log position
- transaction ordering
- event identifier
- operation type
- before and after values when available
- schema version

Handle duplicate delivery and transaction boundaries. Preserve enough provenance to replay events without repeating irreversible side effects.

## Backfills

Design backfills as bounded ranges with the same transform and validation contract as live data.

Specify:

- range partitioning
- concurrency limit
- interaction with live loads
- target write isolation
- checkpoint behavior
- reconciliation per range
- retry and resume
- cleanup of partial output

Do not let a historical backfill advance the live checkpoint accidentally.

## Full Refresh Publication

For replaceable datasets:

1. Build into hidden staging or a new immutable version.
2. Validate and reconcile.
3. Publish atomically through a transaction, swap, or version pointer.
4. Retain the previous version long enough for rollback.

Do not expose a table or directory while it is only partially replaced.
