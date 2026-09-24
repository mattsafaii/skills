# Composition

The page-level rules, with the reasoning. `SKILL.md` carries the short form; this is what you open before laying out a page.

Values are written as plain CSS. Where a token exists, use it (`safaii-css` owns the scale) — the numbers here are the intent, not a second scale.

---

## Hero

The hero is one moment, not a summary of the page.

**It fits the viewport.** Headline at most 2 lines at desktop. Subtext at most 20 words and 4 lines. The primary CTA visible without scrolling. If it doesn't fit, the copy is too long or the type is too large — fix one of those, never let the hero overflow and force a scroll to find the CTA. If the value proposition needs more than 20 words of subtext, the value proposition is unclear, not the rule too tight.

**Scale is planned with the asset.** Decide font size and image size together. A large hero asset with a headline over six words does not start at the top of the scale. A four-line hero headline is always a font-size error, not a copy-length error.

**Top padding is capped.** Around `6rem` at desktop is the ceiling. More and the hero content floats halfway down the viewport and reads as a bug. If it needs more air, increase the type or the asset, not the padding.

**At most four text elements:**

1. An eyebrow, or a brand strip, or neither — zero or one
2. The headline
3. The subtext
4. The CTAs — one primary, at most one secondary

Everything else is not hero content. A tagline under the CTAs, a "trusted by" micro-strip, a pricing teaser, a feature bullet list, a row of avatars — all of those belong in a section directly below the hero. If you have an eyebrow and a tagline, drop the tagline.

**The hero needs a real visual.** Type over a gradient blob is a placeholder, not a hero.

## Trust and social proof

A "used by" or "trusted by" logo wall belongs **under** the hero, never inside it. The hero carries the value proposition and the CTA; the logo wall is its own section.

- **Logos, not wordmarks.** Plain text names in a row read as filler. Use real marks where the brand is real.
- **Logo only.** No industry or category label under each logo. The logo is the credibility; the label adds nothing the reader doesn't already know.
- **One line of attribution at most.**

## Navigation

- **One line at desktop.** If the items don't fit, condense the labels, drop the secondary items, or move to a disclosure. A two-line nav at desktop is broken.
- **64–72px tall by default, 80px maximum.** A nav that eats a sixth of the viewport is an agency cliché, not a statement.

## Layout families

A **layout family** is the shape of a section — three-column cards, a full-width quote, a split text-and-image, a bento grid, a horizontal scroll, a stacked list.

- **Each family appears at most once per page.** "Selected work" must not look like "What we do."
- **Eight sections use at least four families.**
- **No three equal cards.** The generic three-identical-cards row is the single most common generated layout. Use a 2-column zigzag, an asymmetric grid, a pinned section, or a horizontal scroll instead.
- **Zigzag has a cap.** Left-image/right-text alternating with right-image/left-text is fine twice in a row; a third consecutive image-and-text split is banal. Break it with a full-width section, a grid, or a different family.

## Bento grids

- **The cell count equals the content count.** Three items, three cells. Five items, five cells. An empty cell in the middle or at the end means the grid was planned wrong — reshape it, don't paste a blank tile.
- **Rhythm, not repetition.** Don't stack six identical left-image/right-text rows.
- **Background variety.** A grid of six white cards with type inside reads as default even when the rest of the page is good. At least two or three cells carry a real image, a brand-appropriate tint, or a pattern.

## Eyebrows

An **eyebrow** is the small uppercase wide-tracked label above a section headline — the thing that looks like `SELECTED WORK` or `THE HARDWARE`.

It is the most-violated rule in production. Every generated page puts one above every section, and the rhythm is instantly recognisable.

- **Maximum one eyebrow per three sections.** Hero counts as one. Nine sections, at most three eyebrows.
- If a section has an eyebrow, the next two cannot.
- **The check is mechanical:** count small-caps wide-tracked labels above headlines. If the count exceeds a third of the section count, the page fails.
- **Usually, drop it.** The headline alone is enough. A section's position on the page already categorises it.

## Split headers

The pattern "large headline on the left, small explainer paragraph floating in the right column" as a section header is banned by default. A section carries one message. If you genuinely need both a headline and an explainer, stack them — headline, then body, at the measure. Reach for the split only when the right column holds a real visual or interactive element, not filler.

## Content density

A page lives on the first impression, not the full read.

- **Default section shape:** a headline of eight words or fewer, a sub-paragraph of twenty-five words or fewer, and one visual or one CTA. More has to earn its place.
- **No data dumps.** A twenty-row table on a marketing page is the wrong layout. Show the top three to five, link to the rest, or move the data to its own page.
- **Long lists need a different component, not a longer list.** Past five items, reach for a two-column split, a card grid, tabs, or a horizontal scroll rather than a bulleted list or a divided stack.
- **Spec sheets are the worst case.** A long table with a hairline under every row is the generated default for hardware and product briefs. Group into two or three clusters, or give each spec its own small card with the value set large and one line of why it matters.

## Quotes and testimonials

- **Three lines maximum.** If the original is longer, cut it. A quote on a page is a snippet.
- **Attribution is name, role, and optionally company.** Never a name alone.
- **Typographic quotes, or none.** Not straight ASCII quotes.

## Theme

- **One theme for the page.** If it's dark, every section is dark. A light section sandwiched between dark ones makes the reader feel they changed sites mid-scroll.
- The exception is a deliberate one-time theme switch as a composition device, with a real transition. Once per page.
- Tints within the same family are fine — a slightly darker panel next to a darker background. Flipping to a warm cream panel inside a near-black page is broken.
- Set the theme once, at the root. `safaii-css` owns the mechanism.

## Interactive states

Generated pages ship the successful state only. Every interactive element carries the full set:

- **Hover** — gated behind `@media (hover: hover)` so it doesn't stick after a tap.
- **Focus** — a visible `:focus-visible` ring in a token colour (`safaii-html`).
- **Active** — a small physical acknowledgement.
- **Disabled** — visually distinct, and only when genuinely unavailable.
- **Loading** — a skeleton matching the final layout, not a generic spinner.
- **Empty** — composed, and it says how to fill itself.
- **Error** — inline for forms, contextual for the rest.

A component with no empty, loading, or error state is unfinished.

## Forms

- **Label above the input.** Helper text optional but present in the markup. Error text below the input.
- **Never a placeholder as a label.**
- `safaii-html` owns the markup, validation, and announcement.

## CTAs

- **One label per intent.** "Get in touch", "Contact us", and "Let's talk" are the same intent — pick one and use it in the nav, the hero, and the footer. Same for sign-up and for portfolio intents. Two CTAs with the same intent on one page is a failure.
- **Button text fits on one line at desktop.** A wrapped CTA is broken. Shorten the label or widen the button.
- **Button contrast is checked** — no white on white, no transparent button with no border over a photo (`safaii-css` for the check).

## Images

- **A page is a visual product.** A page of nothing but type is not minimalism; it is unfinished work.
- **Source real images, in this order:**
  1. **The client's own assets** from `inventory-brief` — their photography, product shots, logo. Always preferred for anything that is evidence of the business: the work, the product, the team.
  2. **Generate the gaps** via `image-direction` — texture, atmosphere, background, and product context where the client has nothing. Never fabricated evidence: no invented product UI, no screenshot of something that does not exist, no generated stand-in for the actual work.
  3. **A labelled placeholder slot** — a TODO naming the placement and the size, so nothing ships with a silent gap.
- **Never** a fake screenshot built from styled divs, and never a hand-rolled decorative SVG standing in for a photograph.
- **Decorative or content.** Content images get meaningful alt text; decorative ones get `alt=""` (`safaii-html`).
- **Reserve the space.** Set `width` and `height` so the ratio holds before load.

## Mobile

- **Every multi-column layout declares its narrow fallback** in the same place as the wide one. Nothing relies on an assumption that it will wrap acceptably.
- **Asymmetric layouts collapse to a single column** below the narrow breakpoint.
- **The page reflows at 320px** without horizontal scrolling, and works at 200% zoom (`safaii-html`).
