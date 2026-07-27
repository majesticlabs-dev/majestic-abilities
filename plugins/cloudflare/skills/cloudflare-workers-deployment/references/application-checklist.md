# Cloudflare Worker Application Checklist

Retrieve current Cloudflare product and framework documentation before writing API signatures, binding shapes, migrations, or limits.

## Handler Boundary

- Keep request parsing, validation, domain work, and response formatting separable.
- Type the `env` bindings generated from `wrangler.jsonc`.
- Pass bindings explicitly instead of hiding them in module globals.
- Stream large responses and request bodies when buffering is unnecessary.
- Do not log secrets, authorization headers, or sensitive payloads.

## Frameworks

When using Hono or another router:

- verify the framework version and Cloudflare adapter
- type environment bindings and request variables
- keep middleware ordering visible
- return platform-native `Response` objects at the edge boundary
- test error and not-found behavior explicitly

Do not introduce a framework for a trivial Worker that native routing can express clearly.

## Storage Choice

- **KV:** read-heavy, globally distributed data that tolerates eventual consistency
- **D1:** relational data and transactions within D1's documented constraints
- **R2:** objects, files, and large payloads
- **Durable Objects:** per-entity coordination, strong consistency, WebSockets, or stateful workflows
- **Queues:** asynchronous work that can be retried and processed idempotently

Do not select storage from convenience alone. Document consistency, retention, region, failure, and cost assumptions.

## Durable Objects

- Keep object identity and routing deterministic.
- Make storage migrations explicit and deploy them in the required order.
- Avoid unbounded in-memory state.
- Use alarms and WebSockets only with explicit recovery behavior.
- Test concurrent requests, object restarts, and migration paths.

## Queues

- Make consumers idempotent because messages can be retried.
- Define retry, dead-letter, and poison-message handling.
- Bound batch work and external-call concurrency.
- Acknowledge messages only after durable side effects complete.
- Test partial batch failures and duplicate delivery.

## Testing

Use the current `@cloudflare/vitest-pool-workers` guidance when the project uses Vitest. Test:

- generated binding types and configuration drift
- local and remote binding assumptions
- handler success and error paths
- storage consistency boundaries
- Durable Object restart and concurrency behavior
- queue retries and duplicate messages
- deployment compatibility-date changes
