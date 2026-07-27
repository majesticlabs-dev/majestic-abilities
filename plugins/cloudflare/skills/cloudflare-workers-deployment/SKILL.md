---
name: cloudflare-workers-deployment
description: "Configure, validate, and deploy Cloudflare Workers with Wrangler. Use when managing `wrangler.jsonc`, bindings, environments, secrets, local development, generated types, deployment versions, or production rollbacks."
---

# Cloudflare Workers Deployment

Scope this skill to Wrangler configuration and deployment operations. When a change also affects handler architecture, Durable Object state, queues, or framework code, treat that implementation as a separate review surface and load [application-checklist.md](references/application-checklist.md).

Wrangler changes quickly. Retrieve current Cloudflare documentation and inspect the installed Wrangler configuration schema before relying on flags or binding shapes.

## Workflow

### 1. Use a Project-Local Wrangler

```sh
npm install -D wrangler@latest
npx wrangler --version
npx wrangler whoami
```

Prefer `npx wrangler` so local development and CI use the version pinned by the project lockfile.

### 2. Prefer `wrangler.jsonc`

Use `wrangler.jsonc` for new projects. Include the local schema and replace `YYYY-MM-DD` with a reviewed compatibility date from current Cloudflare guidance.

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "YYYY-MM-DD",
  "observability": {
    "enabled": true
  }
}
```

Do not mechanically convert a working TOML configuration. Migrate only when the change is scoped and validated.

### 3. Model Bindings Explicitly

Keep binding names stable across configuration and generated TypeScript types. Separate non-secret variables from secrets.

```jsonc
{
  "kv_namespaces": [
    { "binding": "CACHE", "id": "<NAMESPACE_ID>" }
  ],
  "r2_buckets": [
    { "binding": "ASSETS", "bucket_name": "my-assets" }
  ],
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "<DATABASE_ID>"
    }
  ]
}
```

Verify each binding shape against `node_modules/wrangler/config-schema.json`.

### 4. Generate Types After Configuration Changes

```sh
npx wrangler types
npx wrangler types --check
```

Commit generated binding types when that is the project's convention. Fail CI when config and types drift.

### 5. Handle Secrets Safely

```sh
npx wrangler secret put API_KEY
npx wrangler secret list
```

Use `.dev.vars` only for local secrets and add it to `.gitignore`. Never put secret values in `wrangler.jsonc`, command arguments, logs, or committed example files.

### 6. Validate Locally

```sh
npx wrangler dev
npx wrangler deploy --dry-run
```

Run the project test suite. Exercise each changed binding locally when simulation is supported. Mark remote bindings explicitly and avoid accidental production writes during development.

### 7. Deploy and Observe

```sh
npx wrangler deploy --env production
npx wrangler versions list
npx wrangler tail --env production --status error
```

Capture the deployed version. If production regresses, inspect the current version history and use Wrangler's documented rollback command rather than redeploying unknown local state.

## Review Checklist

- local Wrangler version is pinned
- `wrangler.jsonc` matches the installed schema
- compatibility date is intentional
- environment overrides include every non-inheritable binding they need
- secrets are not committed or logged
- generated types match bindings
- dry run and tests pass
- deployment and rollback procedures are documented

## Completion Report

Report the Wrangler version, environments affected, bindings changed, tests and dry runs executed, deployed version, and remaining operational risks.
