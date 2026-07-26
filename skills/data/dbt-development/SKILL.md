---
name: dbt-development
description: Build and review dbt projects with clear model layers, explicit grain, sources, materializations, incremental behavior, tests, documentation, and scoped verification. Use when creating or changing dbt models, snapshots, macros, sources, data tests, unit tests, or project structure.
---

# dbt Development

Implement transformations in the conventions and dbt version already used by the project. Inspect the adapter, project configuration, packages, and neighboring models before changing code.

## Boundary

Use `data-pipeline-design` to decide source extraction, checkpointing, file publication, and non-dbt pipeline behavior. Use `data-pipeline-testing` for fixture design, multi-run incremental scenarios, and reconciliation oracles. dbt implements transformation logic and warehouse contracts; it does not replace source-change analysis.

## Workflow

### 1. Inspect the project

Read:

- `dbt_project.yml`
- dependency or package files
- source definitions
- neighboring model SQL and YAML
- adapter and warehouse configuration
- CI commands
- installed dbt version when available

Follow existing naming and configuration unless they are the problem.

### 2. State the model contract

Before writing SQL, define:

- model purpose
- grain
- primary or unique key
- upstream sources and models
- downstream consumers
- materialization
- update and delete behavior
- required tests and documentation

Every model should have one explainable grain.

### 3. Place logic in the correct layer

Use the project's layering conventions. A common flow is:

- **Staging:** source-conformed renaming, casting, and light cleanup
- **Intermediate:** purpose-built joins or transformations
- **Marts:** business-conformed entities and facts for consumers

Do not force an intermediate layer when it adds no clarity. Avoid embedding final business metrics in source-conformed staging models.

### 4. Write dependency-aware SQL

- Use `source()` for declared raw sources.
- Use `ref()` for dbt-managed dependencies.
- Select explicit columns once the model contract matters.
- Name transformation CTEs by purpose.
- Make join cardinality and deduplication tie-breakers visible.
- Keep warehouse-specific SQL intentional and documented.

### 5. Choose materialization deliberately

Select view, table, incremental, ephemeral, snapshot, or project-specific materialization based on data volume, update behavior, cost, and consumer needs.

For incremental models, use [dbt-patterns.md](references/dbt-patterns.md) and define:

- reliable filter or change signal
- unique key
- adapter-supported incremental strategy
- overlap and late-arrival behavior
- delete handling
- full-refresh and backfill procedure

A `max(timestamp)` filter without a tie-breaker, overlap, and late-data analysis is not a complete incremental design.

### 6. Add tests at the right level

Use:

- source freshness for arrival expectations
- data tests for dataset invariants
- unit tests for model SQL logic on static inputs when supported by the project version
- singular tests for cross-row or cross-model rules
- reconciliation queries for critical totals

Current dbt documentation calls schema assertions data tests; `tests` may remain a supported alias in some versions. Follow the installed version and project convention.

### 7. Document ownership and meaning

Document model purpose, grain, important columns, owners, and material caveats. Do not write descriptions that merely restate column names.

### 8. Verify narrowly, then broadly

Use the project's commands. Typical progression:

```sh
dbt parse
dbt compile --select <model>
dbt build --select +<model>+
dbt source freshness
```

Scope builds during iteration, then run the required downstream or CI surface. Inspect compiled SQL when Jinja, dispatch, or adapter behavior matters.

### 9. Review generated warehouse behavior

Check:

- query plan or warehouse cost where material
- row count and grain
- duplicates and nulls
- incremental merge behavior
- downstream compatibility
- full-refresh safety

## Output

For implementation, return changed models, YAML, tests, and verification results. For review, return:

1. Contract and grain findings
2. Layering and dependency issues
3. Materialization and incrementality risks
4. Test and documentation gaps
5. Smallest correct changes
6. Commands needed to verify

## Quality Gate

- Model grain and key are explicit.
- `source()` and `ref()` preserve the DAG.
- Layer placement has a clear purpose.
- Incremental behavior covers late data, deletes, and full refresh.
- Tests protect meaningful contracts.
- Verification matches the installed dbt version and adapter.
