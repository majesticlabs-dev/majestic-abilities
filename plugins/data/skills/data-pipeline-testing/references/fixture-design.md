# Data Pipeline Fixture Design

## Prefer Named Minimal Cases

Each fixture row should exist for a reason. Use identifiers that make failures readable:

| ID | Purpose |
| --- | --- |
| `normal-1` | ordinary accepted record |
| `duplicate-newer` | deduplication winner |
| `duplicate-older` | deduplication loser |
| `late-update` | arrives behind live cursor |
| `unknown-status` | quarantine path |
| `deleted-source` | tombstone or anti-join behavior |

Keep expected output beside the input when practical.

## Boundary Cases

Include relevant cases:

- null versus empty string
- zero versus missing
- minimum and maximum allowed values
- decimal rounding boundaries
- Unicode and whitespace
- identifiers with leading zeros
- daylight-saving and timezone boundaries
- duplicate timestamps with distinct tie-breakers
- many-to-one and one-to-many joins
- unmatched foreign keys
- empty input and empty output

## Multi-Run Fixtures

Represent state transitions explicitly:

```text
run-1: initial rows
run-2: exact replay
run-3: new row and update
run-4: late update and delete
run-5: failed partial attempt followed by retry
run-6: overlapping backfill
```

Store the expected target and checkpoint after each run.

## Generated Data

Use generated data for:

- broad numeric ranges
- invariant and property testing
- parser fuzzing
- volume and performance tests

Use fixed seeds. On failure, preserve the minimal failing example as a named regression fixture.

Do not generate only valid data. Inject invalid cases intentionally and label the expected failure path.

## Golden Outputs

Golden outputs work well for complex deterministic transformations when:

- fixtures remain small and reviewable
- updates require intentional review
- order is normalized before comparison
- volatile fields are removed or controlled

Do not accept broad golden-file updates without understanding the semantic change.

## Reconciliation Oracles

Prefer independent expectations:

- source keys minus rejected keys equal target keys
- accepted plus quarantined equals extracted
- partition totals match source control totals
- aggregate amounts reconcile within defined rounding
- rerun leaves target unchanged

Avoid calculating expected values with the same function under test.

## Privacy

Use synthetic or irreversibly anonymized fixtures. Do not copy production personal data into the repository. Preserve domain shape without preserving identities.
