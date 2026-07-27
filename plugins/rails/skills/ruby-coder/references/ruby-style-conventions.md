# Ruby Style Conventions

## Prefer

- guard clauses over nested conditionals
- predicate methods with `?`
- `present?`, `blank?`, and `any?` when they clarify intent
- `map`, `filter`, `sum`, and friends over manual loops
- keyword args for configuration-like call sites

## Avoid

- boolean flag soup on one method
- hidden mutation when a return value would be clearer
- broad rescue blocks with no narrow error intent
- `send` or metaprogramming for routine dispatch

## Modern Ruby

- hash value shorthand: `{ user:, status: }`
- pattern matching only when it truly clarifies branching
- frozen constants for stable lookup tables
