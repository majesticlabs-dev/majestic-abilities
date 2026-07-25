---
name: frontend-design
description: "Choose a coherent visual direction and implement production-grade frontend interfaces. Use when designing or restyling pages, components, design systems, responsive layouts, or interaction states."
---

# Frontend Design

Workflow for creating distinctive, production-grade interfaces.

## Core References

Use supporting references for depth:

| Need | Reference | Content |
|------|-------|---------|
| Missing product or visual direction | [references/ux-brief.md](references/ux-brief.md) | Implementation-ready UX brief |
| Design direction | [references/design-principles.md](references/design-principles.md) | Aesthetic direction, anti-patterns |
| CSS implementation | [references/css-patterns.md](references/css-patterns.md) | Typography, color, motion, spatial composition |
| React/Vue patterns | [references/react-vue.md](references/react-vue.md) | Framer Motion, Vue Transitions |

## Framework Resources

### React/Vue

See [references/react-vue.md](references/react-vue.md) for:
- Framer Motion staggered animations
- Vue Transition/TransitionGroup patterns
- Component architecture with design tokens


## Implementation Resources

| Resource | Content |
|----------|---------|
| [ui-implementation-guide.md](references/ui-implementation-guide.md) | Typography rules, color, forms, buttons, tables |
| [motion-patterns.md](references/motion-patterns.md) | Page load, scroll triggers, hover, performance |
| [css-polish-tips.md](references/css-polish-tips.md) | Accessibility, scroll, focus, defensive CSS |
| [landing-page-design.md](references/landing-page-design.md) | Section design, palettes, typography pairings |

## Workflow

```
1. Clarify product and design direction
   - Load the UX brief when goals, states, responsive behavior, or acceptance criteria are unclear
   - Load the design principles reference for aesthetic guidance
   - Commit to one coherent direction instead of mixing styles.

2. Implement CSS foundation
   - Load the frontend CSS patterns reference for typography, color, motion, and stable dimensions
   - Customize Tailwind or write CSS variables

3. Apply framework patterns
   - React/Vue: Use references/react-vue.md

4. Polish and validate
   - Use references/css-polish-tips.md for accessibility
   - Use references/motion-patterns.md for animation
   - Run the validation checklist below
```

## Quick Reference

### Web Interface Standards

See [references/web-interface-standards.md](references/web-interface-standards.md) for:
- Keyboard operability requirements (WAI-ARIA widget patterns)
- Touch target sizing (44px mobile, 24px desktop)
- Form behavior (Enter submission, autocomplete, mobile keyboards)
- Animation accessibility (`prefers-reduced-motion`)
- Network performance budgets (POST < 500ms, virtualization thresholds)

**Validation Checklist:**
- [ ] Distinctive typography (not default fonts)
- [ ] Intentional, limited color palette
- [ ] Layout breaks predictable patterns
- [ ] Motion serves purpose
- [ ] Clear design direction
- [ ] Responsive quality maintained
- [ ] Accessibility preserved
