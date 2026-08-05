# Solid Rails

Use this reference when the app relies on Rails' database-backed infrastructure defaults such as Solid Queue or Solid Cache.

## Solid Queue

- keep jobs idempotent and explicit about retry behavior
- choose queue names and priorities intentionally
- use concurrency controls only when the app actually needs them and the adapter supports them
- if queue throughput becomes the bottleneck, measure it before inventing a different architecture

### Execution Mode and Connection Budget

Solid Queue lets each worker run `threads: N` or `fibers: N`. Check both:

- is the execution mode matched to the workload? I/O-bound queues (LLM, HTTP, broadcasts) waste a kernel thread and a connection per in-flight job under `threads:`; CPU-bound or long-transaction jobs stall the reactor under `fibers:`
- does the connection budget fit? Sum `worker processes x per-process pool` and compare against the database `max_connections`. Budget `threads + 2` per thread worker process, and 3 to 5 per fiber worker process
- fiber workers require `config.active_support.isolation_level = :fiber`, which applies to the whole process, including Puma when Solid Queue runs via the plugin

## Solid Cache

- fix query shape before adding cache layers
- cache stable render or lookup boundaries, not arbitrary object graphs
- keep cache keys and invalidation rules explicit
- avoid caching data that changes too often to produce a real win

## Review Lens

- is the app using the Solid feature because it fits, or because it is merely available
- does the configuration increase operational simplicity, or hide a scaling bottleneck
- are persistence, invalidation, and observability clear enough for production debugging
