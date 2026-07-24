# ViewComponent Patterns

## Good Fits

- shared buttons, cards, alerts, nav items
- modal, tabs, and other slot-based UI
- collection rendering with a stable API
- components that benefit from previews and isolated tests

## Useful Patterns

- `renders_one` and `renders_many` for slots
- `with_collection_parameter` for repeated components
- previews in `spec/components/previews` when using RSpec
- component specs for structure and variant behavior

## Standards

- document the public inputs
- keep variant logic readable
- avoid pushing controller orchestration into the component
