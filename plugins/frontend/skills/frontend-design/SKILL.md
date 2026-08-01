---
name: frontend-design
description: "Commit to a distinctive art direction and implement production-grade frontend interfaces with token-driven styling, complete interaction states, designed failure paths, and accessibility. Use when designing or restyling pages, components, landing pages, design systems, responsive layouts, or interaction states."
---

# Frontend Design

Produce interfaces that read as authored by a designer with a point of view, not averaged from template patterns.

An interface is correct when all of these hold:

- one distinct visual direction with a named signature element
- tokens drive styling, not one-off values
- every interactive element implements its full state set
- failure and recovery paths are designed, not defaulted
- WCAG AA intent is met by default

## References

| Need | Reference | Content |
|------|-----------|---------|
| Missing product or visual direction | [references/ux-brief.md](references/ux-brief.md) | Implementation-ready UX brief |
| Choosing a direction | [references/art-direction.md](references/art-direction.md) | Direction catalog, signature element, texture, anti-patterns |
| Token system | [references/design-tokens.md](references/design-tokens.md) | Token contract, role notes, extension rules |
| CSS implementation | [references/css-patterns.md](references/css-patterns.md) | Typography, color, motion, spatial composition |
| Measurable UI constraints | [references/ui-implementation-guide.md](references/ui-implementation-guide.md) | Type scale, forms, buttons, tables, dark mode |
| Motion | [references/motion-patterns.md](references/motion-patterns.md) | Page load, scroll triggers, hover, performance |
| States, a11y, failure paths | [references/web-interface-standards.md](references/web-interface-standards.md) | Keyboard, touch targets, failure states, budgets |
| Polish | [references/css-polish-tips.md](references/css-polish-tips.md) | Accessibility debugging, focus, defensive CSS |
| React/Vue | [references/react-vue.md](references/react-vue.md) | Framer Motion, Vue Transitions, token-driven components |
| Landing pages | [references/landing-page-design.md](references/landing-page-design.md) | Section design, palettes, typography pairings |

## Workflow

### 1. Establish context

Determine purpose, audience, constraints (framework, performance budget, accessibility target), and any brand anchors. Load `ux-brief.md` when goals, states, responsive behavior, or acceptance criteria are unclear. Ask only for information that blocks correct execution.

### 2. Commit to an art direction

Load `art-direction.md`. Pick one direction and execute it precisely. Do not blend directions, and do not repeat the previous build's choices. Name the signature element before writing code.

### 3. Define tokens

Load `design-tokens.md` and fill every role before any layout work. Unfilled roles mean skipped decisions.

### 4. Implement

Build with `css-patterns.md` and `ui-implementation-guide.md`. Apply framework patterns from `react-vue.md` when relevant. Every interactive element implements default, hover, active, focus-visible, disabled, loading, error, and empty where applicable.

### 5. Design the failure paths

Use `web-interface-standards.md`. Cover offline, partial or delayed data, user error and recovery. Silent failures and default browser error states are invalid output.

### 6. Validate

Run `css-polish-tips.md` and `motion-patterns.md`, then the quality gate below.

## Output Shape

Deliver an art direction brief followed by the code:

1. **Brief:** direction and tone, type pairing concept, palette logic, motion grammar, material choice, signature element
2. **Code:** complete and runnable at the requested scope, with implementation complexity matched to the aesthetic vision
3. **Extension notes** when relevant: how to extend tokens, components, and states without breaking coherence

## Quality Gate

The output is invalid if any check fails:

- [ ] Signature element exists and carries a function
- [ ] Tokens drive styling decisions
- [ ] Typography is deliberate, not a system default
- [ ] Palette is limited, intentional, and contrast-safe
- [ ] Layout uses consistent grid logic with at least one intentional break
- [ ] Motion communicates structure or feedback and honors `prefers-reduced-motion`
- [ ] All interaction states implemented
- [ ] Failure and recovery states designed on brand
- [ ] Keyboard access and visible focus integrated into the aesthetic
- [ ] Responsive rhythm and narrative preserved across at least three breakpoints
- [ ] Copy is authored and contextual, with no filler
- [ ] Narrative consistency holds across typography, motion, layout, and copy
- [ ] No anti-patterns from `art-direction.md` are present
