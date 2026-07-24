# Rails Architecture

Use this reference when a change is drifting into architecture theater and needs a clearer Rails-shaped boundary.

## Core Bias

- prefer conventions over bespoke layering
- keep controllers small but honest about orchestration
- keep domain behavior close to the model or a small domain object
- treat duplication as cheaper than the wrong abstraction

## Extraction Signals

Extract a dedicated object when multiple signals are present:

- several models or external systems are coordinated
- transaction boundaries or retries need explicit ownership
- the behavior is reused across jobs, controllers, or commands
- tests are hard because responsibilities are mixed

## Anti-Patterns

- services created just because a method is long
- "architected" layers that only forward arguments
- callbacks hiding critical side effects
- policy, validation, and persistence logic smeared across controllers and views

## Review Lens

- is the boundary real, or is the code just moving sideways
- does the new layer reduce coupling, or only add naming
- would a Rails-native approach be simpler and more readable
