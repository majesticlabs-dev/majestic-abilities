---
name: data-validation
description: Design executable data contracts and validation behavior across records, DataFrames, warehouse models, and pipeline boundaries. Use when enforcing schemas, nullability, uniqueness, ranges, relationships, business rules, schema evolution, quarantine, or validation failure policy.
---

# Data Validation

Turn data expectations into executable checks with explicit failure behavior. Validation should protect a boundary, not merely produce a report.

## Boundary

- Use `data-quality` to define ongoing trust indicators, service levels, and alert ownership.
- Use `data-source-assessment` when the source contract is still unknown.
- Use `data-pipeline-testing` to test transformation code and replay behavior.

## Inputs

Establish:

1. Boundary being validated.
2. Declared grain and keys.
3. Required schema and semantic rules.
4. Allowed coercions and schema changes.
5. Batch, record, or table-level failure policy.
6. Evidence and retention requirements for rejected data.
7. Consumer tolerance for partial delivery.

## Workflow

### 1. Write the contract independently of tools

Define:

- required, optional, and forbidden fields
- physical and semantic types
- nullability
- uniqueness and grain
- allowed categories and ranges
- cross-field rules
- referential requirements
- temporal ordering
- schema version and compatibility policy

Do not infer permanent contracts from one sample without domain confirmation.

### 2. Place checks at boundaries

Choose where each invariant is cheapest to diagnose and safest to enforce:

- record ingress
- batch ingestion
- post-normalization
- pre-load
- warehouse model
- publication

Validate raw shape before transformation and business meaning after normalization.

### 3. Choose the smallest implementation

Use [framework-selection.md](references/framework-selection.md).

Prefer:

- language assertions or SQL for a few local invariants
- Pydantic for record and message boundaries
- Pandera for DataFrame-like schemas and checks
- Great Expectations when durable validation runs and shared artifacts justify it
- dbt data tests for warehouse model assertions

Do not add a framework when setup is larger than the contract.

### 4. Make failure semantics explicit

For every check, choose:

- block the entire batch
- quarantine invalid records
- publish with degraded status
- warn and continue
- retry after a transient dependency failure

State severity, owner, evidence retained, and replay behavior. Never silently drop invalid records.

### 5. Control coercion

Document accepted conversions such as string to date or integer widening. Reject ambiguous conversions such as locale-unknown dates or lossy numeric casts.

Report original value, attempted conversion, and error. Validation and normalization must not collapse into invisible mutation.

### 6. Handle schema evolution

Classify changes:

- additive compatible field
- required-field addition
- removal
- rename
- type widening
- type narrowing
- semantic or unit change
- grain or key change

Version contracts when consumers need transition time. A syntactically compatible change can still be semantically breaking.

### 7. Return actionable results

Each failed check should include:

- rule identifier and version
- boundary and dataset
- severity
- failed count and evaluated count
- representative failures with sensitive values redacted
- affected partition or cursor range
- owner and next action

Cap samples without hiding total failure counts.

### 8. Test the validators

Test valid, invalid, null, boundary, malformed, and schema-change cases. Verify quarantine, batch blocking, and replay behavior, not just rule predicates.

## Output

```markdown
# Data Validation Contract

## Boundary and Grain
...

## Rules
| ID | Boundary | Invariant | Severity | Failure behavior | Owner |
| --- | --- | --- | --- | --- | --- |

## Coercion Policy
- ...

## Schema Evolution Policy
- ...

## Validation Result Schema
- ...

## Validator Tests
- ...
```

## Quality Gate

- Every rule protects a named boundary and consumer need.
- Grain, keys, and null semantics are explicit.
- Failure and quarantine behavior is testable.
- Coercions are deliberate and non-lossy.
- Schema evolution covers semantic changes.
- Error evidence is actionable and privacy-safe.
