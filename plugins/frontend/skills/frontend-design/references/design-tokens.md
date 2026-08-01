# Design Tokens

Define tokens before writing layout. Tokens encode the art direction as values, so every component inherits the direction instead of restating it.

## Token Contract

Fill every role. An empty role means a decision was skipped, not that the role is unused.

```css
:root {
  /* Color */
  --color-bg:;
  --color-surface:;
  --color-text:;
  --color-muted:;
  --color-accent:;
  --color-focus:;
  --color-success:;
  --color-warning:;
  --color-danger:;

  /* Typography */
  --font-display:;
  --font-body:;
  --font-mono:;
  --text-xs:;    --leading-xs:;
  --text-sm:;    --leading-sm:;
  --text-base:;  --leading-base:;
  --text-lg:;    --leading-lg:;
  --text-xl:;    --leading-xl:;
  --text-2xl:;   --leading-2xl:;

  /* Spacing */
  --space-1:;
  --space-2:;
  --space-3:;
  --space-4:;
  --space-6:;
  --space-8:;

  /* Radius and shadow */
  --radius-sm:;
  --radius-md:;
  --radius-lg:;
  --shadow-sm:;
  --shadow-md:;
  --shadow-lg:;

  /* Motion */
  --duration-fast:;
  --duration-base:;
  --duration-slow:;
  --ease-out:;
  --ease-spring:;
}
```

## Role Notes

| Role | Decision it encodes |
| --- | --- |
| `--color-bg` / `--color-surface` | Base plane and raised plane. Two values, not one reused. |
| `--color-muted` | Secondary text that still meets contrast, not a lighter guess. |
| `--color-accent` | One dominant hue with one to three accents, each with a defined job. |
| `--color-focus` | Functional, at least 3:1 against adjacent surfaces, part of the aesthetic. |
| `--font-display` / `--font-body` | A characterful display face paired with a refined body face. |
| Type scale | Paired size and line height. Tighter leading on large sizes, looser on body. |
| Spacing | One rhythm. Component padding derives from it rather than ad hoc values. |
| Motion | Durations and easings that express the direction. Luxury reads slow, brutalist reads abrupt. |

## Rules

- Avoid Inter, Roboto, Arial, and system defaults as the identity. Provide fallbacks that preserve tone.
- One dominant hue plus one to three accents. Every accent has a defined role.
- Contrast and focus colors are functional requirements, not palette decoration.
- Add dark mode only when it strengthens the direction. See `ui-implementation-guide.md` for dark mode execution.
- Semantic colors (`success`, `warning`, `danger`) belong to the palette. Do not import defaults from a framework.

## Extending Without Breaking Coherence

- Add new tokens as roles, not as one-off values. A new color belongs to the palette or it does not exist.
- Derive component tokens from base tokens (`--button-padding: var(--space-3) var(--space-6)`), never from raw numbers.
- When a component needs a value no token provides, that is a signal the system is missing a role. Add the role.
- Keep each value in one source of truth. Duplicating a hex or a duration is how a system drifts.

Typography and spatial specifics live in `css-patterns.md`. Measurable typographic and color constraints live in `ui-implementation-guide.md`.
