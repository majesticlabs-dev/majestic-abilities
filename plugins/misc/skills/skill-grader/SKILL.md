---
name: skill-grader
description: Grade one skill execution or audit skill effectiveness across several agent conversations using transcript and output evidence, then identify unsupported claims and justified skill changes. Use when reviewing skill test runs, regression fixtures, generated artifacts, acceptance criteria, or whether installed skills improve real agent work.
---

# Skill Grader

Evaluate whether skill-guided work genuinely met its expectations. Grade one execution or audit a set of conversations. Give passing credit only when available evidence supports it.

## Evaluation Modes

Choose one mode:

- **Execution grade:** Evaluate one skill run against explicit expectations.
- **Effectiveness audit:** Evaluate whether installed skills improved work across several conversations and identify justified skill changes.

Use an effectiveness audit only when the available conversations form a defined sample. Skill use counts alone do not prove effectiveness.

## Inputs

For an execution grade, collect:

- original task prompt
- explicit expectations
- execution transcript or event log
- generated output files
- environment or fixture details needed to interpret the run
- requested result path, if grading must be persisted

For an effectiveness audit, collect:

- conversation transcripts or event logs
- sample scope, time range, and selection method
- installed skill inventory and skill contents, when available
- generated outputs needed to verify material claims
- repository guidance and environment details needed to interpret each conversation
- requested report or proposal path, if results must be persisted

Keep transcripts local unless the user explicitly authorizes another destination. Rewrite vague expectations into verifiable statements before grading. Preserve the original wording alongside any operational interpretation.

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

## Effectiveness Audit Workflow

### 1. Define the evidence boundary

Record:

- conversations included and excluded
- sampling method and time range
- installed skills found
- missing or unreadable transcripts, outputs, and skill files
- limits that prevent attribution

Do not treat the sample as representative when its selection cannot support that claim.

### 2. Grade each conversation

For each conversation:

1. Derive verifiable expectations from the task and available repository guidance.
2. Preserve explicit user expectations separately from derived expectations.
3. Apply the evidence standard and grade each expectation `PASS`, `FAIL`, or `UNVERIFIABLE`.
4. Record which skills were relevant, which were detected in the execution, and whether an applicable skill should have activated but did not.
5. Identify material unsupported claims and avoidable process defects.

A skill mention or invocation does not prove that the skill caused the result. A skill that was not relevant does not count as a coverage failure.

### 3. Attribute failures

Group failed conversations by the smallest verified cause. Attribute a failure to a skill only when:

- the skill owns the task trigger or behavior
- its instruction is missing, wrong, or underspecified
- the proposed rule would have prevented the failure if followed
- the gap repeats, or one severe occurrence proves a missing contract

Do not propose a skill change when the current instruction already requires the correct behavior, the cause is model variance, or the fix belongs to product code, infrastructure, or another instruction surface.

### 4. Draft justified changes

For each supported change:

1. Read the current skill in full.
2. State the missing behavioral rule and its owning skill.
3. Make the smallest change that expresses the rule, preferably by replacing weak guidance.
4. Write the proposal separately from the installed skill.
5. Include a unified diff when both current and proposed files are available.

Do not modify installed skills unless the user asks to apply the proposals.

### 5. Report the audit

Return:

```json
{
  "sample": {
    "conversations_analyzed": 0,
    "time_range": "",
    "selection_method": "",
    "limitations": []
  },
  "results": {
    "passed": 0,
    "failed": 0,
    "unverifiable": 0
  },
  "findings": [
    {
      "finding": "...",
      "conversation_evidence": ["..."],
      "affected_skill": "...",
      "attribution": "verified|uncertain|not_skill_caused"
    }
  ],
  "proposals": [
    {
      "skill": "...",
      "rule": "...",
      "evidence": ["..."],
      "diff": "..."
    }
  ]
}
```

Do not calculate a combined score unless the user supplied a scoring method. Report no proposal when the evidence does not justify one.

## Quality Gate

- Every verdict cites evidence or explicitly states its absence.
- Content is inspected rather than inferred from filenames.
- Unsupported final-summary claims do not receive credit.
- Unverifiable expectations remain visible.
- Evaluation feedback targets real acceptance gaps.
- Multi-session findings state the sample boundary and attribution limits.
- Skill changes trace to failed conversations and a verified instruction gap.
- Installed skills remain unchanged unless the user requested application.
