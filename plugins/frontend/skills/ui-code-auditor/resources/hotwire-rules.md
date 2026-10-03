# Hotwire/Stimulus UI Audit Rules

Patterns specific to Rails Hotwire (Turbo + Stimulus) and ERB views.

## Stimulus Accessibility

### Critical

| Pattern | Issue | Fix |
|---------|-------|-----|
| `<div data-action="click->` or `<span data-action="click->` on non-control | Click-only handler, not keyboard reachable | Use `<button>`; otherwise add `keydown.enter->`/`keydown.space->` actions with `tabindex="0"` and a role |
| Icon-only `<button>` containing only `<svg>`/`<i>` | Missing accessible name | Add `aria-label` or visually hidden text |

### Serious

| Pattern | Issue | Fix |
|---------|-------|-----|
| Controller toggles visibility without updating `aria-expanded`, `aria-selected`, or `aria-hidden` | State not announced | Update the attribute in the `*ValueChanged` callback or action |
| `document.addEventListener` in `connect()` without removal in `disconnect()` | Listener leaks across Turbo visits | Store the bound handler and remove it in `disconnect()` |
| `setInterval`/`setTimeout` started in `connect()` without clear in `disconnect()` | Timer fires on detached elements | Clear in `disconnect()` |
| Controller moves focus into a dialog and never restores it on close | Focus lost (2.4.3) | Use `<dialog>`/`showModal()` or restore `document.activeElement` on close |
| `innerHTML` assignment with request or user data | XSS risk, a11y unknown | Assign `textContent` or re-render a sanitized partial |

### Moderate

| Pattern | Issue | Fix |
|---------|-------|-----|
| Hardcoded CSS classes or selectors in a controller | Not reusable, drifts from design tokens | Use `static classes`/`static values` configured from ERB |
| `alert()`/`confirm()` for feedback | Blocks the page, poor a11y | Use a status region with `aria-live="polite"` |
| Timers or counters updating visible text without `aria-live` region | Changes not announced | Wrap target in `aria-live="polite"` or update only on meaningful boundaries |

## Turbo Frames

### Serious

| Pattern | Issue | Fix |
|---------|-------|-----|
| `<turbo-frame id="...">` with no matching `turbo_stream` target or `dom_id` | Silent update failure | Align ids with `dom_id(record)` and stream targets |
| Form error response rendered with 200 | Turbo treats it as success, errors invisible | Render `status: :unprocessable_entity` (422) |
| Destructive action on a link without confirmation (`data-turbo-confirm`) | One-click irreversible action | Use `button_to` with `data-turbo-confirm` |

### Moderate

| Pattern | Issue | Fix |
|---------|-------|-----|
| Eager `src` frame for below-fold content | Unnecessary request on load | Add `loading="lazy"` |
| `loading="lazy"` frame with empty body | Layout shift or blank flash | Include skeleton or placeholder markup |

## Turbo Streams

### Serious

| Pattern | Issue | Fix |
|---------|-------|-----|
| `broadcast_*_to` with an unscoped stream name | Cross-account data leak | Scope by account/workspace/user: `broadcast_replace_to [account, :cards]` |
| Broadcast partial relying on controller instance variables | Runtime error outside request context | Pass explicit locals to the partial |

### Moderate

| Pattern | Issue | Fix |
|---------|-------|-----|
| Collection rows without a stable `dom_id` wrapper | `append`/`remove` cannot target rows | Wrap each row with `dom_id(record)` |

## ERB Views

### Critical

| Pattern | Issue | Fix |
|---------|-------|-----|
| `link_to` with `href="#"` and a `data-action` that mutates state | Wrong semantics, no keyboard/form semantics | Use `button_to` or a real form control |

### Serious

| Pattern | Issue | Fix |
|---------|-------|-----|
| `data: { turbo: false }` without an adjacent reason comment | Silent full-page reload, intent unknown | Document why Turbo is disabled |

## Custom Implementation Detection

### Recommendations (not violations)

When detecting custom implementations, suggest accessible alternatives:

| Custom Pattern | Suggested Alternative |
|----------------|-----------------------|
| Custom dropdown/select | `<details>`/`<summary>` or a disclosure controller with `aria-expanded` |
| Custom modal/dialog | `<dialog>` element with `showModal()` |
| Copy button | The project's Stimulus clipboard controller, or one using `navigator.clipboard.writeText` |
| Auto-submitting search form | Debounced controller calling `requestSubmit()` |
| Custom tabs | `role="tablist"`/`tab`/`tabpanel` with `aria-selected` and arrow-key actions |
