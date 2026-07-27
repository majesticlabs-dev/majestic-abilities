---
name: pr-screenshot-docs
description: "Capture and document UI changes with before/after screenshots for pull requests. Use when creating PRs that include visual changes to ensure reviewers can assess design modifications."
---

# PR Screenshot Documentation

Guidance for capturing and documenting UI changes with before/after screenshots when creating pull requests.

## When to Use This Skill

- Creating PRs with frontend/UI modifications
- Documenting visual changes for code review
- Building a visual record of design evolution
- Enabling async design review without running the app

## Screenshot Workflow

### 1. Before Making Changes

Capture the current state before implementing UI modifications:

```
1. Set the browser viewport to the target size, starting with mobile.
2. Navigate to the target page.
3. Inspect the page structure to identify the component or region.
4. Capture the target component or a full-page screenshot.
```

Save or note the screenshot for later comparison.

### 2. After Implementing Changes

Capture the same view after your modifications:

```
1. Refresh or navigate to the updated page
2. Inspect the updated page structure
3. Capture the same component or region
```

### 3. Store Screenshots Safely

Use the repository's established PR attachment flow or documentation storage. Prefer durable access-controlled storage over anonymous temporary hosting.

Before uploading, confirm screenshots contain no credentials, personal data, private customer content, internal URLs, or browser extensions. Use stable seeded data when possible.

## PR Description Template

Include a visual comparison section in your PR description:

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| Attach the before screenshot | Attach the after screenshot |

### What Changed
- [Specific visual change 1]
- [Specific visual change 2]
```

## Viewport Recommendations

Choose viewport size based on what you're documenting:

| Target | Width | Height | Use Case |
|--------|-------|--------|----------|
| Mobile | 320 | 568 | Mobile-first responsive |
| Tablet | 768 | 1024 | Tablet layouts |
| Desktop | 1280 | 800 | Standard desktop |
| Wide | 1440 | 900 | Wide desktop layouts |

**Default to mobile (320px)** for documentation - if it looks good on mobile, it usually scales up well.

## Best Practices

### Capture Strategy

- **Focus on the changed component** - don't capture full pages unless layout changed
- **Use consistent viewports** - same size for before and after
- **Capture interactive states** - hover, focus, active when relevant
- **Include error states** - if you changed error handling UI

### Documentation Quality

- **Describe what changed** - don't make reviewers guess
- **Explain why** - connect visual changes to user benefit
- **Note accessibility** - mention contrast, focus indicators if relevant

### When NOT to Capture

- Pure backend changes with no UI impact
- Code refactoring without visual changes
- Test-only changes
- Configuration updates

## Integration with PR Workflow

Before submitting a UI change for review:

1. Capture the baseline before implementation when practical.
2. Implement and verify the change.
3. Capture the same states and viewports afterward.
4. Include the comparison and testing notes in the PR description.
5. Keep screenshot storage consistent with repository policy.

## Example PR Section

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| Attach the baseline button screenshot | Attach the updated button screenshot |

### Changes Made
- Increased button padding from 8px to 12px for better touch targets
- Added subtle shadow for depth
- Improved contrast ratio from 3.5:1 to 4.8:1 (now WCAG AA compliant)

### Tested Viewports
- [x] Mobile (320px)
- [x] Tablet (768px)
- [x] Desktop (1280px)
```

## Related Capability

Apply `visual-validator` when the screenshots also need rigorous goal, accessibility, responsive, and design-system assessment.
