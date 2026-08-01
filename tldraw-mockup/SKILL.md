---
name: tldraw-mockup
description: Mock up a UI feature as several distinct variations in one self-contained HTML file, side-by-side, so Matt can pick the winner before it gets built for real. Use when Matt wants to explore how a feature should look or behave, compare UI options, says "mock this up", "show me variations", "mock this up a few ways", or "/tldraw-mockup".
triggers:
  - mock this up
  - show me variations
  - design a few options
  - /tldraw-mockup
---

# Prototype Skill

Instead of one-shotting a UI and hoping it's right, generate **5 genuinely different takes** on a single feature in **one self-contained HTML file**, shown side-by-side as tabs. Matt picks the winner. Then — and only then — build it for real in the project.

The point is cheap, fast comparison. The HTML is throwaway. The decision is the deliverable.

## Workflow

### 1. Pin down the feature

One feature, not a whole screen. "The grid-density control," "the empty state," "the date picker," "the save toast." If Matt hands you something page-sized, ask which piece to prototype first.

Get just enough to design against:
- What does it do / what does the user accomplish with it?
- Where does it live (what surrounds it)?
- Any hard constraints (must fit a toolbar, touch-friendly, etc.)?

Don't over-interview. One or two questions max, then build.

### 2. Generate the variations

Default to **5**. Each must be a **genuinely different approach**, not a recolor. Different interaction model, different layout, different mental model — like the demo's grid-density control: refined slider / stepped notches / density presets / zoom stepper / grid-size popover. Five real answers to the same question.

Give each variation:
- A short **name** (2-3 words) and a one-line **note** on the tradeoff ("Fastest for power users," "Most discoverable," "Smallest footprint").
- A **live, interactive** implementation — real hover/click/keyboard behavior, not a static picture. The whole point is to feel it.

Rules:
- **One file, no dependencies.** Self-contained `.html` — vanilla HTML/CSS/JS, no build, no CDN, no framework. Double-click to open.
- **Vanilla CSS** (matches Matt's stack rules). No Tailwind, no CSS-in-JS.
- Variations share the same fake content/data so the comparison is apples-to-apples.
- Keep the chrome neutral so the variations are what stands out. Use `assets/template.html` in this skill as the shell — fill in the five panels, keep the tab bar and keyboard nav.

### 3. Save and open

- Write to `prototypes/<feature-name>.html` in the current project (create `prototypes/` if needed). If there's no project context, use `/tmp`.
- Open it: `open prototypes/<feature-name>.html`.
- Tell Matt: tabs across the top (or keys 1-5) switch variations; the note under each tab explains the tradeoff.

### 4. Matt picks; you build it

Once Matt names the winner ("go with 3" / "the stepped notches one"):
- Build that variation **for real** in the actual project — proper components, real data, the project's CSS architecture (`@layer config, reset, elements, components`), wired to real state.
- The prototype was throwaway. Leave the file in `prototypes/` as a record unless Matt says delete it.
- Don't silently carry over prototype shortcuts (inline styles, fake data, magic numbers) into the real build.

## Notes

- If Matt asks for a different count ("just give me 3"), honor it.
- If two variations end up nearly identical, that's a wasted slot — replace one with a more distant idea.
- This is for *look and behavior* — UI variations, not code/API interface shape.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| The 5 variations feel like reskins of the same idea | They differ in color/spacing, not interaction model or layout | Force a genuinely different mental model per variation; merge/replace near-duplicates |
| The file doesn't open or breaks on double-click | A build step, CDN import, or external dependency snuck in | Keep it one self-contained `.html` file — vanilla HTML/CSS/JS only |
| Comparison feels unfair or hard to judge | Variations use different fake content/data | Share the same fake content across every variation |
| The real build inherits prototype shortcuts | Inline styles, fake data, or magic numbers were copy-pasted from the throwaway file | Rebuild for real with the project's CSS architecture and real data — don't carry over prototype code |
| Variations are hard to compare visually | Didn't use the shared `assets/template.html` shell | Use the template; keep the chrome neutral so the variations stand out |
| Scope quietly grows to a whole screen | Started building before pinning down a single feature | Ask which piece to prototype first when handed something page-sized |

## Status

Behavioral evals live in `evals/evals.json` — they test whether this skill *steers* an agent to the conventions (a test of the skill, not a consumer to keep in sync). Not part of normal prototyping work; run them via the skill-crafting tooling when changing the conventions, and add an eval when a new failure mode lands.
