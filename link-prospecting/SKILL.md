---
name: link-prospecting
description: Find link prospects for one client's linkable asset — resource pages, listicles, comparisons, directories, and competitor backlink patterns that have a real reason to mention it — then discover contact paths and draft outreach, written to the client's SEO — Link Prospects — <asset-slug> doc in Basecamp (Internal > SEO). One asset per doc. Use when Matt says "link prospecting for [client]", "find link prospects", "/link-prospecting", "who should link to [asset]", or "outreach targets for [asset]". Needs an existing linkable asset (guide, study, tool, template, strong point of view) — never prospect for a page that doesn't exist yet. Never recreate the doc under a new title.
---

# Link Prospecting Skill

Finds realistic pages, sites, and authors that might reference the client's linkable asset, discovers contact paths, and drafts outreach. DataForSEO does prospect discovery; `webfetch` does contact discovery. Needs an asset worth linking to — this skill comes after content exists.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** Every observation carries a date: "as of <date>". **Market is US by default** (the DataForSEO `location_name`) — a different market only if the context doc says so. Bare backlink counts or ranks are never citable.
2. **Spend is capped and batched.** The default batch is: ≤10 prospecting SERP queries + backlink overview/referring-domains for ≤3 competitor domains + domain overview on the shortlist (capped at ~10 prospects). Then ask before any further call. No re-runs. (Rough scale: SERP ≈ $0.002; backlink summaries ≈ $0.02; domain overview ≈ $0.02.)
3. **Never invent contacts.** No fabricated emails, handles, names, or URLs. Only record contact details actually found — each with its source URL. If you didn't find it, recommend the discovery path instead.
4. **Attribute contact discovery to the real source.** If `webfetch` found it, say so. Don't claim a tool found something it didn't.
5. **Prioritize relevance over volume.** A qualified prospect is one with a real reason to mention the asset. Spammy mass outreach is out; personalize by page and reason.
6. **Flag direct competitors and likely paid placements** — don't prospect them as organic link targets unless a comparison angle is genuinely valid.
7. **Confirm before write.** The prospects doc is written only after Matt confirms. An ambiguous response is not confirmation.
8. **The agent does not send mail.** This skill drafts outreach; Matt (or his ESP) sends it. There is no "send outreach" step, now or later.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- Inputs come from Basecamp, never re-researched: the client's domain and positioning from `SEO — Project Context`, the competitors from its `## Competitors`, and the backlink observations from `competitor-analysis` docs (`SEO — Competitor — <domain>`) when they exist.
- **The doc is one per asset**, titled **`SEO — Link Prospects — <asset-slug>`** (e.g. `SEO — Link Prospects — lte-coverage-map`), slugged from the live URL path — lowercase, path slug only, no scheme, no host, no trailing slash — or a short name Matt confirms before create. It lives in the client's **Docs & Files → Internal → SEO folder**, team-only, never recreated. Prospect the guide in March and the calculator in April → two docs, neither clobbered.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client and the asset

Matt names a client and the **linkable asset** — an existing page, guide, study, tool, template, or strong point of view. Match the client to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous → show Matt the candidates and ask. **Never guess a project or domain.**

Read `SEO — Project Context` — the `Domain:` line, positioning (the claim that makes a link worth giving), `## Competitors`, `## Key pages`. If the context doc is missing, tell Matt to run `seo-project-setup` first and stop.

**Prefer a `## Key pages` row** with role `other` / notes that it's linkable. If Matt names a URL that isn't in Key pages, offer to add it after confirm.

**The asset must exist — prove it, don't assume it.** `webfetch` the asset's URL: a 200 with real content, or stop. A Key pages row is not proof it's live. You can't prospect links for something that isn't there.

### 2. Confirm the asset slug and the reason someone would reference it

Confirm the doc slug (`<asset-slug>` from the live URL path or a short name) with Matt before create. Then ask Matt (or derive from positioning) why someone would cite the asset: fresher data than what's out there, a gap in current resources, a useful tool/template, a strong point of view. That reason is the outreach angle.

### 3. Check reuse

If the same asset was prospected within the last 30 days (same asset, same market), reuse that result and say so instead of re-buying it.

### 4. Mine competitor backlinks first (when competitors exist)

For the strongest competitor domains from the context doc (or the referring domains surfaced by `competitor-analysis`), run `backlinks/referring_domains/live` / `backlinks/summary/live` to see where their links come from — publications, directories, communities, partners. These are the first prospect leads.

**Cap the dump:** after the overview, take a shortlist of ~30 referring domains by rank/traffic — skip the competitor's own properties and obvious spam. Don't ingest thousands of rows. Continue without backlink evidence if it's unavailable.

### 5. Build and run the prospecting queries

Build 5–10 queries from the asset/topic:
- `<topic> resources`
- `best <category> tools`
- `<competitor> alternatives`
- `<topic> statistics`
- `<topic> guide` / `examples` / `templates` / `software`
- `<topic> for <audience>`

Run them batched via `serp/google/organic/live/advanced` (≤10 queries per call). Look for ranking articles, listicles, resource pages, comparisons, statistics pages, templates, and curated lists.

### 6. Filter the prospects

Keep: topical relevance, editorial pages, directories, resource pages, comparisons, statistics, templates, curated lists.
Deprioritize: homepages, login pages, thin affiliate pages, spam, unrelated forums, and direct competitors — unless a comparison angle is valid.

### 7. Qualify the shortlist

For the strongest prospect domains (shortlist capped at ~10), `dataforseo_labs/google/domain_rank_overview/live` to confirm topical fit and size. Qualification is only for prospects you already kept — don't expand into exhaustive research.

### 8. Define the outreach angle per prospect

For each kept prospect:
- **Broken/missing resource** — their list is missing this category
- **Better current data** — the asset is fresher or more complete than what they cite
- **Useful tool/template** — the asset is genuinely useful to their readers
- **Alternative/comparison inclusion** — a comparison page that omits the client
- **Expert quote or supporting reference** — the asset backs a claim they make

### 9. Discover contact paths (`webfetch`)

For the strongest prospects, `webfetch` the prospect site to find the contact path:
- Author byline pages
- Contact pages
- Editorial guidelines
- About/team pages
- LinkedIn / X / professional profiles
- Newsletter or masthead pages
- Public emails in page HTML or visible text
- Structured data (`Person`, `Organization`, `sameAs`, `email`)

**Only record what was actually found, with the source URL.** If nothing surfaces after a reasonable search, list the next-best discovery steps (check the author page, contact page, LinkedIn, a reputable enrichment tool) — don't invent.

### 10. Draft outreach

2–3 reusable drafts, tied to the page and reason:
- **Resource/list inclusion** — "your list of X tools is missing this category"
- **Article update/reference** — "your 2024 statistics are from before this dataset"
- **Competitor alternative/comparison** — "your comparison omits the client's option"

Personalize by page and reason. No mass templates. **Drafts only — Matt sends.**

### 11. Confirm the prospects with Matt

Present before writing:

- **Best outreach angle**
- **Highest-priority prospect type**
- **Data limitations** (backlinks unavailable? contacts not found?)

| Prospect URL | Site/domain | Source | Relevance | Suggested angle | Contact path | Priority |
| --- | --- | --- | --- | --- | --- | --- |

**Do not write until Matt confirms.** Revise in place if he changes the list. After confirmation, **offer** to add the linkable asset to `SEO — Project Context`'s `## Key pages` (and any new competitor whose profile proved useful) — ask, don't silently edit; the context doc is setup-owned.

### 12. Write the doc and log

Write `SEO — Link Prospects — <asset-slug>` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed.

```markdown
## Asset
URL:
Reason to reference:
## Prospect table
| Prospect URL | Site/domain | Source | Relevance | Suggested angle | Contact path | Priority |
## Outreach drafts
### Resource/list inclusion
### Article update/reference
### Competitor alternative/comparison
## Contact discovery notes
## Research log
| Date | Summary |
```

- **`## Prospect table` is the contract** — one row per prospect, with source URLs for any contact path.
- **`## Outreach drafts`** — the 2–3 reusable drafts, personalized by page and reason.
- **Research log** — append an entry: what asset was prospected, the date, the verdict (prospect count, top angle, contacts found). Never replace prior log rows.

**The write loop (every write, every time):**

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the asset line, prospect table, drafts, and notes; **replace** the prospect table with the newly confirmed one; **append** a Research log row — leave prior rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Link Prospects — <asset-slug>" "<markdown>" --in <project_id> --vault <seo_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+)** — prefer `-` for large or multiline markdown to avoid shell quoting and argument-length limits. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Best outreach angle
- Highest-priority prospect type
- Data limitations (backlinks unavailable / contacts not found)
- Prospect count and top few
- Spend note — "reused last 30 days" or "new spend: SERP batch + backlink mining + shortlist qualification"
- Recommended next action: outreach execution (Matt sends the drafts), or `competitor-analysis` first if backlink evidence is missing

## Guardrails

- Do not invent email addresses, social handles, contact names, or URLs.
- Attribute contact discovery to the real source (`webfetch` found it — say so).
- If contact details aren't found after a reasonable search, recommend specific discovery steps — don't fabricate.
- Avoid spammy mass outreach. Personalize by page and reason.
- Flag direct competitors and likely paid placements; don't prospect them as organic targets unless a comparison angle is valid.
- Spend is capped: 5–10 queries batched, competitor backlinks on the strongest profiles (shortlist ~30 referring domains), qualification on ~10 prospects — then ask before any further call.
- The agent never sends mail — drafts only.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Prospected an asset that doesn't exist | Assumed live instead of fetching | `webfetch` the URL — a 200 with real content or stop; a Key pages row isn't proof |
| Two assets collided in one doc | Used a single per-client title | One asset per doc: `SEO — Link Prospects — <asset-slug>` |
| Invented a contact | Fabricated to fill the table | Only record contacts actually found, with source URLs; otherwise recommend discovery steps |
| Contacts attributed to the wrong tool | Claimed a source that didn't provide them | Attribute to the real source (webfetch), with the URL |
| Prospected a direct competitor as organic | Skipped the flag rule | Flag direct competitors and paid placements; only pursue them with a valid comparison angle |
| Backlink dump ingested wholesale | Skipped the cap | Shortlist ~30 referring domains by rank/traffic; skip the competitor's own properties and spam |
| Earlier prospect tables clobbered | Overwrote instead of replacing-then-append | Replace the prospect table, append the log row, leave other sections untouched |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. The `<asset-slug>` is part of the contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the prospects onto it |