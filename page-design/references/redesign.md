# Redesign

Half of client work is a redesign. Misreading the mode is the biggest single source of bad output.

The audit itself is `inventory-brief`; the URL mapping is `structure-redirects`. This file is the design-side protocol those two don't cover.

---

## Detect the mode first

- **Greenfield** — no existing site, or a full overhaul approved. Set the dials from `SKILL.md` section 1.
- **Preserve** — modernise without breaking the brand. Audit, extract the existing tokens, evolve gradually.
- **Overhaul** — a new visual language on existing content. Treat the visuals as greenfield; preserve the content and the information architecture.

If it's ambiguous, ask once: "Preserve the existing brand, or start visually from scratch?"

## Audit before touching anything

Document the current state before proposing a change. Most of this already exists in `inventory-brief` and the client's `Project Context` — read those first rather than re-deriving.

- **Brand tokens** — primary and accent colours, type stack, logo treatment, radii.
- **Information architecture** — page tree, primary navigation, conversion paths.
- **Content blocks** — what exists, what's working, what's filler.
- **Patterns to keep** — signature interactions, a recognisable hero, the copy voice.
- **Patterns to retire** — the tells in `references/tells.md`, broken layouts, dead links, generic stock imagery, performance traps.
- **The existing site's dial reading** — infer its current variance, motion, and density. That's the starting point, not the baseline.
- **SEO baseline** — ranking pages, titles, structured data, social cards. **SEO migration is the number-one redesign risk.**

## What is preserved

- **The information architecture, unless asked.** Keep slugs, anchor IDs, and primary nav labels stable. They carry SEO and muscle memory.
- **The brand colour, before applying the palette rules.** A brand that is already purple stays purple — the rules in `SKILL.md` section 5 are defaults, not mandates.
- **The copy voice, unless a rewrite was asked for.** A visual modernisation is not a content rewrite.
- **Existing accessibility wins.** Never regress focus states, alt text, keyboard paths, or contrast.
- **Existing analytics hooks.** Don't rename buttons, form fields, or section IDs that tracking depends on.

## Modernisation levers, in priority order

Apply in order and stop when the brief is satisfied.

1. **Typography refresh** — the biggest visual lift for the least risk.
2. **Spacing and rhythm** — more section padding, a corrected vertical rhythm.
3. **Colour recalibration** — desaturate, unify the neutrals, keep the brand accent.
4. **Motion layer** — add intensity-appropriate micro-interactions to existing components.
5. **Hero and key-section recomposition** — restructure the top of the funnel using the vocabulary below.
6. **Full block replacement** — only when the existing block is unsalvageable.

## Which path

- IA, content, and SEO sound → **targeted evolution** (levers 1–4). About 70% of the value at 40% of the risk.
- The visual debt is structural — broken IA, no system, broken mobile → **full redesign**, with strict content preservation.
- The brand itself is changing → **greenfield**.

## What never changes silently

Never modify without explicit approval:

- URL structure or route slugs.
- Primary navigation labels.
- Form field names or order — it breaks analytics and autofill.
- The logo or wordmark.
- Legal, consent, or cookie copy.

---

## Pattern vocabulary

Names to think and talk with. This is a vocabulary, not a library — reach for a pattern when the Design Read calls for it, and implement it in vanilla CSS per `safaii-css`.

**Hero**
Asymmetric split · Editorial manifesto (type only, near-poster) · Media-masked · Kinetic type · Curtain reveal · Scroll-pinned.

**Navigation**
Edge dock with hover magnification · Magnetic button · Morphing pill for status · Full-screen reveal with staggered content.

**Layout**
Bento grid · Masonry (via an `auto-fit` grid or, for non-sequential galleries only, columns — never for ordered content) · Split-screen scroll · Sticky-stack sections.

**Cards and containers**
Tilt on pointer · Spotlight border under cursor · Glass panel · Morphing modal (a button that expands into its own dialog).

**Scroll**
Sticky scroll stack · Horizontal pan · Sequence tied to the scrollbar · Zoom parallax · Scroll-progress path.

**Galleries**
Coverflow carousel · Drag-to-pan grid · Accordion slider · Hover image trail.

**Type**
Kinetic marquee · Text-mask reveal · Circular text path · Gradient stroke.

**Micro-interactions**
Directional hover-aware button · Ripple · Animated line drawing · Skeleton shimmer · Mesh-gradient background.

**Motion choice.** CSS scroll-driven animation (`scroll-driven-animation`) is the default for scroll-linked work. JavaScript motion libraries are ask-first (`safaii-css`) and are for what CSS genuinely can't do. Never run two motion systems on the same element.
