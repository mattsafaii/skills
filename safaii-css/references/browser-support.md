# Browser support & feature verification

This skill leans on recent CSS. Support status is the one thing that goes stale faster than this file — **treat the snapshot below as dated (Jan 2026) and verify borderline features at write-time.**

## Support policy

The bar isn't a fixed age (the textbook "Baseline Widely available = 30 months" gate is too conservative). It's **project type × failure cost.**

- **Personal / own projects** → **Baseline Newly available.** Use the latest the moment it's in all three engines. No fallback needed just because it's recent. This is the default; the skill's `@scope`/`cqi`/relative-color usage assumes it.
- **Client projects** → same default, *but* when a feature is **both** recently-shipped **and** fails ungracefully, don't avoid it — **adopt the Baseline feature and ship a removable fallback**, then delete the fallback once the audience is fully on supporting browsers. The preference order:
  1. **Does it degrade gracefully if unsupported?** (The load-bearing question.) If yes, just gate it with `@supports`/`@media` and ship — the unsupported case no-ops.
  2. If it fails ungracefully (broken layout, a dialog that won't open), add an explicit fallback: an `@supports` alternative for CSS, or a feature-detect polyfill-lite for an HTML/JS API. Use the modern feature as the primary path; the fallback is the safety net for not-yet-updated browsers.
  3. Mark the fallback as removable (a comment) so it's deleted later, not carried forever.

  The point: a Baseline feature is *in* — use it. The only question is whether you also need a temporary fallback while the long tail catches up. Avoid a Baseline feature outright only when it's both very recent *and* the fallback would cost more than the feature is worth.

## Writing fallbacks — the `@supports` pattern

The policy above keeps saying "add an `@supports` fallback." Here's how, and when *not* to.

- **Baseline-first, then enhance.** Write the fallback as the default declaration; override it inside `@supports (feature)`. Don't put the modern value first and the fallback in a `not` block.
  ```css
  .button { color: var(--color-text-on-accent, oklch(99% 0 0)); } /* baseline */
  @supports (color: contrast-color(red)) {
  	.button { color: contrast-color(var(--color-accent)); }      /* enhance */
  }
  ```
- **Prefer positive tests over `@supports not (...)`.** Test for what you want and enhance; `not` is harder to read. (Reach for `not` only when the fallback genuinely needs its own logic that's awkward to express as a baseline.)
- **Don't reach for `@supports` when the cascade already handles it.** CSS ignores declarations it doesn't understand, so a single property-value override needs no feature query — just write both, old then new:
  ```css
  .panel { display: flex; display: grid; } /* old browsers keep flex, new ones take grid */
  ```
  Use `@supports` only when the fallback needs **coordinated/different logic** (several related changes at once), or to test something the cascade can't — a **selector**: `@supports selector(:open) { … }`.
- **Caveat:** `@supports` tests whether a declaration *parses*, not whether it works correctly — it can't detect a buggy partial implementation.

## Ask-first features (confirm before using)

Some features are fine to *know about* but shouldn't be reached for silently. Before using one, **surface it to Matt and get his go-ahead** — name the feature, why it's flagged, the concrete implication/caveat, and the fallback plan, then let him decide. This is a confirm-before-acting gate, not a ban (it mirrors the house "when in doubt, do less and ask" rule).

Flag a feature ask-first when any of these hold:

- **Very recent** — Baseline for the *current* year (e.g. Baseline 2026), so the support long tail is still wide.
- **Risky / misleading** — it looks like it solves a problem it doesn't fully solve, so an agent might adopt it and assume the problem is handled when it isn't.
- **Narrow** — only correct in a slice of cases and easy to misapply outside it.

Don't gate well-established Baseline features behind this — e.g. invoker commands (Baseline 2025, clean feature-detect fallback) are a normal use-with-fallback, not ask-first.

**Two flavors of ask — scale the warning to the actual risk:**

- **Recent-but-graceful → a light heads-up.** When the only trigger is recency and the feature degrades cleanly (the rule just no-ops in old browsers) with an easy wider-support fallback, the ask is short: "this is a 2026 feature, OK to use with an `@supports`/attribute fallback?" Usually an easy yes.
- **Risky / misleading → a loud warning.** When the feature can silently do the wrong thing, the ask must foreground the specific danger (the caveat), not just the recency.

Both still gate — Matt decides — but don't make a graceful new selector sound as scary as a misleading one.

**Current ask-first list:**

- **`contrast-color()`** *(risky)* — Baseline 2026 (very recent) *and* risky/misleading *and* narrow. Returns only black or white and **does not guarantee WCAG AA** — reliable only on near-black/near-white backgrounds; on mid-tones it can fail. Legit use: auto text color on a token-driven/dynamic background at the lightness extremes, with an `@supports` fallback. Before using: flag the AA caveat to Matt and confirm.
- **`:open`** *(recent, graceful)* — Baseline 2026 (newly available May 2026). The semantic state selector for native open/close elements (`<details>`, `<dialog>`, `<select>`/picker inputs) — preferred over `[open]` attribute selectors. Degrades cleanly (unsupported → rule no-ops); `details[open]`/`dialog[open]` or `@supports selector(:open)` is the wider-support fallback. Light heads-up before using, then it's usually a yes.
- **View-transition types (`:active-view-transition-type()`)** *(recent, graceful)* — Baseline 2026 (Jan). Extends the starter's `@view-transition` to vary the animation per navigation kind (forward/back). Degrades to instant navigation when unsupported. Two non-support caveats still apply: motion-gate it (`prefers-reduced-motion`) and keep it functional (directional orientation, not decoration). Light heads-up before adding.
- **`field-sizing: content`** *(recent, graceful)* — Baseline 2026 (June). Native auto-sizing for `<textarea>`/`<input>`/`<select>` — the no-JS replacement for textarea auto-grow. Degrades to normal fixed sizing when unsupported. Pair with `min`/`max` bounds; don't set a fixed `width`/`height`. Light heads-up. (Owned by safaii-html forms.)
- **`interpolate-size: allow-keywords` / `calc-size()`** *(experimental, graceful)* — animates `height`/size to/from intrinsic values (`auto`, `max-content`). **Chromium-only as of mid-2026 — not Baseline**, but *pure enhancement*: unsupported browsers just do an instant (non-animated) size change, never broken. Usable as progressive enhancement (motion-gated), with the single-engine reality flagged — not "not-ready" because it can't break. Pairs with `::details-content` for animating `<details>`.
- **`@property` (color animation)** *(narrow)* — Baseline 2024 (July), so not a recency flag; it's ask-first because it's easy to reach for as general animation license rather than the specific, restrained use it's meant for. Typed custom properties let oklch hue/lightness/chroma transition smoothly instead of snapping — legit use is a tasteful, brand-reinforcing micro-interaction (hover accent shift, logo hue drift), reviewed with Matt first per the skill's ask-first-animation rule — not decoration by default. Motion-gate it. Degrades to an instant snap if unsupported.

## Not ready yet (don't use in production)

A step earlier than ask-first. These are **pre-Baseline / experimental / unstable-syntax** features — don't ship them, even with a fallback, because the syntax you'd write today may not be the syntax that ships, and they don't work in most browsers. If asked for one, say it's not production-ready, explain why, and offer the current best stopgap. Revisit when it reaches Baseline.

**Current not-ready list:**

- **CSS masonry layout** — MDN: "Limited availability — not Baseline," experimental, with **active vendor disagreement on the syntax** (`grid-template-rows: masonry` vs `display: masonry` / `grid-lanes` vs `item-pack`). Don't write any of it yet; it silently falls back to a plain grid in ~every browser. **Stopgap when a project wants masonry:**
  - There's no production-ready native masonry today — say so. Then pick by whether true packing is actually the requirement:
  - **If the packing behavior is the point** (items must rise to fill gaps below short ones, Pinterest-style) → `columns` (CSS multicol) is the only CSS that does it. Caveat: it flows **top-to-bottom within each column**, which **breaks sequential reading order** — so use it *only* for non-sequential galleries, never for ordered content (a11y). Use `break-inside: avoid` to keep cards whole.
  - **If equal rows are acceptable** (you don't strictly need the pack) → the existing `auto-fit` grid: predictable, accessible, left-to-right order, no caveat.
  - Revisit `display: masonry`/`grid-lanes` when it's Baseline — it gives true packing *and* correct reading order.

## The graceful-degradation split

- **Enhancement-only features** (`prefers-reduced-motion`, `prefers-reduced-transparency`, `@view-transition`, `text-wrap`, `content-visibility`) — always safe. Gate them with `@media`/`@supports` and they no-op when absent. Use freely regardless of project.
- **Structural features** (`subgrid`, `@scope`, container queries, `oklch()`/`color-mix()`, relative color syntax, `light-dark()`) — fail loudly: broken layout, unstyled leaks, ignored/missing colors. These are the ones to vet against the policy above for client work.

## Verify at write-time

Today's date matters — a feature that's "newly available" in the snapshot may be solidly established now. Before relying on a borderline feature:

- **Baseline status:** https://webstatus.dev — or the Baseline badge on the feature's MDN page
- **caniuse:** https://caniuse.com/?search=<feature>
- **MDN reference:** https://developer.mozilla.org/en-US/docs/Web/CSS/<feature>

When unsure for client work, WebFetch one of these rather than trusting memory or this snapshot.

## Feature map — snapshot Jan 2026 (verify before client use)

| Feature | In all engines since | Degrades gracefully? | Notes |
|---|---|---|---|
| `@layer` | 2022 | n/a (foundational) | Safe everywhere. |
| Container size queries / `cqi` (`@container (inline-size > …)`) | 2023 | mostly (set a `rem` fallback min) | Use. The component-scoped query for discrete layout switches — prefer over `@media`. Intrinsic layout first. |
| Container **style** queries (`@container style(--x: y)`) | emerging, **no Firefox** | yes — query just doesn't match | Experimental, not yet a convention. `@supports`-guard if used. |
| Container **scroll-state** queries (`scroll-state(stuck:…)`) | experimental, early | yes | Skip. Too early. |
| `:has()` | late 2023 | depends on use | Safe now. |
| Trig functions (`sin()`/`cos()`/`tan()`/`atan2()`/…) | 2023 (March, widely available) | **no** — invalid value, declaration dropped | Use. Narrow but real: math-driven circular/radial layout without JS. Not a general calc()/clamp() replacement — reach for it only when the shape genuinely is angular. |
| `subgrid` | late 2023 | **no** — layout breaks | Used in the starter body grid. Established now, but the ungraceful kind. |
| `oklch()` / `color-mix()` | 2023 | **no** — invalid color ignored | Safe now; only ancient browsers need a hex fallback. |
| `color-gamut` media feature (P3 detection) | 2023 (Feb, widely available) | **yes** — query doesn't match, base sRGB value stands | Use. Wide-gamut escalation: sRGB-safe oklch as the base declaration, punch chroma up inside `@media (color-gamut: p3)`. No fallback logic needed — same pattern as the flex/grid cascade override. |
| `prefers-color-scheme` media feature | 2020 (widely available) | **yes** — query doesn't match, light value stands | Use. Ancient and safe; the `@media (prefers-color-scheme: dark)` remap-block dark-mode mechanism. |
| `prefers-reduced-motion` media feature | 2020 (Jan, widely available) | **yes** — query doesn't match, motion just plays | Use. The skill's single most-used gate — every animation/transition bullet wraps in `@media (prefers-reduced-motion: no-preference)`. Ancient and safe. |
| `hover` media feature | 2018 (Dec, widely available) | **yes** — query doesn't match, rule just doesn't apply | Use. Gates hover-only affordances so touch/no-pointer devices don't get a stuck `:hover` state. Ancient and safe. |
| `light-dark()` | 2024 (May, Baseline) | **no** — invalid at computed-value time; the property falls back to inherited/initial, not the light-mode color | Use, but pair with `color-scheme: light dark` on `:root` — the function does nothing without it. The per-token dark-mode mechanism; needs a hex/oklch fallback only for pre-2024 engines if a project must support them. |
| `@scope` | mid-2024 | **no** — styles leak / don't apply | Use where it earns its place — a `to (…)` boundary, or the lower specificity — never as a blanket mandate. On conservative client work the fallback is plain descendant selectors: the same styling with wider support. |
| Relative color `oklch(from …)` | mid-2024 | **no** | Newly available; pairs with `@scope` in age. |
| Popover API | 2024 | needs fallback | Enhancement; vet for client work. |
| `@view-transition` (MPA) | mid-2024 | **yes** — no transition | Safe as enhancement (starter ships it). |
| `text-wrap: balance` / `pretty` | 2023–24 | **yes** — normal wrapping | Safe; `pretty` still missing in some engines. |
| `prefers-reduced-transparency` | 2023–24 | **yes** — no enhancement | Safe; already gated in the conventions. |
| `content-visibility` + `contain-intrinsic-size` | 2023 | **yes** — renders normally (perf only) | Use *as a pair*. CV-auto alone collapses off-screen content → scrollbar jump; `contain-intrinsic-size: auto <len>` gives the estimate. Starter pairs them on `article`. |
| Invoker commands (`command`/`commandfor`) | 2025 (Chrome/Edge 135, FF 144, Safari 26.2) | **no** — button does nothing, dialog won't open | HTML/JS, not CSS. Baseline newly available; use with a removable feature-detect fallback (see safaii-html). |
| `contrast-color()` | 2026 (very recent) | partial — falls back to default `color` | **Ask-first (risky).** Black/white only, NOT a WCAG AA guarantee; reliable only on near-black/near-white bg. Use with `@supports` fallback; confirm with Matt first. |
| `:open` | 2026 (May, newly available) | **yes** — rule no-ops if unsupported | **Ask-first (recent, graceful).** Native open-state selector for `<details>`/`<dialog>`/`<select>`. Fallback: `[open]` attribute selector or `@supports selector(:open)`. Light heads-up before use. |
| View-transition types (`:active-view-transition-type()`) | 2026 (Jan) | **yes** — instant navigation if unsupported | **Ask-first (recent, graceful).** Per-navigation-kind animation on top of the starter's `@view-transition`. Still motion-gate + keep functional. Light heads-up. |
| `field-sizing: content` | 2026 (June) | **yes** — normal fixed sizing if unsupported | **Ask-first (recent, graceful).** No-JS auto-sizing for form fields. Pair with min/max bounds. Owned by safaii-html forms. Light heads-up. |
| `::details-content` | 2025 (Sept) | **yes** — default panel styling if unsupported | Use. Targets the open `<details>` panel; animate with `content-visibility … allow-discrete`. Motion-gate. |
| `interpolate-size` / `calc-size()` | Chromium-only (not Baseline) | **yes** — instant size change if unsupported | Progressive enhancement only. Animate `height` to `auto`. Single-engine for now; motion-gate. Not "not-ready" (can't break). |
| Scroll-driven anim (`animation-timeline: scroll()/view()`) | Chrome/Edge 115 (2023), Safari 26 (Sept 2025); Firefox still flagged in stable, ships ~v155 (Sept 2026) | **yes** — no animation if unsupported | **Use as gated enhancement, through the scroll-driven-animation skill** (re-triaged 2026-07; the old "Skip — no Safari" is stale). Double-gate `@supports (animation-timeline: …)` + `prefers-reduced-motion`; Firefox no-ops to the static document until ~155. Every use runs scroll-driven-animation's propose→approve flow — the ask-first animation rule as procedure; recipes in that skill's `references/patterns.md`. |
| `:user-valid` / `:user-invalid` | 2023 (widely available) | **yes** — falls back to `:valid`/`:invalid` | Use. Form validation styling *after* user interaction. (safaii-html forms.) |
| `inert` attribute | 2023 (widely available) | partial — subtree stays interactive if unsupported | Use. Non-interactive subtree (offscreen nav, custom overlay bg). Pair with visible styling. (safaii-html.) |
| `<search>` element | 2023 (widely available) | **yes** — generic element if unsupported | Use. Native `search` landmark; replaces `role="search"`. (safaii-html.) |
| `@starting-style` | 2024 (Aug) | **yes** — no entry animation if unsupported | Use, gated. Entry animations for popover/dialog/`<details>`. Motion-gate. |
| `transition-behavior: allow-discrete` | 2024 (Aug, same wave as `@starting-style`) | **yes** — discrete property just snaps instantly, no mid-transition visibility | Use, gated. Exit-animation half of the entry/exit pair — keeps `display`/`overlay` visible until the transition finishes. Must be paired with the property named explicitly in `transition-property`; the `transition: all` shorthand doesn't pick up discrete properties. Motion-gate. |
| `text-box-trim` / `text-box-edge` | Chromium-only (not Baseline) | **yes** — default leading if unsupported | Experimental, graceful (like `interpolate-size`). Optical text trim; guard with `@supports`. Single-engine for now. |
| `hanging-punctuation` | Safari-only (not Baseline, stagnant) | **yes** — normal punctuation if unsupported | **Skip.** Safari-only for ~a decade, marginal nicety. Harmless as a Safari-only flourish, but not a house convention. |
| `initial-letter` | Chrome/Safari (`-webkit-`), **no Firefox** | **yes** — normal letter if unsupported | Experimental-graceful. Native drop caps; give a `::first-letter` font-size fallback for Firefox. Needs `-webkit-` prefix. |
| `line-clamp` (`-webkit-box` trio) | all engines (prefixed, spec-permanent) | **yes** — untruncated text if unsupported | Use. Multi-line truncation; the one sanctioned `-webkit-` prefix. Text stays in DOM (SR reads all). |
| `scroll-margin` / `scroll-padding` | 2021 (widely available) | **yes** — no offset if unsupported | Use. `scroll-padding-block-start` on `:root` fixes anchor-under-sticky-header. |
| `scrollbar-gutter` | 2024 (Dec) | **yes** — classic `auto` shift if unsupported | Use. `stable` on `:root` reserves scrollbar space, stops the jump (cuts CLS). |
| `scrollbar-color` / `scrollbar-width` | 2025 (Dec) | **yes** — default scrollbar if unsupported | Dark-mode footnote only (match scrollbar to a dark theme). A11y: ≥3:1 thumb/track contrast, avoid `thin`/`none`, auto-resets in forced-colors. Light ask-first. |
| `hidden="until-found"` | recent, Chromium-led (not Baseline) | **yes** — plain `hidden` if unsupported | Use for *custom* findable collapsibles (prefer `<details>`). Degrades to hidden-but-not-findable. |
| `@property` | 2024 (July, Baseline) | **yes** — untyped variable if unsupported | **Ask-first (narrow).** Typed custom props enable smooth oklch color transitions (hue/lightness/chroma drift) for a tasteful, brand-reinforcing micro-interaction — one instance of the skill's ask-first-animation rule, not general animation license. Confirm the specific use with Matt; motion-gate it. |
| `@function` (CSS custom functions) | Chromium-only (not Baseline) | **no** — declaration using it drops | **Skip** (re-confirmed). Single-engine, and parameterized reusable functions are redundant with plain custom properties + `calc()`/`clamp()`/`color-mix()` for our token approach. Considered earlier for fluid spacing → skipped. Revisit if it reaches Baseline *and* a real need appears. |
| `clip-path` | 2020 (widely available) | **yes** — element shows unclipped | **Skip as decoration** (shaped images, diagonal cuts — against the minimal ethos; reach for it per a specific design, not a convention). Its one *functional* use — `clip-path: inset(50%)` in the `.sr-only` recipe — is documented in safaii-html. |

When this snapshot is clearly old (months past Jan 2026) and a client decision hinges on a borderline row, re-verify rather than trust it.
