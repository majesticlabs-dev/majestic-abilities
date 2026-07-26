# dbt Development Patterns

Verify syntax against the installed dbt Core or platform version and adapter. dbt features and YAML conventions evolve.

## Layering

A common project flow is:

```text
sources -> staging -> intermediate when needed -> marts
```

- Staging models remain source-conformed and usually have a one-to-one relationship with source tables.
- Intermediate models isolate purpose-built transformations that improve readability or reuse.
- Marts expose business-conformed entities and facts at explicit grains.

References:

- <https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview>
- <https://docs.getdbt.com/best-practices/how-we-structure/2-staging>
- <https://docs.getdbt.com/best-practices/how-we-structure/3-intermediate>
- <https://docs.getdbt.com/best-practices/how-we-structure/4-marts>

## Model SQL

```sql
with source_orders as (
    select *
    from {{ source('raw', 'orders') }}
),

renamed as (
    select
        id as order_id,
        customer_id,
        cast(order_date as date) as ordered_on,
        amount as order_amount,
        source_updated_at
    from source_orders
)

select *
from renamed
```

Once a model contract is stable, prefer explicit final columns and document the grain.

## Data Tests

Current dbt documentation calls these data tests. Follow project conventions when `tests` is used as a supported alias.

```yaml
version: 2

models:
  - name: fct_orders
    description: One row per order.
    columns:
      - name: order_id
        data_tests:
          - not_null
          - unique
      - name: customer_id
        data_tests:
          - not_null
```

Add relationship, accepted-value, range, and singular SQL tests where they protect real contracts.

Reference: <https://docs.getdbt.com/docs/build/data-tests>

## Unit Tests

Use dbt unit tests when supported by the installed version to validate model SQL against small static inputs before materializing the model. They are particularly useful for complex `CASE` logic, window functions, date behavior, and edge cases.

Keep data tests for assertions about built datasets. Unit tests and data tests solve different problems.

Reference: <https://docs.getdbt.com/docs/build/unit-tests>

## Incremental Models

An incremental model needs more than `is_incremental()`:

- reliable source change signal
- explicit `unique_key`
- adapter-supported strategy
- deterministic update precedence
- overlap for late changes where needed
- delete behavior
- full-refresh and backfill process
- tests that run the model across multiple states

The exact overlap expression and merge strategy are warehouse-specific. Inspect adapter documentation and compiled SQL.

Reference: <https://docs.getdbt.com/best-practices/materializations/4-incremental-models>

## Snapshots

Use snapshots when source records mutate and consumers need tracked history. Define:

- stable unique key
- timestamp or check strategy
- invalidation or deletion behavior
- timezone semantics
- expected history growth

Do not use snapshots as a substitute for a reliable source change contract without understanding their query and storage cost.

## Macros

Create a macro when SQL behavior is genuinely repeated and one implementation should own it. Keep business logic visible in models when abstraction would hide grain or make compiled SQL harder to review.

Test macros through models or dedicated fixtures. Inspect dispatch and adapter overrides.

## Verification

Typical commands, adjusted to project tooling:

```sh
dbt parse
dbt compile --select <model>
dbt build --select +<model>+
dbt source freshness
```

Review compiled SQL, test failures, row grain, incremental state transitions, and downstream selection. Do not assume a successful command means the model contract is correct.
