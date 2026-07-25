# Optimization Playbook

Use this reference when a complexity finding needs a concrete transformation pattern.

## Common Transformations

### Nested Lookup Loops

Symptom: for each item in one collection, code scans another collection to find a match.

Preferred fix: build a map from the searched collection once, then perform direct lookups.

Complexity: O(a * b) to O(a + b).

Correctness checks:

- Are duplicate keys possible?
- Does the original code pick the first match, last match, or all matches?
- Is output ordering observable?
- Is key normalization required?

### Repeated Membership Checks

Symptom: `includes`, `indexOf`, `find`, `in_array`, `contains`, or equivalent runs inside a loop.

Preferred fix: convert the membership collection to a set or map once.

Complexity: O(n * m) to O(n + m).

Correctness checks:

- Does equality change after conversion?
- Are values normalized the same way?
- Does object identity matter?
- Are the values hashable in the target language?

### Sorting Inside Loops

Symptom: the same or growing collection is sorted repeatedly.

Preferred fix: sort once outside the loop, maintain a heap, or use binary search/insertion.

Complexity: often O(n^2 log n) to O(n log n), or O(n log k) with a heap.

Correctness checks:

- Is each intermediate sorted state externally observed?
- Does the comparator depend on loop-local state?
- Does stable sort behavior matter?

### Pairwise Comparisons

Symptom: code compares every pair to find overlaps, nearest values, conflicts, or ranges.

Preferred fixes:

- sort plus two pointers for pair/range matching
- sweep line for interval overlaps
- spatial or hash bucketing for local-neighborhood checks
- union-find for connectivity

Complexity: commonly O(n^2) to O(n log n) or O(n alpha(n)).

Correctness checks:

- Are boundaries inclusive or exclusive?
- Are equal values meaningful?
- Does the result need all pairs or only the first/best pair?

### Recomputing Derived Data In Render Paths

Symptom: filters, sorts, grouping, or expensive transforms run during every render.

Preferred fixes:

- memoize derived values with correct dependencies
- move derivation to selectors, loaders, or server-side preparation
- virtualize long lists
- stabilize callbacks and object props only when child renders are measurably affected

Correctness checks:

- Dependency arrays include every semantic input.
- Memoization does not hide mutations of mutable input objects.
- Work was actually on a render hot path, not a cold admin screen.

### N+1 Database Or API Calls

Symptom: a query or request runs inside a loop.

Preferred fixes:

- bulk fetch by IDs and join in memory
- use joins, includes, preloads, dataloaders, or batched API endpoints
- preserve filtering, authorization, tenancy, ordering, pagination, and error behavior

Correctness checks:

- Do not fetch records the previous per-item logic would not authorize.
- Preserve missing-record behavior.
- Preserve rate-limit, retry, and partial-failure semantics.

## What Not To Do

- Do not replace clear linear code with complex structures when input sizes are tiny or the path is cold.
- Do not cache without invalidation.
- Do not use JSON serialization as a general-purpose key unless the key format is stable and collision-safe.
- Do not change public ordering unless tests and callers prove it is irrelevant.
- Do not trade O(n) for O(n log n) unless it removes a larger bottleneck or enables batching.
