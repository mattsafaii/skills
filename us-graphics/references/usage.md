# DX-203 — When to use the USGC skills

U.S. Graphics Company office reference. Not a brand book.

Two skills. Same office. Different job.

| Skill | Job | Load when |
|---|---|---|
| `us-graphics` | Form. Marks, layout, type, chrome, critique. | The thing has a silhouette, a grid, or a visual decision. |
| `us-graphics-voice` | Words. Names, strings, mail, commits, slogans. | The thing has a noun or a verb. |

If it has both (landing page, package, identity), use both. Words first, silhouette second. RAMTRON standard — mark + wordmark + name as one system.

---

## Quick pick

| You have | Use |
|---|---|
| A logo, icon, lockup, or “does this mark work” | `us-graphics` |
| A poster, datasheet, bulletin layout, slide, label | `us-graphics` |
| Type choice, UI chrome, motion, density | `us-graphics` |
| “What would US Graphics think of this graphic” | `us-graphics` |
| UI copy, errors, buttons, empty states | `us-graphics-voice` |
| Product / program / file / commit / branch names | `us-graphics-voice` |
| Email, bulletin, README, changelog, spec English | `us-graphics-voice` |
| “De-slop this” / IBM-engineer test | `us-graphics-voice` |
| Full identity or a landing page | both |
| A spreadsheet, a compiler flag, a legal clause | neither |

---

## `us-graphics` — scenarios

### Marks and identity

- Score an existing mark with the eight tests (silhouette, SNR, reduction, one-color, domain, construction, name, time).
- Propose at most two directions — Wyman band and C&G band — not twelve moods.
- Lock mark + wordmark + name. Kill the rounded-square container.
- Decide whether a refresh is earned (name changed, mark fails SNR) or calendar-driven (Eaton: nothing is broken).

Prompts

- Run the eight tests on this mark.
- Two directions only. Silhouette first.
- What would USGC refuse here?
- Lockup for one-color, reverse, and 16 px.

### Layouts and documents

- Art-direct a poster, datasheet, bulletin, packaging stamp, or slide.
- Density, hairlines, registration, part numbers as framing when the piece is documentary.
- Black / white / one hard accent. No fake paper unless it is actually a bulletin.

Prompts

- Layout this as a USGC bulletin, not a Dribbble shot.
- Dense, not sparse. Show the grid.

### UI and chrome

- Static over kinetic. Visible nav. No hamburger-as-ideology.
- Motion only if short, mechanical, reversible.
- Color as named function, not a generated palette.
- Type job when you cannot license Berkeley Mono — name the job, then pick a public face that does that job.

Prompts

- WWUSGD on this settings screen.
- Kill the animation. What stays.

### Critique

Verdict first — pass / salvageable / fail — and which test broke. Name the ancestor (Rand, C&G, Cognex, NASA worm) or the contaminant (Design Communism, 2016 thinning, Liquid Glass). Say what to keep. Give one next move.

Do not use this skill to draw production vectors. It judges. A drawing program still draws.

---

## `us-graphics-voice` — scenarios

### UI strings

- Replace slop with specification English. Transfer Funds, not Move Money. Error, not Oops. Program, not App. Release, not Ship.
- Buttons are verbs. Failures do not grin.
- Empty states may be dry. They may not be kawaii.

Prompts

- De-slop this screen. Edit list only.
- Keep Fatal Error. Do not invent theater.

### Naming

- Products, device lines, programs, slogans.
- Files, scripts, directories, functions, commits, branches.
- Test: the word a 1972 IBM engineer would write in a specification. `deploy_dashboards.sh`, not `push_dashboards.sh`.
- House grammar if you want USGC catalog flavor: TX-02, BT-014, ER-204, `read. match. record.`
- Two or three names, not twelve. State what was refused.

Prompts

- Name this. Two options. IBM test.
- Rename these files and commits. Table only.
- Slogan as a verb/noun triad.

### Mail and documents

- Bulletins and customer mail in office register. Date, number, news. Allies and partners, not the community.
- README, changelog, license page, spec.
- Agent instructions (CLAUDE.md and cousins) so the model stops writing slop.

Prompts

- Draft BT-015 for this release.
- Rewrite this README. Strike slop first.
- Add a Naming section like Neil’s CLAUDE.md.

Do not use this skill for legal copy, medical copy, or ads that must sound like ads.

---

## Both — scenarios

Do the words first so the mark has a name to lock to.

| Job | Order |
|---|---|
| New identity | Name + triad → two silhouettes → lockup |
| Landing page | Hero and strings → layout and type |
| Package / device stamp | Part name + slogan → stamp geometry |
| Release | Bulletin copy → accompanying graphic |
| Competitor teardown | Eight tests + slop table in one pass |
| Repo + site together | Voice on the repo, visual on the chrome |

Prompts

- WWUSGD on this landing page — words and form.
- Full lockup. RAMTRON standard.
- Name it, then score the current mark.

---

## How to run them so they stay useful

1. One repo or one mark first. Not the whole company.
2. Ask for an **edit list** or a **scorecard**, not a surprise rewrite.
3. “Strike slop / fail the test / do not invent theater.”
4. Keep a short before/after (10–20 strings, or one mark at four sizes).
5. If the skill adds kitsch you did not ask for, the prompt was too loose — tighten, do not throw out the skill.

---

## What they will refuse on purpose

- Rounded-square icons, circle plates, even-weight 2016 thinning
- “You’re in!”, “Got it!”, “Ship it”, “Inspo”, “Unlock your journey”
- Twelve logo options, twelve names
- Emoji in professional chrome
- Calendar-driven refreshes
- Claiming Berkeley Mono is free to embed
- Softening a Fatal Error

That refusal is the product.

---

## File map

| File | What it is |
|---|---|
| `us-graphics/SKILL.md` | Visual doctrine |
| `us-graphics/references/logo-doctrine.md` | SNR, silhouette, Wyman–C&G |
| `us-graphics/references/case-law.md` | Cognex, Eaton, Sun, NASA worm |
| `us-graphics/references/worked-examples.md` | Dell fail, RAMTRON pass |
| `us-graphics-voice/SKILL.md` | Language doctrine |
| `us-graphics-voice/references/slop-lexicon.md` | Specification vs slop |
| `us-graphics-voice/references/naming.md` | IBM test, catalog grammar |
| This file | When to use which |

Install both skill folders. Point at a real file. Gate a rename or a redraw before you spend the week.
