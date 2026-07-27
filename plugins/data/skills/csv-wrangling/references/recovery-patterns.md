# CSV Recovery Patterns

## Preserve Evidence

Before parsing, record a cryptographic checksum and file size. Keep the original bytes immutable.

```python
from hashlib import sha256
from pathlib import Path

path = Path("input.csv")
digest = sha256(path.read_bytes()).hexdigest()
print({"bytes": path.stat().st_size, "sha256": digest})
```

For very large files, stream the checksum instead of reading the whole file into memory.

## Encoding Decisions

1. Check for a byte-order mark.
2. Attempt strict UTF-8 when expected.
3. Use source metadata or producer confirmation.
4. Treat statistical encoding detection as a candidate, not certainty.
5. Compare replacement-character and control-character rates across candidates.

Avoid `errors="ignore"` because it deletes bytes without an audit trail. Use strict decoding for the accepted path. When recovery is necessary, preserve the rejected bytes and report replacements.

## Dialect Decisions

Use Python's `csv` module or another standards-aware parser:

```python
import csv

with open("input.csv", encoding="utf-8", errors="strict", newline="") as handle:
    sample = handle.read(65536)
    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    handle.seek(0)
    reader = csv.reader(handle, dialect)
    for row in reader:
        process(row)
```

Validate inferred delimiter and quote behavior against later regions. A delimiter count is unreliable when delimiters occur inside quoted fields.

## Header Recovery

Look for:

- metadata preamble
- duplicate names
- empty names
- repeated headers in concatenated exports
- multi-row headers
- trailing columns created by delimiters

Keep a reversible source-to-output name mapping.

## Malformed Rows

Quarantine instead of silently skipping. Capture:

```json
{
  "record_number": 42,
  "raw_text": "escaped or redacted source record",
  "error": "unexpected field count",
  "expected_fields": 12,
  "observed_fields": 14,
  "recovery": "none"
}
```

Physical lines and logical CSV records differ when quoted fields contain newlines. Prefer parser-provided record context.

## Locale-Sensitive Values

Require explicit rules for:

- `1,234.56` versus `1.234,56`
- `01/02/2026` day and month order
- currency symbols and accounting negatives
- timezone abbreviations
- decimal precision and rounding
- empty, `NULL`, `N/A`, zero, and whitespace-only values

Identifiers such as postal codes and account numbers should remain strings when leading zeros matter.

## Chunked Processing

Infer and approve a schema before loading all chunks. Then apply the same schema to each chunk.

Track per chunk:

- input records
- accepted records
- quarantined records
- coercion failures
- output records
- schema deviations

Do not allow later chunks to silently widen or reinterpret types.

## Reconciliation

Use an explicit equation:

```text
source logical records
= accepted output records
+ quarantined records
+ intentionally filtered records
```

When the producer supplies control totals, reconcile sums or hashes in addition to counts.
