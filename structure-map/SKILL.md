---
name: structure-map
description: Write or update a client's Structure-phase map in Basecamp — "Structure — Sitemap" (pages, templates, paths, page-to-term, status) in the project's Working folder, plus "Structure — Fields" (objects, fields) when the client's catalog in v1 is not "none". Reads the master Project Context, the approved Inventory — Brief, any saved keyword set, and Inventory — Current site in order; assigns terms to URLs, never invents a new set. Never writes template copy, a separate entity-map product, or IA philosophy; no todos, no phase folders, no copies to Review. Use when Matt says "structure map for [client]", "/structure-map", "sitemap for [client]", "map the pages for [client]", or after an Inventory brief is approved.
---

# Structure Map

## Goal

Produce the Structure-phase map for one client, in the project's **Working** folder:

- **`Structure — Sitemap`** — Pages, Templates, Paths, Page-to-term, Status.
- **`Structure — Fields`** — Objects, Fields — **only if** `Project Context` → `This engagement` → `Catalog in v1` is not `none`.

Structure is the blueprint: the pages, the templates those pages use, the paths a stranger or an existing customer takes to inquire or get support, and one URL per important family or service. The map is the writing; template copy comes later (`structure-copy`). Do not decide brand, art direction, or a new IA philosophy here.

## Tone

Direct, practical, structured. Small batches. Confirm inferences. The map is a decision artifact — it stops at pages, paths, and terms.

## Required reads, in order

1. **`Project Context`** — at the root of Internal (how `project-setup` resolves it). **Missing → stop; tell Matt to run `project-setup`.**
2. **`Inventory — Brief`** — in Working (how `inventory-brief` resolves it). **Missing → stop** (run `inventory-brief`). If its `## Status` is not `approved YYYY-MM-DD`, **ask Matt before writing a map** — a draft brief is not a green light.
3. **Saved keyword set** — the client's `SEO — Keyword Research`. **Use the saved set only to assign terms to URLs.** Do not invent a new set; if no set exists, draw terms from the approved brief and say so.
4. **`Inventory — Current site`** (Working) — read when it exists, for the redirects a later step will need. Do not write a redirect doc here.

## Where the answers go

Both docs live in the client's **Working** folder. Resolve the Working folder id per project — never hardcode a vault id:

1. `basecamp -a 6191443 files folders --in <project_id> --json` — find the **Working** vault id.
2. `basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json` — find the docs by exact title.
3. If **Working** is missing, tell Matt the project skeleton isn't set up and stop.

### Frozen heading contract — Structure — Sitemap

Exact headings, in order. Do not rename.

```markdown
## Pages

<URL or planned path> — <template type> (role: hub | spoke | money | other)

## Templates

<home | service | product | index | inquire/support — only what this brief includes>

## Paths

<first-time buyer: …>
<existing customer support: …>
<sales-assisted: …>

## Page-to-term

| URL | Term(s) | Notes |
|---|---|---|

## Status

draft | approved YYYY-MM-DD
```

Reading the contract:

- **Pages** — every page is a URL (existing) or a planned path, each with its template type. Roles key off the same `hub | spoke | money | other` set the SEO docs use; `money`, `hub`, and `spoke` pages in the sitemap and the SEO Key pages are the same URLs.
- **Templates** — only those this brief includes: `home`, `service`, `product`, `index`, `inquire/support`. Do not add templates for work out of scope.
- **Paths** — the three lanes: **first-time buyer** (find product or service → inquire), **existing customer support** (support / service request), **sales-assisted** (form or phone to a person). Name the steps.
- **Page-to-term** — one URL per important product family or service. Terms come from the saved keyword set, or from the approved brief when no set exists. **The client does not approve a keyword sheet** — this is the page-to-term assignment, not a deliverable they sign.
- **Status** — `draft` until Matt approves; then `approved YYYY-MM-DD`.

### Frozen heading contract — Structure — Fields

Only when `Catalog in v1` is not `none`. Exact headings, in order. Do not rename.

```markdown
## Objects

<product | family | service | document | location | manufacturer — only those they actually sell>

## Fields

| Object | Field | Type | Notes |
|---|---|---|---|
```

Reading the contract:

- **Objects** — only from the catalog they actually sell. Skip any object the business has no data for. Do not invent categories the client does not use.
- **Fields** — one row per field the object needs (name, SKU, spec, price, document, location…), with type and notes on how it relates. This becomes the CMS types the build uses.

## Structure is not

- **Not template copy.** Words come in `structure-copy`.
- **Not `seo-strategy`.** No content-opportunity or entity-map product, no IA philosophy. The entity list is the catalog Fields doc, nothing more.
- **Not a redesign.** It maps pages and paths for this job; it does not reopen taste or branding.

## The write loop (every write, every time)

Same loop as `project-setup`. Basecamp docs are full-document replace:

1. Find the doc by exact title **in Working** — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <working_id>`).
5. Re-read and assert the other sections still exist, the title and folder are unchanged, and the content is non-empty.

The post-write check applies to **every** write — create and update.

### First create (only when a title doesn't exist in Working)

1. Create the doc **once** with every heading present, bodies written from this run's confirmed answers.
2. `basecamp -a 6191443 files doc create "Structure — Sitemap" "<full markdown>" --in <project_id> --vault <working_id> --json` (same for `Structure — Fields`) — **must carry `--vault`**, or the doc lands at project root.
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
basecamp -a 6191443 files doc create "Structure — Sitemap" "<full markdown>" --in <project_id> --vault <working_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <working_id> --json
```

`files doc create` takes content as an argument, never `-` stdin — the stdin form silently creates an empty doc. Publish with `--content "$(cat file)"` from a written file, `test -s` the file before publish, and verify stored content == canonical after.

## Checklist

1. **Resolve the client and Working.** Project by exact name; find the Working folder id.
2. **Read in order.** Project Context (missing → `project-setup`); Inventory — Brief (missing → `inventory-brief`; not approved → ask Matt before writing); the saved keyword set if it exists; Inventory — Current site if it exists.
3. **Propose the map.** Pages (URLs/planned paths + template type + role), templates (only in-brief types), the three paths, and page-to-term assignments (from the saved set, or the brief when none). Confirm with Matt.
4. **Propose Fields** only when `Catalog in v1` is not `none`. Objects from what they sell; fields per object. Confirm with Matt.
5. **Write** `Structure — Sitemap`, and `Structure — Fields` when applicable, via the write loop. Return the URLs.
6. **Recommend next.** Matt reviews the map, then `structure-copy`. Not Build.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: brief status, keyword set source (saved set / brief), pages and templates proposed, paths, page-to-term count, whether Fields applies, docs written (with URLs), and next step (Matt's review).

## Guardrails

- Confirm with Matt before writing. Inferences are proposed, not saved as facts.
- Use the saved keyword set only to assign terms. Never invent or re-derive a set; if none exists, terms come from the approved brief and say so.
- The client does not approve a keyword sheet — the Page-to-term section is an internal assignment, not a client deliverable.
- No template copy, no `seo-strategy` product, no new IA philosophy, no redesign.
- No todos, no phase folders. Do not copy to Review — Matt moves docs on approval.
- One owner per doc: this skill owns only `Structure — Sitemap` and `Structure — Fields`.
- Re-runs merge and fill gaps; they never discard.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Master Project Context missing | `project-setup` never ran | Tell Matt to run `project-setup` and stop |
| Inventory — Brief missing | Inventory not run | Stop; run `inventory-brief` first |
| Brief not approved | Status is draft | Ask Matt before writing a map — a draft brief is not a green light |
| New keyword set invented | No set existed and terms were made up | Use the saved set, or the brief's terms; say which source |
| Template copy written | Overstepped into `structure-copy` | Structure maps; copy comes later |
| Entity map treated as its own product | Confused with `seo-strategy` | The entity list is the catalog Fields doc; nothing else |
| Fields doc written for a no-catalog client | `Catalog in v1` is `none` | Skip `Structure — Fields` |
| Doc in the wrong folder | Created at project root or in Internal | Docs must live in Working; fix with `--vault <working_id>` |
| Second doc with the same title | Created instead of found | Find by exact title in Working first; update that file id |
| Empty doc after create | Used the `-` stdin form | Pass content as an argument; verify content length |
| Earlier sections clobbered | Full-doc replace without re-reading | Write loop: read → patch one heading → upload entire doc → re-read |
