# Cloudflare Worker Runtime Patterns

Retrieve current product documentation before using exact APIs, limits, migrations, or configuration shapes.

## Handler Design

- Keep parsing, policy, domain behavior, and persistence separable.
- Type bindings from generated Wrangler types.
- Return platform-native `Response` objects at the runtime boundary.
- Use middleware ordering deliberately and test error propagation.
- Track background work through the execution context.

## Durable Objects

Use a Durable Object when one stable object identity should coordinate state or connections.

Review:

- deterministic object naming and routing
- serialized state transitions and concurrency boundaries
- storage migrations and deployment order
- alarms, retries, and restart behavior
- WebSocket Hibernation for long-lived server-side connections when supported
- bounded in-memory state

Do not use one global object when independent entities can be partitioned.

## Queues

- Treat delivery as retryable and potentially duplicated.
- Make side effects idempotent before acknowledging messages.
- Bound batch size and outbound concurrency.
- Define dead-letter and poison-message handling.
- Report partial failures without redoing successful irreversible work.

## Storage Review

| Need | Candidate | Main question |
| --- | --- | --- |
| globally distributed lookup/cache | KV | Can readers tolerate eventual consistency? |
| relational queries and transactions | D1 | Do schema, transaction, and placement constraints fit? |
| object and file storage | R2 | Are object lifecycle and access controls explicit? |
| strongly coordinated per-entity state | Durable Objects | Is object identity and migration behavior clear? |
| asynchronous processing | Queues | Are retries and duplicate delivery safe? |

## Testing Review

- Use the supported Worker runtime integration, not Node-only mocks, for runtime behavior.
- Generate types after configuration changes.
- Isolate test storage and understand current test-pool reset limitations.
- Exercise Durable Object restarts and queue duplicate delivery.
- Test compatibility-date changes before production rollout.
