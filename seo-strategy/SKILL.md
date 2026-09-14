---
name: seo-strategy
description: Turn a client's SEO research into strategy — content opportunities (ideas pulled from keyword clusters, page map, and competitive gaps) and entity mapping / information architecture (entities, relationships, proposed structure, quick wins) — written to the client's SEO — Content Opportunities and SEO — Entity Map & IA docs in Basecamp (Internal > SEO). Pure analysis; makes no DataForSEO calls; consumes the research docs already written. Use when Matt says "content ideas for [client]", "blog post ideas from the SEO research", "map the entities for [client]", "entity map", "information architecture", "site architecture for SEO", "quick wins for [client]", "/seo-strategy [content|entities]". Never recreate the docs under new titles.
---

# SEO Strategy Skill

Turns a client's research into two strategy docs: **Content Opportunities** and **Entity Map & IA**. Pure analysis — consumes the research docs and the live site, spends nothing. If the research docs don't exist yet, run `keyword-research` first and stop.

## Rules that don't bend

1. **Zero data calls.** This skill never touches DataForSEO. Everything is derived from the client's existing SEO docs (Project Context, Keyword Research, Page Map, Competitive Landscape) plus the live site. If something needs data you don't have, name the gap — don't call for it here.
2. **Every recommendation ties to evidence.** A content idea cites its cluster. An entity cites where it came from (page, keyword, competitor gap). A quick win cites the page it touches. Nothing is asserted from thin air.
3. **Inputs are consumed, never re-researched. Required: `SEO — Project Context` and a dated `## Saved keywords` set.** Optional: `SEO — Page Map` (target URLs, briefs), `SEO — Competitive Landscape` (market, gaps), `SEO — Rank Tracker` (striking distance — zero spend to read). If an optional doc is missing, say what the strategy *won't* be able to do (no target URLs / no gap logic / no near-rank awareness) and get Matt's yes to proceed — never silently pick. If a required input is missing or undated, tell Matt which skill to run first and stop — never re-derive the research.
4. **Ideas, not copy.** You propose directions and angles; Matt and the client write the actual content. Never draft finished blog posts.
5. **Confirm before write.** Each strategy doc is written only after Matt confirms its content. An ambiguous response is not confirmation.
6. **Reuse within 30 days.** Same inputs, same mode, dated under 30 days → reuse the result and say so instead of re-doing the analysis.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- Input docs, all from the client's **Docs & Files → Internal → SEO folder**, read in this order:
  - `SEO — Project Context` — domain, positioning, writing preferences, target markets, key pages **(required)**
  - `SEO — Keyword Research` — `## Saved keywords` (evidence: volume, difficulty, intent) and the `## Research run` header **(required, dated)**
  - `SEO — Page Map` — `## Cluster map` and `## Page briefs` (where keywords land) **(optional)**
  - `SEO — Competitive Landscape` — `## Competitive table` and `## Keyword/theme gaps` (who owns the market, the openings) **(optional)**
  - `SEO — Rank Tracker` — the newest `## Run —` section (which pages already sit in striking distance) **(optional, zero spend)**
- The live site is fair game: `webfetch` on the client's domain (from the context doc's `Domain:` line) and key pages to ground entity work in what actually exists.
- The docs live in the client's **Docs & Files → Internal → SEO folder**, team-only, titled **`SEO — Content Opportunities`** and **`SEO — Entity Map & IA`** — stable contracts, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client

Matt names a client. Match it to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a project or domain.**

### 2. Read the inputs

Read the input docs in order (see Fixed context). **Required:** `SEO — Project Context` and a dated `## Saved keywords` set — if either is missing, tell Matt to run `seo-project-setup` / `keyword-research` first and stop.

**Optional docs missing? Say what the strategy won't do, then get a yes.** If `SEO — Page Map` is missing, content ideas have no target URLs (no page assignment). If `SEO — Competitive Landscape` is missing, no gap logic (opportunities will be intent-matched only). If `SEO — Rank Tracker` is missing, no striking-distance awareness (quick wins can't name pages already close to ranking). Present that limitation and get Matt's explicit yes to proceed without them — never silently pick.

### 3. Check reuse

If the same mode was run on the same inputs within the last 30 days (fingerprint = mode + saved-set date + page map date + landscape date when used), reuse that result and say so instead of re-doing it.

### 4. Confirm the mode

Matt says either "content" or "entities" (or both). Run the one asked for. Both means both docs, in that order.

### 5. Mode A — Content Opportunities

**Page assignments and briefs come from `SEO — Page Map` only.** `SEO — Keyword Research`'s `## Clusters` are run themes, not pages — use them as idea fodder only when the Page Map is missing and Matt agreed to run content on the saved set alone. The saved keywords are **evidence** (volume, difficulty, intent), never a site structure.

For each cluster, propose content that:
- **Matches intent:** informational clusters → educational posts (what is / how to); commercial/transactional clusters → comparison, cost, and buying posts.
- **Fills gaps:** the landscape's `## Keyword/theme gaps` — where a core SERP is owned by publishers and no direct competitor ranks, a content-first post is an open lane. Cite the gap row.
- **Uses customer language:** pull actual phrasing from the keyword data — don't invent topic names.
- **Respects `## Writing preferences`:** angles must stay within the recorded voice and never touch banned phrases or topics.

**Order by winnability, defined:** higher volume + lower KD (from the saved table) + a landscape gap present + an existing page already in striking distance (from the Rank Tracker's newest run) if that input exists. Weight each idea against all four, not volume alone.

Write `SEO — Content Opportunities` (markdown), following the **frozen heading contract**:

```markdown
## Run
Date:
Based on: (saved-set date, page map date, landscape date)
## Opportunities
### <idea title>
Cluster:
Intent:
Keyword evidence:
Angle:
## Why these
## Research log
| Date | Summary |
```

- **`## Opportunities`** — one `###` per idea, each with cluster, intent, keyword evidence (volume/difficulty), and a 1–2 line angle. **Order by the four-factor winnability sort** (see step 5), highest first.
- **`## Why these`** — the gap logic, tied to the research (especially the landscape gaps).
- **Research log** — append an entry: what was analyzed, the date, the verdict. Never replace prior log rows.

### 6. Mode B — Entity Map & IA

Read the saved keywords, the page map's cluster map, the competitive landscape, and the live site (homepage + service/industry pages). Competitor-analysis docs (`SEO — Competitor — <domain>`) are **optional color** — only fetch one if Matt names a domain; don't go hunting for them.

- **Entities:** the client's products/services, industries, the problems they solve, competitors, and the customer language the keywords reveal. Group them by type. Each cites where it came from.
- **Relationships:** how entities connect (service → industry, problem → solution, keyword phrase → page).
- **Information architecture:** the proposed page structure — what exists (from the page map), what's missing (e.g. the cluster a saved keyword implies), what should link to what.
- **Quick wins:** the highest-leverage, lowest-effort moves surfaced by the mapping. **Keep quick wins to IA/internal-link/thin-page fixes only** — "write this new page" belongs in Content Opportunities, not here; a quick win that needs a new page points at the relevant Opportunities `###` instead of duplicating it.

Write `SEO — Entity Map & IA` (markdown), following the **frozen heading contract**:

```markdown
## Run
Date:
Based on:
## Entity inventory
| Entity | Type | Source |
## Relationships
## Proposed IA
| Page | Purpose | Target keywords/cluster | Status |
## Quick wins
| Move | Effort | Payoff |
## Research log
| Date | Summary |
```

- **`## Entity inventory`** — one row per entity, with source (page, keyword, competitor gap).
- **`## Proposed IA`** — one row per page, `Status` = the Key pages role (`hub` / `spoke` / `money` / `other`) plus `existing` / `proposed` (e.g. `money — existing`, `hub — proposed`), so a later clustering run can merge cleanly.
- **`## Quick wins`** — ordered by payoff.
- **Research log** — append an entry. Never replace prior log rows.

### 7. Confirm and write — one cycle per mode

**If both modes run, do two separate confirm-and-write cycles.** Confirm content, write it, then entities — don't hold both until the end, or a "yes" to entities will stall content waiting on one combined sign-off.

**Content cycle:** present the opportunities, ordered by winnability, with the gap logic. **Do not write until Matt confirms.** Revise in place if he changes it. Content ideas need no write-back — they're the deliverable.

**Entities cycle:** present the entity inventory, proposed IA (existing vs. proposed with roles), and quick wins. **Do not write until Matt confirms.** After confirmation, **offer** to merge the *proposed* new pages (from `## Proposed IA`) into `SEO — Project Context`'s `## Key pages` — ask, don't silently edit; the context doc is setup-owned.

Each write follows **the write loop (every write, every time):**

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the run header and content sections; **replace** the content sections with the newly confirmed ones; **append** a Research log row — leave prior rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Content Opportunities" "<markdown>" --in <project_id> --vault <seo_folder_id> --json` (and same for `SEO — Entity Map & IA`). Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+)** — prefer `-` for large or multiline markdown to avoid shell quoting and argument-length limits. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Mode run (content / entities / both)
- Top content ideas or key entities / proposed pages / quick wins
- Inputs consumed and their dates (the reuse fingerprint)
- Spend note — "no spend (analysis only)"
- Recommended next action: `seo-rank-tracking` (pages live, keywords tracked), `link-prospecting` (an asset worth links emerged), or `competitive-landscape` (if the market read was missing)

## Guardrails

- This skill spends nothing. If a step needs live data, name the gap — don't call DataForSEO here.
- Every recommendation cites its evidence (cluster, page, gap, keyword). Nothing from thin air.
- Ideas, not copy — Matt and the client write the actual content.
- Inputs are consumed, never re-researched — a missing input means run the owning skill, not re-derive it.
- The Project Context doc is setup-owned; the research/strategy docs are owned by their skills. This skill writes only its two docs — the exception is the asked merge into `## Key pages` on Matt's explicit yes.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Made a DataForSEO call | Reached for the MCP inside a strategy skill | This skill spends nothing; name the data gap instead |
| Ideas with no keyword backing | Drafted from vibes | Every idea cites its cluster and volume evidence |
| Entities invented | No source page or keyword | Every entity row cites where it came from |
| Re-derived the research | Skipped the input read | Inputs are consumed from the docs; a missing one means run its owning skill |
| Read the stale "SERP caveats" | Referenced a KR section that no longer exists | Gaps come from the landscape's `## Keyword/theme gaps`, not a KR section |
| Doc in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Finished blog posts written | Forgot ideas-not-copy | You propose angles; Matt and the client write the content |
| Doc written without confirmation | Skipped step 7 | Present the content; only a confirmed yes gets written |
| Duplicate docs over time | Doc title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the strategy onto it |