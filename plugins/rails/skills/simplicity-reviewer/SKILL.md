---
name: simplicity-reviewer
description: "Review Rails code for unnecessary complexity."
---

# Code Simplicity Review

**Audience:** Rails developers reviewing code for unnecessary complexity
**Goal:** Reduce unnecessary complexity while preserving behavior. Optimize for bounded context, explicit contracts, searchable names, isolated edits, and fast verification, not fewer lines.

Review substantive Rails code whether written by humans or agents. Return findings without edits unless the user explicitly requests implementation. Keep the requested scope; do not turn this review into unrelated cleanup.

## Simplification Principles

### 1. Question Unnecessary Work

Trace the relevant code path and callers before claiming a check or layer adds no value. Remove a check only when a verified upstream contract makes it redundant. Preserve authorization, validation at trust boundaries, error behavior, side effects, ordering, and persisted data.

### 2. Prefer Explicit and Searchable Behavior

Prefer names and control flow that let an agent locate the behavior without loading unrelated code. Use Rails primitives when they preserve the contract, not merely because they shorten the code. A shorter authorization expression is not a simplification if it changes permission checks.

### 3. Use Early Returns

```ruby
def process
  return unless valid?
  return unless authorized?
  do_work
end
```

### 4. Challenge Coordination-Heavy Abstractions

Question application modules, mixins, and layers that require unrelated changes to pass through a shared file. Keep useful Rails and library primitives. Judge an abstraction by its current contract, context requirements, edit isolation, and verification benefit, not by the number of implementations alone.

### 5. Keep Useful Local Boundaries

Single-use methods and classes can isolate a behavior and make it easier to verify. Inline them only when the change reduces unnecessary context or indirection without weakening the contract.

### 6. Remove YAGNI Violations

Eliminate unused options, speculative extensibility, and dead code only after checking actual consumers. Keep error handling and compatibility paths when supported behavior, persisted data, or external consumers require them.

## Red Flags

- Changes that require loading unrelated subsystems to understand one behavior
- Implicit control flow or names that make behavior difficult to locate
- Shared application files that couple otherwise independent edits
- Layers with no demonstrated contract, isolation, or verification benefit

Method length, single-use helpers, and repetition are not defects by themselves.

## Code Smells

**God Objects:** Class doing authentication, email, reports, payment, analytics
**Feature Envy:** Method uses another object's data excessively
**Inappropriate Intimacy:** `order.customer.address.city` -> `order.shipping_city`

## Code Duplication

Prefer local duplication when consolidation would expand context, couple unrelated behavior, or force independent agent edits through one shared application file. Verify that duplicated rules remain consistent. Consolidate only when a current shared contract or demonstrated correctness benefit justifies the coordination cost. This is not a reason to copy framework primitives such as ActiveRecord.

## Technical Debt Markers

Search for: `TODO`, `FIXME`, `HACK`, `XXX`

## Review Methodology

Apply these lenses systematically:

1. **Necessity** - Does this behavior or layer serve a current requirement?
2. **Logic** - Can control flow be more explicit without changing outcomes?
3. **Consistency** - Do duplicated rules drift, or do local copies preserve independent edits?
4. **Isolation** - Does each boundary keep context and changes local?
5. **YAGNI** - Is anything built for speculative future needs?
6. **Verification** - Do types and behavior checks expose real failures quickly?

Read relevant callers and contracts before recommending a change. Never remove security controls or weaken types or tests. For approved edits, run configured Rails lint and tests matched to the affected behavior, fix failures caused by the change, and report checks that were not run.

## Output Format

```markdown
## Simplification Analysis

### Core Purpose
[What this code actually needs to do in 1-2 sentences]

### Findings (Priority Order)

| Priority | Location | Issue and Evidence | Fix | Behavior Verification |
|----------|----------|--------------------|-----|-----------------------|
| HIGH | file:line | [context, isolation, or correctness cost] | [fix] | [check] |
| MED | file:line | [context, isolation, or correctness cost] | [fix] | [check] |

### YAGNI Violations
- [Speculative code that should be removed]

### Preserved Boundaries and Skipped Findings
- [useful local duplication, framework primitive, or uncertain finding and why it stays]

### Verification
- [checks actually run and results, or checks required before applying findings]
```

Do not estimate lines saved or use deletion count as evidence of improvement. If no verified unnecessary complexity is found, say so.
