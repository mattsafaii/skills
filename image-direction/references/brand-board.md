# Brand boards

An identity overview deck rendered as one image: logo, construction, applications, palette, type, and atmosphere, arranged on a presentation canvas.

A board is not decoration. It is a visual argument for why the brand exists. Every panel answers one of: what does this stand for, what is the metaphor, how does the mark express it, how does the system scale, why is it ownable.

A board is a **concept artifact**. It is not a mark file, not tokens, not a type stack. For a mark as a finished asset, `us-graphics` produces the artifact and the rationale.

---

## Strategy before panels

Infer the brand's position before writing the prompt:

- **Category** — what business is this.
- **Audience** — who has to trust it.
- **Function** — what the product or service actually does.
- **Promise** — the emotional return.
- **Position** — where it sits in its market, and against whom.
- **Trust level** — a compliance tool and a games brand earn trust differently.
- **What it must avoid** — the space it must not look like.

The visual system follows from that. A mark chosen before the strategy is a guess.

### Category to symbol

A starting point, not a lookup. Steal from the field the brand actually belongs to.

| Category | Ideas | Possible symbols |
|---|---|---|
| Developer tool | building, speed, precision, control | cursor, frame, bolt, scaffold, grid |
| AI assistant | delegation, intelligence, clarity | spark, orbit, signal, node |
| Security | protection, vigilance, boundary | shield, eye, seal, protected core |
| Gaming | chance, reward, tension, speed | dice, gem, card, trophy |
| Voice / audio | sound, rhythm, flow | waveform, mic, orb, speech path |
| Compliance | trust, order, rules | seal, badge, document, stamp |
| Drone / robotics | flight, control, vision, mission | wing, crosshair, path, zone |
| Productivity | focus, momentum, clarity | path, check, block, calendar |
| Luxury / editorial | material, ritual, restraint | monogram, seal, emboss, refined mark |

## Layouts

| Layout | Use |
|---|---|
| `3 × 3` | Full identity system — the default |
| `2 × 3` | Cinematic mini-deck |
| `2 × 2` | Compact concept board |
| `1 × 3` | Horizontal brand strip |
| `4 × 2` | Wide contact sheet |

Default canvas: `1536×1024` (3:2) or `1792×1024` (16:9). A board needs width.

### The 3 × 3 panel system

1. **Logo cover** — the mark and wordmark, large, with real negative space.
2. **Construction** — the geometry or negative-space logic behind the mark.
3. **Digital application** — browser chrome, app header, a UI fragment, an app icon.
4. **Brand essence** — one short line of type, sparse.
5. **Colour system** — swatches, a ramp, chips, or a palette card.
6. **Typography** — a specimen, an alphabet row, or the pairing.
7. **Physical application** — a card, badge, label, seal, or packaging mockup.
8. **Image direction** — the brand's photographic world in one panel.
9. **System detail** — chips, an input bar, an icon row, a pattern.

### The 2 × 3 mini-deck

1. Logo / wordmark — minimal
2. Product surface — a browser bar or app frame
3. Functional panel — a command, an input state, a dashboard fragment
4. Atmosphere — a campaign or landscape image
5. Symbol / construction / badge
6. Tagline — one line, large, quiet background

### Panel rhythm

Do not make every panel loud. Plan the sequence: quiet, functional, emotional, technical, atmospheric, detailed. A board where every panel shouts reads as noise.

## The mark

**Qualities:** simple, memorable, symbolic, scalable, ownable, balanced, connected to the idea, and usable as an icon, a wordmark, a badge, and a pattern.

**Avoid:** generic lightning bolts, random animals, fake luxury crests, marks copied from famous brands, overcomplicated symbols, clipart, meaningless sparkles, and inconsistent variants across panels.

### Concept methods — use one, or combine at most two

1. **Monogram plus meaning** — the initial combined with a metaphor. Use negative space, cuts, or folds. Not a letter in a circle.
2. **Product action** — the thing the product does, abstracted. Build becomes a frame or a scaffold; protect becomes a boundary; speak becomes a waveform.
3. **Metaphor fusion** — two ideas reduced into one mark. Owl and drone vision. Shield and mountain. Dice and a mobile economy.
4. **Negative space** — a hidden arrow, a protected centre, a cutout initial, a folded corner.
5. **Construction geometry** — a mark from a clear system: circles, diagonals, a grid, modular blocks, orbital paths.

**State the concept in the prompt.** "A monogram K built from a folded frame, suggesting structure" beats "a modern logo."

## Visual modes

Pick from the brand's category and audience, then hold it across every panel.

**Dark technical** — near-black, monospace accents, command lines, terminal frames, subtle grid; cyan, blue, coral, or lime. For developer tools, infra, automation.

**Dark operational** — black with amber or red, glowing chips, card systems, progress motifs. For business tools, growth, sales.

**Dark calm** — deep green, lime accent, misty landscape, soft overlays. For strategy, wellness, climate, quiet SaaS.

**Dark security** — black or navy, shield forms, radar lines, alert chips, controlled gradients. For security, compliance, monitoring.

**Light editorial** — warm ivory, paper, small serif labels, seals and badges, calm stationery; deep blue, red, gold. For legal, privacy, compliance, trust.

**Luxury** — ivory, stone, espresso; serif wordmark, monogram, paper grain, embossing, editorial crops. For beauty, fashion, hospitality, premium services.

**Voice** — dark indigo, waveform, mic motif, command input, app icon. For voice, chat, audio.

**Cultural** — halftone, CRT texture, analog print, one bold accent, poster panels. For music, creative tools, events.

## Text

Keep it sparse. Type in a generated image is the weakest part of the output.

**Good:** the brand name, one tagline, one URL, one command, two to five section labels, short UI chips.

**Bad:** paragraphs, fake body copy, long menu lists, lorem ipsum, dense explanations, tiny unreadable labels.

## Taglines

Short and specific.

**Good:** "What will you build today?" · "Nothing random." · "Your network. Our watch." · "Every mission under control."

**Avoid:** corporate slogans, long copy, buzzword soup, fake inspiration.

## Colour

One dominant palette: a base, a primary accent, a secondary accent, and neutrals. Accents repeat across panels. No rainbow unless asked. One accent can carry the whole system.

## Anti-generic

Never produce: random floating icons, generic startup gradients, overdesigned marks, meaningless blobs, messy collages, fake tiny UI, inconsistent marks, too many colours, cheap neon, or a corporate slide deck.

Make it quieter, sharper, and more intentional.

## Prompt template

```
A brand identity overview board for "[BRAND NAME]" — a [category] for [audience].

Strategy: [personality], built on [core metaphor]. The mark is [concept: monogram +
meaning / product action / fusion / negative space / construction].

Layout: [3×3] grid on a [canvas] with strong gutters, clean alignment, and generous
negative space.

Panels: logo cover · construction · digital application · brand essence · colour
system · typography · physical application · image direction · system detail.

Visual mode: [mode].

Palette: [base, primary accent, secondary accent, neutrals].

Type: [sparse, large, high hierarchy]. Minimal text only — the brand name, one
tagline, a few section labels. No paragraphs, no tiny fake text.

No copied real-world logos, no stock template board, no clutter.
```

**Worked example — a security monitoring service:**

```
A brand identity overview board for "Meridian" — a network security service for
mid-size companies.

Strategy: vigilant, precise, calm under pressure, built on the idea of continuous
watch. The mark is a shield reduced to a watchful core — a boundary with an eye
formed by the negative space at its centre.

Layout: 3×3 grid on a 1536×1024 near-black canvas, strong gutters, clean alignment.

Panels: logo cover · construction · monitoring dashboard fragment · brand essence ·
colour system · typography · badge mockup · radar atmosphere · alert chip row.

Visual mode: dark security — black and navy, radar lines, controlled gradients,
red and blue alert chips.

Palette: near-black base, steel blue primary, alert red secondary, cool grey neutrals.

Type: sparse and large. Brand name, the line "Your network. Our watch.", a few
section labels. No paragraphs, no tiny fake text.

No copied real-world logos, no stock template board, no clutter.
```

## After generation

- **Review through `vision`** — ask whether the mark reads at small size, whether the panels have rhythm, whether any panel contains text that should not be there, and whether any mark resembles a real company's.
- **A mark from a board is a direction, not an asset.** Redraw it as vectors before it ships. Route to `us-graphics` for the finished artifact.
- **Do not reuse a board's mark across brands.** Each board gets its own concept.
