# Stimulus Lifecycle And Events

## Connect And Disconnect

- initialize third-party widgets in `connect()`
- destroy them in `disconnect()`
- remove global listeners in `disconnect()`
- prepare for multiple connect/disconnect cycles during Turbo navigation

## Listener Hygiene

```js
connect() {
  this.boundResize = this.resize.bind(this)
  window.addEventListener("resize", this.boundResize, { passive: true })
}

disconnect() {
  window.removeEventListener("resize", this.boundResize)
}
```

## Turbo Cache

If a controller mutates DOM that should not survive Turbo cache restore, tear it down before cache.

```js
connect() {
  this.beforeCache = () => this.teardown()
  document.addEventListener("turbo:before-cache", this.beforeCache)
}

disconnect() {
  document.removeEventListener("turbo:before-cache", this.beforeCache)
}
```
