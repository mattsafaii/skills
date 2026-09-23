---
name: safaii-html
description: Safaii Studio's HTML conventions — semantic structure, the document skeleton, forms, accessibility, and coding style/formatting. Use when writing or reviewing any HTML markup, building web components, creating forms, or adding interactive elements (dialogs, accordions, tabs, nav) — even when "accessibility" or "HTML" isn't mentioned. Companion to safaii-css (which owns styling); this owns the markup surface.
---

# safaii-html

How Safaii Studio writes HTML — correct structure, accessible semantics, and consistent coding style, as one thing. Accessibility isn't a separate pass here; it rides along with the markup, because choosing the right element *is* the accessibility decision.

The accessibility core is derived from mikemai2awesome's `frontend-a11y`, diverged to match Safaii conventions; the original's CSS-architecture advice (layer names, `c-`/`u-` prefixes) is dropped because [[safaii-css]] owns all of that. Companion to [[safaii-css]] (the styling surface); this owns the markup surface. **If this skill and safaii-css disagree on anything CSS, safaii-css wins.**

Write as little code as possible. Reach for the native HTML element that's already accessible before adding ARIA, a class, or JavaScript to a generic one — the same "platform primitives first" rule safaii-css follows, applied to markup.

## Core principles

1. **Trust the browser** — native elements ship with built-in behavior and accessibility; don't rebuild it.
2. **Semantic over generic** — use the element that means the thing, not a `<div>` with a `role` or a class.
3. **Less is more** — every ARIA attribute, wrapper `<div>`, and line of JS you don't write is one less thing to break.
4. **Works without JS** — content is visible, links navigate, forms submit before a byte of JavaScript runs. JS enhances; it isn't load-bearing.

## Document skeleton

Every page starts from the same shell:

```html
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Page Name — Site Name</title>
	<meta name="description" content="One-sentence summary of the page.">
	<link rel="stylesheet" href="/style.css">
</head>
<body>
	…
</body>
</html>
```

- `<!doctype html>` and `lang` on `<html>` always — `lang` is cheap, high-value, and easy to forget. It's also load-bearing for CSS `hyphens: auto` (used on headings in the starter), which is language-dictionary-driven and **silently no-ops without `lang`**.
- `charset` is the first thing in `<head>`; `viewport` for responsive.
- A **unique, descriptive `<title>` per page** (`Page — Site`) and a `<meta name="description">` for search and link previews.
- **Never block zoom** — no `maximum-scale` / `user-scalable=no` on the viewport tag.

## Semantic structure

- **Landmarks.** One `<main>` per page; `<header>`/`<footer>` for banner/contentinfo; `<nav>` for navigation; `<aside>` for tangential content; **`<search>`** wrapping a search/filter form (it's the native `search` landmark — use it *instead of* `role="search"`, and don't add `role="search"` to it or its inner `<form>`). Multiple `<nav>`s each get an `aria-label` to tell them apart.
- **Don't repeat implicit roles.** `<header>`/`<nav>`/`<main>`/`<footer>`/`<search>` already carry `banner`/`navigation`/`main`/`contentinfo`/`search`. Never write `<nav role="navigation">` — and since `<search>` *is* the search landmark, never put `role="search"` on it or on a `<form>` inside it (that's a duplicate landmark).
- **Semantic over generic.** `<header><nav>…</nav></header>`, not `<div class="header"><div class="nav">`. A bare `<div>` is fine *only* as a pure styling hook with no meaning of its own.
- **Headings convey the outline, not size.** Exactly one `<h1>` per page; don't skip levels (`h2` → `h4`); rank is the document structure — visual size is CSS's job, not a reason to pick a level.
- **Sectioning.** `<article>` for self-contained content; `<section>` only when it has a heading and represents a real section; don't wrap everything in `<section>`.
- **Lists for lists** — nav links live in a `<ul>`; `<ol>` when order matters. For numbered content, **native `<ol>` is the default** — its numbering is announced to assistive tech, and you can still restyle the markers with `list-style-type` / `@counter-style` / `::marker` without losing that. Reserve CSS counters (`counter-reset`/`counter-increment` + `counter()`/`counters()` in `content`) for *presentational* numbering a native list can't express — section-numbered headings, nested `1.1.1`. Caveat: generated `content` isn't reliably read by screen readers, so if a counter-produced number carries meaning, also put it in real text or an `aria-label`. Never replace a real `<ol>`'s semantics with `list-style: none` + counters when the order matters.
- **`<figure>`/`<figcaption>`** for captioned media; **`<time datetime>`** for dates; **`<address>`** for contact info.
- **Tables for tabular data only** — never layout. Use `<caption>` and `<th scope="col|row">`.
- **Links vs buttons.** `<a href>` navigates (the URL changes); `<button>` performs an action. Never `<a href="#">` wired to JS, never `<div onclick>`. This is the markup side of the Hotwire rule: if it can be a link or a form submission, it should be.
- **Images.** Meaningful `alt` for content images, `alt=""` for decorative ones; set `width`/`height` to reserve space (prevents layout shift); `loading="lazy"` below the fold; use `<img>` (not a CSS `background-image`) when the image *is* content.

## Forms

- **Every control has a label** — a `<label for="id">` or a control wrapped in its `<label>`. Group related controls with `<fieldset>`/`<legend>`.
- **Right type and hints** — `type="email"`, `inputmode`, `autocomplete` so browsers and phones help the user.
- **Native validation first** — `required`, `type=email`, `min`/`max` before any JS validation.
- **Native suggestions → `<datalist>`** — for an input with a list of suggested-but-not-restricted values, wire `<input list="…">` to a `<datalist>` of `<option>`s. Zero JS for a combobox-lite; the user can still type a free value. (For a *restricted* choice use `<select>`; for a true filtered autocomplete that nothing native fits, the APG Combobox pattern.)
- **Validation styling after interaction** — style with `:user-valid` / `:user-invalid`, not `:valid` / `:invalid`. The `:user-*` versions only match once the user has actually interacted (or tried to submit), so a required field isn't flagged red on page load. (Baseline 2023 — mature; degrades to `:valid`/`:invalid` if you need a fallback.)
- **Submit via `<button type="submit">` inside a `<form action>`** — a real submission, per the Hotwire rule; reach for `fetch` only when a form or link genuinely can't express it.
- **Auto-growing fields → `field-sizing: content`** (CSS), not a JS auto-grow script — a `<textarea>` or `<input>` sizes to its content natively. Pair it with `min`/`max-width`/`-height` to bound the growth; never set a fixed `width`/`height` (that overrides it). Ask-first (recent, graceful): Baseline 2026, degrades to normal fixed sizing when unsupported — light heads-up before adding.

## Coding style

- **Lowercase** element and attribute names.
- **Double-quote** every attribute value.
- **Boolean attributes are bare** — `required`, `disabled`, `hidden`, not `required="required"`.
- **Void elements aren't self-closed** — `<br>`, `<img …>`, `<meta …>`, not the XHTML `<br />`.
- **Tabs for indentation**, matching the house style (the same as `safaii-css`'s starter).
- **Attribute order** (loose, don't over-police): `class`, `id`, `name`, `data-*`, `src`/`href`/`type`/`value`, `alt`/`title`, `aria-*`/`role`, then booleans. Keep `class`/`id` first.
- **One attribute-heavy element per line;** wrap long attribute lists rather than running them off-screen.
- **Comments:** ship-facing notes in `<!-- -->`, sparingly. Build-only notes go in the template engine's comment (`{% # … %}` in Liquid) so they never reach the browser.

## Naming & hooks

- **Class names coordinate with safaii-css's `@scope`.** Style through the component root, so classes are mostly component roots plus the occasional utility — no BEM, no `c-`/`u-` system unless the project already has a utilities layer (per safaii-css).
- **`js-` prefix for JavaScript hooks** — never styled, never used as a semantic or a11y hook. Behavior hooks and style hooks stay separate.
- **State lives on ARIA attributes, not modifier classes** (see Accessibility below).

## Template integration

The markup conventions here are engine-agnostic — the template layer just emits this HTML.

- **11ty:** Liquid only (no Nunjucks mixing). Reusable fragments are Liquid `{% include %}` partials; build-only comments use `{% # … %}` or `{% comment %} … {% endcomment %}`.
- **Liquid truthiness:** only `nil` and `false` are falsy — an empty string or empty array is **truthy**. Guard optional values with `!= blank` (`{% if site.phone != blank %}`), never a bare `{% if site.phone %}`, or a blank value renders.
- **Rails:** ERB + Hotwire; prefer a link or form submission over custom `fetch`; extract partials for reuse.

## Component patterns

Use the native element that already has the behavior; only fall back to ARIA patterns when nothing native fits — accordion → `<details>`/`<summary>`, modal → native `<dialog>` opened via invoker commands, dropdown nav → `<button aria-expanded>` toggling `hidden`, live message → a single `role="alert"`, non-interactive subtree → `inert`. When native genuinely isn't enough, follow the [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) pattern rather than improvising.

**Before building any interactive component** (accordion, modal, dropdown, live region), open `references/components.md` — it has the full pattern for each, the code, and the declarative `command`/`commandfor` wiring for dialogs/popovers (with its required pre-2025 browser fallback).

## Accessibility

Native-first markup gets you most of the way; these are the rules that finish the job. safaii-css owns layers, tokens, and units — the CSS referenced here is the accessibility slice that lives wherever the relevant styles do.

- **Skip the `title` attribute** — poorly surfaced by assistive tech; use a visible `<label>`/text instead (exception: `<iframe title="…">`).
- **Every icon-only control needs an accessible name** — `aria-label` or `.sr-only` text, never `title` alone.
- **Hide text visually without losing it from the accessibility tree** via the `.sr-only` recipe — never `display:none`/`visibility:hidden`/`width:0`, which drop it entirely.
- **Style state on ARIA attributes** (`[aria-expanded="true"]`, `[aria-current="page"]`, `[aria-invalid="true"]`) — never invent `.is-expanded` modifier classes.
- **Visible `:focus-visible` on everything interactive**, in a token color.
- **Color contrast meets WCAG 2.1 AA** (4.5:1 normal text, 3:1 large text/UI) — verify with the [WebAIM checker](https://webaim.org/resources/contrastchecker/), not oklch lightness alone. `contrast-color()` does not guarantee AA.
- **Never signal state with color alone** — pair it with an icon, text, underline, or shape.
- **Gate enhancements**: motion inside `prefers-reduced-motion: no-preference`, glass/blur inside `prefers-reduced-transparency: no-preference`.
- **Never hide pre-animation content with `opacity: 0` alone** — screen readers ignore opacity. Use the `js-ready` + IntersectionObserver safe fade-in pattern instead.

**Full recipes** (the `.sr-only` CSS, focus-ring snippet, contrast examples, and the safe fade-in pattern in full) live in `references/accessibility.md` — open it when you need the actual code, not just the rule.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `hyphens: auto` (or other language-dependent CSS) silently no-ops | `<html>` is missing `lang` | Always set `lang` on `<html>` — cheap, easy to forget, and load-bearing for language-dictionary CSS |
| Screen reader spells out a word letter by letter | Uppercase text written directly in the markup (`SUBMIT`) | Write normal case in HTML; apply `text-transform: uppercase` in CSS |
| Icon-only button is unusable with a screen reader | No accessible name — relying on the icon alone, or on `title` | Add `aria-label` or visually-hidden `.sr-only` text; never ship an icon-only control with no name |
| Content is announced before a sighted user can see it | Pre-animation state hidden with `opacity: 0` alone, no `js-ready`/IntersectionObserver gate | Use the safe fade-in pattern (`js-ready` class + IntersectionObserver) — opacity alone doesn't leave the accessibility tree |
| `command`/`commandfor` button does nothing | Invoker Commands isn't supported (pre-2025 browser) and no fallback was shipped | Add the feature-detect fallback snippet, delete it once the audience is fully on supporting browsers |
| Screen reader announces a duplicate landmark | `role="search"`/`role="navigation"` added to an element that already carries that implicit role | Drop the redundant `role` — `<nav>`, `<search>`, etc. already imply it |
| `hidden="until-found"` never reveals on find-in-page | Applied to a `display: none/contents/inline` element | It needs a real box to reveal into — use a `display` that has one |
| A blank value renders anyway (`data-site=""`, an empty `"telephone"`) | Liquid treats empty strings and empty arrays as truthy — only `nil` and `false` are falsy | Guard optional values with `!= blank` (`{% if site.phone != blank %}`), not a bare `{% if site.phone %}` |

## Quick reference

| Instead of | Use |
|---|---|
| `<div role="button">` | `<button>` |
| `<a href="#">` + JS | `<a href>` (navigate) or `<button>` (act) |
| `<div role="dialog">` + focus-trap JS | native `<dialog>` opened via `command`/`commandfor` |
| `onclick="el.showModal()"` / JS open-close wiring | `command`/`commandfor` (+ removable feature-detect fallback) |
| custom accordion JS | `<details>` + `<summary>` |
| `<nav role="navigation">` | `<nav>` |
| `<div class="header">` | `<header>` |
| heading chosen by size | heading chosen by outline rank; size in CSS |
| `.is-expanded` class | `[aria-expanded="true"]` |
| `title="…"` tooltip | a real `<label>` / visible text |
| literal `SUBMIT` in HTML | `Submit` + `text-transform: uppercase` |
| `<br />` (XHTML) | `<br>` (HTML void element) |
| `required="required"` | `required` (bare boolean) |
| `opacity: 0` fade-in | the `js-ready` + IntersectionObserver pattern above |

## References

- `references/components.md` — full component patterns and Invoker Commands code
- `references/accessibility.md` — full accessibility recipes and the safe fade-in pattern
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — find a specific success criterion fast
- [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) — the canonical patterns when native won't do
- [MDN HTML element reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element) — which element means what
- [[safaii-css]] — the styling half of the house style; [[color-expert]] — contrast and palette depth

## Status

Renamed and expanded from `safaii-a11y` (2026-06-29) to cover the full markup surface: structure, semantics, forms, coding style, and accessibility merged in rather than kept separate. Split the Component patterns/Invoker Commands and full Accessibility recipes out to `references/` (2026-07-02), matching safaii-css's reference-file pattern — this file keeps the scannable rules, the reference files keep the code. Switched the 11ty template convention from Nunjucks to Liquid (2026-09-22), matching the client-site starter.

Behavioral evals live in `evals/evals.json` — they test whether this skill *steers* an agent to the conventions (a test of the skill, not a consumer to keep in sync). Not part of normal markup work; run them via the skill-crafting tooling when changing the conventions, and add an eval when a new convention lands.

**Derived view:** the Basecamp doc "Frontend Conventions" (Lab project 46824335, doc 9768197742) is one combined, overview-level summary covering both this skill and [[safaii-css]] — a human-readable view, refreshed downhill, never an edit-gate. It's high-level, so most rule changes here don't require touching it; see safaii-css's Consumers section for the refresh procedure.
