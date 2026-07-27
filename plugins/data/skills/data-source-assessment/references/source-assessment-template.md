# Data Source Assessment Template

## Source Identity

- **Name:**
- **Type:** database, API, event stream, file drop, or object storage
- **System of record:**
- **Owner:**
- **Consumers:**
- **Sensitivity:**

## Access and Sampling

- **Read method:**
- **Authentication boundary:**
- **Rate or query limits:**
- **Samples and time periods:**
- **Sampling filters:**
- **Blind spots:**

## Grain and Keys

- **Declared grain:**
- **Observed grain:**
- **Primary or natural key:**
- **Extraction cursor:**
- **Ordering tie-breaker:**
- **Relationships:**
- **Evidence and confidence:**

## Schema

| Field | Physical type | Semantic type | Nullable | Cardinality | Constraints | Confidence | Evidence |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| | | | | | | | |

Record timezone, precision, units, encoding, and nested structure where relevant.

## Volume and Delivery

- Current size:
- Typical batch:
- Peak batch:
- Growth:
- Delivery cadence:
- Arrival delay:
- Retention and replay:

## Change Behavior

- Inserts:
- Updates:
- Deletes or tombstones:
- Late arrivals:
- Historical corrections:
- Schema changes:
- Backfill limits:

## Quality Baseline

| Signal | Observed baseline | Sample period | Known exceptions |
| --- | --- | --- | --- |
| Missingness | | | |
| Duplicates | | | |
| Invalid values | | | |
| Referential coverage | | | |
| Volume | | | |
| Freshness | | | |

## Recommended Extraction Contract

- Strategy:
- Cursor and tie-breaker:
- Overlap window:
- Target write behavior:
- Delete handling:
- Checkpoint commit point:
- Backfill approach:
- Reconciliation:
- Validation gates:

## Security and Operations

- Secret handling:
- Sensitive-field controls:
- Expected failure modes:
- Owner and escalation:

## Unknowns

| Unknown | Why it matters | Verification | Owner |
| --- | --- | --- | --- |
| | | | |
