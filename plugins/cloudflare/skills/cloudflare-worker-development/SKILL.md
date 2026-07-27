---
name: cloudflare-worker-development
description: "Build and review TypeScript applications for the Cloudflare Workers runtime. Use when implementing Worker handlers, Hono routes, bindings, Durable Objects, Queues, or tests that execute in workerd."
---

# Cloudflare Worker Development

Keep this skill focused on application code and runtime semantics. Wrangler configuration, secrets, deployment versions, and rollback belong to `cloudflare-workers-deployment` when that skill is installed.

Cloudflare APIs, limits, and testing tools change quickly. Retrieve current Cloudflare documentation and inspect the installed Wrangler schema and package types before relying on signatures or limits.

## Workflow

### 1. Inspect the Runtime Contract

Identify:

- module entry point and request handlers
- `wrangler.jsonc` or existing Wrangler configuration
- compatibility date and flags
- generated binding types
- storage and service bindings
- package versions and test setup

```sh
npx wrangler --version
npx wrangler types --check
```

Regenerate types after binding changes instead of maintaining a handwritten `Env` interface that can drift.

### 2. Keep the Request Boundary Small

Separate:

1. request parsing and validation
2. authorization and policy checks
3. domain work
4. storage or service calls
5. response formatting

Pass bindings explicitly through handler or service boundaries. Do not hide request-specific state or bindings in mutable module globals.

Use Hono or another router only when routing, middleware, or typed context provides enough value to justify the dependency. A small Worker may be clearer with the native module handler.

### 3. Choose Storage by Semantics

- **KV:** read-heavy globally distributed data that tolerates eventual consistency
- **D1:** relational data and transactions within current D1 constraints
- **R2:** objects, files, and large payloads
- **Durable Objects:** per-entity coordination, strong consistency, alarms, or long-lived connections
- **Queues:** asynchronous work with retry and duplicate-delivery handling

Load [runtime-patterns.md](references/runtime-patterns.md) before introducing Durable Objects, queue consumers, or a new storage binding.

### 4. Handle Background Work Explicitly

Use the runtime execution context for non-blocking work that must outlive the response. Do not fire untracked promises. Await work that determines response correctness, authorization, billing, or durable state.

Queue consumers must be idempotent. Define retry, dead-letter, partial-batch, and poison-message behavior before deployment.

### 5. Protect Runtime Boundaries

- validate untrusted request data
- enforce authentication and authorization before storage access
- never log secrets, authorization headers, or sensitive payloads
- bound request bodies, batches, loops, and outbound concurrency
- stream large bodies when buffering is unnecessary
- preserve request and trace identifiers across service and queue boundaries

### 6. Test in the Worker Runtime

Prefer the current Cloudflare Vitest integration when the project uses Vitest so tests execute in `workerd`, not a generic Node.js approximation.

Test:

- handler success, validation, authorization, and error paths
- binding/configuration type drift
- storage consistency assumptions
- Durable Object identity, restart, concurrency, and migration behavior
- queue retries, duplicate messages, and partial failures
- compatibility-date or flag changes

Check current testing documentation for beta limitations before depending on unsupported isolation or RPC behavior.

### 7. Verify

Run the repository's narrow test first, then broader tests, type checks, and deployment dry run:

```sh
npx wrangler types --check
npm test
npx wrangler deploy --dry-run
```

Use the package manager and commands already established by the repository.

## Completion Report

Report:

- handlers and bindings changed
- storage and consistency decisions
- Durable Object or queue behavior
- tests and type checks run
- compatibility assumptions checked
- unresolved runtime, migration, or deployment risks
