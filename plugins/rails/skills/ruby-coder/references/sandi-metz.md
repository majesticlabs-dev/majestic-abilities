# Sandi Metz Heuristics

These are pressure signals, not hard laws.

## Watch For

- classes that collect multiple responsibilities
- methods that hide several decisions
- long parameter lists that want a named concept
- controllers that assemble too much data for the view

## Use The Heuristics To Ask

- should this be two objects?
- is this method doing orchestration and domain work?
- would a facade or form object simplify the interface?

Do not contort otherwise clear code just to satisfy a numeric rule.
