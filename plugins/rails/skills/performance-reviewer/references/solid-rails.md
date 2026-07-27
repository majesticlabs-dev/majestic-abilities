# Solid Rails

Use this reference when the app relies on Rails' database-backed infrastructure defaults such as Solid Queue or Solid Cache.

## Solid Queue

- keep jobs idempotent and explicit about retry behavior
- choose queue names and priorities intentionally
- use concurrency controls only when the app actually needs them and the adapter supports them
- if queue throughput becomes the bottleneck, measure it before inventing a different architecture

## Solid Cache

- fix query shape before adding cache layers
- cache stable render or lookup boundaries, not arbitrary object graphs
- keep cache keys and invalidation rules explicit
- avoid caching data that changes too often to produce a real win

## Review Lens

- is the app using the Solid feature because it fits, or because it is merely available
- does the configuration increase operational simplicity, or hide a scaling bottleneck
- are persistence, invalidation, and observability clear enough for production debugging
