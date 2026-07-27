---
name: business-logic-coder
description: "Route Rails business logic to the simplest fitting home: a model, typed operation, state machine, layered boundary, or durable event history."
---

# Business Logic Coder

Use this skill when the user asks where Rails business logic should live or how to implement workflow-oriented domain behavior.

Load:

- [references/rails-business-logic.md](references/rails-business-logic.md)

## Routing

| Need | Use |
| --- | --- |
| Simple invariant or domain behavior with one clear owner | Plain Rails model or concern |
| Typed operation with validations | `active-interaction-coder` |
| Stateful lifecycle | `aasm-coder` |
| Logic leaking across Rails layers | `layered-rails` |
| Durable event history or audit trail | `event-sourcing-coder` |

Start with ordinary Rails objects. Choose a specialized path only when its boundary removes real
complexity; do not combine these patterns by default.

## Output

Return the chosen implementation path, why it fits, transaction boundaries, and tests needed for the behavior.
