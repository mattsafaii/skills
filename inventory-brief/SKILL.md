---
name: inventory-brief
description: Write or update a client's Inventory phase docs in Basecamp — two documents in the project's Working folder, "Inventory — Brief" (in scope, out of scope, finish line, access, status) and "Inventory — Current site" (what exists, what is broken, phone/email/PDF-only leaks, and a Comparables section for 4–6 peer sites: page types and leaks only) — by reading the master Project Context first, inspecting the live site, and confirming every inference with Matt. Never invents products, buyers, or scope; the competitor pass is page types and leaks, never a brand teardown; never writes a separate competitor file or a sitemap; never touches Project Context. Use when Matt says "inventory brief for [client]", "/inventory-brief", "start Inventory for [client]", "survey [client]'s site", or when Project Context exists and the work moves past setup.
---

# Inventory Brief

## Goal

Produce the two Inventory-phase documents for one client, in the project's **Working** folder:

- **`Inventory — Brief`** — what this site job includes: in scope, out of scope, the finish line, access, status.
- **`Inventory — Current site`** — what the live site is today: what exists, what is broken, what only lives in phone calls, email, or PDFs, and how 4–6 peer sites compare (page types and leaks only).

Inventory is the site survey: learn what is true and what this job is. It is not Structure, not a strategy artifact, and not a place to decide positioning. Read the master `Project Context` first; confirm every inference with Matt; reconcile only. Do not invent products, buyers, or scope.

## Tone

Direct, practical, structured. Small batches. Confirm inferences — proposed facts get saved as agreed answers, never guesses.

## First step: read Project Context

1. Resolve the client's project by **exact name** (`basecamp -a 6191443 projects list --json`).
2. Find the master **`Project Context`** doc at the root of Internal (how `project-setup` resolves it).
3. **If it is missing, tell Matt to run `project-setup` and stop.**
4. Read `## Offer` — **if `Clear: no`, stop.** The offer must be settled as a separate advisory job or walked away; Inventory does not start. Do not invent positioning to fill the gap.
5. Read the live `Domain:` from `## Business` — that is the site to inspect.
6. Read the rest for context and copy-don't-ask: what they sell, who buys, markets, `## Access` (Fathom, Search Console), `## Key pages` (existing), `## Writing` (audience, do-not-claim), `## This engagement` (main job, maintenance, secondary in scope, inquire path, catalog in v1, pricing, brief status).

## Where the answers go

Two docs, both in the client's **Working** folder, exact titles:

- `Inventory — Brief`
- `Inventory — Current site`

Resolve the Working folder id per project — never hardcode a vault id from another client:

1. `basecamp -a 6191443 files folders --in <project_id> --json` — find the **Working** vault id.
2. `basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json` — find the docs by exact title.
3. If **Working** is missing, tell Matt the project skeleton isn't set up and stop — this skill does not build the folder tree.

### Frozen heading contract — Inventory — Brief

Exact headings, in order. Do not rename.

```markdown
## In scope

<pages, catalog slice, inquire/support path — this site job only>

## Out of scope

<what this job explicitly does not include>

## Finish line

<one or two sentences as pages and paths — not vibes>

## Access

<domain registrar, GitHub, Cloudflare, Resend, catalog export — plan vs status>

## Status

draft | approved YYYY-MM-DD
```

Reading the contract:

- **In scope** — this site job: the pages, the catalog slice, and the inquire/support path. A portal appears here **only if** `Project Context` → `This engagement` → `Secondary in scope` includes it.
- **Out of scope** — name the things a reader might assume are included but are not (portal, integrations, article program, brand, ads).
- **Finish line** — one or two sentences as **pages and paths**, e.g. "A stranger can find a product family, read its spec, and submit an RFQ. An existing customer can request service." Never "improve the site" or "more business."
- **Access** — from `Project Context` → `Access` and `Kit`; note plan vs status (owned by client / invited / pending / not yet). Do not re-ask what Context records; ask only for what is missing.
- **Status** — `draft` until Matt approves; then `approved YYYY-MM-DD`. The client's approval happens later, in **Review**, and Matt does the copy there — this skill never moves the doc.

### Frozen heading contract — Inventory — Current site

Exact headings, in order. Do not rename.

```markdown
## What exists

<the current site as it is: page types that exist, product/service lines as they sell them, catalog/data source if any>

## What is broken

<missing, thin, unreachable-by-search, dead paths, stale facts>

## Phone / email / PDF only

<what a buyer can only get by calling, emailing, or opening a PDF — the leaks: quotes in email, specs in PDFs, "call for pricing", no service request path>

## Comparables (page types and leaks only)

<4–6 peer sites: domain, name, page types present or absent, and their leaks — never a brand or design critique>
```

Reading the contract:

- **What exists** — grounded in an actual inspection of the live site and the facts in `Project Context`; no fabricated pages, products, or buyers.
- **What is broken** — walk the site: broken links, missing files, orphan pages, dead forms, specs only in PDFs, no inquire/support path. Findings, not redesign proposals.
- **Phone / email / PDF only** — the leak list: product or service information, pricing, quote flows, and support that exist outside the site. This is the raw material Maintenance and Structure later act on.
- **Comparables** — 4–6 peer sites, page types and leaks only. Record the page types the peers have that this client lacks (and the reverse), and where the peers leak to phone, email, or PDF. Page types and leaks — not a brand teardown, not positioning. A separate `Inventory — Competitors` doc only when this section overflows.

## Inspecting the current site

- `webfetch` the live `Domain:` and the `## Key pages` URLs; follow the primary navigation and the inquire/support path.
- Note page types present (home, service, product index, product, proof, inquire, support) and which are absent.
- Note where a product or service is only reachable by phone, email, or PDF.
- Do **not** write a sitemap doc, and do **not** write a separate competitor doc — the competitor pass is the Comparables section of `Inventory — Current site`, page types and leaks only. Escalate to `Inventory — Competitors` only when that section overflows.
- If the site does not exist yet (`Production URL` / `Domain` empty or "not yet"), say so, ground the docs in how the business sells today from `Project Context`, and note the site is greenfield.

## The write loop (every write, every time)

Basecamp docs are full-document replace. Same loop as `project-setup`:

1. Find the doc by exact title **in Working** — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <working_id>`).
5. Re-read and assert the other sections still exist, the title and folder are unchanged, and the content is non-empty.

Without file-id + full-replace + re-read, "never recreate" is a wish. The post-write check applies to **every** write — create and update.

### First create (only when a title doesn't exist in Working)

1. Create the doc **once** with every heading present, bodies written from this run's confirmed answers.
2. `basecamp -a 6191443 files doc create "Inventory — Brief" "<full markdown>" --in <project_id> --vault <working_id> --json` (same for `Inventory — Current site`) — **must carry `--vault`**, or the doc lands at project root.
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
basecamp -a 6191443 files doc create "Inventory — Brief" "<full markdown>" --in <project_id> --vault <working_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <working_id> --json
```

`files doc create` takes content as an argument, never `-` stdin — the stdin form silently creates an empty doc. Publish with `--content "$(cat file)"` from a written file, `test -s` the file before publish, and verify stored content == canonical after.

## Checklist

1. **Resolve the client and gate.** Project by exact name → master `Project Context` exists (else send Matt to `project-setup`) → `Offer: Clear` is yes (else stop).
2. **Read what is already there.** Find both Inventory docs in Working first; summarize known vs missing; confirm or correct rather than re-ask. Read `Project Context` for everything it already answers.
3. **Inspect the current site.** Fetch the live domain and key pages; record findings for `Inventory — Current site` (exists / broken / phone-email-PDF-only / comparables).
4. **Draft `Inventory — Current site`.** Propose it to Matt; on confirmation, write it.
5. **Draft `Inventory — Brief`.** In scope (pages, catalog slice, inquire/support path — portal only if in Secondary in scope), Out of scope, Finish line (pages and paths), Access, Status `draft`.
6. **Confirm before writing.** Inventory docs are research artifacts: write only after Matt confirms. Never invent products, buyers, or scope.
7. **Write both docs** via the write loop. Return both doc URLs.
8. **Recommend next.** Matt reviews the brief, then client approval happens in Review (Matt copies it there when approved). Next step is **not** Structure and **not** seo-strategy — wait for the approved brief.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: Offer gate result, site inspected, brief in/out of scope, finish line, current-site findings, docs written (with URLs), and the recommended next step (Matt's review of the brief).

## Guardrails

- Confirm facts with Matt before writing. Inferences from the site are fine to propose; they get saved as agreed answers, not guesses.
- Never invent products, buyers, or scope.
- Write the competitor pass as the Comparables section of `Inventory — Current site` — page types and leaks only, never a brand teardown. A separate `Inventory — Competitors` doc only when that section overflows. Do not write a sitemap. Do not write anything into `Project Context`.
- Do not create todos. Do not copy the brief to Review — Matt does that on approval.
- One owner per doc: this skill owns only `Inventory — Brief` and `Inventory — Current site`.
- Re-runs fill gaps and merge; they never discard.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Master Project Context missing | `project-setup` never ran | Tell Matt to run `project-setup` and stop |
| Offer is not clear | Skipped the gate | `Clear: no` → stop; advisory job or walk away |
| Working folder missing | Project skeleton not set up | Tell Matt; this skill does not build the folder tree |
| Doc in the wrong folder | Created at project root or in Internal | Docs must live in Working; fix with `--vault <working_id>` |
| Second doc with the same title | Created instead of found | Find by exact title in Working first; update that file id |
| Sitemap written into Working | Overstepped into Structure | Inventory names pages and leaks; sitemaps belong to Structure |
| Brand teardown instead of a comparables read | Treated the competitor pass as strategy | Comparables records page types and leaks only; no positioning, no brand critique |
| Facts invented | Inferences saved as facts | Confirm with Matt before writing; keep proposals as proposals |
| Brief copied to Review | Skill moved it | Matt moves it on approval; leave it in Working |
| Empty doc after create | Used the `-` stdin form | Pass content as an argument; verify content length after create |
| Earlier sections clobbered | Full-doc replace without re-reading | Write loop: read → patch one heading → upload entire doc → re-read |
