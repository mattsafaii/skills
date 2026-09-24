---
name: page-design
description: Sets the design direction for a page and holds it to composition discipline. Reads the brief, declares a one-line Design Read, sets the variance / motion / density dials, then enforces the hero, section, and layout rules with a pre-flight check before shipping. Use when designing or reviewing a page, landing page, marketing site, hero, or section layout; when deciding what a site should look like; when choosing type, palette, or motion direction; or when a build has its structure set and the visual direction still has to be decided. Also the authority for perceptual layout — measure, grouping, alignment, reading order. Not for dashboards, data tables, or dense product UI. Delegates CSS mechanics to safaii-css, markup and accessibility to safaii-html, and copy voice to humanizer / nothing-language / us-graphics-voice.
---

# page-design

How Safaii Studio decides what a page looks like, and how it holds the page to that decision.

Where it sits: `structure-copy` fixes what each template says; this skill decides how it looks and why. It runs after the sitemap and copy exist, during build, and again as a pre-flight pass before Release. For Lab devtool pages it runs alongside `devtool-page`.

**Direction is per company.** There is no house look. A site for a plumbing outfit and a site for a design studio should not resemble each other. `us-graphics` is one voice available to this skill, not its default — reach for it when the brief calls for that register, and reach for something else when it doesn't.

## Delegation

Do not restate what another skill owns. Point at it.

| Concern | Owner |
|---|---|
| CSS mechanics, layers, tokens, oklch, ramps, contrast, layout primitives, motion craft, browser support | `safaii-css` |
| Markup, semantics, forms, accessibility, component patterns | `safaii-html` |
| Copy voice — AI tells, praxis fog, that one USGC register | `humanizer`, `nothing-language`, `us-graphics-voice` |
| Reference before designing — real shipped sites, UI variants, how an effect was built | `inspo`, `ui-mockup`, `explain-interface` |
| Scroll-driven motion | `scroll-driven-animation` |
| Deciding and generating the page's imagery | `image-direction` |
| Redesign audit of an existing site | `inventory-brief`, `structure-redirects` |

## 0. Read the brief first

Most generated design is bad because the model jumps to a default aesthetic instead of reading the room. Read the room.

**Signals, in order:**

1. **Page kind** — landing, service, product, portfolio, editorial, contact.
2. **Vibe words the client used** — "clean", "premium", "playful", "serious", "warm", "technical".
3. **References** — sites they linked, screenshots they sent, competitors they named.
4. **Audience** — a procurement panel picks a different aesthetic than a homeowner picking a contractor. The audience picks the look, not your taste.
5. **Existing brand assets** — logo, colour, type, photography. These are starting material. On a redesign they are not optional input.
6. **Quiet constraints** — regulated industries, trust-first commerce, public-sector, accessibility-critical. These override aesthetic preference.

**Then state one line before writing any CSS:**

> Reading this as: *[page kind]* for *[audience]*, with a *[vibe]* language, leaning toward *[aesthetic family]*.

Examples:
- "Reading this as: a service page for homeowners replacing a roof, with a trust-first plain language, leaning toward photography-led, high contrast, no motion."
- "Reading this as: a product page for a specialty hardware maker, with a warm-craft language, leaning toward editorial type and generous space."
- "Reading this as: a portfolio for a design studio, with an editorial / kinetic-type language, leaning toward asymmetric grids and scroll-driven reveals."

**If the brief is ambiguous, ask one question.** Not a checklist — one. "Should this feel closer to quiet and established, or sharp and new?" If you can infer it, do not ask; declare the read and go.

**Anti-default discipline.** Do not reach for these because they are easy: purple-blue gradients, a centred hero over a dark mesh, three equal feature cards, glassmorphism on everything, infinite micro-animations, Inter plus slate-grey. They are the defaults. Go past them deliberately.

## 1. Set the dials

After the Design Read, set three dials. Every layout, motion, and density call below is gated by them.

- **`DESIGN_VARIANCE`** — 1 = perfect symmetry, 10 = asymmetric chaos
- **`MOTION_INTENSITY`** — 1 = static, 10 = cinematic
- **`VISUAL_DENSITY`** — 1 = airy, 10 = packed

Baseline `8 / 6 / 4` is a starting point for a general landing page, not a default to keep. Derive from the read.

| Read | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Minimalist / calm / editorial | 5–6 | 3–4 | 2–3 |
| Premium consumer / luxury / brand | 7–8 | 5–7 | 3–4 |
| Playful / experimental / agency | 9–10 | 8–10 | 3–4 |
| General landing / marketing | 7–9 | 6–8 | 3–5 |
| Trust-first / regulated / accessibility-critical | 3–4 | 2–3 | 4–5 |
| Redesign — preserve | match existing | existing +1 | match existing |
| Redesign — overhaul | existing +2 | existing +2 | match existing |

**Motion claimed is motion shown.** If `MOTION_INTENSITY > 4` the page must actually move — an entry transition, a scroll reveal, a hover state. A static page claiming 7 is broken. If the scope can't carry working motion, drop the dial to 3 and ship clean and still. Never half-build motion.

## 2. Foundation

**The house foundation is `safaii-css`.** Every page starts from its starter — layers, tokens, oklch, layout primitives. That is not a constraint on direction; it is the substrate. Two sites can share every convention and look nothing alike.

**When a brief justifies something else:** only when the client's organisation already runs a system, or the sector expects one — `govuk-frontend` or `uswds` for public-sector, Bootstrap for a fast local-business build. These are plain CSS and sit fine under the house conventions. Say which one you're using and why. Never import a system's tokens and then override most of them; if you adopt a system, adopt it.

**One foundation per project.** Do not mix.

**When the brief is an aesthetic, not a system** — and this is the usual case — the direction is an aesthetic family. These have no package; build them in vanilla CSS:

| Family | How it's honestly built |
|---|---|
| Glassmorphism | `backdrop-filter`, layered borders, highlight overlays, solid-fill fallback under `prefers-reduced-transparency` |
| Bento tile grids | CSS Grid with mixed cell sizes |
| Brutalism | Native CSS, monospace, raw borders |
| Editorial / magazine | Asymmetric grid, generous whitespace, considered type |
| Dark technical | Mono plus one accent, restrained |
| Kinetic type | Native CSS animation, scroll-driven animation (`scroll-driven-animation`) |
| Warm craft | Photography-led, muted palette, texture |

Apple's Liquid Glass is an Apple-platform material. There is no official web CSS for it; a `backdrop-filter` approximation is web glassmorphism. Label it as such.

## 3. Composition

The full rules, with the reasoning, are in `references/composition.md`. Open it before laying out a page. The short form:

- **The hero fits the viewport.** Headline max 2 lines, subtext max 20 words, CTA visible without scrolling. If the copy is too long, cut the copy or reduce the scale — never let the CTA fall below the fold.
- **The hero holds at most 4 text elements** — eyebrow or brand strip (zero or one), headline, subtext, CTAs. A tagline below the CTAs, a trust strip, a pricing teaser, or a feature list is not hero content; it moves to a section below.
- **Navigation is one line at desktop**, 64–72px tall, 80px max.
- **A layout family appears once per page.** Eight sections use at least four different families.
- **No three equal cards.** Ever.
- **An eyebrow above every section is the single most common tell.** Maximum one eyebrow per three sections.
- **Bento grids have exactly as many cells as they have content.** No empty cell in the middle or at the end.
- **Mobile collapse is explicit.** Every multi-column layout declares its narrow fallback; nothing relies on "it'll wrap."

## 4. Typographic direction

`safaii-css` owns sizing, fluid `clamp()`/`cqi`, and truncation. This skill owns the choice.

- **One type scale, set by element.** Headings scale with the container; body sits at a comfortable measure.
- **Measure is 60–75 characters** on body copy. Wider is unreadable; narrower is jumpy. This is the number `explain-interface` checks against.
- **Serif is not the default for "creative."** That reflex is the most-tested AI tell in production. Reach for a serif only when the brief names one, or the family is genuinely editorial, publication, heritage, or luxury and you can say why this serif fits this company. Otherwise set display type in a sans and make the choice deliberate.
- **Never Fraunces or Instrument Serif as a default.**
- **Emphasis inside a headline stays in the same family** — italic or bold of the same face. Injecting a serif word into a sans headline to add interest is amateur.
- **Italic display type with a descender (`y g j p q`) needs clearance** — a `leading` below about 1.1 clips it. Check every italic word in a headline.
- **Fonts are self-hosted** as woff2 with `font-display: swap`. Never a Google Fonts `<link>` in production.

## 5. Colour direction

`safaii-css` owns the system — oklch, ramps, semantic tokens, dark mode, contrast fixes. This skill owns the calibration.

- **One accent.** Saturation under 80% by default.
- **The accent is locked for the whole page.** A warm-grey site does not get a blue CTA in section 7. One accent, audited across every component.
- **No automatic purple-blue glow.** Neutral base, one high-contrast accent. If the brand genuinely is purple, execute it with intent — consistent palette, harmonised neutrals — rather than reaching for the gradient.
- **No pure `#000` or `#fff`.** Off-black and off-white; pure values flatten depth.
- **The warm-craft palette is banned as a default.** Cream background, brass or oxblood accent, espresso text — every premium-consumer site generated without a brief lands there, and the brand disappears. Rotate: cold silver-grey, forest green and bone, off-black and tan, cobalt and cream, terracotta and slate, monochrome plus one saturated pop. Only use the warm palette when the brand genuinely is warm-craft and you can say why.
- **Never signal state with colour alone.** Pair it with an icon, text, or shape (`safaii-html`).

## 6. Motion direction

Technique belongs to `safaii-css` (motion craft, entry/exit, easing) and `scroll-driven-animation`. This skill decides whether motion belongs at all.

- **Every animation answers "what does this communicate?"** Valid: hierarchy, sequence, feedback, a state change. Invalid: it looked good. If you can't say it in one sentence, cut it.
- **Animate `transform` and `opacity` only.** Never `top`, `left`, `width`, `height`.
- **One marquee per page, at most.**
- **Reduced motion is mandatory** above `MOTION_INTENSITY 3` — `safaii-css` owns the gate.
- **Animation is ask-first.** Bring the specific idea to Matt before building it, regardless of how the request was phrased (`safaii-css`).

## 7. Redesign

Half of client work is redesign, and misreading the mode is the biggest source of bad output. Detect the mode first, audit before touching anything, and know what never changes silently. The protocol is in `references/redesign.md`. The audit itself is `inventory-brief`; the URL mapping is `structure-redirects`. SEO migration is the number-one redesign risk — page slugs, titles, and structured data are not cosmetic.

## 8. Anti-slop tells

The catalogue — the patterns that mark a page as generated — is in `references/tells.md`. Read it before shipping anything. It is the most valuable part of this skill and the part most often ignored.

## 9. Pre-flight check

Run every box before delivering. If one cannot be ticked honestly, the page is not done.

- [ ] **Design Read** declared, and the page matches it?
- [ ] **Dials** set from the brief, not left at baseline?
- [ ] **Foundation** chosen and named (house starter, or a system with a reason)?
- [ ] **Redesign mode** detected and audited, if applicable?
- [ ] **Hero fits** — headline ≤ 2 lines, subtext ≤ 20 words, CTA visible without scrolling?
- [ ] **Hero holds ≤ 4 text elements** — no tagline below the CTAs, no trust strip inside the hero?
- [ ] **Navigation on one line** at desktop, ≤ 80px tall?
- [ ] **No three equal cards** anywhere?
- [ ] **Eyebrow count** ≤ one per three sections?
- [ ] **Layout families** — no family repeated, at least four across eight sections?
- [ ] **Bento cell count** matches content exactly, no empty cells?
- [ ] **Measure** 60–75 characters on body copy?
- [ ] **Serif** justified, and not Fraunces or Instrument Serif by default?
- [ ] **Italic descenders** have clearance in every headline?
- [ ] **One accent**, locked across the page?
- [ ] **No pure black or white**?
- [ ] **Warm-craft palette** avoided unless the brand genuinely is warm-craft?
- [ ] **Every animation** justified in one sentence, `transform`/`opacity` only?
- [ ] **Marquee** at most one?
- [ ] **Reduced motion** gated for everything above intensity 3?
- [ ] **Motion claimed = motion shown?**
- [ ] **Every state** present — hover, focus, active, disabled, loading, empty, error?
- [ ] **Contrast** passes on buttons, forms, and placeholders (`safaii-css`, `safaii-html`)?
- [ ] **No duplicate CTA intent** — one label per intent across nav, hero, footer?
- [ ] **Mobile collapse** explicit per multi-column section?
- [ ] **Copy audited** — no broken, vague, or invented strings?
- [ ] **Tells** from `references/tells.md` all clear?

## 10. Out of scope

Not for dashboards, admin panels, dense product UI, data tables, multi-step wizards, code editors, or realtime collaborative UI. When the brief is one of those, say so and apply only the marketing and about-page parts of this skill to the surfaces where they apply.

## References

- `references/composition.md` — page composition in full, with the reasoning
- `references/tells.md` — the anti-slop catalogue
- `references/redesign.md` — redesign protocol and pattern vocabulary
- `safaii-css` — the CSS substrate; `safaii-html` — markup and accessibility
- `inspo` — real shipped references before you design

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Page looks generic | Jumped to a default aesthetic instead of reading the brief | Re-run section 0; declare the read; re-decide the dials |
| Direction fights the client | Applied a personal or `us-graphics` voice to a brief that didn't call for it | Direction is per company — re-read the audience and existing assets |
| Hero CTA below the fold | Copy too long or scale too large | Cut the copy or reduce the scale; never let the hero overflow |
| Every section has a small caps label above it | Eyebrow reflex | Max one eyebrow per three sections; drop the rest |
| Three identical feature cards | Reached for the easiest row | 2-column zigzag, asymmetric grid, or a different family |
| Page reads as one long sameness | One layout family repeated | At least four families across eight sections |
| Premium-consumer site looks like every other one | Defaulted to cream + brass + espresso | Rotate the palette family; justify warm-craft or leave it |
| Motion added "to feel premium" | No communicative reason | Cut it, or name what it communicates |
| Cited a rule with nothing behind it | A rule from a skill this one replaced | The rule belongs here or in `safaii-css`/`safaii-html` — put it there |
