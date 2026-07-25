# Infrastructure Quality Checks

## Maintainability

- Names reveal environment, purpose, and ownership without duplicating provider terminology.
- Variables and outputs have useful descriptions and stable types.
- Formatting and native validation pass.
- Provider and module versions use intentional constraints and a committed lockfile.
- Repeated values are centralized only when that improves consistency.
- Comments explain operational constraints, not obvious syntax.

## Simplicity

Prefer the smallest structure that preserves:

- independent lifecycle
- clear ownership
- justified reuse
- environment isolation
- provider or state boundaries

Challenge custom modules that wrap one trivial resource, roles that duplicate maintained ecosystem roles, and environment directories copied without a drift-control strategy.

Do not score complexity from universal file-count or directory-depth thresholds. Judge whether each boundary removes more risk than it adds.

## Evidence Questions

- What concrete reuse justifies this abstraction?
- Can an operator locate a resource and its inputs quickly?
- Will a provider upgrade require changes in one obvious place?
- Can environments drift silently?
- Is imperative post-provisioning idempotent and observable?
- Does deleting a component have a clear blast radius?
