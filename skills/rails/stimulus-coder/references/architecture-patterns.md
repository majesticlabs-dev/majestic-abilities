# Stimulus Architecture Patterns

## Prefer

- values for configuration and lightweight state
- targets for important nodes
- actions for events
- custom events for loose communication
- outlets for structured parent-child relationships

## Avoid

- storing large state graphs in JavaScript
- hardcoded selectors or CSS class names
- direct controller lookups unless the relationship is explicit
- one controller that owns unrelated features

## Default Decision

- one behavior: one controller
- shared display state: values
- shared event notification: `dispatch`
- known component relationship: outlets
