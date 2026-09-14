---
name: structure-redirects
description: Decide and write a client's Structure-phase redirects in Basecamp — one doc, "Structure — Redirects", in the project's Working folder, but only when the old site has value worth preserving. Runs a gate first — greenfield sites get no doc; an old site is judged on backlinks and brand/product presence and yields either catch-all only or an old→new map; a domain change is a whole-domain 301. Reads Project Context, Structure — Sitemap, Inventory — Current site, and inspects the old domain; never invents a destination URL and never maps a redirect to a page not on the sitemap. Use when Matt says "redirects for [client]", "/structure-redirects", "map the redirects for [client]", "what happens to the old URLs", or after a Structure map is approved.
---

# Structure Redirects

## Goal

Produce the redirect decision for one client, in the project's **Working** folder, as the single doc **`Structure — Redirects`** — written only when the old site has URLs worth preserving.

When the new site replaces the old, old URLs must not silently 404. Redirects preserve value that lives *outside* the old site: backlinks from directories, suppliers, and old customers; branded and product-name search rankings; customer bookmarks. That value is independent of how good the old site was or whether anyone ever "did SEO" on it. The plan is applied on staging in Build and on the live host in Release.

The gate comes first. Most jobs are either greenfield (nothing to redirect) or catch-all only (one rule, no page-by-page map). Do not produce a map the signals don't justify.

## Tone

Direct, practical. Small batches. The gate decides the size of the work; an empty map is a complete answer.

## Required reads, in order

1. **`Project Context`** — at the root of Internal. Read **Business** (`Domain`, `Production URL` — the old domain), **Kit** (Cloudflare), and **This engagement**. **Missing → stop; tell Matt to run `project-setup`.**
2. **`Structure — Sitemap`** — in Working. The new URLs are the **only legal destinations**. **Missing → stop; run `structure-map`.**
3. **`Inventory — Current site`** — in Working, when it exists; the old page types and leaks. If absent, proceed — this skill enumerates from the live domain.
4. **The old live domain** — enumerate the old URLs and run the signal checks (gate below).

## First step: the gate

Decide which case this job is. The gate decides whether *anything* is written.

- **Greenfield** — no live old site (`Production URL` / `Domain` empty or "not yet"): outcome **greenfield**. **Write nothing.** Tell Matt there is nothing to redirect.
- **Domain change** — the new site lives on a different domain than the old: the lever is a **whole-domain 301** (redirect the entire old domain to the new one at the host, Cloudflare) under `## Rules`, not a page-by-page map — unless the old domain is abandoned, in which case there is nothing to redirect at that layer.
- **Same-domain replacement** — the old site exists and the new site keeps the domain: run the signal checks below.

### Signals (same-domain replacement)

Two cheap checks decide **catch-all only** vs **mapped**.

- **Backlinks** — the old domain's backlink profile via the `dataforseo` skill (`backlinks/summary/live` / `backlinks/referring_domains/live`). Zero or near-zero real referring domains → nothing to map. Any real referring domains → their target URLs are the map candidates.
- **Brand / product presence** — does the old domain appear for its own name or its product/service names (a SERP check), or does a Search Console property exist with top pages? Pages with branded/product ranking or real clicks → map those.

Neither signal → **catch-all only**. This is the likely majority case: a bad old site with no backlinks to anything and no branded rankings.

**"They never did SEO" is not a signal.** A site can be bad and still be linked. The backlinks and the branded presence decide, not the SEO effort.

## Where the answers go

One doc in the client's **Working** folder, titled exactly **`Structure — Redirects`**. Written only for outcomes **catch-all only** or **mapped** (and for a **domain change** when a rule is worth recording). Resolve the Working folder id per project — never hardcode a vault id:

1. `basecamp -a 6191443 files folders --in <project_id> --json` — find the **Working** vault id.
2. `basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json` — find the doc by exact title.
3. If **Working** is missing, tell Matt the project skeleton isn't set up and stop.

### Frozen heading contract

Exact headings, in order. Do not rename.

```markdown
## Basis

<old domain; signals checked (backlinks, brand/product presence, GSC) and what they showed; outcome: catch-all only | mapped | domain change>

## Redirects

| Old URL | New URL | Type | Notes |
|---|---|---|---|

## Rules

<catch-all for unmapped old URLs; trailing-slash / case / query handling; whole-domain 301 when the domain changes>

## Status

draft | approved YYYY-MM-DD
```

Reading the contract:

- **Basis** — the evidence and the outcome. Records *why* the map is empty or short, so a later reader does not think the work was skipped. Always present when the doc is written.
- **Redirects** — one row per old URL worth mapping. `Old URL` is a real enumerated old URL. `New URL` **must exist on `Structure — Sitemap`** — never invent a destination. `Type` is `301` (the default), `410` (a line retired on purpose), or `302` only when genuinely temporary. `Notes` explains the pairing or the retirement. An empty table is valid for **catch-all only**.
- **Rules** — the host-level rules: what an old URL not in the table does (default `301` to home; retired families `410`), trailing-slash / case / query-string handling, and the whole-domain `301` when the domain changes.
- **Status** — `draft` until Matt approves; then `approved YYYY-MM-DD`.

## What Structure Redirects is not

- **Not a sitemap.** Destinations come from `Structure — Sitemap`.
- **Not new URLs.** If an old URL has no sensible new home, it is a `410` or the catch-all — never a made-up page.
- **Not applied here.** This skill plans; Build applies on staging, Release applies on the live host.
- **Not a page-by-page map when the signals don't justify one.** Catch-all only is a complete outcome.
- **Not in Project Context.**

## Enumerating the old URLs

- Fetch the old domain; read `sitemap.xml` and `robots.txt` (the `Sitemap:` line); follow the primary nav and internal links to list old URLs.
- If the client provides an export (a URL list, or Search Console top pages), use it.
- Normalize as you record: scheme / https, host (www vs non-www), trailing slash — the `## Rules` section must state how the host handles them.
- **Only URLs with a signal** (a backlink, branded/product ranking, real clicks) go in the table; everything else rides the catch-all.

## The write loop (every write, every time)

Same loop as `project-setup`. Basecamp docs are full-document replace:

1. Find the doc by exact title **in Working** — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <working_id>`).
5. Re-read and assert the other sections still exist, the title and folder are unchanged, and the content is non-empty.

The post-write check applies to **every** write — create and update.

### First create (only when the title doesn't exist in Working)

1. Create the doc **once** with every heading present, bodies written from this run's confirmed answers.
2. `basecamp -a 6191443 files doc create "Structure — Redirects" "<full markdown>" --in <project_id> --vault <working_id> --json` — **must carry `--vault`**, or the doc lands at project root.
3. Enter the write loop from then on — same file id, full-document updates.

### Canonical CLI shapes

```text
# resolve the Working folder id
basecamp -a 6191443 files folders --in <project_id> --json

# find docs by exact title, ONLY in Working
basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json

# read the current doc
basecamp -a 6191443 files show <file_id> --in <project_id> --json

# first create (only if the title is absent in Working)
basecamp -a 6191443 files doc create "Structure — Redirects" "<full markdown>" --in <project_id> --vault <working_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <working_id> --json
```

`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+); prefer `-` for large markdown. Publish with `--content "$(cat file)"` from a written file, `test -s` the file before publish, and verify stored content == canonical after.

## Checklist

1. **Resolve the client and Working.** Project by exact name; find the Working folder id.
2. **Read in order.** Project Context (missing → `project-setup`); Structure — Sitemap (missing → `structure-map`); Inventory — Current site if it exists.
3. **Run the gate.** Greenfield → nothing to redirect; stop, write nothing. Domain change → whole-domain `301` under `## Rules`. Same-domain → signals next.
4. **Check the signals.** Backlinks and brand/product presence. Neither → **catch-all only**. Either → enumerate the old URLs and map only the ones with a signal.
5. **Propose the outcome** — and, when mapping, the table — to Matt. Confirm.
6. **Write** `Structure — Redirects` for catch-all only / mapped / domain change, via the write loop. Return the URL. Greenfield: write nothing and say so.
7. **Recommend next.** Build applies the rules on staging; `test-site` spot-checks the mapping.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: gate outcome, signals checked and what they showed, rows mapped (or catch-all only), the doc URL (or "no doc — greenfield"), and next step.

## Guardrails

- **Run the gate before writing anything.** Greenfield → no doc.
- **"Never did SEO" is not a reason to skip the check.** Backlinks and branded presence decide.
- **Never invent a destination.** New URLs come from `Structure — Sitemap`; with no sensible home, use `410` or the catch-all.
- **Catch-all only is a valid, complete outcome.** Do not pad it into a page map.
- **Retired lines are `410`,** not silently dropped. **No redirect chains** — every old URL points at the final new URL.
- Confirm with Matt before writing. Inferences are proposed, not saved as facts.
- No todos, no phase folders. Do not copy to Review — Matt moves docs on approval.
- One owner per doc: this skill owns only `Structure — Redirects`.
- Re-runs merge and fill gaps; they never discard.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Redirect doc written for a greenfield client | Gate skipped | No old site → write nothing; say so |
| Page-by-page map with no backlinks and no branded presence | Signals skipped | Catch-all only is enough |
| Old URL mapped to a page not on the sitemap | Invented a destination | Destinations come from `Structure — Sitemap`; else `410` / catch-all |
| Redirect chain (A → B → C) | Pointed at an intermediate URL | Point every old URL at its final new URL |
| Retired line silently dropped | No `410` row | Map it to `410` |
| Domain change handled page by page | Wrong lever | Whole-domain `301` under `## Rules` |
| Master Project Context missing | `project-setup` never ran | Tell Matt to run `project-setup` and stop |
| Structure — Sitemap missing | Structure not mapped | Stop; run `structure-map` first |
| Doc in the wrong folder | Created at project root or in Internal | Must live in Working; fix with `--vault <working_id>` |
| Second doc with the same title | Created instead of found | Find by exact title in Working first; update that file id |
| Empty doc after create | Content not passed (or `-` on a pre-v0.10.0 CLI) | Pass content as an argument or via stdin `-` (v0.10.0+); verify content length |
| Earlier sections clobbered | Full-doc replace without re-reading | Write loop: read → patch one heading → upload entire doc → re-read |
