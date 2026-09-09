# Page anatomy

The fixed skeleton. Every tool page has these five sections in this order. Nothing else without asking.

```
header   wordmark + repo link
hero     name, promise, install command
demo     terminal block (the signature artifact)
proof    hairline rows — what / how / why
footer   license · made by Safaii
```

Measure: `--measure` from starter (64ch) or ~720px, whichever is narrower. Single column at all sizes; no breakpoints needed beyond fluid type.

## 1. Header

Wordmark = tool name in mono, lowercase, linked to `#top`. Right side: repo link (or "source on request" for private repos). No nav bar. One line tall.

## 2. Hero

```html
<header class="hero">
  <p class="kicker">scry</p>
  <h1>Find the right image in your library without scrolling.</h1>
  <p class="sub">Semantic search over a local folder of images. Runs on your machine.</p>

  <div class="install" role="group" aria-label="Install command">
    <code id="cmd">brew install scry</code>
    <button type="button" data-copy="#cmd">Copy</button>
  </div>
</header>
```

- Kicker: tool name, small, mono, accent color.
- H1: the promise. One sentence, plain words, no adjectives that survive deletion.
- Sub: one more sentence max — mechanism or audience, not features.
- Install block: dark surface (`oklch(22% 0 0)` bg, light text), mono, full command visible. Button inside it, right edge.

### Copy button contract

```js
document.querySelectorAll("[data-copy]").forEach(btn => {
  btn.addEventListener("click", async () => {
    const text = document.querySelector(btn.dataset.copy).textContent;
    await navigator.clipboard.writeText(text);
    btn.textContent = "Copied";
    setTimeout(() => (btn.textContent = "Copy"), 1600);
  });
});
```

- `<button>` is keyboard-focusable with a visible `:focus-visible` ring ([[safaii-html]]).
- Feedback via the button label; wrap the swap region so width doesn't change (`min-width: 4.5em` or grid overlay).
- Without JS: button does nothing but the `<code>` is selectable text — page still works (Check 6).
- Announce state change: give the button `aria-live="polite"` so "Copied" is read out.

## 3. Terminal block — the signature artifact

Real output from a real run. This section exists to prove the promise; it's the only place the tool speaks for itself.

```html
<section aria-label="Example output">
  <pre><code>$ zeni "tacos 12 cash"
✓ Added: 2026-08-25 tacos  $12.00  expenses:food → assets:cash</code></pre>
</section>
```

- Same dark surface as the install block — they read as one system.
- Prompt line included (`$ …`) so it reads as a terminal.
- Capture procedure: run the tool fresh, copy stdout verbatim, trim only to fit ~6 lines. Fix nothing, prettify nothing.
- If output is long/interactive, show the most representative moment and note truncation honestly (`… 14 more findings`).

## 4. Proof rows

Three to five rows, each one claim. Hairline top borders between rows, generous block spacing, no boxes.

```html
<dl class="proof">
  <div>
    <dt>Merges engines</dt>
    <dd>Lighthouse, axe, pa11y, Nuclei run as subprocesses; one verdict comes out.</dd>
  </div>
</dl>
```

- dt = short verb phrase (2–4 words), dd = one sentence of mechanism.
- Order: strongest proof first.
- Sourced from the README. If the README hedges, the row hedges too.

## 5. Footer

One line: `MIT · built by Matt Safaii`. Muted color, small size. No social icons, no newsletter unless Matt asks.

## Motion budget

Default is none beyond starter micro-transitions (link underline, focus ring). Allowed, gated behind `prefers-reduced-motion: no-preference` per [[safaii-css]]:

- The install block fading up once on load (opacity + translateY only).
- Copy-button label crossfade (same grid cell, geometry stable).

Nothing else. No counters, no typing effects, no parallax.
