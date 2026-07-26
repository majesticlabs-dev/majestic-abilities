# Pipeline Reliability Patterns

## Idempotency

Define what makes an input operation the same operation:

- source event identifier
- natural key plus version
- partition plus source snapshot
- cursor range plus pipeline version

Choose target behavior explicitly: append once, upsert, replace partition, or publish a new version. Test reruns with the same input and after partial failure.

## Checkpoints

A checkpoint should record enough to resume safely:

- source cursor and tie-breaker
- source partition or offset range
- target publication identifier
- pipeline and schema version
- completion and validation status

Commit the checkpoint only after target writes and blocking validation complete durably. Use compare-and-set or transactional ownership when concurrent workers could advance the same checkpoint.

## Atomic Publication

Keep in-progress output hidden from consumers. Depending on the target, use:

- database transaction
- staging table followed by controlled swap
- immutable version plus pointer update
- temporary object prefix plus manifest publication
- partition replacement with catalog transaction support

A file rename is atomic only within filesystems and boundaries that guarantee it.

## Retries

Retry only failures likely to be transient:

- timeout
- connection reset
- explicit rate limit
- temporary service unavailability

Use bounded exponential backoff with jitter. Respect server retry hints. Do not retry validation failures, authentication failures, malformed input, or deterministic query errors without change.

Make the retried operation idempotent before adding retries.

## Bad Records

Choose one policy per boundary:

- block the batch
- quarantine records with evidence
- publish degraded output with an explicit status

A dead-letter path needs ownership, retention, replay tooling, privacy controls, and alerting. It is not a permanent trash bin.

## Backpressure and Chunking

Bound memory and downstream pressure with pages, batches, or streams. Tune using measured source and target behavior.

Record chunk boundaries and partial outcomes. Chunking without a safe checkpoint can make recovery harder.

## Observability

Record structured run facts:

- run and batch ID
- source and target
- cursor range
- extracted, accepted, rejected, inserted, updated, and deleted counts
- checkpoint transition
- retries and error class
- validation status
- publication version
- duration and resource usage

Avoid raw sensitive records in logs.

## Ownership

Define one owner for the pipeline, one for source contract changes, and one for downstream data-product quality. Escalation must identify who can pause, replay, or replace output.
