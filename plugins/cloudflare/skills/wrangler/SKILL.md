---
name: wrangler
description: "Use before running Wrangler commands for Cloudflare Workers or platform resources."
---

# Wrangler CLI

Use the project's Wrangler version and command runner. Check whether it is available before installing anything. Add or upgrade it only when the requested work needs that change, using the project's package manager.

## Current Sources

Verify the command or configuration fields needed for the task against current [Wrangler documentation](https://developers.cloudflare.com/workers/wrangler/) and the installed version's help or `node_modules/wrangler/config-schema.json`. Bundled examples can lag behind the CLI. Retrieve only the relevant documentation.

Preserve existing configuration format, compatibility date, and environments unless the task requires a change. Generate binding types after changes that affect them.

## Task References

Read only the reference for the requested operation. Load another when a dependency requires it.

| Task | Reference |
| --- | --- |
| Worker configuration and binding types | [Configuration](references/configuration.md) |
| Local server, bindings, and local secrets | [Local development](references/local-development.md) |
| Worker deployment, secrets, versions, and rollback | [Deployment](references/deployment.md) |
| KV namespaces and keys | [KV](references/kv.md) |
| R2 buckets and objects | [R2](references/r2.md) |
| D1 queries, migrations, and backups | [D1](references/d1.md) |
| Vector indexes and queries | [Vectorize](references/vectorize.md) |
| Database connections | [Hyperdrive](references/hyperdrive.md) |
| AI models and bindings | [Workers AI](references/workers-ai.md) |
| Queues and consumers | [Queues](references/queues.md) |
| Container images and registries | [Containers](references/containers.md) |
| Workflows and instances | [Workflows](references/workflows.md) |
| Ingestion pipelines | [Pipelines](references/pipelines.md) |
| Shared secret stores | [Secrets Store](references/secrets-store.md) |
| Pages deployment | [Pages](references/pages.md) |
| Logs and observability configuration | [Observability](references/observability.md) |
| Local tests and scheduled handlers | [Testing](references/testing.md) |
| Authentication, startup, or binding failures | [Troubleshooting](references/troubleshooting.md) |

## Operating Boundaries

- Verify the account, resource, and environment before authenticated operations. Confirm authorization before deployment, remote writes, or deletion.
- Safe local checks with disposable data can run within the requested task. Check remote bindings and service usage before treating local execution as isolated.
- Keep secrets out of source control, logs, output, and command arguments. Use a supported secure input method. Do not run a bundled example that violates this constraint.
- Resource creation, paid services, and remote tests require appropriate authorization. Command examples do not grant it.

## Completion

For implementation, continue until the requested behavior is exercised and relevant checks pass, or a concrete blocker requires user input. Fix failures caused by the change and rerun affected checks. Use existing test tooling; do not add a framework for a routine CLI task.

Report commands run, results, and unresolved checks. A local test or deployment dry run proves only local validation. If deployment is authorized, verify the deployed version and affected behavior before reporting live success.
