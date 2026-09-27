---
name: competitor-analysis
description: Analyze one competitor's organic footprint, ranking keywords, content themes, backlinks, and gaps, and write the findings to the client's SEO — Competitor — <domain> doc in Basecamp (Working on new projects). Deep dive on a single named domain — for the market-level read across several, use competitive-landscape. Compares against the client's own domain by default when the context doc has one, GSC-anchored on the client row. Use when Matt says "competitor analysis for [domain]", "analyze [domain]", "what's [competitor] doing in SEO", "/competitor-analysis", or "deep dive on [domain]". The doc title is stable per competitor — never recreate it under a variant.
---

# Competitor Analysis Skill

Analyzes one competitor deeply enough to decide what to learn from, avoid, counter-position against, or outrank. For a named competitor — if the market leaders aren't identified yet, run `competitive-landscape` first to name them.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** MCP calls are real geo-located measurements. Every observation carries a date: "as of <date>". **Market is US by default** (the DataForSEO `location_name`) — a different market only if the context doc says so. Bare footprints or ranks are never citable.
2. **Spend is capped and batched.** One domain overview, one ranked-keywords pass (filtered), optional backlink summary, and a small head-to-head SERP batch — then ask before any further call. No re-runs of the same query in a session. (Rough scale: domain overview ≈ $0.02; ranked keywords ≈ $0.02; backlink summaries ≈ $0.02; SERP ≈ $0.002.)
3. **Failed call → Unknown, never a guess.** A call that fails goes on the doc's Unknown list or is skipped silently.
4. **Separate evidence from inference.** A keyword row is evidence. A claim about a page's content or the reason a domain wins is inference — mark it as such. Do not infer page/content patterns from keyword rows alone; use SERP or `webfetch` on the actual page for page-level claims (a SERP snippet is not "their guide is 3,000 words").
5. **Filter for business fit, not just traffic.** Not all competitor keywords are desirable — drop branded, off-strategy, and irrelevant terms.
6. **Never recommend copying.** Recommend a stronger angle or a better answer to the same intent.
7. **Confirm before write.** The analysis doc is written only after Matt confirms. An ambiguous response is not confirmation.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `SEO — Project Context` in Internal → SEO. For research docs, check exact titles in Working and legacy Internal → SEO; stop if both have the same title. Use the existing folder id for updates, or Working for first create (`research_folder_id`).
- The client's own domain comes from `SEO — Project Context`'s `Domain:` line; the competitor's domain is the one Matt names (or the one `competitive-landscape` surfaced). The context doc's `## Competitors` says whether this domain is already known and what was concluded about it before.
- The doc lives in **Working on new projects**, or its existing legacy Internal → SEO folder, team-only, titled **`SEO — Competitor — <domain>`** where `<domain>` is the **registrable host, lowercase, no scheme, no `www`, no path** (e.g. `SEO — Competitor — bearcom.com`, never `www.bearcom.com` or `https://bearcom.com/radios`). Confirm that normalized string with Matt before create — it's the stable contract per competitor, never recreated under a variant.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client and the competitor

Matt names a client and a competitor domain. Match the client to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous → show Matt the candidates and ask. **Never guess a project or domain.**

Read `SEO — Project Context` — the `Domain:` line, `## Competitors` (is this domain already known? what was concluded?), target markets, positioning. If the context doc is missing, tell Matt to run `seo-project-setup` first and stop.

**Confirm the domain is an SEO competitor before the expensive pass.** If the domain is already in `## Competitors` or the landscape table, proceed. If not, don't jump to overview + ranked keywords — ask Matt, or run one cheap `dataforseo_labs/google/serp_competitors/live` overlap check against the saved-keyword set to see whether this domain actually competes for the client's terms. Only after confirmation (or a positive overlap) do you spend on the full analysis.

### 2. Check reuse

If the same competitor was analyzed within the last 30 days (same competitor domain, **same market/location** — AU vs US is not the same analysis), reuse that result and say so instead of re-buying it.

### 3. Baseline the footprint

`dataforseo_labs/google/domain_rank_overview/live` for the competitor — estimated organic traffic, ranking keyword count, rank distribution. Market from the context doc. Label estimates as estimates.

### 4. Pull ranked keywords (filtered, capped)

`dataforseo_labs/google/ranked_keywords/live` for the competitor. Filter to keep the rows relevant, then **cap the ingest**:
- **`maxRank`** — cap at the range that matters (e.g. top 50–100)
- **`minSearchVolume`** — drop near-zero-volume noise
- **`excludeBrandTerms`** — strip the competitor's own brand queries (not winnable)
- **`resultTypes`** — organic only, unless local-pack is the point
- **Hard cap** — after the filters, take the top ~150 by volume or estimated traffic. Themes built on 2,000 leftovers are sludge, and the payload costs more.

One pass, batched. Do not re-run.

### 5. Group the competitor's keywords into themes

- **Product/category terms** — what they sell and rank for
- **Alternatives/comparisons** — comparison and "vs" demand
- **Templates/tools/calculators** — free-asset demand
- **Educational guides** — informational content
- **Branded demand** — their brand (excluded from targets, noted as a moat)
- **Local/neighborhood terms** — when relevant

Filter for business fit as you go — drop what the client shouldn't chase.

### 6. Compare against the client (default when `Domain:` exists)

The gap is fake without the client row. **When Project Context has a `Domain:` line, run the comparison by default** — `dataforseo_labs/google/domain_rank_overview/live` for the client's domain too, and GSC-anchor the client's row with the existing fetch (no new paid call) — real clicks/impressions/position beat an estimated traffic number. Competitor-only only when the `Domain:` line is missing. If the client's domain isn't available, frame the analysis as competitor-only.

### 7. Head-to-head SERPs

For the important shared or target keywords, one `serp/google/organic/live/advanced` check each to compare positioning — who's on page one, where the client sits, what SERP features are present. Keep the batch small (the terms where the comparison would change the recommendation). Every observation carries date + location.

### 8. Authority (optional)

`backlinks/summary/live` for the competitor — referring domains, backlinks, spam score — **when authority appears to explain rankings** (or Matt asks why they win). Compare against the client's profile if the client row is in scope. **Backlinks sit inside the spend ceiling** — like landscape, they need a yes after the default batch. If backlinks data is unavailable, continue on SERP/domain evidence and say so.

### 9. Produce the action plan

- **What they're doing well** — the patterns that explain their visibility
- **Where they're vulnerable** — gaps, thin pages, weak themes, spammy links
- **Which pages/keywords to pursue** — business-fit targets the client can actually win
- **What to avoid copying** — and the stronger angle for the same intent

### 10. Confirm the analysis with Matt

Present before writing:

- **Competitor snapshot** — footprint, top themes, one-line read
- **Biggest lesson** — the single thing to take from them
- **Best opportunity to beat them** — the concrete opening

| Area | Competitor pattern | Evidence | Client opportunity |
| --- | --- | --- | --- |

Plus sections for top keyword themes, content/page types working for them, backlink/authority notes, head-to-head SERP observations, priority actions.

**Do not write until Matt confirms.** Revise in place if he changes the read. After confirmation, **offer** to update the competitor's note in `SEO — Project Context`'s `## Competitors` (strengths + where it's vulnerable) — ask, don't silently edit; the context doc is setup-owned.

### 11. Write the doc and log

Write `SEO — Competitor — <domain>` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed.

```markdown
## Competitor snapshot
Domain:
Footprint:
Top themes:
Biggest lesson:
Best opportunity:
## Opportunity table
| Area | Competitor pattern | Evidence | Client opportunity |
## Keyword themes
## Content/page types working
## Backlink/authority notes
## Head-to-head SERP observations
## Priority actions
## Research log
| Date | Summary |
```

- **`## Opportunity table` is the contract** — one row per area, evidence separated from inference.
- **Research log** — append an entry: what was analyzed, the date, the verdict (the competitor's strength, where they're vulnerable, priority actions). Never replace prior log rows.

**The write loop (every write, every time):**

1. Find the doc by exact title in Working and legacy Internal → SEO — stop on duplicates; never create a second copy.
2. Read the full markdown into memory.
3. Patch the analysis sections; **replace** the opportunity table with the newly confirmed one; **append** a Research log row — leave prior rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <research_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in both Working and legacy Internal → SEO. Create in Working: `basecamp -a 6191443 files doc create "SEO — Competitor — <domain>" "<markdown>" --in <project_id> --vault <research_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <research_folder_id> --json`.

**`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+)** — prefer `-` for large or multiline markdown to avoid shell quoting and argument-length limits. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Competitor snapshot
- Biggest lesson
- Best opportunity to beat them
- Spend note — "reused last 30 days" or "new spend: overview + ranked keywords + <N> SERPs [ + backlinks]"
- Recommended next action: `keyword-clustering` (turn the pursuable keywords into page targets), `seo-strategy` (content against their gaps), or `link-prospecting` (if their backlinks reveal outreach targets)

## Guardrails

- Do not treat all competitor keywords as desirable — filter for business fit.
- Separate evidence from inference. Page-level content claims need SERP or `webfetch` evidence, not keyword rows alone.
- Do not recommend copying content — recommend a stronger angle or better answer to the same intent.
- If the client's domain isn't available, frame the analysis as competitor-only.
- **Pursuable keywords are recommendations, not a new saved set** — don't write them into `SEO — Keyword Research`. Point Matt at `keyword-research` / `keyword-clustering` if he wants them tracked.
- **Local markets:** this skill covers organic. If the context doc says the client is a local business, tell Matt this skill will miss pack strength — don't half-run Maps.
- The client's row is GSC-anchored where wired; the competitor's row is estimated. Don't blur the two.
- Spend is capped: one overview, one ranked pass (capped at ~150), optional backlinks, small SERP batch — **then ask before any further call, including backlinks**; authority calls aren't free extras after the default batch.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Analyzed the wrong competitor | Took the domain from the landscape without confirming | The competitor domain comes from Matt's naming or the landscape table — confirm which domain before spending (step 1's SEO-competitor check) |
| Pursuable keywords written into `SEO — Keyword Research` | Treated recommendations as a new saved set | Pursuable keywords are recommendations; point Matt at keyword-research/clustering if he wants them tracked |
| Branded terms treated as targets | Filter skipped | `excludeBrandTerms`; the competitor's brand is a moat, not a target |
| Page/content claims from keyword rows alone | Evidence/inference not separated | Keyword rows are evidence of what ranks; page-level claims need SERP or web evidence |
| Recommended copying | Confused a gap with a template | Recommend a stronger angle, never a copy |
| Client row estimated instead of GSC-anchored | Skipped the existing fetch | Anchor the client's row with GSC where wired; competitor row stays estimated |
| Re-bought research | Skipped the reuse check | Same competitor analyzed < 30 days ago → reuse and say so |
| Doc written without confirmation | Skipped step 10 | Present the analysis; only a confirmed yes gets written |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. The `<domain>` in the title is part of the contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the analysis onto it |