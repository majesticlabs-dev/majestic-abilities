---
name: code-review
description: Review a concrete change set for correctness, regressions, security, data risk, unnecessary complexity, and missing tests, then give evidence-backed findings or a release verdict. Use when reviewing a diff, pull request, patch, staged changes, or deciding whether code is ready to merge or ship.
---

# Code Review

Review the requested change set against its intended behavior. Prioritize defects and release risk over style commentary.

## Boundary

Review only the requested diff, patch, files, or comparison range, plus the surrounding code needed to validate behavior. Do not modify code unless the user explicitly asks for fixes.

Use specialist review guidance when the main question is narrower, such as algorithmic complexity, test quality, infrastructure, privacy, or framework conventions.

## Required Context

Establish:

- the exact review scope and comparison base
- the requested behavior, acceptance criteria, or issue being solved
- repository guidance and relevant architectural constraints
- checks already run and any known failures

If the scope is empty or ambiguous, say so instead of reviewing an assumed change set.

## Workflow

1. Read the entire change set before forming conclusions.
2. Trace each changed behavior through callers, consumers, data boundaries, and failure paths.
3. Compare the implementation with the stated requirement and existing repository patterns.
4. Check for correctness failures, regressions, unsafe defaults, authorization gaps, data loss, concurrency hazards, compatibility breaks, and incomplete migrations.
5. Challenge new abstractions, configuration, dependencies, and indirection that are not required by the change.
6. Inspect tests for observable behavior, important branches, failure handling, and regression protection.
7. Run the narrowest relevant repository checks when execution is available. Distinguish checks actually run from checks merely recommended.
8. Keep only findings supported by a concrete code path and user-visible or operational consequence.

## Finding Standard

Each finding must include:

- severity: critical, high, medium, or low
- file and line reference
- the incorrect or risky behavior
- the conditions that trigger it
- why it matters
- the smallest safe correction

Do not report optional refactors, personal style preferences, or speculative concerns as defects.

## Release Verdict

When asked for a quality gate, return exactly one verdict:

- `APPROVED`: no unresolved material defect and required verification passed
- `NEEDS CHANGES`: one or more actionable defects must be corrected
- `BLOCKED`: missing scope, evidence, environment, or prerequisite prevents a responsible decision

Passing tests do not prove correctness. Conversely, do not block release on unrelated cleanup or optional polish.

## Output

1. **Findings**, ordered by severity and confidence
2. **Verdict**, when requested
3. **Open questions or assumptions**
4. **Checks run** and their results
5. **Residual risk**

If there are no findings, say so directly and identify any verification that was not possible.
