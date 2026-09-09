---
name: devtool-page
description: Build the small landing page for one of Matt's dev tools (scry, zeni, tribunal, garp, or any new CLI/gem) — one static HTML page, Safaii house look, real terminal output as the centerpiece. Triggers on "landing page for X", "make a page for [tool]", "site for my CLI/gem", "devtool page", "/devtool-page". Not for client sites (safaii-css + /build own those) or content sites (garp/11ty).
---

# devtool-page

One small static page per tool. Same skeleton every time; only the accent changes. The page's job is one thing: get a developer from promise → install command in under ten seconds.

**Delegates, never duplicates:** all CSS conventions come from [[safaii-css]] (starter.css, layers, oklch, `@scope`, Checks); markup conventions from [[safaii-html]]. This skill owns only what is specific to a dev-tool page: anatomy, the install-command CTA, and the terminal-artifact rule.

## Workflow

1. **Preflight** — ask only what changes the output, batched into one message:
   - Tool name + one-line promise in plain words (what it does, for whom)
   - Exact install command (`go install …`, `gem install …`, `brew install …`)
   - Accent hue for this tool (one oklch hue; each tool gets its own)
   - Repo URL, public or private (private → GitHub link becomes "source available on request" or is dropped; never link to a 404)
2. **Capture real output.** Run the actual tool once and paste its real output into the terminal block. Never invent output, metrics, star counts, or testimonials. If the tool errors when you run it, show the error path to Matt instead of fabricating a happy path.
3. **Scaffold** — `index.html` + `css/style.css` in the tool repo's `site/` dir (or a standalone repo if Matt says so). Copy `references/starter.css` as the stylesheet.
4. **Config** — fill starter tokens: `--color-accent` set to the tool's hue (P3 boost per [[safaii-css]] where it earns it), `--font-body: var(--font-sans)` (sans, not the serif document default — these are product pages, not essays).
5. **Build the sections** per `references/page-anatomy.md`.
6. **Run both Checks tables** — this skill's below, then [[safaii-css]]'s.

If Matt wants immediate execution, pick sensible values yourself and note them — don't stop for a questionnaire.

## Rules

- **One skeleton, one accent.** Structure, type, spacing are fixed by this skill. Per-tool variation is limited to the accent hue and the real content. Don't redesign per tool.
- **Real artifacts only.** The terminal block shows output from an actual run. Copy comes from the README, tightened — not marketing prose.
- **Install command above the fold**, copyable, with the package-manager name visible. It is the primary CTA; everything else is secondary.
- **No dependencies.** No fonts fetched (system stacks), no JS libraries, no analytics unless asked. The one allowed script is the ~15-line clipboard handler in page-anatomy.md.
- **No cards.** Sections separate with hairline borders (`--line` color via `color-mix`). Rows, not tiles.
- **Compact scope.** One viewport of hero, one terminal block, 3–5 proof rows, quiet footer. If it needs a nav bar with dropdowns, it has outgrown this skill — that's an 11ty site.

## Checks

| # | Check | Pass criteria | If fail |
|---|-------|---------------|---------|
| 1 | Install command above fold | visible without scroll at 375px width | Move it up; cut hero copy |
| 2 | Copy works keyboard-only | focusable `<button>`, `aria-live` feedback, geometry stable across copied→copied states | Fix per page-anatomy.md pattern |
| 3 | Terminal output is real | matches a run of the actual tool (diff against captured output) | Re-capture; never fake |
| 4 | No invented claims | no metrics/testimonials/stars not present in the repo | Delete them |
| 5 | Single file pair | exactly `index.html` + `css/style.css` (+ optional screenshot asset) | Collapse extras |
| 6 | Works without JS | page fully readable, command selectable as text | Check with JS disabled |

Then the full [[safaii-css]] Checks table.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Page drifts toward SaaS template | Adding feature grids/badges/testimonials | Cut back to anatomy; hairline rows only |
| Each tool page looks different | Redesigning instead of swapping accent | Diff against the last tool page; keep skeleton identical |
| Fake-looking terminal | Hand-typed plausible output | Run the tool; paste real stdout |
| Copy button shifts layout on click | Label swap changing width | Overlay labels in same grid area |

## Examples

None yet. After the first tool page ships (scry or tribunal likely first), add its repo path here and record any new failure modes.

## Status

First version, written from compact-landing-skill's structure plus Matt's decisions: one house look, per-tool accent, single static HTML, install-command CTA.
