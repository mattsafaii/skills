# Component patterns

Use the native element that already has the behavior; only fall back to ARIA patterns when nothing native fits.

- **Accordion → `<details>`/`<summary>`.** Zero JavaScript. To animate the open/close (no JS), style the panel with the **`::details-content`** pseudo-element (Baseline 2025) and transition `opacity` + `content-visibility … allow-discrete` so the fade survives collapse; for a smooth height expand add `interpolate-size: allow-keywords` and transition `height` to `auto` (Chromium-only for now — pure enhancement, animates there and instant-toggles elsewhere). Gate the whole thing behind `prefers-reduced-motion: no-preference`, and keep it subtle — functional reveal, not decoration. (`<details>` content is already findable by browser find-in-page — browsers auto-expand it on a match — so prefer it for collapsibles.)
- **Findable collapsibles → `hidden="until-found"`.** When you have a *custom* show/hide that isn't a `<details>` (a "read more", a collapsed FAQ answer), hide it with `hidden="until-found"` instead of `display: none` — the content stays discoverable via find-in-page and scroll-to-text, and the browser auto-reveals it (fires `beforematch`) on a match. Recent/Chromium-led; degrades to a plain `hidden` (content hidden, just not findable) elsewhere, so it's safe. Don't use it on `display: none/contents/inline` elements — it needs a box to reveal.
- **Modal → native `<dialog>`, opened with invoker commands** (`command`/`commandfor`) — no `onclick`, no JS. Focus trapping, Escape-to-close, `::backdrop`, and inert-background are all automatic — no focus-trap library. See "Invoker commands" below.
- **Dropdown nav → `<nav>` with a `<button aria-expanded>` toggling a `hidden` list.** Don't use `role="menu"`/`menuitem`/`aria-haspopup` for site navigation — those are for app menus, not links. (A native `popover` toggled by `command="toggle-popover"` is a valid declarative alternative — see below — but `aria-expanded` + `hidden` has wider support; use it as the default.)
- **Live message → a single `role="alert"`.** That's the whole pattern.
- **Non-interactive subtree → the `inert` attribute** (Baseline 2023). Put `inert` on an off-canvas nav while it's closed, or on background content behind a *custom* overlay — it removes the subtree from tab order, the a11y tree, and find-in-page in one attribute, no `tabindex="-1"` juggling. (A native `<dialog>` opened with `.showModal()` already makes the rest of the page inert for you, so `inert` is for the custom cases.) Caveat: `inert` has no visual signal of its own — pair it with visible styling so sighted users see what's disabled.

```html
<details>
	<summary>Section</summary>
	<p>Content</p>
</details>

<div role="alert">Your changes have been saved.</div>
```

When native genuinely isn't enough, follow the APG pattern rather than improvising: [Combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-autocomplete-both/) (custom selects), [Switch](https://www.w3.org/WAI/ARIA/apg/patterns/switch/examples/switch-button/) (on/off toggles), [Manual Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-manual/), [Feed](https://www.w3.org/WAI/ARIA/apg/patterns/feed/examples/feed/) (infinite scroll), [Carousel](https://www.w3.org/WAI/tutorials/carousels/).

## Invoker commands

Wire a `<button>` to a `<dialog>` or popover **declaratively**, with no event listeners and no `onclick` — the relationship lives in the HTML. `commandfor` points at the target's `id`; `command` is the action. This is the platform-primitive replacement for `onclick="el.showModal()"`.

```html
<button command="show-modal" commandfor="signup">Sign up</button>

<dialog id="signup">
	<h2>Sign up</h2>
	<button command="close" commandfor="signup">Close</button>
</dialog>
```

- **Dialog commands:** `show-modal`, `close`, and `request-close` (fires a *cancelable* close request — the hook for an unsaved-changes guard, still without wiring open/close in JS).
- **Popover commands:** `toggle-popover`, `show-popover`, `hide-popover` (target has the `popover` attribute).
- **Custom commands** start with `--` and dispatch a `command` event on the target you listen for — a declarative alternative to `onclick`.

**Support & fallback.** `command`/`commandfor` is **Baseline newly available** (Chrome/Edge 135, Firefox 144, Safari 26.2 — all 2025). It fails *ungracefully*: in an older browser the button does nothing and the dialog won't open. Per the house policy ([[safaii-css]] `references/browser-support.md`), use the Baseline feature **and ship a removable feature-detect fallback**, then delete the fallback once the audience is fully on supporting browsers:

```js
// Fallback for browsers without Invoker Commands (pre-2025). Delete once
// the audience is fully on Baseline-supporting browsers.
if (!("commandForElement" in HTMLButtonElement.prototype)) {
	for (const btn of document.querySelectorAll("[commandfor][command]")) {
		btn.addEventListener("click", () => {
			const el = document.getElementById(btn.getAttribute("commandfor"));
			const cmd = btn.getAttribute("command");
			if (cmd === "show-modal") el.showModal();
			else if (cmd === "close") el.close();
			else if (cmd === "toggle-popover") el.togglePopover();
			else if (cmd === "show-popover") el.showPopover();
			else if (cmd === "hide-popover") el.hidePopover();
		});
	}
}
```
