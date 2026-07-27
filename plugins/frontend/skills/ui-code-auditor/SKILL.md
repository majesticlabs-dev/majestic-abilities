---
name: ui-code-auditor
description: "Review frontend source code for accessibility, UI-quality, and performance problems with file-and-line evidence. Use when statically auditing HTML, CSS, Tailwind, React, Vue, or component code without relying on screenshots."
---

# UI Code Auditor

Static code analysis for UI quality and accessibility. Use `visual-validator` separately when rendered screenshots are available.

## Input

```yaml
path: string           # File or directory to audit (default: src/ or app/)
tech_stack: string[]   # From config, e.g., ["react", "vue", "generic"]
focus: string          # Optional: "accessibility", "performance", "all"
```

## Review Process

### 1. Detect Tech Stack

Inspect project manifests, file extensions, framework configuration, and existing component conventions. Default to framework-neutral checks when the stack is unclear.

### 2. Load Rules

Always load [resources/generic-rules.md](resources/generic-rules.md). Also load [resources/react-rules.md](resources/react-rules.md) when React or JSX is in scope.

### 3. Find UI Files

```bash
# React/JS projects
find . -type f \( -name "*.tsx" -o -name "*.jsx" \) | head -100

# CSS
find . -type f \( -name "*.css" -o -name "*.scss" \) | head -50
```

### 4. Audit Each File

For each UI file:

1. Read file content
2. Apply patterns from loaded rules
3. Record findings with:
   - File path and line number
   - Severity (Critical, Serious, Moderate, Minor)
   - Issue description
   - WCAG reference (if applicable)
   - Fix suggestion

### 5. Generate Report

## Output Format

```markdown
## UI Code Audit Summary

**Verdict: PASS | FAIL**

- **Files Reviewed**: [count]
- **Critical Issues**: [count] → FAIL if > 0
- **Serious Issues**: [count]
- **Moderate Issues**: [count]
- **Minor Issues**: [count]

### Critical Findings

| File:Line | Issue | WCAG | Fix |
|-----------|-------|------|-----|
| `src/Button.tsx:45` | DIV with onClick, not keyboard accessible | 2.1.1 | Use `<button>` element |
| `src/Card.tsx:23` | Image missing alt text | 1.1.1 | Add `alt="description"` |

### Serious Findings

| File:Line | Issue | WCAG | Fix |
|-----------|-------|------|-----|
| `src/Modal.tsx:89` | Focus not trapped in modal | 2.4.3 | Implement focus trap |

### Moderate Findings

| File:Line | Issue | WCAG | Fix |
|-----------|-------|------|-----|
| `src/List.tsx:12` | Touch target 24px (< 44px) | 2.5.5 | Use `min-w-11 min-h-11` |

### Recommendations

- Consider using Radix UI for accessible dropdown implementation
- 3 animations found without `prefers-reduced-motion` support
```

## Severity Definitions

| Severity | Definition | Verdict Impact |
|----------|------------|----------------|
| **Critical** | Blocks accessibility (can't use with keyboard/screen reader) | FAIL |
| **Serious** | Significantly degrades UX for assistive tech users | Warning |
| **Moderate** | Best practice violation, minor UX impact | Warning |
| **Minor** | Polish opportunity, no functional impact | Info |

## WCAG Quick Reference

| Code | Name | Common Violations |
|------|------|-------------------|
| 1.1.1 | Non-text Content | Missing alt text |
| 1.3.1 | Info and Relationships | Missing form labels |
| 2.1.1 | Keyboard | Click-only handlers |
| 2.1.2 | No Keyboard Trap | Modal without escape |
| 2.4.3 | Focus Order | tabindex > 0 |
| 2.4.7 | Focus Visible | outline: none |
| 2.5.5 | Target Size | Touch target < 44px |
| 4.1.2 | Name, Role, Value | Missing ARIA |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No UI files found | Return PASS with "No UI files to audit" |
| tech_stack not configured | Use generic rules only |
| Stack rules fail to load | Log warning, continue with generic |
| File cannot be parsed | Skip file, note in report |
| Multiple tech_stacks | Load rules for each, merge findings, deduplicate |
