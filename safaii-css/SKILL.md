---
name: safaii-css
description: Safaii Studio CSS conventions and starter stylesheet. Use whenever writing CSS, creating a stylesheet, scaffolding a new site (11ty/Rails), or styling components — every project starts from the same starter and follows the same patterns.
---

# safaii-css

How Safaii Studio writes CSS.

**Source of truth:** this skill and `references/starter.css`, together. `starter.css` is canonical for the stylesheet itself — tokens, layer order, scope patterns. This `SKILL.md` is canonical for everything not expressible as CSS — process, rules, and the Checks — and points at `starter.css` rather than restating its values, so the two can't drift apart. Both are version-controlled and machine-checkable; edit them directly.

The Basecamp doc "Frontend Conventions" (Lab project 46824335, doc 9768197742 — one combined overview also covering [[safaii-html]]) is a **derived, human-readable view** — refresh it from this skill when convenient. Its lag is cosmetic, not functional; you never have to update it first to change a rule.

## Process

### New static site (11ty)
1. Copy `references/starter.css` as the project's stylesheet (one file, usually `css/style.css`).
2. Fill in `config`: project palette (oklch only), project fonts. Keep the token names `starter.css` ships with (`--gutter`, `--stack`, `--measure`, `--radius`, `--color-*`) — that file is the canonical list; don't maintain a parallel one here.
3. Style elements before inventing classes — the page must work as a styled document first. But element-first applies to *default document elements* (`h1`, `p`, `a`, `button`'s baseline). An **opt-in visual variant** — a filled brand button among ghost/secondary/icon buttons, a callout, a card — earns a class; don't dissolve it into a bare element selector, which would restyle every instance and change selector semantics. When refactoring, preserve the original selector's contract (a `.button` class stays a class) unless told otherwise.
4. Add components only when a pattern can't be expressed on bare elements. Each one uses `@scope` *if it has descendant rules*; a single-rule variant on its root class stays a plain rule.
5. Run the Checks before calling it done.

### Rails apps
Same layers, same rules, different file layout: Propshaft loads every file in `app/assets/stylesheets/`, so split by concern instead of one file — `config.css` (the `@layer` declaration + tokens), `reset.css`, `elements.css`, then one file per component (`flash.css`, `dialog.css`, `inputs.css`, `nav.css`). The `@layer` declaration keeps the cascade order correct regardless of file load order. App components (flash, dialog, inputs) live in the `components` layer and use `@scope` like everything else. Skip the starter's body grid — app layout is its own decision, not the document grid.

### Existing project
Don't restructure working CSS uninvited. New styles follow the conventions; flag (don't fix) existing violations.

## Rules

- **Vanilla CSS only.** No Tailwind, no CSS-in-JS, no preprocessors, no utility-class systems.
- **One declaration order:** `@layer config, reset, elements, components;` — first thing after fonts/keyframes.
  - `config` — custom properties and `@view-transition` only. No selectors styling elements.
  - `reset` — the minimal reset from starter.css. Resist additions.
  - `elements` — bare HTML elements. This is where most of the stylesheet lives.
  - `components` — the few classes that earn their existence.
  - `utilities` — appended (fifth, last) only when the project needs one-off utility classes like `.sr-only` (canonical visually-hidden recipe in [[safaii-html]]) or `.bleed`; last so a utility beats component styles. Utility-class *systems* stay banned.
- **Components use `@scope`.** Scope to the component root instead of prefixing every selector with the component class; use `@scope (...) to (...)` to stop at nested component boundaries. Style the root via `:scope`. A component that is a single rule on its root class (no descendant rules) stays a plain rule — don't wrap it pointlessly.
- **Colors are oklch.** Custom properties in `config`; derive muted variants with `color-mix(in oklch, ...)`, not new hex values or opacity. Converting inherited hex/rgb/hsl **and named colors** (`white`, `black`, `tomato`, …, — actual color literals, just spelled as words) to oklch (a legacy-CSS refactor): convert the color values and leave everything else alone — don't restructure the CSS around it. **Leave untouched — these aren't color literals:** the functional CSS keywords `currentColor`, `inherit`, `initial`, `unset`, `transparent`. Also leave a gradient's function/interpolation method alone (convert only its color *stops*), and anything in a third-party library config that specifically expects a hex string.
- **Chroma ranges as a sanity check, not a hard limit.** Max in-gamut chroma varies by hue — yellows/cyans tolerate more than reds/blues at the same lightness — but as rough bands: neutrals ~0–0.10, sRGB-safe saturated colors ~0.20–0.32, wide-gamut-only ~0.32–0.40. DevTools flags out-of-gamut oklch values directly; trust that over the bands when they disagree.
- **Wide gamut via Display P3** (graceful enhancement). Declare the sRGB-safe oklch value as the base, then raise chroma behind `@media (color-gamut: p3)` for capable displays — same lightness and hue, just more saturated:
  ```css
  .button-primary { background: oklch(0.52 0.26 264); }
  @media (color-gamut: p3) {
    .button-primary { background: oklch(0.52 0.36 264); }
  }
  ```
  Non-P3 displays just render the base value — no fallback logic needed. Reach for this only where a brand color genuinely benefits from the extra vividness (hero accents, primary CTA), not across the whole palette.
- **Color animation via `@property`** (ask-first, project-dependent). Untyped custom properties snap between values instead of transitioning — a typed `@property` declaration lets a single channel (hue, lightness, chroma) interpolate smoothly on its own:
  ```css
  @property --hue {
    syntax: '<number>';
    inherits: false;
    initial-value: 250;
  }
  .brand-mark {
    background: oklch(var(--lightness) var(--chroma) var(--hue));
    transition: --hue 0.4s var(--easing-base, ease);
  }
  ```
  **Check first whether a plain `transition` already does the job.** A `transition: color 0.2s` between two full `oklch()` values already interpolates smoothly across lightness, chroma, *and* hue natively — no `@property` needed, and no JS. `@property` earns its complexity only when something a plain two-endpoint color transition genuinely can't do is actually needed: the channel value read or computed elsewhere, or a hue journey with real, visible range (a multi-stop arc, an overshoot big enough to see) — not a fixed hover-state swap between two named tokens, which a plain transition already handles. Built and measured on `mattsafaii`'s masthead hover: the `@property` version's only actual delta over the existing plain crossfade was a ~0.4° hue overshoot (invisible) and 3x the duration (200ms → 600ms, reads as slower, not premium) — reverted, nothing gained. Verify the same way before shipping: measure the actual behavioral difference against the plain-transition baseline, don't assume typing the property automatically improves on it.

  This follows the general ask-first-animation rule below — reserve it for a specific, tasteful brand-reinforcing micro-interaction that a plain transition genuinely can't produce, bring that idea to Matt to review before building it, and gate it under `prefers-reduced-motion` like any other motion. Baseline 2024 (all engines); degrades to an instant snap if unsupported.
- **Font-relative units.** Spacing is a fixed rem scale on a 4px grid (`--space-1`…`--space-16`, where the number is px÷4); `--measure` for line length. The semantic tokens `--gutter` (inline) and `--stack` (block) are fluid but **bounded by scale steps** — `clamp(var(--space-4), 2.5vmax, var(--space-6))` — so spacing rides between grid stops and never leaves the system; anything needing an exact value uses `--space-*` directly. Derive spacing from the tokens via `calc()`, not magic numbers. Corner radius is a small rem scale (`--radius-sm`/`--radius`/`--radius-lg`), not literal `px`. For a rounded element nested inside another (an inset image in a rounded card), don't reuse the outer radius — concentric corners need `inner = outer − gap`, where the gap is padding + border + spacing: `border-radius: calc(var(--radius-lg) - var(--gutter) - 1px)`. Write the formula from tokens so it holds when spacing changes; then trust your eye for a ±1–2px nudge. (The formula assumes round corners; `corner-shape` squircles don't offset cleanly — eyeball those.) Relative units everywhere — the only `px` exceptions are `border-width` and `outline-width`, where hairlines and focus rings should stay crisp at any zoom.
- **Spacing rhythm of three.** Reach for scale steps by nesting level, not by eye: ~`--space-2` (8px) *within* a group, ~`--space-4` (16px) *between* groups, ~`--space-8`–`--space-10` (32–40px) *between* sections. Keeps vertical rhythm legible without per-element fiddling; `--stack` (≈12–16px) already sits at the between-group level for document flow.
- **Fluid type with `clamp()` + `cqi`.** For headings/display text that should scale with available space, use `clamp()` with `cqi` (1% of the container's inline size) as the ideal value and a `rem` minimum so the hierarchy survives 200%+ zoom: `font-size: clamp(1.25rem, 5cqi, 3rem)`. `cqi` responds to the element's container, not the viewport, so type scales right inside a narrow column on a wide screen — but the parent must set `container-type: inline-size`. Fall back to `vb` only when there's genuinely no containment context.
- **Optical text trimming — `text-box-trim` / `text-box-edge`** (experimental, graceful). Trims the font's half-leading above caps / below the baseline so text optically centers in buttons/badges and headings align precisely: `text-box: trim-both cap alphabetic`. Chromium-only as of mid-2026 — *pure enhancement*, so guard it with `@supports (text-box-trim: trim-both)` and keep your normal spacing as the baseline; non-supporting browsers just keep the default leading. Use it to remove fiddly magic-number padding, not as load-bearing layout.
- **Drop caps — `initial-letter`** (experimental, graceful). Native sunk initial for an essay/article opening: `p:first-of-type::first-letter { -webkit-initial-letter: 3 2; initial-letter: 3 2; }`. **Firefox doesn't support it**, so it's pure enhancement — give a plain `::first-letter { font-size; font-weight }` baseline so Firefox shows an enlarged (not sunk) letter; supporting engines get the real drop cap. Needs the `-webkit-` prefix.
- **Multi-line truncation — `line-clamp`** (the `-webkit-box` trio). To clamp a card excerpt/teaser to N lines with an ellipsis, use the broadly-supported, spec-permanent set: `display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden;`. This is the one sanctioned `-webkit-` prefix use — it works in every engine and MDN confirms it stays supported. (The full text remains in the DOM, so screen readers still read all of it — the clamp is visual only.)
- **Platform primitives first.** Before writing a component ask: does an element, pseudo-class, or modern CSS feature already do this? (Popover API over JS lightboxes, `:has()` over state classes, `<details>` over toggles.) Same for state styling: select on ARIA attributes (`[aria-expanded]`, `[aria-current="page"]`, `[aria-invalid]`) instead of inventing modifier classes. For elements with a *native* open state (`<details>`, `<dialog>`, `<select>`/picker inputs), the `:open` pseudo-class is the semantic hook — `details:open > summary { … }` — over `[open]` attribute selectors or classes. `:open` is **ask-first (recent, graceful)**: Baseline 2026, so confirm before using, but it degrades cleanly (unsupported → the rule no-ops) with `details[open]`/`dialog[open]` or `@supports selector(:open)` as the wider-support fallback.
- **Gate enhancements:** `@media (prefers-reduced-motion: no-preference)` around motion, `@media (hover)` around hover-only affordances, `@media (prefers-reduced-transparency: no-preference)` around translucent/backdrop-blur effects.
- **View transitions.** The starter ships `@view-transition { navigation: auto }` — a subtle cross-page fade on MPA navigation, on by default. To vary the animation by navigation kind, use **view-transition types**: label the transition (`forward`/`back`) via the `pageswap`/`pagereveal` events, then style per type with the `:active-view-transition-type(forward)` pseudo-class over `::view-transition-old/new`. Two rules bite: typed animations are motion, so **gate them** (zero `::view-transition-group(*)` duration under `prefers-reduced-motion`), and the animation-off-by-default rule still applies — use types for **directional orientation** (forward/back aids spatial sense), not a decorative flip on a document site. Ask-first (recent, graceful): Baseline 2026, degrades to instant navigation when unsupported — light heads-up before adding, no JS animation library.
- **Entry & exit animations — `@starting-style` + `transition-behavior: allow-discrete`** (both Baseline 2024). The native way to animate an element *in and out* of the top layer (popover/dialog open/close, `<details>` reveal) with no JS, no library, and no class-toggle/`setTimeout` choreography:
  - **Entry** — `@starting-style` defines the from-state; place it *after* the open-state rule and the browser transitions from it automatically on first render.
  - **Exit** — `display`/`overlay` are discrete (they flip, they don't interpolate), so add `transition-behavior: allow-discrete` to keep the element visible and painted until the rest of the transition finishes, instead of vanishing the instant `display: none` applies.
  - **Gotcha:** the `transition: all 0.3s` shorthand does **not** pick up discrete properties. List `display`/`overlay` explicitly in `transition-property` (or its own declaration) alongside `transition-behavior: allow-discrete` — leaving it to the shorthand is the most common way this silently fails to animate.
  - Same motion rules apply as any animation — gate it under `prefers-reduced-motion` and keep it subtle/functional. Both degrade cleanly (no unsupported browser sees anything worse than an instant show/hide).
  - Scope: this covers basic show/hide entry-exit. Complex sequencing, scroll-driven choreography, or physics-based motion is still a JS problem — don't stretch these two properties past what they're for.
- **Logical properties** (`margin-block`, `inline-size`, `padding-inline`) over physical ones — and prefer the logical longhands over the 2-value `padding`/`margin` shorthand too: write `padding-block: var(--space-2); padding-inline: var(--space-4)`, not `padding: var(--space-2) var(--space-4)`, so block/inline intent is explicit. The bare `padding`/`margin` shorthand is fine only for symmetric resets to `0` (as in the reset layer).
- **Scroll paper-cuts (CSS, no JS).** Two mature fixes worth defaulting to: (1) **anchor under a sticky header** — set `scroll-padding-block-start` on `:root` to the header's height so `#anchor` links and `:target` land *below* the fixed header, not behind it (per-target override: `scroll-margin-block-start`). (2) **scrollbar layout shift** — `scrollbar-gutter: stable` on the scroll container (usually `:root`) reserves the classic-scrollbar space so content doesn't jump horizontally when the bar appears (also cuts CLS). Both degrade cleanly; Baseline (2021 / 2024).
- **`content-visibility: auto` always pairs with `contain-intrinsic-size`.** Skipping off-screen rendering is a real perf win, but alone it collapses off-screen elements to zero and the **scrollbar jumps** as you scroll (CLS). Always give a size estimate: `contain-intrinsic-size: auto <length>` — the `auto` makes the browser remember the real size after first render, so the length is just an initial guess (use `auto none` instead inside grid/multicol, where `0` would overflow). The starter already pairs them on `article`; keep them together anywhere you add `content-visibility`. Both Baseline 2023.
- **Media fitting — `aspect-ratio` + `object-fit`.** For an image that must fill a fixed box without distorting (card thumbnails, avatars, hero crops), give the box an `aspect-ratio` and set the `<img>` `object-fit: cover` (`object-position` to steer the crop) — the image crops instead of squashing. For a ratio-locked embed (16:9 video/iframe), put `aspect-ratio: 16 / 9` on the wrapper. Still also set the `<img>`'s `width`/`height` attributes (per safaii-html) so the intrinsic ratio reserves space before load. Both Baseline, mature.
- **Animation: off by default, ask-first when it earns its place.** Minimal by default — most animation on the web is decoration for its own sake (full-bleed hero pieces, 3D showpieces, attention-grabbing reveals) that distracts from the copy/content, costs performance, and can drive a visitor to bounce. The test isn't "does it look impressive," it's "does removing it lose something the visitor needed." Legitimate reasons, still ask-first and never assumed by default: **UI/UX** — easing a state change that would otherwise feel jarring, a loading state so a wait doesn't read as broken; **branding/ambiance** — a subtle, tasteful touch that reinforces identity without competing for attention (`@property` color micro-interactions above are one instance of this, not the only one). Bring the specific idea to Matt to review together before building it — this skill doesn't add animation on its own judgment. **This holds regardless of how the request is phrased** — a direct instruction to add a specific animation doesn't skip the review step any more than a hedged "should we add...?" does; naming the exact technique isn't the same as approving it. Keep the check-in itself proportionate to the ask-first calibration already used elsewhere (a light one-line confirmation for an obviously-tasteful, on-model case; more discussion for anything closer to the line) — this is a design-review moment, not a permission gate to route around. Real example: `mattsafaii`'s footer **ouroboros colophon mark** (`~/Code/personal/mattsafaii/src/css/style.css`, `@scope (.colophon)`, `slow-spin` keyframe) rotates continuously but at `120s linear infinite` — one full turn every two minutes, imperceptible as motion in the moment, felt only as a slow-burn ambient detail. It's also symbolic rather than decorative (the site's AGENTS.md: the mark represents the site's own content cycle, formless-to-tangible-and-back) — the ambient-lighting case from Matt's retail-store analogy. **A passing-the-review-gate isn't the same as passing the value bar.** A homepage masthead ink-pour entrance and a hover color-shift micro-interaction were both proposed, reviewed, and greenlit under this exact rule, then built and honestly tested — the ink-pour was killed on a real perf problem (Chrome freezes from a heavier filter variant), and the hover color-shift was killed after live measurement showed its actual delta over a plain oklch crossfade was a ~0.4° hue overshoot (invisible) plus 3x the duration (reads as slower, not better). Both reverted cleanly, nothing shipped. The lesson: review-and-build isn't the finish line — verify the built thing actually earns the animation budget it spent, and revert without ceremony when it doesn't.
- **Motion craft, once something's approved.** The ask-first gate above decides *whether* to animate; these rules decide whether the approved animation reads as crafted or cheap:
  - **Easing over duration.** The easing curve, not the duration, is what separates cheap from crafted motion. Beyond the `ease`/`ease-in-out` defaults, a custom `cubic-bezier()` signals intent: snappy entrance `cubic-bezier(0.22, 1, 0.36, 1)`, spring/overshoot `cubic-bezier(0.34, 1.56, 0.64, 1)` (y > 1 overshoots past the target before settling), anticipation/pullback `cubic-bezier(0.36, 0, 0.66, -0.56)` (negative y pulls back before moving forward). Match the curve to the meaning of the motion, not just the trend.
  - **Duration as weight.** Longer reads as heavier/more significant; keep it proportional to what's happening: ~50–100ms micro-interactions (a checkbox, a toggle), ~150–300ms ordinary UI transitions (the skill's default motion tokens sit here), ~300–500ms layout changes, 500ms+ reserved for a genuinely cinematic moment (rare, and still ask-first per the rule above).
  - **Stagger via a custom property, not N hand-written delays.** `animation-delay: calc(var(--i) * 60ms)` with `--i` set per item (inline style or `:nth-child` via `@property`-free counting) scales to any list length without writing a delay per element. Direction carries meaning: top-to-bottom follows reading order, center-outward emphasizes hierarchy — pick deliberately, don't default to whichever is easiest to write.
  - **`animation-fill-mode: both` on anything with a delay.** Without it, a staggered/delayed entrance flashes in its final state before the delay elapses, then jumps back to the start state when the animation begins — `both` holds the pre-animation state through the delay and the post-animation state after it finishes. Treat this as required, not optional, on any staggered entrance.

## Color tokens

The starter is `color-scheme: light` — **light-only by default is deliberate**, not an oversight. Brand colors are declared explicitly, so dark mode is a conscious opt-in, not something to switch on reflexively with `color-scheme: light dark`.

When you *do* opt into dark mode, the mechanism is `light-dark()` per semantic token plus a `color-scheme` switch — define each token once, let the browser pick: `--color-bg: light-dark(oklch(98% 0 0), oklch(15% 0 0));`. Set `color-scheme: light dark` on `:root` to follow the system, or toggle explicitly with `[data-theme="light"]{color-scheme:light}` / `[data-theme="dark"]{color-scheme:dark}`. No token values get repeated — flip lightness, keep chroma and hue. As a starting point, a fixed **+0.10–0.15 L offset** (dark value = light value + offset, chroma/hue held constant) reads as equivalent visual weight against the opposite background — formula first, then adjust by eye if a specific hue looks off.

Optional dark-mode polish: a default OS scrollbar can look mismatched on a dark page — set `scrollbar-color: <thumb> <track>` on `:root` from your semantic tokens so it matches (Baseline 2025, graceful → default scrollbar when unsupported; light ask-first). A11y caveats: keep thumb/track at **≥3:1** contrast, don't reach for `scrollbar-width: thin`/`none` (hurts usability), and note it auto-resets under `forced-colors` (correct — leave it). It's a footnote to dark mode, not a default; light-mode sites leave scrollbars alone.

`light-dark()` only swaps a single value per property, so it covers token-level color swaps but not rules that need real logic (swapping a background image, changing a shadow recipe, disabling an effect entirely). For those, fall back to a `@media (prefers-color-scheme: dark)` block instead — it can hold any declaration, not just a two-way color pick. Same `color-scheme` switch drives both; use `light-dark()` by default and only reach for the media query when a rule outgrows a value swap.

Two sizes, both in the `config` layer:

- **Small palette** (most personal/document sites): just the semantic tokens — `--color-bg`, `--color-text`, `--color-accent`. This is what starter.css ships with; add muted variants via `color-mix()` only once a component actually needs one, rather than pre-declaring them as tokens.
- **Bigger palette** (client work): three layers — primitives, semantics, and an optional dark-mode remap.
  - **Layer 1 — Primitives:** a named neutral ramp (`--base-50` … `--base-950`, plus named endpoints like `--cream`/`--paper`/`--ink`) and named accents (`--primary`, `--yellow`, …). If the project ships dark mode, give at least the accents a dark-side primitive too (`--primary-dark`, built with the +0.10–0.15 L offset above) — that's the raw material layer 3 remaps into.
    - **Generating a ramp — formula, not hand-tuning.** Steps `50/100/200/300/400/500/600/700/800/900/950`, **lightness** decreasing in roughly uniform steps end to end, **hue held constant** throughout. **Chroma tapers differently by ramp type:**
      - **Neutral ramp** (the common case — `--base-*`, what actually ships): chroma stays low the whole way (inside the neutral band above) and *gently increases* toward the dark end, rather than peaking mid-ramp — a flat `C: 0` reads as dead/grey, so the warmth (or coolness) has to survive into the dark steps or the ramp goes muddy at the bottom. Reference ramp, warm neutral (hue 75 — this is `mattsafaii`'s actual background hue; `konnectedconcepts` sits at hue 78, "cream to ink"):
        ```css
        --base-50:  oklch(0.97 0.005 75);
        --base-100: oklch(0.93 0.006 75);
        --base-200: oklch(0.86 0.007 75);
        --base-300: oklch(0.76 0.008 75);
        --base-400: oklch(0.64 0.010 75);
        --base-500: oklch(0.52 0.012 75);
        --base-600: oklch(0.42 0.015 75);
        --base-700: oklch(0.34 0.020 75);
        --base-800: oklch(0.26 0.028 75);
        --base-900: oklch(0.18 0.038 75);
        --base-950: oklch(0.12 0.050 75);
        ```
        (`mattsafaii`'s real `--color-bg: oklch(94.5% 0.009 75)` sits almost exactly at step `100`/`200` here — this isn't a hypothetical, it's close to what's already in production.)
      - **Accent ramp** (`--primary`, `--yellow`, a named brand color): chroma *does* peak mid-ramp instead, tapering at both extremes — up into the sRGB-safe band above (~0.20–0.32) at the middle steps, down toward the light/dark extremes, because those clip out of gamut fast. Same lightness progression and constant-hue rule as the neutral ramp; only the chroma curve's shape changes.
      
      Retargeting a ramp to a different brand hue is a hue-angle swap — every L/C value carries over unchanged, no per-hue recalibration.
    - **Multiple accents, one formula (the multi-brand technique).** When a project needs several equally-weighted accent tokens — status colors, secondary brand accents, or reskinning the same template for a different client — hold **L fixed and vary H**, but hold **chroma as a percentage of each hue's own max chroma, not a flat absolute number**. Different hues have very different max chroma at the same lightness — at L 0.5 in sRGB, purple's ceiling (~0.29) is over 3x cyan's (~0.09) — so a flat absolute C reads vivid on one hue and washed-out on another, where the same C *percentage* of each hue's own ceiling reads as consistent vividness, because oklch L is perceptual. This matters most at mid-lightness, where max chroma diverges most across hues — it matters far less near the light/dark extremes, where every hue's ceiling converges lower anyway. konnectedconcepts's status colors (`L 0.55, C 0.14`, hue varies) are a reasonable approximation, not a precise application of this rule — verify per-hue in DevTools when accents sit at a mid-range lightness like that one does. Same idea for a subtle-tint row across named accents, where the light `L` already keeps every hue's ceiling low and close together so a flat C is safer:
      ```css
      --brand-subtle-blue:   oklch(0.96 0.02 250);
      --brand-subtle-teal:   oklch(0.96 0.02 195);
      --brand-subtle-violet: oklch(0.96 0.02 295);
      ```
      For a template that gets reskinned across clients, this generalizes further: parameterize hue off one custom property (`--color-accent: oklch(0.55 0.16 var(--brand-hue));`) so every accent's L stays fixed and a full reskin is a single-value change — but re-verify chroma per reskin rather than assuming `0.16` stays equally vivid and in-gamut across every possible brand hue.
      - **Escalation — relative-recipe ramps (when N brand colors each need a full ramp, not just one shade).** The techniques above cover one flat token per brand hue. When a project needs the *entire* 11-step ramp for an arbitrary and possibly-growing number of source colors — a shared template reskinned per client, each getting its own full tint/shade system — hand-tuning an 11-step absolute ramp per hue (the primitives technique above) doesn't scale: it's real design work, repeated per client. Relative color syntax lets the step *recipes* be written once, as fragments relative to whatever source they're later applied to, so a new brand color is a single line that gets the full ramp for free:
        ```css
        /* recipes — written once; c and h resolve to whatever source is plugged in */
        --tint-50:  97% calc(c / 12) h;
        --tint-100: 94% calc(c / 5) h;
        --tint-200: 88% calc(c / 2.5) h;
        --tint-300: 76% calc(c * 0.6) h;
        --tint-400: 64% calc(c * 0.8) h;
        --tint-500: 52% c h;                 /* peak — the source's own natural chroma, unscaled */
        --tint-600: 42% calc(c * 0.9) h;
        --tint-700: 34% calc(c * 0.75) h;
        --tint-800: 26% calc(c / 2) h;
        --tint-900: 18% calc(c / 3) h;
        --tint-950: 12% calc(c / 6) h;

        /* each source color is one line, and gets the whole ramp instantly: */
        --primary: oklch(52% 0.24 250);
        --client-acme: oklch(55% 0.20 140);
        /* used as: oklch(from var(--primary) var(--tint-800)) */
        ```
        This tapers chroma down at *both* extremes — near-zero at `50`/`950`, peaking unscaled (`c`, no division or multiplication) at `500` — mirroring the same taper shape as the hand-tuned accent ramp above, just expressed as ratios of the source's own chroma instead of absolute numbers. That taper is the part that matters: a version that only scales down the very ends and uses the source's *full* chroma across the middle steps (light through mid-dark) will clip out of gamut for any reasonably saturated source, because sRGB's chroma budget shrinks fast near white. Treat these ratios the same as the absolute ramp — a starting curve to verify in DevTools per real source color, not gospel. Same opt-in bar as everything else here: reach for this only once a real multi-ramp need exists, not preemptively.
  - **Layer 2 — Semantic tokens** built from the primitives, grouped by purpose: backgrounds (`--color-bg`, `--color-bg-card`, `--color-bg-dark`), text with muted/faint steps and `-invert` variants for dark sections, borders (`--color-border`, `--color-border-hover`, `--color-border-active`), accents (`--color-accent`, `--color-link`), status (`--color-success/warning/error`).
  - **Layer 3 — Dark-mode remap** (opt-in — same rule as above: a conscious choice, not a default). Same semantic names, different primitives underneath; nothing downstream changes, only which primitive a token resolves to. Two ways to wire it — pick per project, not both:
    - **`light-dark()` per token** (default — composes with the `[data-theme]` manual-toggle pattern above): `--color-brand: light-dark(var(--primary), var(--primary-dark));`
    - **When a full ramp exists (Layer 1), pick a mirrored step instead of computing an offset.** The +0.10–0.15 L-offset heuristic above computes a *new* value per token. If a ramp already exists, skip the computation — just point dark mode at a different, already-tuned step from the same ramp. With the absolute `--base-*` ramp, that's a direct swap, no relative color needed (each step is already a complete color): `--color-text: light-dark(var(--base-800), var(--base-100));`. With the relative-recipe `--tint-*` ramp, wrap both in `oklch(from <source> …)` since the steps are fragments, not colors: `--color-text: light-dark(oklch(from var(--primary) var(--tint-800)), oklch(from var(--primary) var(--tint-100)));`. The hard part (evenly-spaced, perceptually tuned lightness steps) was already done once when the ramp was built; reusing an existing far step is free, where the offset heuristic redoes a small piece of that work per token. It's not an exact mathematical mirror (the ramp's steps aren't symmetric around precisely 50% L) — "an appropriately-far existing step in the other direction" is good enough.
    - **The L-offset heuristic still applies, and still has a place** — it isn't replaced, just no longer the only option: (1) it's the *only* mechanism for the small-palette tier, which has no ramp to pick a step from; (2) relative color syntax gives it a cleaner form even where a ramp exists — the bare `l` keyword inside `oklch(from <source> ...)` refers to the source's own native lightness, so the offset can be written directly against it, `oklch(from var(--primary) calc(l + 0.12) c h)` (relative color's `l` resolves to a plain `0–1` number, not a percentage — `calc(l + 12%)` doesn't work, mixing a number and a percentage silently invalidates the declaration), instead of hardcoding a new absolute L. Use this when a bespoke nudge is wanted on top of whatever step is already chosen, rather than jumping to a different named step entirely.
    - **`@media (prefers-color-scheme: dark)` remap block** (when the project only ever follows the OS setting, never a manual toggle, and a grouped block reads better than scattering `light-dark()` through every token line):
      ```css
      @media (prefers-color-scheme: dark) {
        :root {
          --color-brand: var(--primary-dark);
          --color-bg: var(--base-900);
        }
      }
      ```
      Trade-off: this form has no manual toggle on its own — a `[data-theme="dark"]` block would have to duplicate the whole remap.
  - Everything outside `config` uses semantic tokens only — never a primitive directly. Renaming a brand color then touches one line.
  - Derive related colors with relative color syntax instead of new literals: `--color-link: oklch(from var(--primary) 0.30 0.12 h);` shadow alphas as `oklch(from var(--color-shadow) l c h / 5%)`.

**Fixing failing contrast — adjust L, not C or H.** In hex/rgb, fixing a failing text/background pair means trial-and-error across three channels at once. In oklch, contrast is controlled almost entirely by the **lightness distance** between foreground and background — widen or narrow the `L` gap and leave chroma and hue alone (chroma has negligible effect on contrast). Rough landmarks, not a replacement for a real check (per safaii-html: verify with the WebAIM checker or an APCA calculator, not lightness alone):
- **Light/dark boundary:** a background reads as light above `L 0.6` — use dark text on it above that line, light text below.
- **Comfortable gap:** foreground `L` below ~0.45 on a background above `L 0.85`; foreground `L` above ~0.75 on a background below `L 0.15`.
- **Thresholds to actually check against:** WCAG 2 — 4.5:1 normal text / 3:1 large text & UI components (the number `safaii-html` already gates on). APCA (more perceptually accurate, pairs naturally with oklch since both are lightness-based) — `|Lc| ≥ 60` normal text, `≥ 75` for a stronger pass, `≥ 30` for UI components.

If a hand-tuned pair is failing, move `L` in the direction that widens the gap; don't reach for a new hue or a chroma tweak to "fix" what's actually a lightness problem.

**Text on a dynamic background — `contrast-color()` (ask-first).** `color: contrast-color(var(--color-accent))` auto-picks black or white text for a token-driven or user-chosen background, instead of a hand-set `-invert`/`-on-primary` token. Sharp caveats: it only ever returns black/white and **does not guarantee WCAG AA** — reliable only for near-black/near-white backgrounds; on mid-tone brand colors it can fail. It's Baseline 2026 (very new), so pair it with an `@supports` fallback. Because it's recent *and* easy to misapply, it's an **ask-first** feature (`references/browser-support.md`): flag the AA caveat to Matt and get his OK before using it — don't reach for it silently.

```css
button {
	background: var(--color-accent);
	color: var(--color-text-on-accent, oklch(99% 0 0)); /* hand-set fallback */
}
@supports (color: contrast-color(red)) {
	button { color: contrast-color(var(--color-accent)); }
}
```

### Other token groups (client tier only)

The minimal default doesn't ship these — add them in `config` only when a client project actually needs elevation or motion, same "semantic, in config, referenced everywhere" rule as colors. Don't tokenize what the project doesn't use.

- **Shadow** — `--shadow-sm/md/lg`, alphas via `oklch(... / <a>)`. Reach for these only when the design genuinely uses elevation; the default aesthetic is flat.
- **Motion** — `--duration-fast/base/slow` (e.g. `150ms`/`250ms`/`400ms`) and `--easing-*`. Tokenize durations/easings so animation stays consistent — but the animation-off-by-default rule and `prefers-reduced-motion` gating still apply; tokens don't license decoration.

No formal `--font-size-*`/`--font-weight-*` scale: that pushes toward sizing type by token instead of by element, which fights the document-first default. Fluid `clamp()` headings + element defaults cover it.

## SVG filters (ask-first, opt-in)

SVG filter primitives (`feTurbulence`, `feGaussianBlur`, `feMorphology`, `feColorMatrix`, `feSpecularLighting`, `feDisplacementMap`, `feOffset`, `feFlood`, …) recreate physical print effects — ink gain, texture, relief, glow — on type or shapes. Not a default technique for any project; the same bar as the animation rule above applies: a specific, brand-reinforcing use, brought to Matt for review, not reached for as decoration. **This confirm-first gate applies no matter how the request is phrased** — a direct instruction ("add a grain texture using an SVG filter") doesn't pre-authorize skipping the check-in any more than a hedged question does; the point is a quick design-review moment before building, not permission-seeking. Keep the check-in itself light — a one-line "this matches the paper-grain pattern already in use, sound good?" is enough, not a negotiation. One real, static, already-shipped example sets the model (`mattsafaii`'s `src/css/style.css`):

- **Paper-grain texture** — a tiny inline data-URI SVG (`feTurbulence type="fractalNoise"`) tiled as `background-image` on `body`, blended with `background-blend-mode: multiply` at low opacity (`0.16`). Pure CSS, no JS, and static in the sense that matters: the noise pattern itself never animates, it's a fixed grain sitting under all content.
- **Soft mask edges** (illustrative pattern, not a currently-shipped example) — `feGaussianBlur` inside an SVG `<mask>`, referenced via `filter="url(#id)"` on the masked group, softens a hard-edged shape without animating the filter itself.

**Default to static.** CSS can't transition individual filter-primitive attributes, so an *animated* filter effect (mouse-tracking light, a shimmering chroma-split, a turbulence wobble) is JS-driven (`requestAnimationFrame`), not CSS — that's a second, separate ask on top of the animation-off-by-default rule, since it also trades away "works without JavaScript." A static, one-time-rendered filter (a texture, a fixed glow, a gilded initial) stays inside the existing ask-first bar; an animated one needs its own explicit case made, gated the same way (`IntersectionObserver` so it only computes while visible, and settle on a representative still frame under `prefers-reduced-motion` rather than removing the effect outright).

**Mechanics, for when it's approved:**

- Define once in an inline `<svg><defs>…</defs></svg>`, reference from CSS (`filter: url(#id)`) or an SVG attribute (`filter="url(#id)"`). Keep the defs container in the render tree without displaying it: `position: absolute; width: 0; height: 0; overflow: hidden;` — not `display: none` (Chromium drops the filter reference entirely if the defs are `display: none`).
- Always set `color-interpolation-filters="sRGB"` on the `<filter>` — the SVG default (`linearRGB`) washes out blending between primitives.
- The filter region (`x`/`y`/`width`/`height`) is relative to the element's bounding box; expand it ~20–50% when an effect (blur, glow, extrusion) bleeds past the glyph edges, or it clips.
- **Tuning `feTurbulence`** — treat its attributes as a parameter space, not magic numbers: `baseFrequency` is scale (lower = larger organic blotches, higher = fine grain — the paper-grain example above uses `0.65` for fine grain), `numOctaves` adds detail layers at a real processing cost (more isn't free, keep it low for a background texture), `seed` reruns the same settings with a different pattern (useful for trying variations without touching the frequency/octave values that are already tuned).
- `feImage` is the flakiest primitive on HTML content (unreliable in Safari and Firefox) — avoid it.

## @scope component pattern

```css
@layer components {
	@scope (.site-nav) {
		:scope {
			display: flex;
			gap: var(--gutter);
		}

		a {
			text-decoration: none;
		}
	}

	/* `to` keeps card styles out of nested components rendered inside .card-body */
	@scope (.card) to (.card-body) {
		img {
			border-radius: var(--radius);
		}
	}
}
```

## Layout patterns

No-breakpoint layouts that wrap intrinsically. Both tie the wrap threshold to readable content width via `ch`, not arbitrary pixels.

```css
@layer components {
	/* Self-wrapping column grid — columns fill space, wrap below the minimum.
	   The scoped --grid-col-min makes the threshold overridable per instance. */
	@scope (.grid) {
		:scope {
			--grid-col-min: 20ch;
			display: grid;
			gap: var(--gutter);
			grid-template-columns: repeat(auto-fit, minmax(var(--grid-col-min), 1fr));
		}
	}

	/* Items that wrap independently at their own threshold (deconstructed pancake).
	   Each grows/shrinks freely but won't collapse below 20ch before wrapping. */
	@scope (.cluster) {
		:scope {
			display: flex;
			flex-wrap: wrap;
			gap: var(--gutter);
		}

		> * {
			flex: 1 1 20ch;
		}
	}
}
```

Use `auto-fill` instead of `auto-fit` when empty columns should keep their space (locking the grid to N columns even with fewer items).

These two come from [Every Layout](https://every-layout.dev/) (the Cluster and Grid primitives). It's the canonical source for intrinsic, no-breakpoint layout primitives and worth reaching for when a layout needs more than these — Center, Sidebar, Switcher. Its **Stack** primitive (owl selector `* + *` for vertical rhythm) is the formal version of what the starter already does by hand with `main > * + *` and `--stack`.

**Masonry isn't production-ready** (experimental, unsettled syntax — it's a "not-ready" feature in `references/browser-support.md`). Don't write `grid-template-rows: masonry` / `display: masonry`. Until it's Baseline: the `auto-fit` grid above (predictable, accessible) or, for *non-sequential* galleries only, a `columns` approximation — never `columns` for ordered content, since it flows top-to-bottom per column and breaks reading order.

**Container queries for discrete switches.** Intrinsic layout (the grid/cluster above, fluid `clamp`) handles most responsiveness with no queries — that's the default. When a component genuinely needs a *discrete layout change* (a card going stacked → side-by-side once it has room), use **`@container`** (Baseline 2023), not a `@media` viewport breakpoint: it responds to the component's own width so the component stays portable wherever it's placed. Set `container-type: inline-size` on the wrapper (the same declaration `cqi` already needs) and query it: `@container (inline-size > 30rem) { … }`. Same component-relative principle as `cqi`-over-`vw`. (Style queries — `@container style(--x: y)` — aren't Baseline yet, no Firefox; if you must, `@supports`-guard them. Scroll-state queries are experimental — skip.)

**Trig functions for math-driven layout** (`sin()`, `cos()`, `tan()`, `atan2()`, …, Baseline 2023). For a layout that's genuinely circular/radial — dots around a dial, items fanned around a center point — native CSS math beats a JS positioning loop: `left: calc(50% + var(--radius) * cos(var(--angle))); top: calc(50% + var(--radius) * sin(var(--angle)));`, with `--angle` set per item (e.g. `calc(360deg / var(--count) * var(--i))`). No JS, no library. Reach for it only when the shape genuinely is circular/angular — for ordinary wrapping layouts the grid/cluster primitives above are still correct; this is a narrow-but-real tool for the specific case they don't cover.

## Standing out from AI-sameness

A build-order checklist for a page before calling it done — not new rules, a pass over ones already in this skill plus two new checks:

1. **Spacing & padding.** Container/cluster/grid rhythm, the spacing-rhythm-of-three tokens. Makes content easy to scan.
2. **Typography.** Font family, fluid `clamp()`/`cqi` sizing, weight, tracking, color. This is where the page starts to have a voice.
3. **Layering.** Flat pages (bg color, text, done) read as generic. Stack elements — a gradient behind a hero, a card overlapping a z-indexed button/image, a background video/image bleeding behind content — before shipping a hero or feature section.
4. **One deliberate specific detail.** Every design should have at least one element that reinforces what *this* brand/product specifically is, not a generic embellishment (a noise texture, an icon shape, a motif tied to the product's own meaning). Same ask-first bar as animation/SVG filters above — bring the specific idea to Matt, don't add it silently.
5. **Animation.** Last, and still gated by the ask-first rule above — motion is what ties the rest together once it's earned its place, not a default.

## Browser support

This skill uses recent CSS (`@scope`, `cqi`, `oklch`, relative color, `@view-transition`). Support policy and a per-feature support map live in `references/browser-support.md`. The short version:

- **Personal projects** → Baseline *Newly available*: use the latest the moment it's in all three engines.
- **Client projects** → same default, but when a feature is **both** recently-shipped **and** fails ungracefully, adopt it *with a removable fallback* (`@supports` / feature-detect) rather than avoiding it; delete the fallback once support is ubiquitous. Write fallbacks baseline-first then enhance in `@supports (feature)` — but don't wrap a single property override in a feature query; the plain `prop: old; prop: new;` cascade already handles that (pattern in `references/browser-support.md`).
- **Ask-first features.** Some features are flagged ask-first in `references/browser-support.md` — very recent (Baseline current-year), risky/misleading, or narrow. **Don't reach for these silently: surface the feature, its caveat, and the fallback to Matt and get his go-ahead first.** Scale the warning to the risk: a recent-but-graceful feature (`:open`) is a light heads-up; a risky/misleading one (`contrast-color()`) needs the caveat foregrounded. Current list: `contrast-color()`, `:open`, view-transition types, `field-sizing: content`, `@property` (color animation); `interpolate-size` + `text-box-trim` + `initial-letter` (experimental/incomplete-engine).
- **Not-ready features.** A step earlier — pre-Baseline / experimental / unsettled-syntax features (currently CSS **masonry**). **Don't ship these at all, even with a fallback;** if asked, say it's not production-ready and offer the stopgap (see `references/browser-support.md`). The three tiers: **use** (Baseline) → **ask-first** (recent/risky) → **not-ready** (experimental).
- Support status goes stale; **verify borderline features at write-time** (webstatus.dev / caniuse / MDN) rather than trusting memory or the file's snapshot.

## Checks

| # | Check | Pass criteria | If fail |
|---|-------|---------------|---------|
| 1 | Layer order | `grep -cE '^@layer config, reset, elements, components(, utilities)?;' style.css` → 1 | Add/fix the declaration; it must precede all `@layer` blocks |
| 2 | No frameworks | `grep -nE '@tailwind|@apply|!important' style.css` → no matches | Remove; express with layers/specificity instead |
| 3 | Scoped components | every component with descendant rules sits inside `@scope`; **and** no `@scope` block is root-only (a `@scope` whose only rule targets `:scope`, even with `:scope:hover`/`:scope:focus`, is needless) | Descendant rules: wrap in `@scope (.component-root)`. Root-only wrapped in `@scope`: unwrap to a plain `.component-root { … }` rule |
| 4 | oklch only | `grep -nE '#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\(' style.css` → no matches (SVG data-URIs exempt) | Convert to oklch |
| 5 | Tokens used | spacing values reference `--gutter`/`--stack` (grep for stray `margin.*px`) | Derive from tokens via `calc()` |
| 6 | Motion gated | every `animation:`/`transition` on motion is inside `prefers-reduced-motion: no-preference` (micro-transitions like color/underline exempt) | Wrap in the media query |

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Styles in wrong layer win/lose unexpectedly | Element styles placed in `components`, or tokens outside `config` | Move rules to the layer matching their role |
| Component styles leak into nested content | `@scope` without a `to` boundary around a component that contains other components | Add `to (.inner-component)` limit |
| Scaffold drifts per project | Starter copied from a previous project instead of this skill | Always copy `references/starter.css` |
| Derived views stale | Skill / starter.css changed but `rules.txt` and the Basecamp doc weren't refreshed | Regenerate the derived views from this skill; the skill + starter.css are the source of truth, so this is cosmetic, not a conflict |
| Garp scaffold off-spec | `garp new` ships a baked-in `style.css` const that was hand-written instead of derived from this skill | Refresh garp's `new.go` `scaffoldStyles` const from `starter.css`; canonical token names here win over whatever the scaffold currently uses |

## Consumers (keep in sync)

These materialize the conventions; when this skill or `references/starter.css` changes, refresh each — none auto-update:

- **11ty sites** — copy `references/starter.css` as the project's `css/style.css`.
- **Rails apps** — split `starter.css` by concern into `app/assets/stylesheets/`.
- **garp** (`~/Code/personal/garp`) — `new.go` bakes the starter into a Go string const: `scaffoldStyles` → `static/style.css`. A *compiled snapshot*: it ships with `garp new` and silently drifts when the conventions move. Refresh the const from `starter.css` and rebuild. Canonical token names here win over the scaffold's.

### Derived human-readable views

Not project stylesheets — readable renderings of the conventions. Their lag is cosmetic, so refresh on demand and only for reader-facing rule changes (not wording/meta); batch tweaks, don't sync per edit.

- **Basecamp "Frontend Conventions"** (Lab project 46824335, account 6191443, doc 9768197742) — a combined, **overview-level** human summary covering both this skill and [[safaii-html]] (philosophy → what css owns → what html owns → skills as source of truth). Deliberately not a deep rule-by-rule mirror, so most rule tweaks here don't require a doc edit. When a change is overview-relevant, refresh by editing the live HTML in place, not regenerating from scratch:
  1. Pull the raw HTML: `basecamp -a 6191443 docs show 9768197742 -p 46824335 -j -q` → read the `content` field.
  2. Surgically edit only the changed section in that HTML.
  3. Push back: `basecamp -a 6191443 docs update 9768197742 -p 46824335 -t "Frontend Conventions" -c "<full html>"`.
  - **Gotcha:** `update` replaces content wholesale — you must pass the *complete* HTML and *both* `--title` and `--content`; omitting either wipes it (see [[basecamp-docs-update]]). Re-fetch with `--md` afterward to verify formatting survived.

## Examples

Real stylesheets that follow the conventions. Study before starting:

- **`references/starter.css` — the canonical artifact and source of truth for the stylesheet itself.** Every project starts from this; the examples below are real-world applications of it, not replacements for it. When in doubt, the starter wins.
- `~/Code/personal/mattsafaii/src/css/style.css` — layer order, config tokens, body grid with named bleed/content columns, element-first styling, `color-mix` muting, gated motion/hover, `@scope` components (including a `to (.lightbox)` boundary example).
- `~/Code/_safaii-studio/clients/konnectedconcepts/src/assets/css/base.css` (config layer) — the bigger-palette token system: primitive ramp + accents, semantic tier built on top, relative color syntax for derived values. Color structure only — its layer list and utilities predate the conventions (8-layer order, hex neutral ramp, not oklch).
- Basecamp "Frontend Conventions" (derived human-readable view, not authoritative): https://app.basecamp.com/6191443/buckets/46824335/documents/9768197742

## Status

First version, with one example. After the next CSS project, add any new failure modes to the table and the finished stylesheet to Examples.

Behavioral evals live in `evals/evals.json` — they test whether this skill *steers* an agent to the conventions (a test of the skill, not a consumer to keep in sync). Not part of normal CSS work; run them via the skill-crafting tooling when changing the conventions, and add an eval when a new convention lands.
