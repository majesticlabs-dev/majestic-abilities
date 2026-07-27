# Data Safety Checklist

Use this reference when a Rails change touches schema, backfills, deletes, exports, authorization-sensitive data, or personally identifiable information.

## Data Integrity

- add database constraints for invariants the app truly depends on
- stage large backfills before enforcing `NOT NULL` or uniqueness
- use foreign keys when dangling rows would be a bug, not just an inconvenience
- make uniqueness real with indexes, not controller hope
- keep migrations reversible when practical and operationally safe when not

## Review Heuristics

- ask what happens under concurrent writes, retries, and partial failure
- check whether validations and database constraints disagree
- verify bulk updates and backfills preserve derived fields and callbacks intentionally
- watch for silent data loss in replace-all updates, JSON blobs, or destructive sync jobs

## Privacy And Exposure

- minimize PII in logs, background job payloads, and admin screens
- keep exports, search, and audit surfaces aligned with authorization rules
- prefer explicit redaction and serializer boundaries over "filter this later"
- if retention or deletion behavior changes, call that out directly

## Warning Signs

- a migration that assumes a tiny table
- controller-level uniqueness checks with no index
- background jobs carrying raw secrets or large serialized models
- new admin visibility with no policy or scope check
