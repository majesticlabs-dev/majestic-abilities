# Data Validation Framework Selection

Choose the smallest tool that owns the validation boundary clearly. Verify APIs against the installed version before implementation.

## Plain Assertions or SQL

Use when:

- there are few local invariants
- the execution environment already supports the checks
- failure output can be made actionable
- no shared validation artifact is required

Avoid when checks need reusable schemas, structured error collection, or durable validation history.

## Pydantic

Use for:

- record, message, configuration, or API boundaries
- parsing structured objects into typed application models
- field and cross-field validation
- explicit coercion and serialization behavior

Do not use record-by-record validation blindly for large tabular batches without measuring cost. Decide whether to fail fast or collect bounded errors.

Reference: <https://docs.pydantic.dev/>

## Pandera

Use for:

- DataFrame-like schema validation
- column and cross-column checks
- lazy collection of tabular failures
- typed transformation boundaries
- supported pandas, Polars, PySpark, Ibis, or other configured backends

Confirm backend-specific behavior, coercion, strictness, and lazy validation against the installed Pandera version.

Reference: <https://pandera.readthedocs.io/en/stable/>

## Great Expectations

Use when the team needs:

- named data assets and batches
- reusable expectation suites
- durable validation results
- checkpoints and operational validation runs
- shared human-readable validation artifacts

This operational surface can be excessive for a few DataFrame assertions. Current APIs differ materially from older 0.x examples, so use the documentation matching the installed version.

Reference: <https://docs.greatexpectations.io/>

## dbt Data Tests

Use for:

- warehouse model invariants
- source and model checks that belong in the dbt DAG
- singular SQL assertions
- reusable generic tests

Use dbt unit tests separately when model SQL logic should be checked against static inputs before materialization.

Reference: <https://docs.getdbt.com/docs/build/data-tests>

## Selection Questions

1. What exact boundary is protected?
2. Is validation record-oriented, tabular, or warehouse-resident?
3. Is coercion allowed?
4. Must all failures be collected?
5. Is durable validation history required?
6. Who owns rule definitions and failures?
7. What volume and latency must the validator handle?
8. Can one existing tool own the rule without duplication?

## Warning Signs

- Framework setup exceeds the contract complexity.
- The same invariant exists in several tools without one owner.
- Validation errors omit counts, locations, or next actions.
- Coercion changes values without an audit trail.
- A library version was assumed from stale examples.
