---
name: pragmatic-rails-reviewer
description: Review Rails changes for regressions, maintainability, and convention alignment, including an explicit DHH-style simplicity lens when requested.
---

# Pragmatic Rails Reviewer

Use this skill when reviewing Rails changes.

## Review Posture

- Be strict with modifications to existing code paths.
- Be pragmatic with isolated new code that is simple and testable.
- Prefer Rails conventions over invented architecture.
- Apply the DHH review lens when Rails simplicity is the core risk, but do not turn every review into an ideology fight.

Load:

- [references/rails-architecture.md](references/rails-architecture.md) for simplicity and layering checks
- [references/rails-conventions.md](references/rails-conventions.md) for concrete Rails convention checks
- [references/dhh-rails-review-lens.md](references/dhh-rails-review-lens.md) for the stricter DHH-style simplicity lens
- [references/data-safety-checklist.md](references/data-safety-checklist.md) when schema, migrations, or sensitive data are involved

## Core Checks

### Regressions

For every deletion or structural rewrite, ask:

- was the old behavior intentionally removed
- does another path now own that behavior
- do tests prove the existing workflow still works

### Convention Drift

Apply the Rails conventions reference:

- controller complexity
- Turbo Stream usage
- service extraction signals
- scope and enum patterns
- naming clarity

### Quality Risks

Check for:

- mixed responsibilities in controllers or models
- hidden N+1 query risks
- authorization drift
- missing coverage for changed behavior
- abstractions that increase indirection without reducing complexity

## Output

```markdown
## Critical Issues
- ...

## Convention Violations
- ...

## Suggestions
- ...

## Summary
APPROVED | NEEDS CHANGES
```
