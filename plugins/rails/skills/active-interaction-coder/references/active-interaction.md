# ActiveInteraction Guidance

Use ActiveInteraction when the app wants typed, validated operation objects.

## Good Fits

- multi-step writes with structured inputs
- reusable operations invoked from controllers, jobs, or commands
- composition of smaller interactions

## Bad Fits

- trivial model methods
- pure queries
- one-off wrappers that only move code around

## Standards

- namespace interactions by domain
- keep `execute` readable
- compose smaller interactions instead of nesting giant conditionals
- return domain objects or useful results, not vague booleans
