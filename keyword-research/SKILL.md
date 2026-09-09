---
name: keyword-research
description: Find keyword opportunities for one client and write them into that client's SEO — Keyword Research doc in Basecamp (Internal > SEO). Starts with the cheapest signal that has data — Google Search Console striking-distance terms for an established site, seeds + DataForSEO for a new one — then scores and filters, confirms the saved set with Matt, and writes it. Pure keyword research — no backlinks, no clustering. Use when Matt says "keyword research for [client]", "/keyword-research", "find keywords for [client]", or "what keywords should [client] target". The saved-keyword set is the contract the rank-tracking skill reads — never recreate the doc under a new title.
---

# Keyword Research Skill

Turns a client's seeds + first-party search data into a prioritized, confirmed keyword set, written to their `SEO — Keyword Research` doc in Basecamp. Basecamp is the record; this skill exists so the research survives the session.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** MCP calls are real geo-located measurements. Every data row in a doc carries a date: "as of 2026-09-01". **Market is US by default** (that's the DataForSEO `location_name`) — a different market only if the context doc's target markets say so. A bare volume or rank is never citable.
2. **Every call charges money.** Batch up to 1,000 keywords into one volume/difficulty task. One pass, no re-runs of the same query in a session. (Rough scale: keyword-volume tasks ≈ $0.09 each regardless of count; SERP checks ≈ $0.002 each.)
3. **Failed call → Unknown, never a guess.** A call that fails goes in an "Unknown" line or is skipped silently. Never hand-wave a number. If DataForSEO returns no value for a field, write `unknown`.
4. **A snapshot, not a trend.** One call = one point in time. No implied change without multiple dated calls.
5. **Reuse within 30 days, never across clients.** Same client, same seeds, **and same GSC-wired-or-not as the last run** (a run that adds striking-distance terms is a different seed set), dated under 30 days → reuse the result and say so instead of re-buying. Another client's table, or an undated run, is never reused — throw it out and re-fetch.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`, then read the client's `SEO — Project Context` doc (Internal > SEO) for the domain, positioning, competitors, and key pages. The domain comes from the context doc's `Domain:` line — never guessed.
- GSC data is fetched with the shared script: `~/Code/scripts/gsc-fetch/gsc-fetch.rb` (canonical copy, shared with client-report — no per-skill copies; Ruby stdlib only, no deps). The property comes from the context doc's Search Console section; the service-account JSON is resolved from 1Password (`op://Secrets/GSC Service Account JSON/notesPlain`) — never a file on disk.
- The doc lives in the client's **Docs & Files → Internal → SEO folder**, team-only, titled **`SEO — Keyword Research`** — a stable contract, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client

Matt names a client. Match it to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a project or domain.**

### 2. Read the project context and your own doc

Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does (match project by name, walk Internal → SEO). Do not invent a second folder walk. Find `SEO — Project Context` and read it — the `Domain:` line, target markets, positioning, competitors, key pages. If it's missing, tell Matt to run `seo-project-setup` first and stop — never research a client whose context isn't recorded.

Then find `SEO — Keyword Research` and read its **Research log**: if the same research ran within the last 30 days (same client, **same seeds, and same GSC-wired-or-not as the last log row**), reuse that result and say so instead of re-buying it. A run that adds GSC striking-distance terms is *not* the same seed set — don't reuse just because the calendar is inside 30 days.

### 3. Start with the cheapest signal that has data

GSC only shows terms the site *already has impressions for* — it points at where you are, not where you could be. So the ordering depends on the project's stage:

**Established site with GSC history → GSC first.** Striking-distance terms are the highest-ROI keywords you'll find, and it's free, so it sharpens what you spend DataForSEO money on. Fetch the property from the context doc:

```bash
cd ~/Code/scripts/gsc-fetch
GSC_SERVICE_ACCOUNT_JSON="$(op read 'op://Secrets/GSC Service Account JSON/notesPlain')" \
ruby gsc-fetch.rb \
  --property "<GSC_PROPERTY from context doc>" \
  --start <3-months-ago> --end <today> \
  --query-page
```

Use the output to sharpen the research before buying anything:
- **Striking-distance terms** — queries at positions 5–20 with impressions are the highest-ROI seeds; add them to the candidate list even if they're not in the seed set. These get worked first.
- **Pages with existing demand** — top pages by impressions tell you which existing pages deserve keyword work; note them for clustering.
- **Cannibalization — from real data, not structure.** The `query_page` output maps each query to the URLs earning its impressions. A query appearing against **two different URLs** is confirmed cannibalization — flag it in the research log so `keyword-clustering` reads it. If the query_page table is empty (GSC skipped or no combined rows), don't invent it.

**New or empty site → skip GSC, go straight to DataForSEO.** A brand-new property has no impressions yet — GSC starts collecting the moment the site gets traffic, so a fetch on a new project returns zeros. That's not a failure and not a stall: note "GSC too new, no data yet" in the research log and run the research on DataForSEO from the context doc's seeds. If GSC isn't wired at all (no note in the context doc, or the service account hasn't been added to the property), same thing — skip with a one-line note, never fail the run, never fabricate first-party data.

**A neglected existing site is still "established" — do not skip GSC just because no one has done SEO.** An old site that was never worked on can still have years of impressions in Search Console. If the property is wired and has data, harvest those striking-distance terms first regardless of whether any SEO work was ever done. "Never did SEO" ≠ "new site."

### 4. Gather seed keywords

Take the seed set from the project context (positioning + business overview). If GSC had data (step 3), merge the striking-distance terms in — they get worked first. If the doc doesn't pin down seeds, ask Matt for the client's core topics/services (3–5). Confirm the seed shortlist with Matt before spending on it.

### 5. Discover candidates — one batched pass

- **Suggestions first:** `dataforseo_labs_google_keyword_suggestions` per seed keyword is the primary idea source — it returns on-topic long-tail queries, not category noise. Take up to ~20 per seed, dedupe, keep the combined list under ~100 candidates.
- **Skip `keyword_ideas` for enterprise/B2B clients** — it returns consumer-driven category junk ("wifi test", "wifi router") that has to be thrown away. Use it only when suggestions come back too thin for a consumer-facing client.
- **Metrics:** one `dataforseo_labs_google_keyword_overview` task for the whole candidate list → volume, difficulty, CPC, intent.

### 6. Filter the candidates

Remove anything that is:
- **Irrelevant** — off-topic to the client's business or positioning
- **Duplicate** — the same query under a different spelling/casing
- **Branded-only** — the client's own brand terms (not winnable from another domain)
- **Off-intent** — intent that doesn't fit what the client can satisfy

### 7. Prioritize by practical opportunity, not volume alone

Score the survivors against every factor — a term wins on the combination, not any single one:

- **Strong match** to the client's product/page/topic
- **Clear search intent** — you can say what the searcher wants
- **Reasonable difficulty** — KD low enough that ranking is plausible
- **Useful volume/CPC signal** — demand or commercial value that matters
- **SERP where the client can compete** — the front page isn't all incumbents and publishers

### 8. Inspect SERPs for load-bearing terms

For candidates where intent is ambiguous or the volume makes the call load-bearing, run one `serp_organic_live_advanced` check per term to see who actually owns the page. Keep this small and targeted — only terms where the SERP would change the recommendation. Note the finding in the priority decision.

### 9. Confirm the saved set with Matt

Present the shortlist before writing anything:

- **Best opportunity theme** — the cluster to attack first
- **Top keywords to target now** — with one line each on why
- **Keywords to save** — the tracking set (this is the rank-tracking contract)
- **Risks / SERP caveats** — what could make these hard

A compact table:

| Keyword | Intent | Volume | Difficulty | CPC | Priority | Notes |
| --- | --- | --- | --- | --- | --- | --- |

**Do not save or write the set until Matt confirms it.** Revise in place if he changes the selection. An ambiguous response is not confirmation.

### 10. Write the doc and log

Write `SEO — Keyword Research` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed. Other skills parse by them.

```markdown
## Research run
Date:
Location: (US unless the context doc says otherwise)
Seeds:
GSC: wired | skipped
## Clusters
### <cluster name>
| Keyword | Volume | Difficulty | Intent | Notes |
## Saved keywords
| Keyword | Cluster | Volume | Difficulty | Intent | Notes |
## Research log
| Date | Summary |
```

- **`## Saved keywords` is the only section `seo-rank-tracking` may read.** Keep it the confirmed set, dated by the run header above it. An undated saved set is not a tracking contract.
- **`###` cluster headings are themes for this run, not a page map** — that's `keyword-clustering`'s job. Don't let this skill drift into clustering.

**The write loop (every write, every time):**

Basecamp docs are full-document replace. On a re-run, create-or-replace-the-whole-file would wipe the previous research log and any saved set Matt already confirmed. The procedure:

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the clusters; **replace** `## Saved keywords` with the newly confirmed set (rank-tracking needs a single current set — old sets live in the research log, don't accumulate); **append** a Research log row — leave the prior log rows and other sections untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Keyword Research" "<markdown>" --in <project_id> --vault <seo_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes content as an argument, not stdin** — the `-` stdin form silently creates an empty doc. Verify content length after any write.

After Matt confirms the saved set (step 9), offer a one-line merge of newly-discovered competitors into `SEO — Project Context`'s Competitors table — ask, don't silently edit; the context doc is setup-owned.

Return the doc URL, and state which keywords made the saved set — that's what rank tracking will chase.

## Output format

When the run finishes, summarize in-session (highest signal first):

- Best opportunity theme
- Top keywords to target now
- Keywords saved
- Risks or SERP caveats
- GSC status (wired / skipped)
- Spend note — "reused last 30 days" or "new spend on <N> keywords" so Matt can see whether money moved
- Recommended next action: run `seo-rank-tracking` (keywords are confirmed), `seo-strategy` (content/entities), or `seo-project-setup` (context missing)

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Saved set written without confirmation | Skipped step 9 | Present the shortlist; only a confirmed yes gets written |
| Bare metrics in the doc | Forgot the measurement rule | Every number carries date + location; undated numbers are never written |
| One client's data in another's doc | Reused another client's table or an undated run | Throw it out and re-fetch; same-client, same-seeds, same GSC-wired-or-not, dated under 30 days is the only reuse allowed |
| Saved set written without date+location on the run header | Run header skipped | An undated saved set is not a tracking contract — the run header must carry date and location |
| GSC data missing | Service account not added to the client's property | Skip the GSC step with a one-line note; flag the one-time Search Console add for Matt |
| GSC claim overreaches | Striking-distance terms presented without positions/dates | GSC rows carry the query, position band, and the date range; no bare "we rank here" |
| Branded terms in the saved set | Filter step skipped | Remove the client's own brand terms in step 6; they're not winnable targets |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the saved set onto it |
| Doc exists but is empty | Created with the `-` stdin form | Pass content as an argument; verify content length after create |