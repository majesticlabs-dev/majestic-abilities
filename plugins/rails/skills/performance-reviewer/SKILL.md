---
name: performance-reviewer
description: Review Rails code for query, memory, locking, and throughput problems before they become production incidents.
---

# Performance Reviewer

Use this skill after implementation or when a Rails path is slow under load.

## Review Areas

- query shape and N+1 behavior
- missing or badly chosen indexes
- eager loading and `strict_loading`
- pagination and batch processing
- cache fit and cache invalidation cost
- lock scope and transaction duration
- work that belongs in a background job

## Workflow

1. Identify the hot path and the dominant resource: database, memory, network, CPU, or lock time.
2. Inspect query count, query shape, and association loading.
3. Check whether the code scales with dataset size or quietly falls apart at 10x.
4. Recommend the smallest fix that materially changes the bottleneck.

Load [references/solid-rails.md](references/solid-rails.md) when the fix involves Solid Cache or Solid Queue.
Load [references/data-safety-checklist.md](references/data-safety-checklist.md) when performance work also touches constraints, backfills, or sensitive data flows.

## Standards

- Prefer fixing query shape before adding cache layers.
- Prefer counter caches and preloading over repetitive aggregate queries.
- Call out transaction scope when external calls happen under locks.
- Do not recommend speculative tuning with no identified bottleneck.
