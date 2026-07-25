# Agent-Ready Repository Patterns

## Repository Guidance Entry

```markdown
## Database migrations

- Run `bin/db-migrate`; direct schema edits are overwritten.
- Verify with `bin/check-schema`.
- Production rollback requires the migration runbook in `docs/database.md`.
```

Include the supported path and verification command, not just a prohibition.

## Command Catalog

```markdown
## Repository commands

| Command | Purpose | Mutates data |
| --- | --- | --- |
| `bin/test` | Run the test suite | No |
| `bin/lint` | Check formatting and static rules | No |
| `bin/setup` | Prepare local dependencies | Development only |
| `bin/deploy staging` | Deploy staging | Yes, approval required |
```

## Teaching Validation Error

```text
ERROR: src/api/orders.ts imports src/internal/database.ts
Reason: API handlers must use the public data-access boundary.
Fix: import OrderRepository from src/data-access/orders.ts
Guide: docs/architecture/data-access.md
```

## Structural Test Questions

- What boundary is important enough to block a merge?
- Can the check parse structure instead of relying on fragile text matching?
- Does the failure identify the smallest correction?
- Can contributors run the exact check locally?
- Is there a fixture proving the validator catches the prohibited case?

## Guidance Placement

- Root guidance: repository-wide commands and invariants
- Nested guidance: package-specific commands, generated-file rules, and local boundaries
- Reference docs: long rationale, runbooks, and provider details
- Scripts: deterministic checks and transformations

Do not repeat the same rule at every level. The nearest applicable guidance should own the detail.

## Maintenance Review

```text
1. Find guidance whose referenced paths or commands no longer exist.
2. Find duplicated rules with different wording.
3. Confirm each important rule has a check or explicit manual verification.
4. Remove historical commentary that no longer changes behavior.
5. Run links, schema, and structural checks after cleanup.
```
