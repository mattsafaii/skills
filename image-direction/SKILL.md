---
name: image-direction
description: Decides what images a project needs and writes the prompts that produce them. Two modes — site imagery (hero, product, atmosphere, texture for a page) and brand boards (identity overview decks). Derives the art direction from the project's Design Read and palette, then calls gpt_imagegen with the right size and output path. Use when a page needs real imagery, when a build reaches the point where photography or texture has to exist, when a section needs a background or product shot, or when someone wants a brand-kit or identity overview board. Not for a logo as a final asset — that's us-graphics; a board is a concept artifact.
---

# image-direction

Decides what images a project needs, and writes the prompts that produce them.

Two modes:

- **Site imagery** — the photography, product shots, atmosphere, and texture that go into a page.
- **Brand boards** — an identity overview deck: logo, construction, mockups, palette, type, as one presentation image.

Direction comes from the project, not from a house look. The prompt carries it.

Where it sits: `page-design` sets the Design Read, the palette, and the dials; this skill turns them into images. It runs during build, once the structure and copy exist and the imagery has to become real.

## Delegation

| Concern | Owner |
|---|---|
| The page's direction, palette, and dials | `page-design` |
| CSS, tokens, oklch values | `safaii-css` |
| Markup, alt text, responsive images | `safaii-html` |
| A mark as a finished asset | `us-graphics` |
| Looking at what came back | the `vision` subagent |

**A board is a concept artifact, not a mark.** For a real logo, `us-graphics` produces the artifact and the rationale. This skill produces a picture of a direction.

## The tool

`gpt_imagegen({ prompt, outputPath, provider, model, size, quality, outputFormat, referenceImages })`.

- **`outputPath`** — relative paths resolve against the session directory, and **an existing file is never replaced**. So it cannot overwrite; choose a new name, or clear the old file first if you mean to replace it.
- **`provider`** defaults to `openai`; **`model`** defaults to that provider's default. **`size`** is `WIDTHxHEIGHT` on OpenAI models — match the placement, not a default. **`outputFormat`** is `png`, `jpeg`, or `webp` on OpenAI, `png` or `jpeg` on Gemini.
- **`referenceImages`** — passing local images switches to the edits endpoint, and the prompt becomes the edit rather than a fresh generation. This is how you fix a specific image or build a variant that must match one.

**Look at what comes back.** The primary model cannot see images. Route the result to the `vision` subagent (`vision-cloud` if the local one is slow) with what you asked for and what to check. Never ship an image nobody has looked at.

## Shared craft

Every prompt in both modes obeys these.

**Direction first.** The image serves the Design Read. Read it before writing a prompt. An image that contradicts the page's palette or mood is worse than no image.

**Real assets first.** The client's own photography, product shots, and logo come first, always. Generate where they have nothing: texture, atmosphere, background, product context, abstract material. A generated hero photo untethered from the actual business reads as a stock photo, and a stock photo reads as a page nobody cared about.

**No fabricated evidence.** Do not generate a screenshot of a product that does not exist, a dashboard, a terminal, a review, a testimonial, or another company's logo. If the product is real, show the real thing. This is the same rule `page-design` carries.

**Text in a generated image is a liability.** Image models render type badly, and small labels turn to mush. Keep it to a brand name and one short line at most. Never paragraphs, menu items, fake body copy, or a wall of tiny labels. If a piece needs real text, generate the image without it and set the text in the page.

**Palette discipline.** One dominant palette, taken from the page's tokens. Accents repeat across a set. No rainbow, no generic purple-blue glow, no neon.

**Anti-generic.** No stock people at laptops, no cliché robot or handshake imagery, no floating unrelated icons, no meaningless blobs, no overbusy scenes, no cheap glossy mockups, no corporate-slide look.

**Consistency beats novelty.** A set of images for one project must look like one shoot — same light, same grade, same palette, same treatment. Assembled-from-anywhere is the failure mode.

---

## Mode 1 — Site imagery

The full treatment is in `references/site-imagery.md`. The short form:

- **Know the placement before writing the prompt.** Each placement has a job, a crop, and an aspect ratio. A hero is wide; a product shot is square or portrait; a texture tiles.
- **One image per placement, one shoot across the set.** Decide the light, the grade, and the palette once, then hold them across every image in the page.
- **Subject from the business, not from a category.** Read `inventory-brief` and the client's `Project Context`. A roofing company's hero is roofs, ladders, and the actual work, not an office.
- **The client's assets win.** Generate only the gaps.
- **Alt text is not optional** — every generated content image gets real alt text, per `safaii-html`.

## Mode 2 — Brand boards

The full treatment is in `references/brand-board.md`. The short form:

- **A board argues for the brand, it does not decorate.** Every panel answers: what does this stand for, what is the metaphor, how does the mark express it, how does it scale.
- **Default layout is a 3×3 grid**, on a presentation canvas with real gutters. Other layouts (`2×3`, `2×2`, `1×3`, `4×2`) suit different needs.
- **The mark is simple, symbolic, and ownable** — and its concept is stated, not implied. The concept methods are in the reference.
- **Panels have rhythm** — quiet, functional, emotional, technical, atmospheric. Not every panel is loud.
- **Pick a visual mode** (dark technical, light editorial, luxury, cultural, and others) from the brand's category and audience, and hold it across every panel.
- **Keep the text sparse.** Brand name, one tagline, a few section labels, one command or URL.

---

## Pre-flight

- [ ] The mode is decided — site imagery or brand board?
- [ ] The Design Read and palette were read first, and the prompt matches them?
- [ ] The client's real assets were checked before generating?
- [ ] `size` matches the placement?
- [ ] `outputPath` is a new name, or the old file was cleared?
- [ ] Text in the image is a name and at most one short line?
- [ ] The palette is one dominant set, accents repeated?
- [ ] No fabricated product UI, screenshot, testimonial, or third-party logo?
- [ ] Site imagery: the whole set shares one light, grade, and palette?
- [ ] Brand board: the mark's concept is stated, and the panels have rhythm?
- [ ] The result was reviewed through the `vision` subagent?
- [ ] Content images have real alt text (`safaii-html`)?

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The image looks like stock | No direction taken from the Design Read; generic subject | Re-read the direction and `inventory-brief`; prompt the actual business |
| The set looks assembled from different sources | Consistency was not decided up front | Fix light, grade, and palette once, then regenerate the outliers |
| Text in the image is unreadable | Too much text asked of the model | Strip to a name and one line; set real text in the page |
| A fake product UI appeared | The prompt implied a screenshot | Describe the real product, or drop the preview |
| The mark is generic | No concept behind it | State the metaphor and use a concept method; or route to `us-graphics` for the real asset |
| Every panel is loud | No rhythm planned | Decide which panels are quiet and which carry the idea |
| An image shipped unviewed | Skipped the vision pass | Route it to `vision` before it reaches the page |
| `gpt_imagegen` returned null or refused | Output path exists, or the prompt tripped a policy | Never replaces an existing file — pick a new name; rephrase a policy-tripping prompt |

## References

- `references/site-imagery.md` — placements, aspect ratios, set consistency, prompt templates
- `references/brand-board.md` — board layouts, panel system, mark standard, visual modes, prompt template
- `page-design` — the direction this serves; `us-graphics` — marks as finished assets
