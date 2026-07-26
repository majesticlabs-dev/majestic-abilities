# PostgreSQL Data Pipeline Patterns

These patterns are PostgreSQL-specific. Verify syntax and planner behavior against the deployed major version and workload.

## Deterministic Incremental Reads

Use a stable composite cursor when timestamps can repeat:

```sql
SELECT id, source_updated_at, payload
FROM source_records
WHERE (source_updated_at, id) > ($1, $2)
ORDER BY source_updated_at, id
LIMIT $3;
```

This does not capture records that arrive late with an older timestamp. Add a measured overlap window and idempotent upsert when the source permits late corrections.

## Upsert

Use a real unique constraint as the conflict target:

```sql
INSERT INTO target_records AS target (
    id,
    source_updated_at,
    payload
)
VALUES ($1, $2, $3)
ON CONFLICT (id) DO UPDATE
SET source_updated_at = EXCLUDED.source_updated_at,
    payload = EXCLUDED.payload
WHERE target.source_updated_at IS NULL
   OR EXCLUDED.source_updated_at >= target.source_updated_at
RETURNING id, source_updated_at;
```

Define precedence explicitly. Do not overwrite newer target state with an older retry.

Reference: <https://www.postgresql.org/docs/current/sql-insert.html>

## Batched Work

PostgreSQL does not support a generic `UPDATE ... LIMIT` or `DELETE ... LIMIT`. Select keys in a CTE, then modify those rows:

```sql
WITH batch AS (
    SELECT id
    FROM events
    WHERE processed_at IS NULL
    ORDER BY id
    LIMIT 1000
    FOR UPDATE SKIP LOCKED
)
UPDATE events AS event
SET processed_at = clock_timestamp()
FROM batch
WHERE event.id = batch.id
RETURNING event.id;
```

`SKIP LOCKED` is appropriate for queue-like concurrent consumers, not for obtaining a consistent analytical view. Commit each bounded batch and record progress outside the mutable selection predicate.

For deletes:

```sql
WITH batch AS (
    SELECT id
    FROM event_staging
    WHERE loaded_at < $1
    ORDER BY id
    LIMIT 1000
)
DELETE FROM event_staging AS target
USING batch
WHERE target.id = batch.id
RETURNING target.id;
```

## Deduplication

Make the tie-breaker deterministic:

```sql
WITH ranked AS (
    SELECT
        source_records.*,
        row_number() OVER (
            PARTITION BY business_key
            ORDER BY source_updated_at DESC, ingestion_id DESC
        ) AS row_priority
    FROM source_records
)
SELECT *
FROM ranked
WHERE row_priority = 1;
```

If the final ordering columns can still tie, the selected record remains nondeterministic.

## Grain and Join Fanout

Measure cardinality before and after joins:

```sql
SELECT customer_id, count(*)
FROM customers
GROUP BY customer_id
HAVING count(*) > 1;
```

State the expected grain in model documentation. Pre-aggregate many-side tables when a join would multiply facts unintentionally.

## NULL-Safe Comparisons and Conditional Aggregation

```sql
SELECT *
FROM current_rows AS current
JOIN previous_rows AS previous USING (id)
WHERE current.value IS DISTINCT FROM previous.value;
```

```sql
SELECT
    count(*) AS total,
    count(*) FILTER (WHERE status = 'accepted') AS accepted,
    count(*) FILTER (WHERE status = 'rejected') AS rejected
FROM load_results;
```

Use `COALESCE` only when the replacement has correct domain meaning.

## Time-Series Generation

PostgreSQL provides `generate_series` for calendar and gap analysis:

```sql
SELECT day::date
FROM generate_series(
    $1::date,
    $2::date,
    interval '1 day'
) AS generated(day);
```

Join generated periods to observed data to distinguish missing periods from zero-valued periods.

## Indexes

Design indexes from measured query predicates and ordering. Useful PostgreSQL options include:

- multicolumn indexes matching cursor order
- partial indexes for a stable selective predicate
- expression indexes for repeated expressions
- `INCLUDE` columns for covering access patterns

Example queue predicate:

```sql
CREATE INDEX CONCURRENTLY index_events_unprocessed
ON events (id)
WHERE processed_at IS NULL;
```

`CREATE INDEX CONCURRENTLY` has operational restrictions and cannot run inside a transaction block. Review write amplification, lock behavior, and migration tooling before use.

## Query Plans

Start with estimated plans. Use actual execution carefully:

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS)
SELECT ...;
```

`ANALYZE` executes the statement. Do not run it casually for destructive or expensive statements in production. Inspect estimated versus actual rows, loops, buffer reads, spills, and scan choice. Refresh statistics when evidence shows they are stale rather than adding indexes reflexively.

Reference: <https://www.postgresql.org/docs/current/sql-explain.html>

## Materialized Views

Use materialized views for expensive reusable results with acceptable refresh semantics. Define refresh cadence, staleness tolerance, and failure behavior. `REFRESH MATERIALIZED VIEW CONCURRENTLY` has prerequisites, including a qualifying unique index, and still requires operational planning.

Reference: <https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html>
