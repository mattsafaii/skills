# Tells

The patterns that mark a page as generated. This catalogue came from real production rounds, not theory. Treat everything here as a hard ban unless the brief explicitly calls for it.

Read this before shipping. It is the part of the skill most often ignored, and the part that matters most.

---

## Visual and CSS

- **No neon or outer glows by default.** Inner borders and subtle tinted shadows instead.
- **No pure black.** Off-black, near-black warm grey, or charcoal.
- **No oversaturated accents.** Desaturate to sit with the neutrals.
- **No gradient text on large headings.**
- **No custom mouse cursors.** Outdated, hostile to accessibility, hostile to performance.

## Typography

- **No Inter by default.** It is the model's reflex. Choose deliberately; if the brief genuinely wants a neutral standard face, that's a reason, not a default.
- **No oversized headlines that just shout.** Hierarchy comes from weight and colour, not raw scale.
- **No serif for "creative".** See `SKILL.md` section 4.
- **No `<br>`-broken italic headlines** as a design move — "for thirty`<br>`*years.*" Headlines read naturally first.

## Colour

- **No purple-blue AI glow.** Neutral base, one high-contrast accent.
- **No warm cream plus brass plus espresso** as a premium-consumer default. See `SKILL.md` section 5.
- **No colour carrying meaning alone.**

## Layout

- **No three equal feature cards.**
- **No mathematically perfect symmetric padding** with awkward gaps elsewhere. Deliberate asymmetry beats accidental evenness.
- **No section-number eyebrows** — `00 / INDEX`, `001 · Capabilities`, `06 · how it works`. An eyebrow names the topic in plain language or doesn't exist.
- **No `01 / 4` pagination** on images or tiles. If the reader can count, the label is noise.
- **No floating top-right sub-text** in a section header — a giant left headline with a small unexplained paragraph in the corner.
- **No crosshair or hairline grid lines as decoration.** Only when they organise real content.
- **No rotated vertical text** unless the brief is genuinely agency or experimental and it serves the composition.
- **No `border-top` and `border-bottom` on every row** of a long list or spec table. Pick one, use it sparsely.

## Content and data

- **No generic names.** "John Doe", "Jane Smith". Use real, locale-appropriate names.
- **No generic avatars.** No egg shapes, no default user glyphs.
- **No fake-perfect numbers.** `99.99%`, `50%`, `1234567`. If a number is invented it is banned; if it comes from the brief or public data it's fine; if it's a mock, label it as one.
- **No startup-slop brand names.** "Acme", "Nexus", "SmartFlow", "Cloudly".
- **No filler verbs.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize". Concrete verbs only.

## Hero and top of page

- **No version labels in the hero** — `V0.6`, `BETA`, `EARLY ACCESS` — unless the brief is genuinely a launch.
- **No "Brand · No. 01" sub-eyebrows.**
- **No decoration text strip at the hero bottom** — `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`. Only if it carries real links or real status.
- **No "Used by" strip inside the hero.** It goes below.
- **No scroll cues.** `Scroll`, `↓ scroll`, `Scroll to explore`, animated mouse-wheel icons. The reader knows what scroll is.

## Pills, labels, stamps

- **No pills or tags overlaid on images.** Let the image speak, or caption it below.
- **No photo-credit captions as decoration.** "Plate 03 · House archive", "Frame XII · 35mm". Credit a real photographer for a real photo, or write a functional caption.
- **No version footers on marketing pages** — `v1.4.2`, `Build 0048`, `last sync 4s ago`.
- **No "Reservation 412 of 800" live counters** as decoration.

## Locale and time

- **No city, time, or weather strips** — "Lisbon, working with founders", "Lisbon 14:23 · 18°C". Allowed only for a genuinely distributed studio, a travel brand, or a physical venue. A contact address in the footer is fine; an atmospheric locale strip is not.
- **No decorative status dots.** A coloured dot before nav items, list rows, or badges is a tell. Only for real semantic state, sparingly.
- **The middle dot (`·`) is rationed** — at most one per line in a metadata strip, not the default separator for everything.

## Marketing copy

- **No "Quietly in use at" / "Quietly trusted by".** Use plain language or skip the heading.
- **No poetic section labels** — "From the field", "Field notes", "On our desks". Use functional labels.
- **No generic step labels** — "Stage 1 / Step 1 / Phase 01". Use the verb: "Install", "Configure", "Ship".
- **No mock-humble industry references** in body copy.
- **No micro-meta-sentences under eyebrows** explaining the section's own purpose. Eyebrow, headline, body. That's enough.

## Copy audit

Before declaring anything done, re-read every visible string — headlines, subheads, eyebrows, button labels, body, captions, alt text, footer text, error messages. Flag and rewrite any string that is:

- **Grammatically broken**, or reads as though a word is missing.
- **Unclear in its referent** — "we plan to stay that way" with nothing before it.
- **AI hallucination** — wordplay that doesn't track, a forced metaphor, an elegant-sounding nothing.
- **An LLM performing thoughtfulness** — false humility, fake-craftsman phrasing.

If unsure whether a string makes sense, replace it with a plain functional sentence. Generated cute copy is worse than boring copy.

**Em-dash overuse** is the strongest single copy tell. Do not use it as a design flourish or a default pause. `humanizer` owns the general prose case; this is the page-copy instance of it.

**One register per page.** Don't mix technical, editorial, and marketing voices in one composition unless the brand genuinely carries all three.

## Motion

- **No animation without a stated reason.** See `SKILL.md` section 6.
- **No perpetual micro-interactions on every card.** A pulse, a float, a shimmer, a typewriter — only where the section genuinely benefits, and only above intensity 5.
- **No second marquee.**
- **No `window.addEventListener('scroll')`.** Use CSS scroll-driven animation (`scroll-driven-animation`), `IntersectionObserver`, or the platform.
- **No animation on `top`, `left`, `width`, or `height`.** `transform` and `opacity` only.
- **No unmotivated scroll-jacking.** If a section pins or pans, it says something.

## Components and assets

- **No hand-rolled SVG icons.** Use a real icon set. Hand-rolled decorative SVGs are strongly discouraged — acceptable only when the brief asks for a mark and the output is genuinely simple and good.
- **No div-based fake screenshots.** A product preview built from styled rectangles is the number-one design tell. Use a real screenshot, or omit the preview.
- **No broken image links.** A real asset, a labelled placeholder slot, or nothing.
- **No stock-photo people looking at laptops.** If the imagery is generic, the page is generic.
