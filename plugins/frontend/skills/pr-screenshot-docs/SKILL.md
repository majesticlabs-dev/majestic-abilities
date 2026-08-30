---
name: pr-screenshot-docs
description: "Capture, verify, and attach before/after screenshots or video for pull requests with visual changes. Use when creating or updating a PR that changes rendered UI or interaction behavior."
---

# PR Screenshot Documentation

Prove UI changes with current visual evidence that reviewers can inspect from the pull request.

## When to Use This Skill

- Creating PRs with frontend/UI modifications
- Documenting visual changes for code review
- Recording changed interaction or motion behavior
- Building a visual record of design evolution
- Enabling async design review without running the app

## Visual Evidence Workflow

### 1. Before Making Changes

Capture the current state during reproduction, before implementing UI modifications:

```
1. Set the browser viewport to the target size, starting with mobile.
2. Navigate to the target page and state.
3. Inspect the page structure to identify the component or region.
4. Capture a screenshot for a static change or video for changed interaction or motion.
```

Record the viewport, data, theme, and interaction state so the comparison can reproduce them. For a new surface with no prior state, state that the surface did not exist and capture its nearest existing entry point when useful.

### 2. After Implementing Changes

Capture the same view during verification:

```
1. Refresh or navigate to the updated page and state.
2. Restore the recorded viewport, data, theme, and interaction state.
3. Capture the same component, region, or interaction.
4. Inspect the media and confirm that it shows the intended result.
```

Use screenshots for static changes. Use video when timing, animation, drag behavior, focus movement, or another interaction is the claim.

### 3. Store Media Safely

Do not commit review media. Use the repository's established PR attachment flow and prefer durable access-controlled storage over anonymous temporary hosting. For GitHub repositories that provide `GITHUB_ATTACHMENTS_TOKEN`, follow [GitHub User Attachments](references/github-user-attachments.md).

Before uploading, confirm that media contains no credentials, personal data, private customer content, internal URLs, browser extensions, or unrelated applications. Use stable seeded data when possible.

If the required upload credential or attachment mechanism is unavailable, do not claim that media was attached. Keep the media outside git and report the PR evidence as blocked.

### 4. Completion Rule

Do not report visual verification as complete until the evidence exists, has been inspected, and is linked from the current PR body. A UI implementation can be complete while its required PR evidence remains blocked. Report those states separately.

## PR Description Template

Include a visual comparison section in your PR description. For screenshots:

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| ![Before: target state](user-attachments URL) | ![After: target state](user-attachments URL) |

### What Changed
- [Specific visual change 1]
- [Specific visual change 2]
```

For videos, put each attachment URL on its own line:

```markdown
## Visual Changes

### Before
https://github.com/user-attachments/assets/...

### After
https://github.com/user-attachments/assets/...
```

## Viewport Recommendations

Choose viewport size based on what you're documenting:

| Target | Width | Height | Use Case |
|--------|-------|--------|----------|
| Mobile | 320 | 568 | Mobile-first responsive |
| Tablet | 768 | 1024 | Tablet layouts |
| Desktop | 1280 | 800 | Standard desktop |
| Wide | 1440 | 900 | Wide desktop layouts |

Start with the smallest affected viewport. Capture every viewport class needed to prove the changed responsive behavior. A mobile capture does not prove desktop behavior.

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
- Configuration updates with no rendered or interactive effect

## Integration with PR Workflow

Before submitting a UI change for review:

1. Capture the baseline during reproduction, before implementation when practical.
2. Implement and verify the change.
3. Capture the same states and viewports afterward.
4. Inspect the media for correctness and sensitive content.
5. Upload and embed the comparison in the PR body.
6. Preserve unrelated existing `user-attachments` embeds when editing a PR or issue body.
7. Re-read the saved body and confirm that each new embed resolves.
8. If a later change makes the evidence stale, recapture it and replace only the stale embeds.

## Example PR Section

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| ![Before: button](user-attachments URL) | ![After: button](user-attachments URL) |

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
