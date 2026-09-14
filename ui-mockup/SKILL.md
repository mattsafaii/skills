---
name: ui-mockup
description: Mock up one UI feature as several genuinely different variations in a single self-contained HTML file, opened in the browser, so Matt can compare them and pick a winner before it's built for real. Use when Matt wants to explore how a feature should look or behave, compare UI options, says "mock this up", "show me variations", "mock this up a few ways", or "/ui-mockup".
triggers:
  - mock this up
  - show me variations
  - design a few options
  - /ui-mockup
---

# UI mockup

Instead of one-shotting a UI and hoping it's right, build **several genuinely different takes** on one feature in **one self-contained HTML file**, shown side by side as tabs. Matt flips between them and picks a winner. Only then is it built for real in the project.

The file is throwaway — vanilla HTML/CSS/JS, no build, no CDN, no framework, double-click to open. The decision is the deliverable.

## Different answers, not different tints

Takes that differ only in accent color teach nothing — you flip between them, see no real choice, and the run is wasted.

Each take is a different **answer to the same brief**, on one **primary axis**:

| Axis | What varies |
| --- | --- |
| Structure | Grouping, order, column count, what collapses |
| Density | Spacing scale, hit areas, how much fits |
| Emphasis | Where filled color goes, what recedes |
| Type | Scale steps, weight contrast, measure |
| Voice | Labels, tone, how much copy |
| Interaction | The model itself — slider vs steppers vs presets vs popover |

Pick **one primary axis** and give each take a different position on it. Secondary choices follow from it rather than varying on their own — a dense take may need a smaller type step, and that is coherence, not a second axis. Vary every axis at once and you learn which you liked, not what made it work.

## The floor every take clears

A take that wins on looks and fails on the basics is a bug with a nice surface. Before it enters the file, each take clears:

- Every control has an accessible name.
- Keyboard reaches everything a pointer does.
- Focus is visible.
- Nothing clips at 320px.
- No meaning rides on color alone.

The floor is identical across takes. It is not an axis and never trades against one. Where a direction can only work by breaking it, say so and drop the direction.

## 1. Scope one piece

One feature per run — "the grid-density control", "the empty state", "the save toast". Not a whole screen; if Matt hands you something page-sized, ask which piece to mock up first.

Restate the brief in one sentence: what it is, where it renders, what it has to do.

## 2. Learn the ground

The takes have to look like they could ship tomorrow, so read what they stand on:

- The project's CSS and token layer (`safaii-css` for the house conventions), component library, motion library.
- Color, spacing, radius, type scale, easing.
- The product's density and voice.
- Where the piece lives — what background, which neighbours, which widths.

No project context? Use neutral grays, one accent, and the system font stack, and say that is what you did. (`assets/template.html` ships that neutral shell.)

## 3. Name the axis before writing code

Write the set down first — a name and an axis position each. Names say the direction: `Quiet`, `Editorial`, `Dense`, `Stepped` — never `Option A`.

Default to **5**; drop to 3 when the space is narrow, and cap at 5 — past five, nobody compares, they scroll. Done when no two takes share a position and you can state each one's axis in a phrase. If two come out nearly identical, that is a wasted slot — replace one with a more distant idea.

## 4. Build the file

- **One file, no dependencies.** Self-contained `.html`, vanilla HTML/CSS/JS — no build, no CDN, no framework. Double-click to open.
- **Vanilla CSS** (matches the stack rules). No Tailwind, no CSS-in-JS.
- **Tabs across the top, keys 1–5** switch takes. Use `assets/template.html` as the shell — fill in the panels, keep the tab bar, the keyboard nav, and the neutral chrome so the takes are what stands out.
- **Real content, shared across every take**, so the comparison is apples-to-apples: product-shaped copy, plausible names, and the item count the page will really carry. Lorem ipsum and three rows make every structure look good.

## 5. Save and open

- Write to `prototypes/<feature-name>.html` in the current project (create `prototypes/` if needed). No project context → `/tmp`.
- Open it: `open prototypes/<feature-name>.html`.
- Tell Matt which key flips it and which width you judged at — the answer can change between 375px and 1440px.

## 6. Present the tradeoffs and hand over

Flip through every take yourself first: each renders, each interaction responds, the console is clean. Then present a table and mark no favourite:

| Take | Axis position | Right when | Costs |
| --- | --- | --- | --- |
| Quiet | Lowest visual weight | The piece is used daily | Least memorable |
| Editorial | Largest type, most space | The moment deserves weight | Eats vertical space |

Asked directly which you would pick, answer from how often the piece is seen and the product's personality — not from which one you enjoyed building.

## 7. Promote one, keep the file

On a choice: build that take **for real** in the project — proper components, real data, the project's own CSS architecture, wired to real state. Don't carry over prototype shortcuts (inline styles, fake data, magic numbers). Leave the HTML in `prototypes/` as a record unless Matt says delete it.

Asked for another round instead, keep the file and run step 3 again, taking new positions around the direction he leaned toward.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Takes feel like reskins of one idea | They differ in color/spacing, not position on the primary axis | Give each a distinct axis position; merge or replace near-duplicates |
| Every axis varies at once | No primary axis chosen | Vary one and let the rest follow from it |
| The file won't open on double-click | A build step, CDN, or dependency snuck in | Keep it one self-contained `.html` — vanilla HTML/CSS/JS only |
| Comparison feels unfair or hard to judge | Takes use different content | Share the same realistic content across every take |
| A take looks great but breaks keyboard or focus | The floor was skipped | Clear the floor or drop the direction |
| A favourite marked in the table | Not the agent's call | State each take's cost and let Matt choose |
| The real build inherits prototype shortcuts | Inline styles, fake data, or magic numbers copy-pasted | Rebuild for real with the project's CSS architecture and real data |
| Scope quietly grows to a whole screen | Started building before pinning a piece | Ask which piece to mock up first |
| Picker chrome fights the takes | The shell got styled with the product's tokens | Keep the shell neutral so the takes stand out |

## Status

Behavioral evals live in `evals/evals.json` — they test whether this skill *steers* an agent to the conventions (a test of the skill, not a consumer to keep in sync). Not part of normal mockup work; run them via the skill-crafting tooling when changing the conventions, and add an eval when a new failure mode lands.
