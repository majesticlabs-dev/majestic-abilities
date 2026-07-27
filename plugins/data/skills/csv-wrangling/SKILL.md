---
name: csv-wrangling
description: Diagnose and recover messy delimited files without silently dropping or corrupting records. Use when CSV or TSV files have uncertain encoding, delimiters, headers, quoting, malformed rows, locale-specific values, schema drift, or excessive size.
---

# CSV Wrangling

Turn an unreliable delimited file into a reproducible typed dataset while preserving raw evidence and quarantining unresolved records.

## Boundary

Use this skill when parsing itself is uncertain. Use `data-source-assessment` after the file can be read consistently and its broader extraction contract needs analysis.

## Safety Rules

- Preserve the original bytes and record a checksum.
- Work on a copy.
- Never use character-decoding error suppression as an unexplained final solution.
- Never skip malformed rows without counting and retaining them.
- Do not parse quoted CSV with a delimiter-splitting regular expression.
- Treat inferred headers, dates, booleans, identifiers, and numeric formats as hypotheses.

## Workflow

### 1. Inspect bytes before rows

Record:

- file size and checksum
- byte-order mark
- line-ending style
- null bytes or binary contamination
- candidate encodings and confidence
- whether concatenated files have repeated headers

Try strict UTF-8 first when appropriate. If detection is ambiguous, compare candidate decodings against known text and replacement-character counts.

### 2. Detect the dialect

Sample multiple regions, not only the first line. Evaluate:

- delimiter
- quote character
- escaping convention
- line terminator
- expected field count
- comments or metadata before the header

Prefer a standards-aware CSV parser. Validate the inferred dialect against later rows.

### 3. Locate and normalize headers

Identify metadata lines, repeated headers, unnamed columns, duplicate names, and whitespace differences.

Keep a mapping from source names to normalized names. Do not erase source names from the audit report.

### 4. Parse with quarantine

Parse rows under an explicit dialect and expected column count. For failures, retain:

- physical line or record number
- raw bytes or safely escaped raw text
- parser error
- observed field count
- attempted recovery

Choose and document whether malformed rows block the load, enter quarantine, or are repaired by a deterministic rule.

### 5. Normalize values deliberately

Handle per-column rules for:

- null sentinels versus empty strings
- decimal and thousands separators
- currency symbols and accounting negatives
- dates with locale and timezone
- booleans and categorical values
- identifiers with leading zeros
- embedded whitespace and control characters

Do not infer day/month ordering from ambiguous values without source context.

### 6. Control type inference

Infer from a representative sample, then validate across all chunks. Lock the resulting schema before concatenating chunks.

Use nullable types where missing values are valid. Record coercion failures rather than silently turning them into nulls.

### 7. Scale safely

For large files:

- stream or process fixed-size chunks
- preserve schema across chunks
- aggregate rejected-row counts
- avoid loading the whole raw file merely to detect a delimiter
- write typed intermediate outputs atomically

### 8. Reconcile

Verify:

- source record count
- parsed record count
- quarantined count
- intentionally filtered count
- output count
- checksum or control totals when available

The counts must reconcile exactly.

## Detailed Guidance

Use [recovery-patterns.md](references/recovery-patterns.md) for encoding, malformed-row, locale, and large-file decisions.

## Output

Return:

1. Source checksum and byte-level findings
2. Chosen encoding and dialect with confidence
3. Header mapping
4. Locked output schema
5. Normalization rules
6. Quarantine summary and sample failures
7. Reconciliation equation
8. Reproducible read or conversion command
9. Remaining ambiguities

## Quality Gate

- Raw bytes remain recoverable.
- No record disappears without an accounted reason.
- Parsing uses a CSV-aware parser.
- Type and locale assumptions are explicit.
- Chunk processing produces a stable schema.
- Counts reconcile from source to output.
