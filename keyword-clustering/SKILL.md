---
name: keyword-clustering
description: Turn a client's saved keywords into a page map — cluster keywords by intent and SERP reality, assign each cluster to an existing or new page, flag cannibalization, and write the result to the client's SEO — Page Map doc in Basecamp (Internal > SEO). Pure analysis of what keyword-research and project-setup already produced; the only spend is a small SERP batch for borderline terms. Use when Matt says "cluster keywords for [client]", "keyword clustering", "/keyword-clustering", "map keywords to pages for [client]", or "turn the keywords into a page plan". The page map is what seo-strategy reads to draft content — never recreate the doc under a new title.
---

# Keyword Clustering Skill

Groups a client's confirmed keywords into page-level clusters and decides which existing or new page should target each. This is a keyword mapping workflow, not a semantic grouping exercise — similar words do not guarantee the same page; SERP intent wins.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials for the small SERP batch:

1. **SERP intent wins over lexical similarity.** Two keywords that read alike but serve different intents go on different pages. Two keywords with the same intent and similar ranking pages belong together even if they read differently. Don't cluster on word overlap.
2. **Inputs come from Basecamp, never re-researched.** The keyword set comes from `SEO — Keyword Research`'s `## Saved keywords` (required, with a dated run header); the existing pages come from `SEO — Project Context`'s `## Key pages` (optional — if missing, every target defaults to `proposed: <name>`). Never invent keywords or pages.
3. **Spend is small and targeted.** The only paid calls are `serp/google/organic/live/advanced` checks for important borderline terms (intent ambiguous, or the page assignment would flip on the result). Keep the batch small — 3–6 terms max. One call per term, no re-runs. (≈ $0.002 each.) Every observation carries a date; **market is US by default**.
4. **Confirm before write.** The cluster map is written only after Matt confirms it. An ambiguous response is not confirmation.
5. **Do not over-cluster.** Fewer than 10 usable terms → produce a simple map (one table, no page briefs), don't manufacture clusters.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- The doc lives in the client's **Docs & Files → Internal → SEO folder**, team-only, titled **`SEO — Page Map`** — a stable contract, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client

Matt names a client. Match it to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a project or domain.**

### 2. Read the inputs

Find `SEO — Project Context` and read it — the `## Key pages` table (existing pages + roles) and the target markets. Find `SEO — Keyword Research` and read **only** the `## Saved keywords` table (the confirmed set), the `## Research run` header (`Date:` / `Location:` — used by the refuse check), and the `## Research log` (last run, and any cannibalization already flagged). **Ignore its `## Clusters` theme headings** — those are run themes, not a page map; never promote them into `SEO — Page Map` rows.

**Refuse to run without the inputs:** if `## Saved keywords` is missing/empty, or its `## Research run` header has no `Date:` / `Location:`, tell Matt to run `keyword-research` first and stop. If `## Key pages` is empty, run with proposed pages only (label them proposed — the guardrail below).

### 3. Check reuse

If the same keyword set was clustered within the last 30 days (same saved-set fingerprint — count + `Date:` from the KR run header — and same pages), reuse that result and say so instead of re-doing it.

### 4. Cluster by intent and page type

Group the saved keywords:

- **Same SERP intent + similar ranking pages → same cluster.** They're one page's keyword family.
- **Different intent, buyer stage, or SERP format → split**, even if the words look related.
- **Weak or off-strategy terms → a do-not-target bucket**, not forced into a cluster.

This is the agent's judgment — don't lean on word overlap.

### 5. Check SERP overlap for borderline terms

For the 3–6 terms where intent is ambiguous or the page assignment would flip on the result, run one `serp/google/organic/live/advanced` check each. If two "borderline" keywords return the same set of ranking pages, they likely belong together; if the SERPs diverge, split them.

### 6. Assign each cluster to a page

- **Existing URL** from `## Key pages`, if supplied and appropriate.
- **New page recommendation**, if no existing page fits — label it proposed.
- **Do-not-target / later**, for weak or off-strategy clusters.

If existing URL data is missing entirely, label every target page as proposed.

### 7. Flag cannibalization

Cannibalization is **two live URLs already competing for one intent**, or **two separate target pages assigned to the same intent** — not two keywords sharing a target. Two keywords on the same page is a correct cluster, not cannibalization; don't split a good cluster because of it.

Evidence, in order of strength:
- The research log's cannibalization note from keyword-research's GSC `query_page` pull — a query earning impressions across two URLs is confirmed.
- Two existing `## Key pages` URLs assigned to the same intent by this map.
- If neither exists (GSC skipped, or no real data), say so in the log and map from structure only — don't fabricate a cannibalization flag.

### 8. Confirm the map with Matt

Present before writing:

- **Summary:** number of clusters, pages to create, existing pages to update, cannibalization/consolidation issues.
- **The cluster table** (below).
- **Page briefs** for the clusters that matter.

| Cluster | Primary keyword | Secondary keywords | Intent | Target page | Priority | Notes |
| --- | --- | --- | --- | --- | --- | --- |

**Primary keyword** = the term the page should rank for — best intent fit × plausible KD × volume. Secondaries support it. Don't just pick the highest-volume token.

**Use Key pages `role`:** money-intent clusters prefer `money` URLs, hub clusters prefer `hub`. Don't park a commercial cluster on a spoke blog post because the slug shares a word.

**Do not write until Matt confirms.** Revise in place if he changes the map.

After Matt confirms, **offer** to merge the approved new pages into `SEO — Project Context`'s `## Key pages` — ask, don't silently edit; the context doc is setup-owned. Otherwise the next clustering run keeps proposing the same URLs.

### 9. Write the doc and log

Write `SEO — Page Map` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed. seo-strategy reads this doc.

```markdown
## Cluster map
| Cluster | Primary keyword | Secondary keywords | Intent | Target page | Priority | Notes |
## Page briefs
### <page or proposed page>
Page type:
Searcher problem:
Required sections:
Internal-link opportunities:
## Research log
| Date | Summary |
```

- **`## Cluster map` is the contract** — one row per cluster, target page filled with an existing URL or "proposed: <name>".
- **Page briefs** are for the clusters that matter (money pages, topic hubs) — skip do-not-target and trivial clusters.
- **Research log** — append an entry: what was clustered, the date, the verdict (cluster count, pages to create, cannibalization found). Never replace prior log rows.

**The write loop (every write, every time):**

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the cluster map and page briefs; **replace** the cluster map with the newly confirmed one; **append** a Research log row — leave prior rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Page Map" "<markdown>" --in <project_id> --vault <seo_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+)** — prefer `-` for large or multiline markdown to avoid shell quoting and argument-length limits. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Number of clusters
- Pages to create
- Existing pages to update
- Cannibalization or consolidation issues
- Spend note — "no spend (reused or analysis-only)" or "small SERP batch on <N> borderline terms"
- Recommended next action: `seo-strategy` (content opportunities / entity map), or `seo-rank-tracking` if pages are live

## Guardrails

- Do not over-cluster tiny keyword sets. Fewer than 10 usable terms → a simple map, no page briefs.
- Do not rely on lexical similarity alone. SERP intent wins.
- If existing URL data is missing, label target pages as proposed — never invent a page's URL.
- Do not call keyword research tools to re-expand the set — the saved set is the input, not a starting point.
- The Project Context doc is setup-owned; `SEO — Keyword Research` is keyword-research-owned. This skill writes only its own doc — the only exception is the asked merge into Project Context `## Key pages`, and that happens only when Matt says yes to the step-8 offer.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Clustered on word overlap | Skipped the intent check | SERP intent wins; two similar words with different intents split, not merge |
| Invented keywords or pages | Started without the input docs | Refuse if `## Saved keywords` is missing or undated; point Matt at keyword-research |
| Target pages invented | No existing URL data | Label proposed pages as "proposed: <name>", never a fake URL |
| Map written without confirmation | Skipped step 8 | Present the map; only a confirmed yes gets written |
| KR themes promoted into the map | Read `## Clusters` as a page map | Read only `## Saved keywords`; KR themes are run themes, not pages |
| Cannibalization flagged on a shared target | Confused "two keywords, one page" with cannibalization | That's a correct cluster; cannibalization is two live URLs or two target pages fighting one intent |
| Primary keyword = biggest volume | No primary rule applied | Primary = best intent fit × plausible KD × volume; secondaries support it |
| Earlier cluster maps clobbered | Overwrote instead of replacing-then-append | Replace the cluster map, append the log row, leave other sections untouched |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the cluster map onto it |