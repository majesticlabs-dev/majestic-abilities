---
name: stimulus-coder
description: "Use when creating or refactoring Stimulus controllers. Applies Hotwire conventions, controller design patterns, targets/values usage, action handling, and JavaScript best practices."
---

# Stimulus Coder

**Audience:** Developers building interactive UIs with Stimulus.js and Hotwire.

**Goal:** Write maintainable Stimulus controllers where state lives in HTML and controllers add behavior.

## Core Concepts

- **Controllers** attach behavior to HTML elements
- **Actions** respond to DOM events
- **Targets** reference important elements
- **Values** manage state through data attributes

## Controller Design Principles

### Keep Controllers Small and Reusable

```javascript
// Good: Generic, reusable controller
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static values = { open: Boolean }

  toggle() { this.openValue = !this.openValue }

  openValueChanged() {
    this.contentTarget.classList.toggle("hidden", !this.openValue)
  }
}
```

### Use Data Attributes for Configuration

```javascript
export default class extends Controller {
  static values = {
    delay: { type: Number, default: 300 },
    event: { type: String, default: "input" }
  }

  connect() {
    this.element.addEventListener(this.eventValue, this.submit.bind(this))
  }

  submit() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => this.element.requestSubmit(), this.delayValue)
  }
}
```

```erb
<%= form_with data: { controller: "auto-submit", auto_submit_delay_value: 500 } %>
```

### Compose Multiple Controllers

```erb
<div data-controller="toggle clipboard" data-toggle-open-value="false">
  <button data-action="toggle#toggle">Show</button>
  <div data-toggle-target="content" class="hidden">
    <code data-clipboard-target="source">secret-code</code>
    <button data-action="clipboard#copy">Copy</button>
  </div>
</div>
```

## Targets and Values

### Targets for Element References

```javascript
export default class extends Controller {
  static targets = ["tab", "panel"]
  static values = { index: { type: Number, default: 0 } }

  select(event) { this.indexValue = this.tabTargets.indexOf(event.currentTarget) }

  indexValueChanged() {
    this.panelTargets.forEach((panel, i) => panel.classList.toggle("hidden", i !== this.indexValue))
    this.tabTargets.forEach((tab, i) => tab.setAttribute("aria-selected", i === this.indexValue))
  }
}
```

## Action Handling

```erb
<button data-action="click->toggle#toggle">Toggle</button>
<input data-action="input->search#update focus->search#expand">
<button data-action="modal#open" data-modal-id-param="confirm-dialog">Open</button>
<input data-action="keydown.enter->form#submit keydown.escape->form#cancel">
```

### Action Parameters

```javascript
open(event) {
  const modalId = event.params.id
  document.getElementById(modalId)?.showModal()
}
```

## Common Controller Patterns

### Dropdown Controller

```javascript
export default class extends Controller {
  static targets = ["menu"]
  static values = { open: Boolean }

  toggle() { this.openValue = !this.openValue }

  close(event) {
    if (!this.element.contains(event.target)) this.openValue = false
  }

  openValueChanged() {
    this.menuTarget.classList.toggle("hidden", !this.openValue)
    if (this.openValue) document.addEventListener("click", this.close.bind(this), { once: true })
  }
}
```

### Clipboard Controller

```javascript
export default class extends Controller {
  static targets = ["source", "button"]
  static values = { successMessage: { type: String, default: "Copied!" } }

  async copy() {
    const text = this.sourceTarget.value || this.sourceTarget.textContent
    await navigator.clipboard.writeText(text)
    this.showSuccess()
  }

  showSuccess() {
    const original = this.buttonTarget.textContent
    this.buttonTarget.textContent = this.successMessageValue
    setTimeout(() => this.buttonTarget.textContent = original, 2000)
  }
}
```

## Turbo Integration

```javascript
export default class extends Controller {
  connect() {
    document.addEventListener("turbo:before-visit", this.dismiss.bind(this))
    this.timeout = setTimeout(() => this.dismiss(), 5000)
  }

  disconnect() { clearTimeout(this.timeout) }
  dismiss() { this.element.remove() }
}
```

## Architecture Patterns

### Make Controllers Configurable

Externalize hardcoded values into data attributes. Never embed CSS classes, selectors, or thresholds in controller logic.

```javascript
// Bad: hardcoded
export default class extends Controller {
  toggle() { this.element.classList.toggle("hidden") }
}

// Good: configurable
export default class extends Controller {
  static classes = ["toggle"]
  toggle() { this.element.classList.toggle(this.toggleClass) }
}
```

### Mixins Over Deep Inheritance

Use mixins when behavior is shared but doesn't represent specialization.

Decision framework:
- **"is a"** → inheritance (class extends BaseController)
- **"acts as"** → mixin (apply behavior at connect)
- **"has a"** → composition (separate controller + outlets)

```javascript
// Mixin pattern
const Sortable = (controller) => {
  const original = controller.prototype.connect
  controller.prototype.connect = function() {
    if (original) original.call(this)
    this.sortable = new Sortable(this.element, this.sortableOptions)
  }
}
```

### Targetless Controllers

If a controller mixes element-level and target-level concerns, split it. Controller acting on `this.element` is one responsibility; acting on targets is another.

Communicate between split controllers via custom events or outlets.

### Namespaced Attributes

For flexible parameter sets without explicitly defining each value:

```javascript
// Read arbitrary data-chart-* attributes
get chartOptions() {
  return Object.entries(this.element.dataset)
    .filter(([key]) => key.startsWith("chart"))
    .reduce((opts, [key, val]) => {
      opts[key.replace("chart", "").toLowerCase()] = val
      return opts
    }, {})
}
```

See [architecture-patterns.md](references/architecture-patterns.md) for SOLID principles applied to Stimulus.

## Detailed Reference

Load [restored-examples.md](references/restored-examples.md) for the preserved examples, templates, and advanced patterns from the marketplace source.
