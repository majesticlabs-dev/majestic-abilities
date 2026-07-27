---
name: skill-grader
description: Grade a skill execution against explicit expectations using transcript and output evidence, then audit unsupported claims and weak evaluations. Use when reviewing skill test runs, regression fixtures, generated artifacts, or acceptance criteria for an agent capability.
---

# Skill Grader

Evaluate whether a skill execution genuinely met its expectations. Give passing credit only when available evidence supports it.

## Inputs

Collect:

- original task prompt
- explicit expectations
- execution transcript or event log
- generated output files
- environment or fixture details needed to interpret the run
- requested result path, if grading must be persisted

Rewrite vague expectations into verifiable statements before grading. Preserve the original wording alongside any operational interpretation.

## Evidence Standard

Use this precedence:

1. Directly inspectable output or machine result
2. Transcript evidence showing the relevant action and result
3. Self-reported final summary
4. No evidence

A statement in the final summary does not prove that the work happened. A correct filename with incorrect content does not pass a content expectation.

## Workflow

### 1. Inventory the run

Record:

- available transcript and outputs
- missing or unreadable artifacts
- execution errors and retries
- final reported result
- environment limitations

Do not infer success from absent evidence.

### 2. Grade each expectation

For every expectation:

1. State the exact verification method.
2. Locate supporting and contradicting evidence.
3. Check substance, not keyword presence.
4. Return `PASS`, `FAIL`, or `UNVERIFIABLE`.
5. Cite the evidence location.

Use `UNVERIFIABLE` when required evidence is unavailable. Count it separately rather than quietly passing or failing it.

### 3. Extract implicit claims

Identify material factual, process, and quality claims made by the execution.

For each claim, record:

- claim text
- type
- evidence
- status
- consequence if false

Focus on claims that affect acceptance. Do not inventory harmless prose.

### 4. Audit the expectations

Flag an expectation when:

- superficial output could pass it
- it tests formatting but not the intended outcome
- no available artifact can verify it
- an important failure mode has no expectation
- multiple expectations duplicate the same evidence

Suggest the smallest stronger check.

### 5. Summarize without hiding failures

Report expectation counts by `PASS`, `FAIL`, and `UNVERIFIABLE`. Calculate pass rate as:

```text
PASS / total expectations
```

Also report verified rate when useful:

```text
(PASS + FAIL) / total expectations
```

Do not remove unverifiable expectations from the denominator without saying so.

## Output

```json
{
  "expectations": [
    {
      "text": "Output includes X",
      "verdict": "PASS",
      "evidence": ["path or transcript location"],
      "reason": "Why the evidence proves or fails to prove the expectation"
    }
  ],
  "summary": {
    "passed": 0,
    "failed": 0,
    "unverifiable": 0,
    "total": 0,
    "pass_rate": 0.0
  },
  "claims": [
    {
      "claim": "...",
      "type": "factual",
      "verdict": "VERIFIED",
      "evidence": ["..."]
    }
  ],
  "evaluation_feedback": [
    {
      "expectation": "...",
      "gap": "...",
      "stronger_check": "..."
    }
  ]
}
```

Persist the JSON only when requested or when the caller supplied a result path.

## Quality Gate

- Every verdict cites evidence or explicitly states its absence.
- Content is inspected rather than inferred from filenames.
- Unsupported final-summary claims do not receive credit.
- Unverifiable expectations remain visible.
- Evaluation feedback targets real acceptance gaps.
