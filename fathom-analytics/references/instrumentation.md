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

## Page-load / pathname-based triggers

Some conversions are better tracked as "did this page load" than "was this clicked" — a form that redirects to a success page on confirmed completion (not just on submit, which fires before you know if it actually succeeded) is the common case:

```html
<script>
  if (window.fathom && location.pathname === '/thank-you') {
    window.fathom.trackEvent('site survey requested')
  }
</script>
```

**Verify the exact pathname against the deployed site, not the source filename.** Static hosts routinely rewrite URLs: Cloudflare Pages strips `.html` (the template file is `thank-you.html`, the served path is `/thank-you`), some hosts add or remove trailing slashes, some serve `/thank-you/index.html` at `/thank-you/`. A check written against the template's literal filename can pass code review and still never fire in production — nothing errors, the event just silently reports zero forever. Confirm with a real request (`curl -sI <live-url>` or open it in a browser) before wiring the check, not just by reading the template.

## If the site already has a component/behavior layer

Don't add the raw listener above alongside an existing one — read the same `data-fathom-event`/`data-fathom-value` attributes from whatever the site already uses to wire behavior (a Stimulus controller, an Alpine directive, a React handler, htmx). One source of truth for "what's tracked" (the data attribute), wired through whatever mechanism is already idiomatic for that codebase. Don't introduce a second framework just to fire an analytics event.

## Rules

- One event name, one exact string, used identically in the Fathom event definition and the `data-fathom-event` value. A typo here means the event exists in the dashboard but never receives data — nothing errors, it just silently reports zero.
- Don't fire on `mousedown` or `pointerdown` to "catch it before navigation" — `click` is what Fathom's own examples use and what's testable in DevTools' Network tab.
- Values are always cents, always a number when passed to `trackEvent`, even though the data attribute carries it as a string.
