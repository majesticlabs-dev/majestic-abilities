---
name: data-source-assessment
description: Assess an unfamiliar data source by profiling its schema, grain, volume, change behavior, quality baseline, and extraction constraints. Use when evaluating a database, API, CSV, JSON, Parquet dataset, file drop, or event stream before pipeline integration.
---

# Data Source Assessment

Characterize a source before designing extraction or declaring a schema contract. Separate observed facts from inferences and recommendations.

## Boundary

Use this skill for source discovery and ingestion planning.

- Use `csv-wrangling` when a delimited file cannot be parsed reliably.
- Use `data-quality` to define ongoing trust signals and service levels.
- Use `data-validation` to implement executable contracts.
- Use `data-pipeline-design` after source behavior is understood.

## Inputs

Collect only the access needed for safe inspection:

1. Source type, location, and owner.
2. Read-only access method and authentication boundary.
3. Available documentation or schema registry.
4. Representative samples from more than one time period when possible.
5. Expected consumers and required freshness.
6. Known incidents, quirks, or compliance constraints.

Do not copy secrets into the report. Do not run unbounded queries against production.

## Workflow

### 1. Identify the source contract

Record:

- system of record and owner
- object, endpoint, topic, or file naming convention
- declared grain
- delivery mechanism and cadence
- retention and replay availability
- authentication and rate limits
- personally identifiable or regulated fields

Treat documentation as a claim to verify, not proof.

### 2. Sample safely

Use bounded queries, representative partitions, or byte-limited file samples. Include:

- normal periods
- recent data
- known peak periods
- at least one boundary such as month end or daylight-saving transition when relevant

Record sampling filters and blind spots. A head-only sample cannot prove global uniqueness, distributions, or maximum lengths.

### 3. Profile structure

For each field, measure or infer:

- physical and semantic type
- null and empty rates
- cardinality and representative values
- minimum, maximum, and length bounds
- timestamp timezone and precision
- nested or repeated structure
- candidate keys and relationships
- observed format violations

Assign confidence to inferred types and constraints. Leading zeros, identifier-like numbers, locale-specific dates, and mixed units require special caution.

### 4. Establish grain and keys

State the grain in one sentence. Test candidate keys on the largest safe sample and across periods.

Distinguish:

- source primary key
- business or natural key
- extraction cursor
- ordering tie-breaker
- foreign-key-like relationship

A timestamp alone is rarely a safe unique cursor.

### 5. Measure volume and change behavior

Record:

- current size and growth
- typical and peak batch size
- arrival cadence and delay distribution
- insert, update, and delete behavior
- late-arriving and corrected records
- schema change history
- backfill and replay limits

For APIs, also capture pagination semantics, rate limits, retry headers, and consistency behavior.

### 6. Establish a quality baseline

Measure relevant baselines without turning observations into permanent thresholds:

- missingness
- duplicate rate
- invalid categories or ranges
- referential coverage
- volume by partition
- freshness and latency
- distribution shifts across sampled periods

Explain known exceptions such as negative refunds or historically nullable fields.

### 7. Recommend extraction behavior

Choose the safest initial approach:

- bounded full refresh
- timestamp plus tie-breaker
- source sequence or cursor
- change data capture
- immutable append
- snapshot comparison

Specify watermark semantics, overlap window, delete handling, checkpoint commit point, backfill path, and reconciliation checks. Use full refresh when safe incrementality cannot be justified.

## Deliverable

Use [source-assessment-template.md](references/source-assessment-template.md). Include:

1. Source identity and ownership
2. Access and sampling method
3. Grain, keys, and relationships
4. Schema with inference confidence
5. Volume, cadence, and change behavior
6. Quality baseline
7. Security and compliance notes
8. Recommended extraction contract
9. Unknowns and verification plan

## Quality Gate

- Observed, declared, and inferred facts are labeled separately.
- Sampling limits are explicit.
- Grain and cursor are not conflated.
- Deletes, late data, and schema drift are addressed.
- Recommendations map to measured source behavior.
- Unknowns remain visible instead of becoming guessed contracts.
