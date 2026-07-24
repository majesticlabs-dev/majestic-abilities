# Stimulus Coder Detailed Reference

## Controller Communication

Choose pattern based on coupling needs:

| Pattern | Coupling | Direction | Use When |
|---------|----------|-----------|----------|
| Custom events | Loose | Broadcast (1→many) | Sender doesn't know receivers |
| Outlets | Structured | Direct (1→1, 1→few) | Known relationships in layout |
| Callbacks | Read-only | Request/response | Sharing state without triggering actions |

### Custom Events (Preferred Default)

```javascript
// Sender
this.dispatch("submitted", { detail: { id: this.idValue }, bubbles: true })

// Receiver (in HTML)
// data-action="sender:submitted->receiver#handleSubmit"
```

Rules:
- Always set `bubbles: true` for cross-controller events
- Namespace event names: `form:submitted`, `cart:updated`
- Document the `detail` contract

### Outlets (Structured Relationships)

```javascript
export default class extends Controller {
  static outlets = ["result"]

  search() {
    const results = this.performSearch()
    this.resultOutlets.forEach(outlet => outlet.update(results))
  }

  resultOutletConnected(outlet) { /* setup */ }
  resultOutletDisconnected(outlet) { /* cleanup */ }
}
```

## Lifecycle Best Practices

### Don't Overuse `connect()`

`connect()` is for **third-party plugin initialization only**. Not for state setup (use Values API) or event listeners (use `data-action`).

```javascript
// Good: plugin init in connect
connect() {
  this.chart = new Chart(this.canvasTarget, this.chartConfig)
}

disconnect() {
  this.chart.destroy()
  this.chart = null
}
```

### Always Pair connect/disconnect

Every resource acquired in `connect()` must be released in `disconnect()`. Controllers can connect/disconnect multiple times during Turbo navigation.

### Turbo Cache Teardown

Prevent "flash of manipulated content" when cached pages return:

```javascript
connect() {
  document.addEventListener("turbo:before-cache", this.teardown.bind(this))
  this.slider = new Swiper(this.element, this.config)
}

teardown() {
  this.slider?.destroy()
  // Restore original DOM state before caching
}

disconnect() {
  this.teardown()
}
```

## Event Listener Hygiene

### Store Bound References

`.bind()` creates a new function each call. Store the reference for proper removal:

```javascript
connect() {
  this.boundResize = this.resize.bind(this)
  window.addEventListener("resize", this.boundResize, { passive: true })
}

disconnect() {
  window.removeEventListener("resize", this.boundResize)
}
```

### Prefer Declarative Actions

```erb
<%# Good: Stimulus manages lifecycle %>
<div data-controller="search"
     data-action="resize@window->search#layout keydown.escape@window->search#close">

<%# Bad: manual addEventListener in connect() %>
```

Global events use `@window` or `@document` suffix in `data-action`.

See [lifecycle-and-events.md](lifecycle-and-events.md) for complete patterns.

## Application Controller

Create `app/javascript/controllers/application_controller.js` as a base for shared functionality:

```javascript
import { Controller } from "@hotwired/stimulus"

export default class ApplicationController extends Controller {
  handleError(error, context = {}) {
    console.error(`[${this.identifier}]`, error, context)
    // Sentry.captureException(error, { extra: context })
  }
}
```

Extend it in domain controllers:

```javascript
import ApplicationController from "./application_controller"

export default class extends ApplicationController {
  async save() {
    try {
      await this.persist()
    } catch (error) {
      this.handleError(error, { action: "save", id: this.idValue })
    }
  }
}
```

Rules:
- Use `try-catch` for async operations and third-party library calls
- Never swallow errors — log or report via `handleError()`
- Use `requestSubmit()` not `submit()` for forms — fires validation and Turbo intercept

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Creating DOM extensively | Fighting Stimulus philosophy | Let server render HTML |
| Storing state in JS | State lost on navigation | Use Values in HTML |
| Over-specific controllers | Not reusable | Design generic behaviors |
| Manual querySelector | Fragile, bypasses Stimulus | Use targets |
| Inline event handlers | Unmaintainable | Use data-action |
| Overloading connect() | Bloated, mixes concerns | Values for state, data-action for events |
| Tight controller coupling | Fragile, hard to test | Custom events or outlets |
| Missing disconnect cleanup | Memory leaks, duplicate listeners | Always pair connect/disconnect |
| Unbound event references | Can't removeEventListener | Store `.bind()` result |

## Output Format

When creating Stimulus controllers, provide:

1. **Controller** - Complete JavaScript implementation
2. **HTML Example** - Sample markup showing usage
3. **Configuration** - Available values and targets
4. **Integration** - How it works with Turbo if applicable
