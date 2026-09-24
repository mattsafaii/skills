# Site imagery

The photography, product shots, atmosphere, and texture that go into a page.

The job is not "make an image." It is "give this placement the image it needs, and make the whole page look like one shoot."

---

## Know the placement first

Every placement has a job. Write the prompt from the job, not from a vibe.

| Placement | Job | Aspect | Typical size |
|---|---|---|---|
| **Hero** | Carry the value proposition; the page's first impression | 3:2 or 16:9 | 1536×1024, 1792×1024 |
| **Product** | Show the actual thing, clearly | 1:1 or 4:5 | 1024×1024, 1024×1280 |
| **Product detail / macro** | Texture, material, craft, a close crop | 4:3 or 1:1 | 1024×768, 1024×1024 |
| **Context / atmosphere** | Place the work in the world — the site, the setting, the job | 3:2 or 16:9 | 1536×1024 |
| **Portrait / team** | A person, if the business genuinely needs one | 4:5 or 1:1 | 1024×1280 |
| **Texture / background** | A surface the page sits on; must not fight the text | 1:1, tileable | 1024×1024 |
| **Section band** | A wide strip behind a section | 21:9 or 3:1 | 1792×768 |

Match `size` to the placement. A square product shot cropped into a wide hero band is a wasted generation.

## The set is the unit of work

Do not write prompts one at a time. Decide the set first, then generate.

**Write the set brief before any prompt:**

- **The subject** — what this business actually is, from `inventory-brief` and the client's `Project Context`.
- **The light** — one lighting story for the whole set. Overcast daylight, hard afternoon sun, controlled studio, blue hour. Pick one.
- **The grade** — one colour treatment. Warm and filmic, cool and clean, high-contrast monochrome, muted and matte. Pick one.
- **The palette** — from the page's tokens. The images should sit inside it, not beside it.
- **The treatment** — how much the image is stylised. Documentary and unstyled, or art-directed and composed.
- **What is out** — the things that would break the set. People, branding, clutter, a competing colour.

Every prompt in the set repeats the light, the grade, and the palette. That repetition is what makes the page read as one world.

## Subject discipline

**From the business, never from the category.** A roofing company's hero is a roof, a ladder, the actual work, the actual neighbourhood. Not a generic office. Not a handshake. Not a person pointing at a laptop.

Read the client's facts first. If you cannot name what the business physically does, you cannot prompt its imagery.

**No stock-photo tells.** People looking at laptops, high-fives, generic handshakes, cliché robots, glowing abstract networks, a world map with pins, a plant on a desk.

**If a person appears**, they are doing the actual work, in the actual place, in the actual clothing for that job. Not posed, not smiling at the camera.

## The client's assets win

Check what exists before generating anything:

1. **The client's own photography** — from `inventory-brief`, their site, their brand assets. Always preferred.
2. **Generate the gaps** — texture, atmosphere, a missing product angle, a background.
3. **A labelled placeholder** — if generation is unavailable or refused, leave a TODO naming the placement and size.

Generating a hero when the client has a real photograph of their own work is a downgrade. The real one is proof; the generated one is decoration.

## Prompt template

```
[Subject and action, concretely]. [Setting and context].
[Light]. [Grade and palette]. [Treatment and composition].
[What is excluded]. No text, no logos, no watermarks.
```

**Worked example — a roofing company's hero:**

```
A two-storey house with a new shingle roof, a ladder against the gable and
a worker mid-installation on the slope, in a quiet residential street.
Overcast late-afternoon daylight, soft and even.
Muted natural palette — warm grey shingles, deep green foliage, cool sky.
Documentary treatment, shot from street level, wide composition with room
for headline text on the left. No text, no logos, no watermarks.
```

Note what the prompt does: it names the trade, the setting, the light, the grade, the treatment, the composition (with space for the headline), and what to leave out. It does not say "professional," "premium," "stunning," or "high quality" — those words produce nothing.

**Words that do work:** the subject, the light, the palette, the lens and framing, the treatment, the exclusions.
**Words that do not:** beautiful, stunning, premium, professional, high quality, 8k, masterpiece, trending.

## Textures and backgrounds

- **The text has to survive on it.** A texture behind a headline must be quiet enough that the headline reads. Ask for low contrast, a single tone, or generous empty areas.
- **Tileable when it will tile.** Say "seamless tileable pattern" if the placement repeats.
- **Never a competing subject.** A background with a subject in it becomes a competing hero.

## After generation

- **Review through `vision`.** Ask specifically: does it match the palette, is the light consistent with the rest of the set, is there any text or logo that should not be there, is the subject actually the business.
- **Alt text** — a content image describes its meaning; a decorative one gets `alt=""` (`safaii-html`).
- **Set `width` and `height`** so the ratio reserves space before load.
- **Compress** before it ships. A generated PNG is often far larger than the placement needs.
