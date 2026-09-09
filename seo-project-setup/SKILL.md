---
name: seo-project-setup
description: Populate a client's shared SEO project context — site scope, goals, positioning, competitors, key pages, and writing preferences — stored as the SEO — Project Context doc in that client's Basecamp (Internal > SEO). That doc is read first by every other SEO skill (keyword-research, seo-rank-tracking, seo-strategy), so seeds, competitors, positioning, and key pages stop being judgment calls each run. Use when Matt says "set up SEO for [client]", "SEO project setup", "/seo-project-setup", "update the SEO context for [client]", or when another SEO skill reports the context doc is missing.
---

# SEO Project Setup Skill

## Goal

Interview Matt about one client's SEO project and store the answers in that client's `SEO — Project Context` doc in Basecamp. That doc is read first by every other SEO skill, so it survives new sessions and new agents, and research skills stop re-deriving what's already known. This is a context setup workflow, not a full audit, and it spends no credits. Run it once to establish context, then again whenever context goes stale — it fills only the gaps, so re-runs are short.

## Tone

Be direct, practical, and structured. Ask questions in small batches. Explain why each item matters only when useful. Matt is experienced — skip the SEO-101 framing, keep it tight.

## Where the answers go

All writing happens through the basecamp CLI into the client's **Docs & Files → Internal → SEO folder**, document titled **`SEO — Project Context`** — a stable contract title, never recreated. The doc is the record; the session holds nothing. Written in markdown (Basecamp 5 renders it, GFM tables included) — clean prose with tables where lists genuinely help. Humans read this doc too; keep it readable, not agent-minified.

### Frozen heading contract

These headings and columns are exact. **Do not rename them.** Other skills parse the doc by these names, so a renamed heading is a silent break. **Formats only, no real client data** — the examples below use a placeholder domain; never copy a filled-in client's values here.

```markdown
## Business overview
Domain: https://example.com
Site launched: YYYY-MM-DD
## Current goal
## Positioning
## Writing preferences
## Competitors
| Domain | Name | Notes |
## Key pages
| URL | Role | Topic | Notes |
## Search Console
Property: sc-domain:example.com
## Analytics
Fathom site id: <id or "not in use">
Fathom goals: <event names, comma-separated, or "not in use" / omitted>
## Reporting
Plan: <Foundation | Growth — the invoice and the report shape; omitted for off-plan/private deals>
Scoreboard metrics: <comma-separated metric names for the monthly report's scoreboard, or omitted>
Brand terms: <comma-separated terms that mark a search query as brand (client name, product names, common misspellings), or omitted>
## Research log
| Date | Summary |
```

Roles stay `hub | spoke | money | other` — keyword-research and seo-strategy key off them.

### The write loop (every write, every time)

Basecamp docs are full-document replace. "Write as you go" must not mean "create extra docs" or "clobber earlier sections." The procedure:

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section and every research-log line untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

Without file-id + full-replace + re-read, "never recreate" is a wish. The post-write check applies to **every** write — create and update — not just first-run.

### First create (only when the doc doesn't exist)

The write loop assumes a doc exists. On first run, if the title is missing in the SEO folder, create it **once with every heading present and empty tables** — never a partial doc with only Business overview:

1. Build the full markdown: every heading in the frozen contract, empty Competitors / Key pages / Research log tables with the correct column headers, and the placeholder `Domain:` / `Site launched:` / `Property:` / `Fathom site id:` / `Fathom goals:` / `Scoreboard metrics:` lines filled from this run's answers.
2. `basecamp -a 6191443 files doc create "SEO — Project Context" "<full markdown>" --in <project_id> --vault <seo_folder_id> --json` — **must carry `--vault`**, or the doc lands at project root (the exact failure mode the failure table lists).
3. Enter the write loop from then on — same file id, full-document updates.

### Canonical CLI shapes

The real basecamp CLI commands, verified — do not invent flags:

```text
# resolve the SEO folder id (find Internal, then SEO under it)
basecamp -a 6191443 files folders --in <project_id> --json
basecamp -a 6191443 files list --vault <internal_folder_id> --in <project_id> --json

# find the doc by exact title, ONLY in the SEO folder
basecamp -a 6191443 files list --vault <seo_folder_id> --in <project_id> --json

# read the current doc
basecamp -a 6191443 files show <file_id> --in <project_id> --json

# first create (only if title absent in the SEO folder)
basecamp -a 6191443 files doc create "SEO — Project Context" "<full markdown>" --in <project_id> --vault <seo_folder_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <seo_folder_id> --json
```

`files doc create` takes content as an argument, not stdin — the `-` stdin form silently creates an empty doc.

### Sibling-doc titles are contracts too

`SEO — Keyword Research`, `SEO — Rank Tracker`, `SEO — Page Map`, `SEO — Competitive Landscape`, `SEO — Content Opportunities`, `SEO — Entity Map & IA`, and `SEO — Local Audit` are stable titles owned by other skills. `SEO — Competitor — <domain>` and `SEO — Link Prospects — <asset-slug>` are **families of docs** owned by competitor-analysis and link-prospecting respectively — any title matching those patterns is a contract doc. This skill matches all of these by exact name (exact pattern for the families) — never fuzzy-match a variant like "Keyword research June" as the same doc, and never rename one.

## Checklist

### 1. Verify the connection and resolve the client

1. Confirm the basecamp CLI is available and authenticated. Always pass `-a 6191443` (Safaii Studio) explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
2. List projects: `basecamp -a 6191443 projects list --json`. Match the client to a project by the **exact name** Matt gave. If two projects share a similar name, stop and ask which one — never pick the first hit.
3. Ambiguous or missing match → show Matt the candidate projects and ask — never guess which project is the client.

Do not run research tools to test connectivity. If the CLI is unavailable, say so and stop; nothing can be saved without it.

### 1b. Resolve the SEO folder

The context doc lives in **Docs & Files → Internal → SEO**. Get the folder ids before doing anything else:

1. `basecamp -a 6191443 files folders --in <project_id> --json` — find the Internal vault id.
2. `basecamp -a 6191443 files list --vault <internal_id> --in <project_id> --json` — look for the SEO folder.
3. If SEO is missing under Internal, create it (vaults API: `basecamp -a 6191443 api post "/buckets/<project_id>/vaults/<internal_id>/vaults.json" --data '{"title":"SEO"}'`), then confirm it exists.
4. **Never create the context doc until the SEO folder id is known** — a doc at project root or in another vault is a failure, not a shortcut.

### 2. Read what is already there

Resolve the SEO folder id first (step 1b), then find `SEO — Project Context` **only in that folder** via `files list --vault <seo_folder_id>`. Listing the whole project risks grabbing a root-level namesake. Read it if present, and also read `SEO — Keyword Research` and `SEO — Competitive Landscape` if they exist (the landscape doc carries competitor authority notes) — their saved keywords and competitor rows already answer some questions. There is no `SEO — Backlinks` doc; backlink work lives in `SEO — Competitor — <domain>` and `SEO — Link Prospects — <asset-slug>`, so don't look for one. Show Matt a short summary of what's known and what's missing. Confirm or correct existing entries rather than re-asking questions already answered — this skill is often re-run after another skill filled in part of the context.

### 3. Collect website scope

Ask for:

- Primary website/domain
- Additional domains or subdomains
- Important products, services, categories, or pages
- Target countries/languages
- Whether the site is new, established, migrating, or recovering from a drop
- When the current site launched — record it as a `Site launched:` line. Ask; the client knows the date. If analytics or Search Console tracking predates the launch, note that too — pre-launch data describes a different site, and sibling skills will otherwise misread "tracking went live" as "site went live"
- CMS or publishing workflow, if relevant (one line in Business overview is enough)

Write the durable parts to **Business overview**: what the business does, who it is for, the target markets/locales, and the site's current stage. **Lead with the primary domain as a `Domain:` line** — sibling skills read that exact line to know the site to research; without it they can't run.

### 4. Capture goals

Ask what the client wants from SEO:

- More qualified leads
- More signups/trials
- More ecommerce revenue
- More brand/category awareness
- Recovery from traffic loss
- Better ranking for specific pages

Ask for success metrics and timeframe. If goals are vague, help turn them into measurable goals such as "rank top 10 for 20 buying-intent terms" or "grow non-branded organic sessions 30% in 6 months."

Write the result to **Current goal**, including the metric and timeframe.

### 5. Capture positioning and strategy context

Ask what research already exists about the company, product, audience, and competitors. Request any notes, docs, customer interviews, positioning docs, pitch decks, or strategy memos.

Probe for:

- Who the product or site is for
- What pain it solves
- Why buyers choose it over alternatives
- Competitors and substitutes
- Strong positioning claims
- Best customers and bad-fit customers
- Existing content that already converts
- Topics the client does not want to target

Write to **Positioning**: audience, the problem, the differentiator, and any claims to defend. Ask about voice, banned words or phrases, and topics to avoid, and write those to **Writing preferences** — content-drafting workflows read that section.

### 6. Ask how to source Positioning and Key pages

Ask Matt once how he wants Positioning and Key pages sourced: the skill drafts them from the website (`webfetch` the client's `url` and key pages) for him to confirm, or he provides them himself. Default to draft-and-confirm — Matt correcting a draft beats composing from a blank box. The choice applies to both sections; if he has positioning notes already, take them and skip the draft.

**New site with nothing live to fetch → positioning comes from the interview.** If the client's site doesn't exist yet (brand-new build), there's nothing to `webfetch` — skip the draft entirely and ask Matt directly for the planned services, audience, and differentiator. The same applies if the client's `url` in the context doc is empty. Never fabricate positioning from a site that isn't there; a draft must be grounded in something real.

### 7. Save competitors

Turn the competitors and substitutes from step 5 into the **Competitors** table: one row per domain, with a short `notes` line on why they matter ("direct competitor, owns the comparison pages"). Default 3–5; more only if Matt names them.

If Matt is unsure who competes in search, **pause here.** Do not call DataForSEO. Tell Matt to run `/keyword-research` with a handful of seed keywords to name the SERP competitors, then when it's done re-read `SEO — Keyword Research`, and merge the confirmed competitors into this doc. Resume after the merge.

### 8. Inventory key assets

Ask for or discover:

- Sitemap or important URL list
- Current blog/resources/content library
- Product/category/feature pages
- Existing keyword lists
- Current rank trackers
- Linkable assets: studies, templates, tools, datasets, calculators

Save the pages that actually matter as **Key pages** — money pages, topic hubs, and the linkable assets. This is a curated shortlist, not a site inventory: 10–30 URLs is normal. Give each one a role (`hub` = category/pillar, `spoke` = supporting article, `money` = service/product/contact, `other`) and, where known, the topic it targets.

### 9. Record Search Console access

GSC is the richest first-party signal: impressions, near-ranking terms, cannibalization, pages with existing demand. `keyword-research` (and the future `keyword-clustering` skill) read it as an input, so setup must confirm it's wired.

- The GSC property comes from step 3's website scope; the service-account JSON is resolved from 1Password (`op://Secrets/GSC Service Account JSON/notesPlain`), used by `client-report`'s `gsc-fetch.rb` — setup doesn't re-invent any of that.
- Add a line to the doc's **Search Console** section: connected for property X (e.g. `Property: sc-domain:example.com`). Sibling skills read this line to know the property to query.
- If the service account hasn't been added to the client's property yet, flag it: it's a one-time manual step in Search Console (add the service-account email as a restricted user), and GSC intake will sit out until it's done.

### 9b. Record Analytics access

Fathom is the analytics signal used by `client-report`. Ask Matt for the site's Fathom site id and write it as a line in the doc's **Analytics** section (`Fathom site id: <id>`). If the client doesn't use Fathom, write "not in use" — `client-report` reads it and skips gracefully.

Then capture the goal events the client cares about — the conversions that answer "did this site do its job": form completions, call clicks, PDF downloads, bookings. Each site has its own goals (some may repeat across sites). Write them **exactly as the event names exist in Fathom** — lowercase, human-readable, matching what `fathom-analytics` created (e.g. `quote request submitted`, not `Quote Requests`) — a title-cased guess won't match the API. Write them as a comma-separated `Fathom goals:` line under `Fathom site id:` in the same Analytics section. If there are no goals or the client doesn't use Fathom, omit the line or write "not in use" — `client-report` reads the line and sits the goals out gracefully either way.

### 9c. Record scoreboard metrics

The monthly `client-report` opens with a locked scoreboard — 4–6 rows that stay the same every month so the client learns where to look and months compare. Ask Matt which numbers matter to *this* client; the usual rows are visits, the named Fathom conversions (use the exact goal names from 9b), and Google clicks. **Never average position** — it moves the wrong way when page-two impressions grow, so it reads as a loss when visibility is actually improving. Write them as a comma-separated `Scoreboard metrics:` line in the **Reporting** section. Set once, changed rarely — a scoreboard whose rows change monthly stops comparing. Omit the line for the default scoreboard: visits, total named-goal conversions, Google clicks.

Every token on the line must be one the report skill can fetch — nothing invented:

| Scoreboard token | Source |
| --- | --- |
| `visits` | Fathom visits |
| `pageviews` | Fathom pageviews |
| `uniques` | Fathom uniques |
| an exact `Fathom goals:` event name | that goal's conversions |
| `Google clicks` | GSC clicks |
| `Google impressions` | GSC impressions |

Anything else (`sessions`, `organic clicks`, `form fills`) has no field to fetch — map it to a token above or leave it off.

If the context doc predates this change and has no `## Reporting` heading, add the heading on this run — a missing section is a gap to fill, not "Matt already chose the default."

### 9d. Record plan and scoreboard

The `## Reporting` lines are the monthly report's scope contract. Ask Matt, then write:

- `Plan:` — `Foundation` ($150/mo — watch + report, no change hours; report ships **without** Rankings) or `Growth` ($500/mo — Foundation plus acting on the data: search and conversion work, quarterly tests, content when the data says; report ships **with** Rankings, standing every month). Omit the line for off-plan or private deals that fit neither, and default those to Foundation-only report scope unless Matt says otherwise. The plan name is the whole scope contract — the report derives everything from it.
- `Scoreboard metrics:` (step 9c above).
- `Brand terms:` — the terms that mark a search query as brand (the client's name, product names, common misspellings people actually type). The monthly report splits Google clicks into brand vs non-brand with these — matching is substring, case-insensitive, so shorter tokens match more variants. Omit for the default of no split.

A client who changes plans gets a re-run of this skill — one line edits, no drift.

### 10. Recommend the next workflow

After intake, recommend one next step — pick from the guide's router, not a second guide:

- `keyword-research`: seeds, volumes, and a saved-keyword set
- `keyword-clustering`: when the question is pages, not positions — map the set onto the site
- `seo-rank-tracking`: when keywords are already saved and they want positions tracked
- `seo-strategy`: when research exists and they want content opportunities or entity mapping
- `local-seo`: storefront clients where the Maps pack matters
- `seo-audit`: fresh-domain client-facing one-pager
- `client-report` (existing clients): when they want the monthly maintenance report

## Output format

Use a checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize:

- Client and project resolved
- Sites in scope
- Goals (metric + timeframe)
- Known positioning
- Competitors saved
- Key pages saved
- Search Console status (wired / service-account add pending)
- Analytics status (Fathom wired / not in use)
- Scoreboard metrics (locked rows / default)
- Brand terms (brand vs non-brand split / no split)
- Plan (Foundation / Growth / off-plan)
- Sections still missing from the context doc
- Recommended next workflow

Return the doc URL. Tell Matt he can read and edit everything saved in the doc directly in Basecamp.

## Guardrails

- Keep setup lightweight. Matt should feel oriented, not assigned homework.
- Confirm facts with Matt before writing them. Inferences from the site are fine to propose, but they get saved as agreed answers, not guesses. Distinguish source evidence from inference.
- Never re-ask what's already recorded. Merge new answers into existing prose on a re-run instead of discarding it.
- Keep setup focused on setup and context unless Matt asks for live research.
- This skill spends no credits. If a step needs live data (e.g. the competitor SERP check in step 7), route it through `keyword-research` and let that skill handle its own logging and doc — don't run DataForSEO calls directly here.
- The Project Context doc is setup-owned. Research and strategy skills keep their own run history in their own docs — this skill never writes anywhere else.
- Research log: first run logs "Project context established, <date>." Re-runs log a one-line diff ("added 4 key pages, corrected goal timeframe") so the log records change, not just "updated."

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| Doc in the wrong folder | Created at project root or in a non-SEO vault | Doc must live in the Internal → SEO folder; move or update there, never treat a root copy as canonical |
| Create succeeded but vault is wrong | `--vault` dropped or wrong id on create | Delete the misplaced doc and re-create with `--vault <seo_folder_id>`; never start the write loop on that file id |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly; this skill never runs on any other account |
| Empty doc after create | Used the `-` stdin form | Pass content as an argument; verify content length after create |
| Re-asked a question already answered | Skipped the read step | Read the existing doc (and research docs) before interviewing |
| Earlier sections clobbered | Full-doc replace without re-reading first | Use the write loop: read → patch one heading → upload entire doc → re-read and assert |
| Headings drift between runs | Renamed a section | Follow the frozen heading contract exactly; sibling skills parse these names |
| Interview dragged on | Front-loaded the whole questionnaire | Small batches, write as you go, skip knowns |
| Duplicate doc over time | Title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Context lost on re-run | Overwrote instead of merged | Merge new answers into existing prose; preserve every existing section and log entry |
| Competitor list invented | Asked for a SERP check mid-skill and guessed | Pause, route through `/keyword-research`, re-read its doc, merge confirmed competitors |