---
name: code-simplifier
description: Simplify or review settled, recently changed code for unnecessary complexity while preserving behavior. Use for explicit simplification requests, deletion-focused reviews, or questions such as "what can we delete?" and "is this over-engineered?" after implementation and before handoff.
---

# Code Simplifier

Refine settled, recently changed code. Reduce accidental complexity and duplication while keeping the same observable behavior. Read the complete target scope and its relevant callers before forming findings.

## Scope and gate

Use a scope named by the user as the authoritative boundary. Otherwise use the current branch diff. If that is unavailable, use relevant files edited earlier in the conversation. Do not guess an empty scope. Ask the user what to simplify when no non-empty scope can be resolved.

Before detailed review, skip a scope that contains only documentation, generated files, vendored code, dependency or lockfiles, or purely mechanical changes. For a mixed scope, retain substantive human-authored code. This is a kind gate, not a size gate. An explicitly named small code scope still runs.

## Review mode

Follow the repository's mode convention:

- For analysis or review requests limited to simplification, including requests to find over-engineering or code to delete, return findings without edits.
- For explicit requests to simplify or apply a simplification, make only surgical edits in the resolved scope and necessary in-scope seams.
- Do not use this skill for general code review or broad correctness, security, accessibility, framework, or performance review. Keep those review tasks outside this workflow.

Do not turn this pass into a broad cleanup or new implementation.

## Three review lenses

Apply each lens as a distinct pass. Run the passes inline or in separate contexts. Do not require parallel dispatch or any specific host orchestration.

### Reuse

Search the repository for behavior-equivalent helpers and established abstractions before adding or keeping duplicate logic. Consider standard-library or runtime primitives, and verified platform, framework, or downstream guarantees, only when they preserve every relevant input and output. For version-sensitive runtime, framework, or platform replacements, check supported versions before relying on portability guarantees. If support is unknown, keep the existing code. Do not change locale behavior, sort stability, serialization, error behavior, side effects, or ordering without proof.

### Quality

Find redundant state, copy-paste variation, parameter sprawl, leaky boundaries, raw strings where established types exist, deeply nested conditionals, comments that only restate code, and dead or unused code. Keep named concepts and abstractions when they improve comprehension, testability, or extension. Verify project-wide non-use before removing code, including re-exports, dynamic imports, framework exports, and external consumers.

Remove pre-release compatibility scaffolding only after verifying that it has no deployed, persisted, public, external, dependent-branch, or in-repository consumer. If any consumer or guarantee is uncertain, keep it.

### Efficiency

Find clearly redundant computation or I/O, repeated calls, recurring no-op updates, and overly broad reads or loads when simplification can remove them without changing behavior. Leave broader performance concerns, such as N+1 work, concurrency, hot-path blocking, existence-check races, leaks, and unbounded structures, outside this simplification pass. Change only work that is proven unnecessary and behavior-equivalent.

## Safety and changes

Preserve outputs, errors, side effects, ordering, persisted data, and public or external contracts. Never remove trust-boundary validation, authorization, sanitization, data-loss protection, or accessibility behavior. Preserve transformations before downstream projection and do not treat newly reachable branches as dead code.

Inspect code outside the scope when needed to validate a finding, but do not edit outside the resolved boundary. Apply a finding only when its benefit is clear and behavior preservation is established. Record false positives, uncertain findings, and low-value findings as skipped. Do not use removed lines as a success measure. Never weaken types or tests.

## Verification

After edits, run configured project-wide type and lint checks. Run tests matched to the blast radius: scoped tests for local changes, broader tests for shared changes, and the full suite when the runner cannot scope tests. Fix or revert failures caused by a simplification. State explicitly when a check is not configured or was not run.

## Report

For a deletion-focused review, report only verified opportunities, one line each:

```text
path:line: <category>: <what to cut>. <safe replacement or "Nothing">.
```

Use these categories:

- `delete`: dead code, unused flexibility, or speculative behavior
- `stdlib`: custom code replaced by a standard-library primitive
- `native`: code or a dependency replaced by a verified runtime, platform, or framework feature
- `yagni`: an abstraction, option, or layer without a current consumer
- `shrink`: equivalent logic with a materially smaller clear form

Each finding must preserve observable behavior and identify the evidence that makes the removal safe. Do not estimate net lines saved or treat fewer lines as proof of a better result. If there are no verified opportunities, say `No unnecessary complexity found.`

For an applied simplification, report:

1. What was already sound.
2. Applied findings by lens: reuse, quality, and efficiency.
3. Skipped findings and why.
4. Checks actually run and their results.
5. Residual risk and any scope limits.

If no edit was needed, say so and still report the review and checks.
