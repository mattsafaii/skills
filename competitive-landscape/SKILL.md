---
name: competitive-landscape
description: Map the SEO market for one client — who wins the target queries, what content is working, where the openings are — and write it to the client's SEO — Competitive Landscape doc in Basecamp (Internal > SEO). The market query set comes from the client's saved keywords, competitors start from the context doc, and DataForSEO fills in recurring domains, footprints, and authority. Use when Matt says "competitive landscape for [client]", "who's winning this market", "/competitive-landscape", "market overview for [client]", or "map the SEO market for [client]". For a deep dive on one domain, use competitor-analysis. Never recreate the doc under a new title.
---

# Competitive Landscape Skill

Answers: "Who is winning this SEO market, what content is working for them, and where are the openings?" A market-level read across several competitors — for a deep dive on one domain, use `competitor-analysis`.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** MCP calls are real geo-located measurements. Every observation carries a date: "as of <date>". **Market is US by default** (the DataForSEO `location_name`) — a different market only if the context doc says so. Bare footprints or ranks are never citable.
2. **Spend is capped and batched.** This is the spendiest skill in the chain — control it: reuse the last 30 days when the query set matches, batch SERP checks, default to the top 3–5 domains before expanding, and never re-run a query twice in a session. (Rough scale: SERP ≈ $0.002; domain overview ≈ $0.02; ranked keywords and backlink summaries ≈ $0.02.)
3. **Failed call → Unknown, never a guess.** A call that fails goes on the doc's Unknown list or is skipped silently.
4. **Distinguish SEO competitors from business competitors.** The pages winning search traffic are often publishers, directories, forums, or comparison sites — not direct product competitors. Label domain types clearly; don't assume a publisher is a product competitor.
5. **Don't overstate traffic.** DataForSEO footprint numbers are estimates. Call them estimates.
6. **Confirm before write.** The landscape doc is written only after Matt confirms. An ambiguous response is not confirmation.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- Inputs come from Basecamp, never re-researched: the market query set from `SEO — Keyword Research`'s `## Saved keywords` (required, with a dated run header), and the starting competitor roster from `SEO — Project Context`'s `## Competitors` (optional — a starting roster, not a gate; if empty, infer from SERP and confirm with Matt). Never invent keywords.
- The doc lives in the client's **Docs & Files → Internal → SEO folder**, team-only, titled **`SEO — Competitive Landscape`** — a stable contract, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client

Matt names a client. Match it to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a project or domain.**

### 2. Read the inputs

Read `SEO — Project Context` — the `## Competitors` table (starting roster + why they matter), `## Key pages`, positioning, and target markets. Read `SEO — Keyword Research` — **only** `## Saved keywords` (the market query set), the `## Research run` header (`Date:` / `Location:` — used by the refuse rule), and the `## Research log` (last run). **Refuse to run** if the saved set is missing/undated — tell Matt to run `keyword-research` first.

### 3. Check reuse

If the same market was mapped within the last 30 days — reuse fingerprint = saved-set date + count + market/location + competitor roster — reuse that result and say so instead of re-buying it.

### 4. Build the market query set

The saved set is a **tracking set** — what Matt agreed to chase, often commercial and already filtered. It answers "who wins *our* money queries," not "who wins the category." Use it as the default, then sharpen:

- **If it's one intent** (mostly commercial), ask Matt to add 3–5 informational/comparison terms from the positioning — no new discovery dump, just enough to see who owns the whole category.
- **If it's under ~10 terms**, call the read **directional**, or confirm a small `dataforseo_labs_google_related_keywords` broaden — capped (5 seeds × ~10 terms, then stop).

Write the final query list under `## Query set used` — that's the next run's reuse fingerprint.

### 5. Find the recurring domains

- **Start from the roster:** the context doc's competitors are the starting list — ground the read in them.
- **Confirm with SERP data:** `dataforseo_labs_google_serp_competitors` across the query set surfaces the domains that actually recur. Use `serp_organic_live_advanced` for live SERP composition on a few representative queries (at most ~10 queries, batched).
- If the context doc's competitor list is empty, infer the roster from the SERP competitors and confirm with Matt before spending deeper on it.

### 6. Group domains by type

Label each recurring domain:
- **Direct product competitor** — sells the same thing
- **Publisher/media** — editorial content
- **Marketplace/directory** — listings, comparisons
- **Community/forum** — discussions
- **Documentation/resource** — how-tos, references

This is the guardrail in practice — a publisher owning the SERP is not a product competitor.

### 7. Size the strongest domains — and the client

Run the same footprint calls on the **client's own domain** plus the top 3–5 recurring domains (before expanding):
- **Organic footprint:** `dataforseo_labs_google_domain_rank_overview` (estimated traffic, ranking keywords, distribution) — same date/location, labeled estimate.
- **Keyword coverage:** `dataforseo_labs_google_ranked_keywords` for the direct competitors and relevant publishers — what they rank for, at what position, with what intent.

The client's row is what makes the "opening" concrete — without it, "the gap" is a vibe. For the client's row only, if GSC is wired, anchor with the existing first-party fetch (no new paid call): clicks/impressions beat an estimated traffic number for *their* row. Batch these; don't expand beyond the top 5 without a reason.

**Hard spend ceiling:** after the default batch (SERP competitors + ≤10 live SERPs + ≤5 domain overviews + ranked keywords for those 5 + the client's row), ask before any further call.

### 8. Authority (optional)

Use `backlinks_summary` for the client's domain and the top competitors **when authority appears to be why someone wins** — a publisher or directory dominating on reach, or the user asks why. Compare referring domains and spam score. **Authority calls sit inside the step-7 spend ceiling** — they also need a yes after the default batch. If backlinks data is unavailable, continue on SERP/domain evidence and say so — don't stall.

### 9. Synthesize the market read

Patterns across the data:
- **Winning content types/themes** — what the recurring leaders publish and rank for
- **SERP formats** — informational content, directories, comparison pages, local packs
- **Authority advantages** — who wins on reach vs. relevance
- **Underserved angles** — the themes/format gaps the leaders ignore

### 10. Confirm the landscape with Matt

Present before writing:

- **Market read:** leaders, most winnable opportunity area, biggest barrier to ranking
- **The competitive table** (below)
- **Query set used**, content formats working, keyword/theme gaps, authority observations

| Domain | Type | Why they matter | Organic footprint | Winning themes | Weakness/gap |
| --- | --- | --- | --- | --- | --- |

**Do not write until Matt confirms.** Revise in place if he changes the read. After confirmation, **offer** to merge newly-confirmed competitors into `SEO — Project Context`'s `## Competitors` — ask, don't silently edit; the context doc is setup-owned.

### 11. Write the doc and log

Write `SEO — Competitive Landscape` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed.

```markdown
## Market read
Leaders:
Most winnable area:
Biggest barrier:
## Competitive table
| Domain | Type | Why they matter | Organic footprint | Winning themes | Weakness/gap |
## Query set used
## Content formats working
## Keyword/theme gaps
## Authority observations
## Research log
| Date | Summary |
```

- **`## Competitive table` is the contract** — one row per domain, labeled by type. **The client's domain is always the first row with type `client`** (its GSC-anchored position where available); the competitors follow.
- **Research log** — append an entry: what market was mapped, the date, the verdict (leaders, winnable area, new competitors confirmed). Never replace prior log rows.

**The write loop (every write, every time):**

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the read sections; **replace** the competitive table with the newly confirmed one; **append** a Research log row — leave prior rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Competitive Landscape" "<markdown>" --in <project_id> --vault <seo_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes content as an argument, not stdin** — the `-` stdin form silently creates an empty doc. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Market leaders
- Most winnable opportunity area
- Biggest barrier to ranking
- Spend note — "reused last 30 days" or "new spend: SERP batch + top-N domain sizing"
- Recommended next action: `competitor-analysis` on **<the one named domain worth diving into>**, `seo-strategy` (content from the gaps), or `seo-rank-tracking` (if pages are live)

## Guardrails

- Distinguish SEO competitors (publishers, directories) from business competitors — label types clearly.
- Do not overstate exact traffic; DataForSEO footprint numbers are estimates.
- A small query set → call the result directional.
- Do not assume a publisher is a product competitor.
- **The client's domain is always a row in the table** — the gap is only concrete against it.
- **Local markets:** this skill covers organic. If the context doc says the client is a local business, tell Matt this skill will miss pack winners — don't half-run Maps.
- Spend is capped: reuse when the market matches, top 3–5 domains, batched calls. Don't let this skill expand into exhaustive research.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Publisher treated as a product competitor | Skipped the type labeling | Label domain types clearly; a publisher owning the SERP is not a competitor in the same bucket |
| Traffic numbers overstated | Presenting estimates as exact | DataForSEO footprints are estimates — say "estimated" |
| Re-bought research | Skipped the reuse check | Same market mapped < 30 days ago → reuse and say so |
| Invented the query set | Didn't read `## Saved keywords` | The market query set starts from the saved set, then sharpens — never a fresh discovery dump |
| Client's domain omitted from the table | Only sized competitors | The client is always a row; the gap is only concrete against it |
| Doc written without confirmation | Skipped step 10 | Present the read; only a confirmed yes gets written |
| Earlier landscapes clobbered | Overwrote instead of replacing-then-append | Replace the competitive table, append the log row, leave other sections untouched |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the landscape onto it |