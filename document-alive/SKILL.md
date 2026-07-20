---
name: document-alive
description: Bring a document website alive — propose and implement approved moments of scroll-driven life (CSS animation-timeline scroll()/view()) as a pure enhancement layer on a complete HTML document. Use when Matt wants a page to "come alive", asks for scroll animations, scroll-driven reveals, scrollytelling, reading progress, or wants an essay/album/document page to respond to scroll — and as the review mechanism whenever any scroll-driven animation is being considered. Scrollytelling, never scroll-cinema; the document stays the product.
---

# document-alive

The document-web inversion of scroll-cinema (Emons, Apple, scroll-world): there, the page is a film and the document is a hidden SEO mirror. Here, the document is the product — complete and readable with zero CSS and zero JS — and motion is an approved enhancement layer on top. Text primary; visuals annotate the reading.

**The one rule: nothing animates that wasn't approved.** This skill proposes, Matt decides, the default is zero. This is the safaii-css ask-first animation rule turned into a procedure — invoking the skill does not pre-approve any motion, and neither does a request naming a specific technique.

## Invariants (hard rules, no exceptions)

- **Enhancement layer only.** The page must be complete — same content, same order, fully readable — with CSS off, JS off, or the feature unsupported. An unsupported browser gets the finished document, not a degraded one; that's a success state.
- **Native scroll.** No scroll-jacking, no smooth-scroll libraries, no wheel handlers.
- **CSS-only patterns.** v1 animates with scroll-driven animations (`animation-timeline: scroll()`/`view()`); no JS, no dependencies, no polyfills.
- **Output lives in the project.** CSS goes into the project's own stylesheet in its `@layer` architecture (per safaii-css); markup edits follow safaii-html. Never injected styles, never script-built DOM.
- **Double-gated motion.** Every scroll-driven rule sits inside BOTH `@supports (animation-timeline: scroll())` (or `view()`) AND `@media (prefers-reduced-motion: no-preference)`. No exceptions, including "it's subtle."
- **Compositor-only keyframes.** Animate `opacity`, `transform`/`translate`/`scale`/`rotate`, `stroke-dashoffset`. Never layout properties (`width`, `height`, `top`, `margin`, `font-size`) — they jank and shift layout.
- **Hide enhancement-only elements by default.** An element that exists only for a motion pattern (a progress bar) is `display: none` in base CSS and shown *inside* the gates — otherwise unsupported browsers render a dead element.
- **Client projects:** this whole skill is one instance of the ask-first animation rule. Flag client use explicitly; own work and Lab projects are the default habitat.

## Procedure

1. **Read the document.** The page's template/HTML and its stylesheet. If the page isn't a complete document yet (content missing, structure unsettled), stop — motion comes after the document works, never before.
2. **Inventory candidates** against `references/patterns.md`. A candidate needs a *reader-side* reason: the text references something scrolled away (sticky-figure), the piece is long enough that position feedback helps (reading-progress), a figure's meaning unfolds in sequence (scrubbed illustration), an arrival deserves a beat (reveal).
3. **Propose 2–4 moments, maximum — and show the rejections.** Each proposal: **location** (which element/section), **pattern**, **purpose** — named from the closed list (*position feedback / referenced figure / sequential meaning / arrival beat*); "it would look good" is not on the list, and a candidate whose purpose can't be named in one of those four is dead — **exposure** (tier from the gate below), and **cost** (markup touched + rough CSS size). The proposal must also list **2–5 candidates considered and rejected**, each with the test that killed it — the rejections are what make the approval meaningful and what separates this from a motion wishlist. If nothing on the page earns motion, say so and stop — zero moments is a valid, complete outcome.
4. **Per-moment approval** (`AskUserQuestion`, multiSelect). Implement nothing before this. A partial yes implements exactly that subset.
5. **Implement approved moments only.** Markup per safaii-html; CSS per safaii-css into the project's layers (`components` for scoped patterns, keyframes at the top of the file with the other keyframes). Each moment is one self-contained block — deleting the block deletes the moment cleanly.
6. **Run the Checks** (below). Report pass/fail with the specific fix for each failure.
7. **Summarize:** what animates, where each block lives, and the one-line removal instruction per moment.

## The exposure gate

How much of the read a moment occupies sets how strict its test is — the document analog of the frequency gate in app-UI motion (adapted from Emil Kowalski's find-animation-opportunities):

| Exposure | Examples | Bar |
|---|---|---|
| **Persistent** (on screen the whole read) | reading progress | Strictest: near-imperceptible, information-bearing, never competing with the text |
| **Recurring** (fires many times in one read) | per-paragraph or per-item reveals | Reject by default — a page where everything animates is a slideshow, not a document |
| **Once per read** | a thesis-beat reveal, one scrubbed figure, one scrolly section | Where the whole budget lives |

## Support (triaged 2026-07 — re-verify when it matters)

`animation-timeline: scroll()/view()`: Chrome/Edge 115+ (2023), Safari 26+ (Sept 2025; progress-accuracy fixes through 26.5), **Firefox behind a flag in stable (on in Nightly; caniuse projects v155, ~Sept 2026)**. ~84% global. Not Baseline until Firefox ships — but it degrades to nothing (static document) behind the `@supports` gate, so per the safaii-css policy it's usable as a **gated enhancement** on personal/own projects now. Firefox users get the complete document until ~155. Verify at write-time via caniuse/webstatus.dev when a client decision hinges on it; the safaii-css `references/browser-support.md` row is the ledger entry.

## Checks

Run against the changed files after implementing. #1–#3 are greppable; #4–#6 are procedures.

| # | Check | Pass criteria | If fail |
|---|-------|---------------|---------|
| 1 | Double gate | Every `animation-timeline` declaration is inside both an `@supports (animation-timeline: …)` block and a `prefers-reduced-motion: no-preference` media block | Wrap it; no bare scroll-driven rules |
| 2 | Compositor-only keyframes | New/edited `@keyframes` contain no `width\|height\|top\|left\|right\|bottom\|margin\|padding\|font-size\|inset` declarations | Re-express with transform/opacity |
| 3 | No JS added | The diff introduces no `<script>` and no event handlers | Remove; v1 is CSS-only |
| 4 | Approved list | Every selector carrying `animation-timeline` maps 1:1 to an approved moment | Remove unapproved motion |
| 5 | No-CSS completeness | With the stylesheet disabled, the page shows the same content in the same order; no meaning delivered via CSS `content` | Move content into HTML |
| 6 | Enhancement elements gated | Any element existing only for motion is `display: none` in base CSS, shown inside the gates | Add the base hide |

Plus: the project's safaii-css Checks must still pass — this skill adds to a conventional stylesheet, it doesn't fork one.

## The tier above: video scrubbing

When a project genuinely wants the cinematic tier — a scrubbed hero video, a camera flight — that is a **separate, explicit ask** with real costs (asset production, page weight, device quirks). `references/video-scrub-ledger.md` documents the entire technique (seam doctrine, encoding, iOS/Low Power Mode traps) so the cost is known before choosing it. This skill never implements it silently.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Proposal argues "it would look great" | Decoration test, not reader test | Re-test: what does the reader lose if it's removed? If the purpose isn't one of the four named shapes — drop it |
| Proposal lists only survivors | Rejections section skipped | 2–5 considered-and-rejected candidates are required; restraint must be legible |
| Every list item / paragraph reveals on entry | Recurring-exposure motion slipped the gate | Recurring tier is reject-by-default (exposure gate) |
| Progress bar visible but static/full in Firefox | Element not hidden in base CSS | `display: none` base, `display: block` inside the gates |
| Content invisible in unsupported browsers | A `from { opacity: 0 }` start state leaked outside the gates (base style or ungated `animation` shorthand) | The hidden start state may only ever exist inside both gates |
| Reveal fires but text flashes before it | Missing `both` fill on a delayed/ranged animation | `animation-fill-mode: both` (see safaii-css motion craft) |
| Scrub feels janky | Keyframes animate layout properties | Compositor-only (Check 2) |
| Sticky figure overlaps footer / pins too long | No height relationship between figure and steps | Steps column drives height; figure `align-self: start` + `inset-block-start` offset |
| Motion plays for reduced-motion users | Single-gated rule | Both gates, always (Check 1) |
| Skill invoked on an unfinished page | Motion before document | Stop at step 1; finish the document first |
| Asked directly to "add X animation" without review | Direct phrasing treated as pre-approval | The proposal/approval step runs regardless of phrasing (same as safaii-css) |

## Examples / Status

v1 (July 2026), validated on a demo document (Target 1, scratchpad). First real target: the sace6 album experience — expect it to surface pattern gaps; fold them back into `references/patterns.md` and this file (skill-crafting flywheel). Origin: shaped from the scroll-world skill teardown — Lab card 10096845881 holds the pitch + PRD. Gate mechanics (named purpose, exposure tiers, required rejections) adapted from Emil Kowalski's find-animation-opportunities skill (July 2026) — his covers app-UI interaction motion; this covers document reading motion. One deliberate divergence: his reduced-motion stance is "gentler, not zero"; here reduced-motion is fully static, because the static document is a complete success state.
