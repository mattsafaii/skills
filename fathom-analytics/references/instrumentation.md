# Wiring trackEvent() into a site

Default to one delegated listener driven by a data attribute, instead of a bespoke handler per event. Adding a new tracked element becomes "add the attribute," not "write more JS." This works on any stack — no framework assumed:

```html
<script>
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-fathom-event]')
    if (el && window.fathom) {
      var value = el.dataset.fathomValue
      window.fathom.trackEvent(el.dataset.fathomEvent, value ? { _value: Number(value) } : undefined)
    }
  })
</script>
```

Usage:

```html
<a href="tel:+13105551234" data-fathom-event="phone link clicked">(310) 555-1234</a>
<button data-fathom-event="pricing cta clicked">Get a quote</button>
```

For a form submission, listen on `submit` instead of `click`, same `closest('[data-fathom-event]')` pattern, placed on the `<form>` element.

## If the site already has a component/behavior layer

Don't add the raw listener above alongside an existing one — read the same `data-fathom-event`/`data-fathom-value` attributes from whatever the site already uses to wire behavior (a Stimulus controller, an Alpine directive, a React handler, htmx). One source of truth for "what's tracked" (the data attribute), wired through whatever mechanism is already idiomatic for that codebase. Don't introduce a second framework just to fire an analytics event.

## Rules

- One event name, one exact string, used identically in the Fathom event definition and the `data-fathom-event` value. A typo here means the event exists in the dashboard but never receives data — nothing errors, it just silently reports zero.
- Don't fire on `mousedown` or `pointerdown` to "catch it before navigation" — `click` is what Fathom's own examples use and what's testable in DevTools' Network tab.
- Values are always cents, always a number when passed to `trackEvent`, even though the data attribute carries it as a string.
