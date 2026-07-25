# Frontend CSS Patterns

Use this reference for framework-agnostic typography, color, motion, and spatial composition patterns.

## Typography

- Choose display and body fonts intentionally.
- Avoid scaling body text with viewport width.
- Use a clear type scale with stable bounds.
- Match text size to the density of the surface.

Example:

```css
:root {
  --font-display: "Clash Display", "Space Grotesk", sans-serif;
  --font-body: "Satoshi", "General Sans", sans-serif;
  --text-display: clamp(2rem, 5vw, 4rem);
  --text-heading: clamp(1.5rem, 3vw, 2.5rem);
}
```

## Color

- Commit to a small palette.
- Use accent colors sparingly.
- Maintain contrast for interactive and reading surfaces.
- Avoid one-note hue families unless the product explicitly requires it.

## Motion

Use motion for page load, state changes, disclosure, and feedback. Avoid scattered hover effects that make the UI feel noisy.

```css
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## Spatial Composition

- Use asymmetry only when it helps hierarchy.
- Let whitespace reflect content density.
- Define stable dimensions for cards, boards, controls, and media.
- Prevent hover, loading, and dynamic labels from shifting layout.

## Defensive CSS

- Use responsive constraints.
- Handle long words and labels.
- Preserve focus states.
- Respect `prefers-reduced-motion`.
