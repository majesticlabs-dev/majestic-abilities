---
name: code-review
description: Review a concrete change set for correctness, regressions, security, data risk, unnecessary complexity, and missing tests, then give evidence-backed findings or a release verdict. Use when reviewing a diff, pull request, patch, staged changes, or deciding whether code is ready to merge or ship.
---

# Code Review

Review the requested change set against its intended behavior. Prioritize defects and release risk over style commentary.

## Boundary

Review only the requested diff, patch, files, or comparison range, plus the surrounding code needed to validate behavior. Do not modify code unless the user explicitly asks for fixes.

Identify the language, framework, and relevant versions before reviewing framework-dependent behavior. Apply framework-specific review guidance whenever the change runs inside a framework. If that guidance or the required version context is unavailable, limit the review to demonstrated language-neutral defects and do not approve framework-dependent behavior.

Use other specialist guidance when the main question is narrower, such as algorithmic complexity, test quality, infrastructure, or privacy.

## Required Context

Establish:

- the exact review scope and comparison base
- the requested behavior, acceptance criteria, or issue being solved
- the language, framework, runtime, and relevant versions
- repository guidance and relevant architectural constraints
- checks already run and any known failures

If the scope is empty or ambiguous, say so instead of reviewing an assumed change set.

## Workflow

1. Read the entire change set before forming conclusions.
2. Trace each changed behavior through callers, consumers, data boundaries, and failure paths.
3. Assess change risk from the actual semantic change. Trace changed contracts through static and dynamic dependents, side effects, criticality, and relevant cross-cutting failure modes. For each material risk, name the triggering changed path, plausible failure and consequence, evidence strength, and mitigation or verification. Risk without a concrete defect belongs in residual risk, not Findings. Treat missing evidence as residual risk, not proof of safety.
4. Compare the implementation with the stated requirement and existing repository patterns.
5. Check for correctness failures, regressions, unsafe defaults, authorization gaps, data loss, concurrency hazards, compatibility breaks, and incomplete migrations.
6. Challenge new abstractions, configuration, dependencies, and indirection that are not required by the change.
7. Inspect tests for observable behavior, important branches, failure handling, and regression protection.
8. Run the narrowest relevant repository checks when execution is available. Distinguish checks actually run from checks merely recommended.
9. Keep only findings supported by a concrete code path and user-visible or operational consequence.

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
