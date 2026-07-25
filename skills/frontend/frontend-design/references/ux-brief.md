# UX Brief

Use this template when a UI request lacks enough direction for implementation and visual review. Omit sections that do not affect the work.

## Brief

### Product Context

- **Audience:** who uses this repeatedly
- **User goal:** what they need to complete
- **Surface:** page, component, or flow in scope
- **Out of scope:** adjacent surfaces that should not change
- **Technical constraints:** framework, component library, browser, performance, or delivery constraints

### Visual Direction

- **Direction:** one coherent style, such as restrained editorial, utilitarian, playful, or premium
- **Desired feeling:** two or three concrete adjectives
- **Avoid:** specific visual clichés or existing problems
- **Existing system:** tokens, components, typography, and brand assets that must remain authoritative

Do not use vague instructions such as “modern,” “clean,” or “make it pop” without concrete implications.

### Layout And Hierarchy

- page or component structure
- primary action and secondary actions
- content priority
- mobile stacking and reordering
- desktop width, columns, and density
- overflow, truncation, and long-content behavior

### Visual System

| Area | Decision |
| --- | --- |
| Typography | families, roles, scale, weight, line height |
| Color | surfaces, text, accent, semantic states, contrast target |
| Spacing | base rhythm and density |
| Shape | borders, radius, elevation, dividers |
| Media | image style, aspect ratios, cropping, empty fallback |
| Motion | purpose, timing range, reduced-motion behavior |

Use semantic tokens when exact reusable values are needed. Keep each value in one source of truth.

### Components And States

For every changed component, define relevant states:

- default
- hover and active
- keyboard focus
- disabled
- loading
- empty
- validation error
- network or server failure
- success

Specify behavior, not only appearance.

### Accessibility

- semantic element and heading expectations
- keyboard and focus behavior
- accessible name and instructions
- contrast requirement
- zoom, text scaling, and reflow expectations
- touch-target and pointer alternatives
- reduced-motion behavior

### Responsive Acceptance

List the representative viewport classes and what must remain true at each. Prefer behavior-based requirements over device-specific screenshots.

### Validation Evidence

- implementation checks to run
- screenshots or states required for review
- accessibility checks
- performance-sensitive assets or interactions
- explicit visual acceptance criteria

## Quality Check

The brief is ready when an implementer can answer:

1. What user outcome matters?
2. What must change and remain unchanged?
3. What visual direction governs decisions?
4. How does the surface behave across states and viewport sizes?
5. What evidence proves the result is correct?
