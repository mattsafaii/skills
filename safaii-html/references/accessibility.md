# Accessibility

Native-first markup gets you most of the way; these are the rules that finish the job. safaii-css owns layers, tokens, and units — the CSS snippets here are the accessibility slice that lives wherever the relevant styles do.

- **Skip the `title` attribute.** Poorly surfaced by assistive tech; the only good use is `<iframe title="…">`. For a real label, use a visible `<label>` or text.
- **Accessible name for icon-only controls.** An icon button with no text needs a name: `aria-label` on the button (simplest), or visible-to-SR text via the `.sr-only` utility. Don't rely on `title`, and never ship an icon-only button with no name. `<button aria-label="Close"><svg …></svg></button>`, or `<button><svg …></svg><span class="sr-only">Close</span></button>`.
- **Visually-hidden text → the `.sr-only` utility** (in the `utilities` layer). Hides text *visually* while keeping it in the accessibility tree — for icon-button names, a label on a search field, or a visually-hidden heading that labels a landmark. Use this exact recipe; `display:none`/`visibility:hidden` would remove it from the a11y tree (wrong), and `width/height:0` gets dropped by some screen readers. `clip-path: inset(50%)` is `clip-path`'s one functional use here; the `1px` size is the sanctioned exception (`0` is ignored by some SRs).

  ```css
  @layer utilities {
  	.sr-only {
  		position: absolute;
  		inline-size: 1px;
  		block-size: 1px;
  		margin: -1px;
  		padding: 0;
  		border: 0;
  		overflow: hidden;
  		clip-path: inset(50%);
  		white-space: nowrap;
  	}

  	/* Skip-to-content link: hidden until focused. */
  	.sr-only-focusable:focus-visible {
  		position: static;
  		inline-size: auto;
  		block-size: auto;
  		margin: 0;
  		overflow: visible;
  		clip-path: none;
  		white-space: normal;
  	}
  }
  ```
- **Visual uppercase belongs in CSS,** never the markup — a screen reader spells out literal `SUBMIT` letter by letter. Write `Submit` and apply `text-transform: uppercase` (on the element, or a `.u-uppercase` utility if the project already has a utilities layer).
- **ARIA attributes are the styling hook for state.** Style `[aria-expanded="true"]`, `[aria-current="page"]`, `[aria-disabled="true"]`, `[aria-invalid="true"]` directly — don't invent `.is-expanded` / `--collapsed` modifier classes. (safaii-css states this too; this is its home.)
- **Visible focus on everything interactive,** keyboard-only via `:focus-visible`, using a token color so it stays on-brand:

  ```css
  :where(:focus-visible) {
  	outline: 2px solid var(--color-accent);
  	outline-offset: 2px;
  }
  ```

- **Color contrast — meet WCAG 2.1 AA.** One of the most commonly failed checks. Normal text **4.5:1**, large text (18pt+/14pt+ bold) **3:1**, UI components and focus indicators **3:1** against neighbors. oklch lightness is a rough guide — a wide `L` gap between text and background usually clears it — but it's not a guarantee (chroma and hue shift the ratio), so verify a real pair with the [WebAIM checker](https://webaim.org/resources/contrastchecker/). When a pair is actually failing, [[safaii-css]] has the fix technique (adjust `L` only, plus APCA/WCAG threshold landmarks and the `L 0.6` light/dark boundary) in its Color tokens section. For palette-level contrast work, see [[color-expert]]. Note: CSS `contrast-color()` does **not** satisfy this — it only picks black/white and can fail AA on mid-tone backgrounds; it's an ask-first convenience (see [[safaii-css]]), not a contrast guarantee.

  ```css
  /* Comfortable AA pairs (verify final values) */
  --color-text: oklch(38% 0 0);   /* on --color-bg oklch(96% 0 0) → ~9:1 */
  --color-text-muted: oklch(52% 0 0); /* on the same bg → ~5:1, use sparingly */
  /* Watch out: oklch(67% 0 0) on white ≈ 2.9:1 — fails normal text */
  ```

- **Never signal state with color alone.** Color is invisible to color-blind users and in forced-colors mode. Pair it with a non-color cue: an icon, text, underline, weight, or shape. A red `[aria-invalid]` field also gets an error message; a "live"/"error"/"online" dot also gets a label; a link in body copy stays underlined, not just colored.
- **Gate enhancements** exactly as safaii-css does: motion inside `@media (prefers-reduced-motion: no-preference)`, glass/blur inside `@media (prefers-reduced-transparency: no-preference)`.

## The safe fade-in

The one pattern worth memorizing. **Never hide pre-animation content with `opacity: 0` alone** — screen readers ignore opacity, so the element is still in the accessibility tree and gets announced before a sighted user can see it. Layer two protections: a `js-ready` gate so content stays visible if JS never loads, and an IntersectionObserver so the reveal fires when the element enters the viewport (including when a screen-reader's virtual cursor scrolls to it).

```css
@media (prefers-reduced-motion: no-preference) {
	.js-ready .fade-in { opacity: 0; }
	.fade-in.is-visible { animation: fade-in 0.6s ease forwards; }
}

@keyframes fade-in { to { opacity: 1; } }
```

```js
document.documentElement.classList.add("js-ready");

const observer = new IntersectionObserver((entries) => {
	for (const entry of entries) {
		if (entry.isIntersecting) {
			entry.target.classList.add("is-visible");
			observer.unobserve(entry.target);
		}
	}
});

for (const el of document.querySelectorAll(".fade-in")) observer.observe(el);
```

No JS → `js-ready` never lands → content stays visible. Reduced-motion → hidden state never applies → content visible immediately. Otherwise the reader scrolling to the element triggers the reveal before announcement.

**This is the house pattern for scroll reveals — prefer it over scroll-driven CSS animations** (`animation-timeline: scroll()/view()`). Those aren't Baseline (no Safari yet), they lean decorative (against "no animation unless functional"), and this IntersectionObserver pattern already covers the accessible reveal. Reach for `animation-timeline` only if Matt asks for it specifically.
