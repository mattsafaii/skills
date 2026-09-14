---
name: structure-copy
description: Write or update a client's Structure-phase template copy in Basecamp — the single "Structure — Template copy" doc in the project's Working folder, covering only the templates that exist on Structure — Sitemap (Home, Service, Product, Inquire, Support), each written as words in order that lead to the next action, with the headings, short body, and form labels or empty states that template needs. Reads Project Context (Writing, Constraints, Offer), Structure — Sitemap, and Inventory — Brief. Never invents claims banned in Project Context, never starts a new page type, never writes CSS or layout or one file per URL, never touches Project Context. Use when Matt says "template copy for [client]", "/structure-copy", "write the page copy for [client]", or after a Structure map is approved.
---

# Structure Copy

## Goal

Write the copy for a client's pitching templates into one Basecamp doc, **`Structure — Template copy`**, in the project's **Working** folder. Copy is produced in Structure and placed in Build; there is no separate copywriting phase.

Each pitching template is a document: the words, in order, that a stranger must read to take the next action. Not a mood, not lorem, not a novel. Layout and brand go on these words later in Build.

## Tone

Direct, plain, specific. Short paragraphs. The studio voice: clear, specific, no slogan layer.

## Required reads

1. **`Project Context`** — at the root of Internal. Read **Writing** (audience, voice, do-not-claim, banned phrases), **Constraints** (industry notes, topics they will not put on the site), and **Offer** (how they sell today — use their words, not a new framework). Missing → stop; tell Matt to run `project-setup`.
2. **`Structure — Sitemap`** — in Working. **Missing → stop; tell Matt to run `structure-map`.** The sitemap decides which templates exist and the page-to-term assignments the copy targets.
3. **`Inventory — Brief`** — in Working, for the **inquire path** and the **finish line**. Missing → run `inventory-brief` first.

## Where the answers go

One doc in the client's **Working** folder, titled exactly **`Structure — Template copy`**. Resolve the Working folder id per project — never hardcode a vault id:

1. `basecamp -a 6191443 files folders --in <project_id> --json` — find the **Working** vault id.
2. `basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json` — find the doc by exact title.
3. If **Working** is missing, tell Matt the project skeleton isn't set up and stop.

### Frozen heading contract

Include **only** the templates that exist on `Structure — Sitemap`. Exact headings, in order. Do not rename. Do not add a heading for a template the sitemap does not include.

```markdown
## Home

<headline>
<short body — the words in order that lead to the primary action>

## Service

<headline>
<short body — one service page pattern: what it is, who it is for, the next action>

## Product

<headline>
<the pattern: the fields a product page shows and the pitch that frames them — not 200 SKUs>

## Inquire

<headline>
<short body>
<form labels: …>

## Support

<headline>
<short body>
<form labels: …>
<empty states where they apply>
```

Reading the contract:

- **Order the words as a path.** Each template reads top to bottom as what a stranger needs, in order, to reach the next action (inquire, request support, call, submit).
- **Heading, short body** — the headline and the few sentences that do the work. Bullets only where a real list helps.
- **Form labels or empty states** where that template has them — the actual label text a buyer sees, and the empty-state line for index/support lists.
- **Product is a pattern:** the fields a product page carries (name, spec, document, price or gated-price note) plus the pitch that frames them. It is not a page per SKU.
- **Include only templates on the sitemap.** If the sitemap lists no `Support`, there is no `## Support` heading. Home, Service, Product, Inquire, Support — that set; Index is not a copy heading.

## What Structure Copy is not

- **Not new claims.** Never write a claim banned or regulated away in `Project Context`'s Writing/Constraints. Never invent a promise the client cannot stand behind.
- **Not a new page type.** Copy only the templates on the sitemap.
- **Not CSS or layout.** No color, spacing, component, or design decisions — Build applies those to these words.
- **Not one file per URL.** One doc, one heading per template. Product covers the whole product template, not every product.
- **Not in Project Context.** The copy lives in `Structure — Template copy`, never scattered into the context doc.

## The write loop (every write, every time)

Same loop as `project-setup`. Basecamp docs are full-document replace:

1. Find the doc by exact title **in Working** — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <working_id>`).
5. Re-read and assert the other sections still exist, the title and folder are unchanged, and the content is non-empty.

The post-write check applies to **every** write — create and update.

### First create (only when the title doesn't exist in Working)

1. Create the doc **once** with every in-scope heading present, bodies from this run's copy.
2. `basecamp -a 6191443 files doc create "Structure — Template copy" "<full markdown>" --in <project_id> --vault <working_id> --json` — **must carry `--vault`**, or the doc lands at project root.
3. Enter the write loop from then on — same file id, full-document updates.

### Canonical CLI shapes

```text
# resolve the Working folder id
basecamp -a 6191443 files folders --in <project_id> --json

# find the doc by exact title, ONLY in Working
basecamp -a 6191443 files list --vault <working_id> --in <project_id> --json

# read the current doc
basecamp -a 6191443 files show <file_id> --in <project_id> --json

# first create (only if the title is absent in Working)
basecamp -a 6191443 files doc create "Structure — Template copy" "<full markdown>" --in <project_id> --vault <working_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <working_id> --json
```

`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+); prefer `-` for large markdown. Publish with `--content "$(cat file)"` from a written file, `test -s` the file before publish, and verify stored content == canonical after.

## Checklist

1. **Resolve the client and Working.** Project by exact name; find the Working folder id.
2. **Read in order.** Project Context (Writing / Constraints / Offer; missing → `project-setup`); Structure — Sitemap (missing → `structure-map`); Inventory — Brief (inquire path + finish line).
3. **Determine the heading set.** Only the templates the sitemap lists — no invented templates.
4. **Draft the copy.** For each in-scope template: heading, short body, form labels / empty states. Order the words as the path to the next action. Product is a pattern, not a SKU list. Check every line against the banned and do-not-claim list.
5. **Confirm with Matt**, then **write** via the write loop. Return the doc URL.
6. **Recommend next.** Matt rewrites the pitch, then **Build**.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: templates covered, inquire path used, any claims deliberately avoided, the doc URL, and next step (Matt rewrites the pitch, then Build).

## Guardrails

- Confirm with Matt before writing. Proposed copy is a proposal; he rewrites the pitch.
- Never write a banned or do-not-claim line from `Project Context`.
- Copy only templates on the sitemap — no new page types, no per-URL files.
- No CSS, layout, or design decisions.
- No todos, no phase folders. Do not put copy into `Project Context`.
- One owner per doc: this skill owns only `Structure — Template copy`.
- Re-runs merge and fill gaps; they never discard.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Master Project Context missing | `project-setup` never ran | Tell Matt to run `project-setup` and stop |
| Structure — Sitemap missing | Structure not mapped | Stop; run `structure-map` first |
| Template copy for a page not on the sitemap | Invented a page type | Copy only the sitemap's templates |
| Banned claim written | Skipped Project Context's Writing/Constraints | Re-read them; pull the line |
| 200 product pages drafted | Treated Product as per-SKU | Product is one pattern: fields + pitch |
| Design decided in the copy | Overstepped into Build | Words only; layout and brand come later |
| Doc in the wrong folder | Created at project root or in Internal | Must live in Working; fix with `--vault <working_id>` |
| Second doc with the same title | Created instead of found | Find by exact title in Working first; update that file id |
| Empty doc after create | Content not passed (or `-` on a pre-v0.10.0 CLI) | Pass content as an argument or via stdin `-` (v0.10.0+); verify content length |
| Earlier sections clobbered | Full-doc replace without re-reading | Write loop: read → patch one heading → upload entire doc → re-read |
