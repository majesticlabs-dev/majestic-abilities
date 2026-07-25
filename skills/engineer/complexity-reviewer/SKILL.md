---
name: complexity-reviewer
description: "Review code for algorithmic complexity and performance hotspots without changing behavior. Use when auditing inefficient loops, repeated scans, rendering work, N+1 queries, or proposed performance optimizations."
---

# Complexity Reviewer

Use this skill when asked to scan, audit, review, report on, or fix code that may have inefficient
loops, repeated scans, costly rendering work, N+1 queries, or avoidable O(n^2) behavior.

## Core Rule

Optimize only when the current behavior is understood and can be preserved. Prefer a small proven
improvement with tests over a broad rewrite with unclear correctness.

## Default Behavior

When the user asks for analysis, an audit, a scan, a review, or a report, do not modify files.
Return a complexity report with:

- scope analyzed and detected stack or test commands
- top findings ranked by likely impact
- file and line for each finding
- current pattern and why it may be costly
- estimated current complexity
- recommended change
- estimated complexity after the change
- risk level
- tests, benchmarks, or manual checks needed
- clear patch status: proposed, implemented, or blocked

Only edit files when the user explicitly asks to implement, fix, optimize, apply, change, refactor,
or otherwise requests code modification.

## Workflow

1. Establish the baseline.
   - Identify the language, framework, test command, build command, and performance-sensitive paths.
   - Inspect existing tests before touching code.
   - Run `python3 scripts/analyze_complexity.py /path/to/repo --format markdown` from this skill
     directory for a first-pass hotspot list when scanning a repository.
2. Rank opportunities.
   - Prioritize hot paths, large input paths, rendering loops, database/API loops, and shared utilities.
   - Separate algorithmic complexity from constant-factor cleanup.
   - Treat scanner output as leads, not proof.
   - For report-only requests, inspect enough surrounding code to estimate current and proposed complexity.
3. Prove behavior before changing code.
   - Locate or add focused tests for the function, query, component, or data flow being changed.
   - Cover edge cases: empty input, duplicates, ordering stability, missing values, errors,
     permissions, pagination, time zones, and mutation side effects.
   - If behavior is ambiguous, ask for expected behavior before changing semantics.
4. Optimize conservatively.
   - Replace repeated linear lookup with maps or sets when key equality is stable.
   - Replace nested scans with indexing, grouping, two-pointer scans, sweep-line logic, binary search,
     memoization, batching, or precomputation only when the data shape supports it.
   - In UI code, reduce unnecessary renders with stable props, memoized derived data, virtualization,
     debounced work, and moving expensive work out of render paths.
   - In data access code, remove N+1 behavior with bulk fetches, joins, preloading, caching, or
     batching while preserving authorization and filtering.
5. Verify.
   - Run the narrow test first, then the broadest relevant test, type, lint, or build command.
   - Add a benchmark or measurement when the improvement is non-obvious or performance-critical.
   - Report original complexity, new complexity, changed files, tests run, and residual risk.

## Safety Checks

Before editing:

- Confirm data sizes are large enough for complexity to matter.
- Confirm the path is hot enough to justify added structure.
- Confirm output ordering is preserved where callers may rely on it.
- Confirm object identity, mutability, and reference sharing are not public behavior.
- Confirm caches have a valid invalidation strategy.
- Confirm deduplication does not collapse distinct records with the same display label.
- Confirm database batching preserves tenant, permission, soft-delete, pagination, and sorting constraints.

After editing:

- Run focused tests for the changed behavior.
- Run the relevant broader validation command.
- Compare before and after benchmark numbers when a benchmark exists or was added.
- Keep the patch localized and avoid unrelated formatting churn.

## References

Load [references/optimization-playbook.md](references/optimization-playbook.md) for common
transformations and correctness traps.

Load [references/report-template.md](references/report-template.md) when preparing a complexity
analysis or audit report.
