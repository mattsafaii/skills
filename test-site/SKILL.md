---
name: test-site
description: Run the Test phase for a Safaii Studio client site — prove the paths from the brief against staging (desktop + phone, form to the real inbox, search, redirects, links), run a visual-resilience pass over the templates with the client's real content, and produce the punch list (fix / defer / out of scope) plus a go/no-go for Release. Use when Matt says "test [client]", "/test-site", "run the test phase", "punch list for [client]", or after a build reaches staging.
triggers:
  - test the site for
  - run the test phase
  - punch list for
  - test-site
---

# Test the site — prove the paths

The gate between Build and Release. Inspection, not redesign: find the breaks and the wrong facts, list them, decide go / no-go. Test does **not** reopen taste — it checks the build against the brief.

## Read first

- `Project Context` (Internal root) — Writing, Constraints, Kit, contacts.
- `Inventory — Brief` — the paths in scope and the finish line.
- `Structure — Sitemap` — templates and paths (Home, Service, Product, Inquire, Support).
- `Structure — Redirects` — the old→new mapping for the redirect spot-check (absent on a greenfield site — then there is nothing to redirect).
- The staging URL from the Build record.

## 1. Path checks — the core

Walk every path the brief names, on desktop and phone. Drive the real staging site with the `browser-control` skill.

- [ ] Every path in the brief loads.
- [ ] Broken links and missing files.
- [ ] Redirect spot-check (skip on a greenfield site): the old→new pairs in `Structure — Redirects` land on the right new pages; a retired line returns `410`; an unmapped old URL follows the catch-all rule.
- [ ] Current Chrome, Safari, Edge — not a museum of old browsers.

## 2. Form path

Submit the inquiry / service form and confirm it arrives at the real destination with the fields intact (Resend → inbox or CRM). Check the spam path and the from-address.

## 3. Search — only if the catalog has it

A real part number, a real spec or service name, a misspelling. Filters behave.

## 4. Login — only if auth exists

Wrong password, reset, first login.

## 5. Visual-resilience pass

Render each template and its components under the content shapes real use will produce — **the client's own worst-case data, not synthetic fixtures**. This is where a site built against the happy path falls over. The method: one page, every scenario side by side, one look, report what visibly broke.

Run only the axes whose cue matches:

- **Content length** — the component renders text it doesn't author (CMS content, catalog, translations): empty string, one word, typical, several sentences, one unbreakable string (a long part number or URL).
- **Content shape** — text can come from users or locales the team doesn't write: emoji, RTL, mixed-direction text, diacritics and tall scripts, numbers where columns align.
- **Quantity** — the component repeats over items (product lists, categories): zero, one, realistic, ten times realistic.
- **Container** — always: widths as fixed containers on the page, never a resized viewport — 320px, squeezed by a flex/grid sibling, very wide.
- **State** — only states the component actually has: loading, error, disabled.
- **Environment** — name these in the report for Matt to toggle, don't simulate them: OS dark mode, browser zoom, reduced motion.

Report each break in the vocabulary of the owning skill, so the fix starts in the right place:

| Break | Owner |
|---|---|
| Wrapping, truncation, tall scripts | `safaii-css` |
| Container has no room, mirroring | `safaii-css` |
| Unbounded measure, grouping, hierarchy | `page-design` |
| Dark mode, contrast from color alone | `safaii-css` |
| Source copy is the problem, empty state | `page-design` |
| State, zoom, motion, missing accessible name | `safaii-html` |
| Purely visual polish | `page-design` |

The page is half the report — render the instances on a throwaway page, mark each break under its label, and leave it up until Matt says he's done.

## 6. Punch list + go / no-go

Produce:

- **Punch list** — every item classified **fix / defer / out of scope**. Wrong facts are fixes; new sections are out of scope (that's a new conversation, not a Test finding).
- **Go / no-go for Release.**

Write the punch list to the client's Basecamp Working folder as `Test — Punch list` (find-or-create by title), and post the go/no-go as a comment on it. Never place Test output in a client-visible folder.

**Stop when** the punch list is empty or holds only deferred items the client accepted.

## Rules

- One focused pass on staging. Breaks and wrong facts, not new sections.
- Test checks the brief; it does not reopen taste.
- Don't fix during the pass — collect, classify, then fix.
- Nothing posts or publishes to the client without Matt's approval.
