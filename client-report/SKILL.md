---
name: client-report
description: Generate the combined monthly report for a Safaii Studio Foundation or Growth client — runs Matt's tribunal audit CLI against the client's site, diffs against last month's run, pulls Fathom Analytics and Google Search Console data for the same window, and consumes the Rank Tracker / market read as the Rankings section (standing on Growth only — Foundation omits the heading and the appendix) — then drafts a ready-to-send month-over-month report in the standardized frozen template (opening verdict, locked scoreboard, what I did, site health, traffic and search, rankings) for Matt's review. Report drafts live in the client's Docs & Files > Internal > Reports; nothing posts or sends without Matt's explicit approval. Content/approval asks ship as separate standalone messages, never inside the monthly report. Use whenever Matt says "client report for [client]", "/client-report [client]", "monthly report for [client]", "run the monthly audit for [client]", or it's report time for a plan client (Foundation or Growth). Clients only — prospects get the teardown skill; ad-hoc audits get audit-website.
---

# Client Report Skill

Turns tribunal's run history + Fathom + Google Search Console into the monthly proof-of-value report for Foundation and Growth clients, consuming the Rank Tracker and market read (keyword movement) as the Rankings section — **standing on Growth only; a Foundation client omits the heading and the appendix entirely**. The scan diff says what changed, analytics and search data say what it did, Rankings says where the keyword set stands. One combined report per month, in Matt's client voice, reviewed by Matt before anything reaches a client. Every report uses the same frozen body (step 5) so months and clients compare — only the numbers and the sections with data change. In client prose it's never a "program" — say tracking / the keyword set.

**Cadence decision (2026-09-02): the monthly report is the single combined report.** On Growth clients it folds in the Rankings section every cycle — not as optional color, as a standing section (one line when tracking is quiet); on Foundation the heading sits out like any other out-of-scope section. Content/approval asks are **never** in the monthly report at all — zero mentions, not even status references. They go out as their own standalone message when they happen, their published results land in the next monthly report, and only the handoff email may carry an ask (one line, step 7a) when something is genuinely pending. Report drafts always go to the client's **Docs & Files > Internal > Reports** folder.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. Each client's report posts to **that client's own Basecamp project** (matched by name) — never anywhere else.
- **The report is an artifact, not a message body.** The flow: create the report doc in the client's **Internal > Reports** folder (team-only, born hidden), Matt reviews and manually moves it to **Deliverables > Reports** (client-visible — the move flips visibility), then a short message posts to the client's Message Board with a link to the moved doc. The report itself lives in Docs & Files; the message is the email-body-style handoff.
- Client and project are resolved from Basecamp, never a local file: the prep script at `~/Work/scripts/client-report-prep.rb` (see step 1) matches the project by name and reads per-client facts from two context docs. Company facts (domain, Fathom site id + goals) come from the master `Project Context` doc at the root of Internal — built by `project-setup` — and fall back to the SEO doc when the master doc doesn't exist yet. Search facts (GSC property, scoreboard metrics, plan, brand terms) come from the `SEO — Project Context` doc (Internal > SEO).
- **The SEO docs are consumed, never re-pulled.** Keyword positions come from `SEO — Rank Tracker`'s newest `## Run —` section and `## Tracker config` — never re-run SERP checks here. Market context comes from `SEO — Competitive Landscape`'s `## Market read` when present. On Growth clients the Rankings section is standing: if the docs don't exist, the section says in one line that tracking hasn't produced keyword positions or a market read yet (Foundation omits the heading entirely — see `Plan:`).
- tribunal lives at `~/Work/personal/tribunal`; it runs via its Docker image (see step 2).
- This skill uses the shared prep script at `~/Work/scripts/client-report-prep.rb` (canonical copy — no per-skill copies) plus the shared GSC helper at `~/Work/scripts/gsc-fetch/gsc-fetch.rb` (canonical copy, shared with keyword-research — no per-skill copies). No dependencies; Ruby stdlib only.
- Local secrets live in 1Password, resolved on demand with `op read` — the Fathom token is `op://Secrets/Fathom API Token/password`, the GSC service-account JSON is `op://Secrets/GSC Service Account JSON/notesPlain`. Both are shared across clients; nothing sits in a file on disk.

## Per-client facts come from the context docs

Company facts are owned by the master `Project Context` doc (Internal root, built by `project-setup`); search facts by the `SEO — Project Context` doc (created by `seo-project-setup`). Read the master doc first when it exists; fall back to the SEO doc for company facts when it doesn't:

- **Domain** — the master doc's `Domain:` line (Business), falling back to the SEO doc's `Domain:` line (Business overview). Must be the same form every month — tribunal slugs the target URL to find its history folder; a changed form orphans the history.
- **Fathom site id** — the master doc's `Fathom site id:` line (Access); fallback: the SEO doc's Analytics section. **Sit out on absent *or* `not in use`** — if the line is missing, empty, or literally `not in use`, the Fathom section sits out with a one-line note. It never fails the run, and never curl with a placeholder.
- **Fathom goals** — the master doc's `Fathom goals:` line (Access); fallback: the SEO doc's Analytics line: comma-separated event names, e.g. `quote request submitted, call now clicked`. Goals are per-site — each client has its own set, names may repeat across clients. **Sit out on absent, empty, or `not in use`** — same rule as the site id; the goals line never fails the run.
- **GSC property** — the context doc's `Property:` line (Search Console section). **Sit out on absent, empty, or a placeholder** — same rule as Fathom.
- **Scoreboard metrics** — the context doc's `Scoreboard metrics:` line: comma-separated names for the report's locked scoreboard rows (e.g. `visits, quote request submitted, call now clicked, Google clicks`). 4–6 rows, set once, changed rarely — a scoreboard whose rows change monthly stops comparing. **Never average position.** Absent or empty → default scoreboard: visits, total named-goal conversions, Google clicks.
- **Plan** — the context doc's `Plan:` line (`## Reporting`): `Foundation` or `Growth`; omitted for off-plan/private deals (default to Foundation-only scope and confirm with Matt). This single line gates the report's shape:

  - **Foundation — $150/mo.** Watch + report, no change hours. Report: the frozen body **minus Rankings, the Appendix, and the pages/queries tables** — short by design; the trend chart and the conversions table stay.
  - **Growth — $500/mo.** Foundation plus acting on the data: search and conversion work, quarterly tests, content when the data says so. Report: the full frozen body — **Rankings is standing** (heading every month, one line when tracking is quiet) and the Appendix is optional. Kickoff $500 unless Growth started at launch.
  - There is no third plan and no mix-and-match scope. If a custom deal ever needs partial scope, that's an explicit conversation with Matt — not a token to pre-build.
- **Rank Tracker** — the newest `## Run —` + `## Tracker config` from `SEO — Rank Tracker` (optional; consumed, never re-pulled). If absent, the Rankings line sits out.
- **Competitive Landscape** — `## Market read` from `SEO — Competitive Landscape` (optional; consumed for context only).
- If the master and SEO context docs are both missing, tell Matt to run `project-setup` (company facts) and `seo-project-setup` (search facts) and stop — never guess a domain. If only the SEO doc is missing, tell Matt to run `seo-project-setup` and stop.
- GSC setup per client: add the service account's email as a (restricted) user on the client's Search Console property once.

## Workflow

**Scratch files are keyed by project id, never by client name** — two clients sharing a prefix (`acme` vs `acme-corp`) would collide. All `/tmp` files below use `<project_id>` in the filename.

### 1. Resolve the client

**Preferred: run the prep script in one pass.** `ruby ~/Work/scripts/client-report-prep.rb "<client name>"` resolves the project by name, reads both context docs (master `Project Context` at the Internal root when it exists — company facts fall back to the SEO doc when not — and `SEO — Project Context` in Internal → SEO for search facts), and returns JSON with everything steps 1–4 need: `master_context` (whether the master doc was used), `domain`, `fathom_site_id`, `fathom_goals`, `gsc_property`, `scoreboard_metrics` + `scoreboard` (each token classified as `fathom_goal` / `fathom_metric` / `gsc_metric` — unknown tokens surface here, at prep time), `plan`, `brand_terms`, **computed windows** (`report_window`, `prev_window`, `ly_window` — start/end dates plus labels; **use these dates everywhere, never do your own month math**), and `ly_available` (whether same-month-last-year is fillable — computed from the Fathom site's created date), plus `rank_tracker` (newest `Run —` + `Tracker config`) and `market_read`. Exit 1 with a message on failure — read the stderr and act on it.

**Fallback (script missing or errors):** match the client to a project by name via `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a domain or project.** Then resolve the folder ids (never guess a folder): find the master `Project Context` at the root of Internal, and `SEO — Project Context` in Internal → SEO. Read the master doc first for the `Domain:` line, `Fathom site id:`, and `Fathom goals:`; where a master line is absent (or the doc doesn't exist), read the same values from the SEO doc; read the SEO doc for `Property:` (GSC) and `Scoreboard metrics:`.

Missing context docs → step 1's rule applies (master `project-setup` first if the master doc is gone, `seo-project-setup` if the search doc is gone) and stop. **Refuse to run if `Domain:` is still the unfilled placeholder** (`https://example.com`) — setup hasn't been filled in, so there's no real site to report on.

### 1c. Read the Rank Tracker / market read (Rankings — Growth only)

When step 1 used the prep script, this data is already in the JSON (`rank_tracker.newest_run` + `rank_tracker.tracker_config`, `market_read`). Fallback only when the script didn't run: find `SEO — Rank Tracker` and read the **newest** `## Run —` section plus `## Tracker config` — keyword positions, movers, device, saved-set date. Find `SEO — Competitive Landscape` and read `## Market read` for context on who's winning.

**Consume, never re-pull.** These are the Rank Tracker's and Competitive Landscape's own measurements — do not re-run SERP checks or re-fetch keyword data here. The Rankings section is a standing part of the report **when the client is on Growth** (`Plan: Growth`): if the docs don't exist, write the one-line note (tracking hasn't produced keyword positions or a market read yet) — never fail the run. When the client is Foundation-only, the section sits out whole — no standing "rankings aren't set up" line.

### 1d. Work-record candidates ("What I did")

The report's **What I did** list is tasks, not findings — proof of what the retainer bought this month. Assemble the candidate list from:
1. The diff's resolved items (step 2's JSON) — fixes that published.
2. Published items — content or work the Rank Tracker/strategy notes mark as published since the last report.
3. The client project's Basecamp todo completions in the report window: `basecamp -a 6191443 todos list --status completed --in <project_id> --json`, then keep items whose `completed_at` falls in the window. If the CLI can't produce completions, skip this source and let Matt fill — never scrape.

**Git commits and dev logs are internal — never auto-sourced.** Commit messages and dev-log prose may reference things the client shouldn't see. The list goes to Matt as a *candidate list* in-session, and he curates what the client sees at the review gate — the curation note never prints inside the draft body. Running the monthly scan is never a bullet — Site health is its proof. If the pipeline yields nothing, say so and let Matt add — never invent watch tasks ("ran a scan") without an artifact.

### 2. Run tribunal: audit, then diff

Same mechanics as the teardown skill — Docker image, history volume mount (without the mount, `--rm` silently deletes the run tribunal just saved):

```bash
# Rebuild when the image is older than the newest tribunal commit — the build-if-missing
# guard never catches a stale image, and a stale image silently drops engines (verified:
# crux was missing for a month this way).
IMAGE_CREATED=$(docker image inspect tribunal --format '{{.Created}}' 2>/dev/null)
SOURCE_UPDATED=$(git -C ~/Work/personal/tribunal log -1 --format=%cI)
if [ -z "$IMAGE_CREATED" ] || [[ "$SOURCE_UPDATED" > "$IMAGE_CREATED" ]]; then
  (cd ~/Work/personal/tribunal && docker build -t tribunal .)
fi
mkdir -p ~/.local/share/tribunal/history
docker run --rm -e GOOGLE_CrUX_API_KEY="$(op read 'op://Secrets/GOOGLE_CrUX_API_KEY/password')" \
  -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal audit <domain> --format json > /tmp/client-report-<project_id>-run.json
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal diff <domain> --format json > /tmp/client-report-<project_id>-diff.json
```

The audit run carries `-e GOOGLE_CrUX_API_KEY` (resolved from 1Password, headless-safe via the service account) — the CrUX engine needs it for real-user CWV. The diff run doesn't need it: no engines run against saved history.

Pass the context doc's `Domain:` value to both, verbatim.

- `diff` errors with "need two saved runs … found 1" → **month one**. Switch to baseline mode (step 5) — that's normal, not a failure.
- Stay passive — never `--authorized`. Foundation and Growth clients consented to monitoring, not intrusive scanning; if Matt ever wants an active scan, that's a separate, explicit conversation outside this skill.
- Engines coming back `unavailable`/`failed` are fine; work with the `merge_groups` that exist.

**The report window is the calendar month the report covers** — default: the last full calendar month (run on Sep 1 → the report covers Aug 1–31). Fathom, GSC, and the scoreboard all use it; the prior period is the previous calendar month, whatever its length. **The scan window stays run-to-run** (previous run's `finished_at` → now) — that is the only valid diff, and the report header states both windows. First-ever report: the last full calendar month when the history reaches back, else the last 30 days.

### 3. Fetch Fathom (skip if the context doc has no Fathom site id — absent or `not in use`)

Token is resolved from 1Password. Two calls per group — `<FROM>/<TO>` are the prep script's `report_window` dates, `<PREV_FROM>/<PREV_TO>` its `prev_window` dates. Save every response to a scratch file (the charts step reads them):

```bash
TOKEN=$(op read 'op://Secrets/Fathom API Token/password')
# totals: visits, uniques, pageviews (both windows)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits,uniques,pageviews&date_from=<FROM>&date_to=<TO>" \
  > /tmp/client-report-<project_id>-fathom-totals-now.json
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits,uniques,pageviews&date_from=<PREV_FROM>&date_to=<PREV_TO>" \
  > /tmp/client-report-<project_id>-fathom-totals-prev.json
# top pages (report window) — report content AND the traffic weight used to
# order findings in step 5
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=pageviews&field_grouping=pathname&sort_by=pageviews:desc&limit=10&date_from=<FROM>&date_to=<TO>" \
  > /tmp/client-report-<project_id>-fathom-pages.json
# daily traffic trend (report window) — feeds the trend-line chart
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits,pageviews&date_grouping=day&date_from=<FROM>&date_to=<TO>" \
  > /tmp/client-report-<project_id>-fathom-trend.json
# top referrer sources (both windows) — traffic-move guard evidence
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits&field_grouping=referrer_source&sort_by=visits:desc&limit=5&date_from=<FROM>&date_to=<TO>" \
  > /tmp/client-report-<project_id>-fathom-referrers-now.json
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits&field_grouping=referrer_source&sort_by=visits:desc&limit=5&date_from=<PREV_FROM>&date_to=<PREV_TO>" \
  > /tmp/client-report-<project_id>-fathom-referrers-prev.json
# referrer hostnames (both windows) — AI surfaces (chatgpt.com, perplexity.ai) and notable referrals surface here
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits&field_grouping=referrer_hostname&sort_by=visits:desc&limit=5&date_from=<FROM>&date_to=<TO>" \
  > /tmp/client-report-<project_id>-fathom-hostnames-now.json
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits&field_grouping=referrer_hostname&sort_by=visits:desc&limit=5&date_from=<PREV_FROM>&date_to=<PREV_TO>" \
  > /tmp/client-report-<project_id>-fathom-hostnames-prev.json
```

**Goal completions (skip if the context doc has no `Fathom goals:` — absent, empty, or `not in use`).** Goals are event names on the client's Fathom site; each one is queried by its event name via `entity_name` (the old `entity_id` goal-code form is retired). Query per goal for both windows, and save:

```bash
# per goal, both windows: the report calendar month and the previous calendar month
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=event&site_id=<SITE_ID>&entity_name=<GOAL_NAME>&aggregates=conversions&date_from=<FROM>&date_to=<TO>"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=event&site_id=<SITE_ID>&entity_name=<GOAL_NAME>&aggregates=conversions&date_from=<PREV_FROM>&date_to=<PREV_TO>"
```

Collect the goal results (goal name → conversions for both windows) into `/tmp/client-report-<project_id>-fathom-goals.json` as an array of `{name, conversions_now, conversions_prev}`.

- `entity_name` is the goal's event name from the context doc's `Fathom goals:` line — URL-encode spaces.
- **Timezone edge:** Fathom reports in the *site's* configured timezone, so a site whose TZ differs from yours has month edges shifted by a day. The prep script computes windows in local time — for a mismatched-TZ site, verify the first/last day totals look sane before trusting deltas.
- **LY window:** when the prep script's `ly_available` is `true`, repeat the **totals and goals** fetches for `ly_window` dates (the scoreboard's LY column needs totals + goal conversions; pages/trend/referrers are not needed for LY). When `false` or `nil`, the LY column does not render at all — same principle as a section with no data: a column of dashes is table-level N/A, not a metric. Never guess at history.
- **LY in Search Console:** when `ly_available` is `true`, run `gsc-fetch.rb` a second time with `--start <ly_start> --end <ly_end>` (no prev args) and read its `totals` for the LY column's Google-clicks row.
- **Fathom API capabilities (verified 2026-09-06 against usefathom.com/api/llms.txt + live):** groupings include `pathname`, `entry_page`, `exit_page`, `referrer_hostname`, `referrer_pathname`, `referrer_source`, the `utm_*` family, `browser`, `device_type`, `country_code`; aggregates include `visits`, `uniques`, `pageviews`, `avg_duration`, `bounce_rate` (events: `conversions`, `unique_conversions`, `value` — in cents). Guessing field names 400s ("not a supported field") — check llms.txt, don't probe blind. UTM attribution is per-session: a conversion later in the same session attributes to the entry link's UTM (usefathom.com/docs/how-tos/measure-a-campaign). The report deliberately uses only `pathname` (top pages), the daily trend, and `referrer_source` (traffic-move guard); `avg_duration`/`bounce_rate` stay out — noisy at this traffic, not actionable, and the deterministic watch canaries (form test, silence alert) already cover "site feels broken."
- A goal name from the context doc that doesn't match a site event → **flag it to Matt in the draft**, never invent a number. It usually means the `Fathom goals:` line drifted from what `fathom-analytics` actually wired — fix the context doc line, don't guess the event.

### 4. Fetch GSC (skip if the context doc has no `Property:` — absent, empty, or a placeholder)

```bash
cd ~/Work/scripts/gsc-fetch
GSC_SERVICE_ACCOUNT_JSON="$(op read 'op://Secrets/GSC Service Account JSON/notesPlain')" \
ruby gsc-fetch.rb \
  --property "<GSC_PROPERTY from context doc>" \
  --start <FROM> --end <TO> --prev-start <PREV_FROM> --prev-end <PREV_TO> \
  --inspect "<url1>,<url2>,..." \
  > /tmp/client-report-<project_id>-gsc.json
```

Returns search analytics (clicks/impressions/position, current vs previous window, top queries, top pages) plus per-URL index inspection results. Note: a `sc-domain:` property includes **all subdomains** — top_pages can surface subdomain sites (e.g. a product/tool subdomain) picking up search traffic the main site doesn't see. That's report-worthy signal, not noise. For `--inspect`, take the Fathom top-10 pages mapped to full URLs, **minus error paths** (any pathname containing "404") — inspection is per-URL and quota-limited, so top pages are the ones worth checking.

**API honesty:** GSC's API has no site-wide index-coverage report and no CWV data. Never present the inspected sample as a full index check. (CWV field data comes from tribunal's `crux` engine — the key resolves from 1Password (`op://Secrets/GOOGLE_CrUX_API_KEY`) and reaches the engine via `-e` on the audit run; low-traffic sites return no field data, which is normal, not a failure.)

If the script fails (auth, property not shared with the service account yet), the GSC section sits out with a one-line note — same as a missing config field.

### 4a. Generate charts

The **pingplot** CLI (`~/Work/personal/pingplot/src/cli.js`) turns the fetched data into charts via Observable Plot. Write chart data files to `/tmp` (keyed by `<project_id>`), run pingplot, then embed via the attach-and-position recipe below (step 4a's chart embedding — verified live).

Invocation (pingplot is a global npm package — `pingplot` is on PATH):
```bash
pingplot --data <data-file> --mark <mark> --x <field> --y <field> [--color-range "hex,..."]
pingplot --data <data-file> --spec <spec-file>
```

**Output lands next to the data file** (same base name, `.png`). Data files are JSON (`.json` = JSON) or CSV (anything else). Colors come from `--color-range` (an ordered list mapped to the color scale's range) or a spec's `color.range`.

**The chart allowlist — a valid report can ship with one chart.**

1. **Traffic trend** — **required** when the Fathom trend data exists (missing = failed step); daily visits + pageviews across the report window (the "Traffic and search" headline). pingplot's `--mark line` takes one `y`, so a two-series line needs a spec file:
   - Data: from `fathom-trend.json` (the `date_grouping=day` response — array of `{date, visits, pageviews}`); map `timestamp` → `date` if needed. **Fathom returns every number as a string and trend rows out of date order — coerce numerics (`int(...)`) and sort by date, then **reshape: two rows per day** — one row for the visit count, one for the pageview count — as three columns: `date`, `value`, `series` (the series column reads `Visits` or `Pageviews`; the chart needs one value column to draw and one series column to color by). Skipping any of this produces client-facing garbage: string values render as an alphabetized categorical axis (`1, 10, 11, 2, 23…`), unsorted rows connect day-to-random-day into spaghetti. Output file: `/tmp/client-report-<id>-trend.json`
   - Spec `/tmp/client-report-<id>-trend-spec.json` (the `y` domain pins a 0 baseline with headroom above the month's peak; `stroke` is a **field name**, which hands the series to Observable Plot's default color scheme — two separate line marks with literal strokes would render both lines the same color):
     ```json
     { "marks": [
       { "type": "line", "x": "date", "y": "value", "stroke": "series" }
     ], "x": { "type": "utc", "grid": true }, "y": { "domain": [0, 40], "grid": true } }
     ```
   - The color scale orders series alphabetically: Pageviews draws gold (`#efb118`), Visits blue (`#4269d0`) — map those exact words in the caption/filename.
   - Run: `pingplot --data /tmp/client-report-<id>-trend.json --spec /tmp/client-report-<id>-trend-spec.json`. **pingplot's "strings that appear to be numbers" warning is a failure signal, not noise** — it means the data file wasn't coerced; stop and fix the data file, never ship past it.
   - **Vision-verify before embed** (charts are client-facing visuals; structural checks can't see): read the PNG through the vision subagent and confirm — numeric linear axis with a 0 baseline, two continuous series (no spaghetti), nothing outside the labeled scale, white background. Only then embed.

2. **Everything else is a table by default.** Top queries, top pages, and goal completions are short lists, not shapes — a two-bar chart of 5 forms and 1 call makes a win look thin. Escalate one to a chart only when it has **3+ meaningful data points and the shape is the story** (e.g. a rank-movers bar when 4+ tracked terms actually moved — horizontal `barX` with `marginLeft: 160` so long labels aren't truncated). Never chart fewer than three meaningful points. A missing optional chart is a skip, never a failed step. A **second** chart has to earn its slot — e.g. a rank that actually moved across months — never decoration (five form-bars is a thinner win, not a story).

**Rename before embed — the claim-title filename IS the caption.** Basecamp renders the attachment's **filename** as the visible caption under the chart, so the renamed file replaces any caption paragraph. After pingplot runs, rename each PNG to its claim-title ("Daily visits (blue) and pageviews (gold), August 1–31 (Fathom).png") and reference that path — and never also write a separate caption paragraph below the embed; the double caption is a defect.

```bash
mv /tmp/client-report-<id>-trend.png "/tmp/Traffic — daily visits and pageviews, Aug 1-31.png"
```

**Chart embedding — verified live (dry run 2, Sep 2026).** Local paths do NOT upload, and upload-URL embeds (`download_url`) render broken in the doc. The working sequence:

1. Create the report doc with the chart attached: `basecamp -a 6191443 files doc create "<title>" "<body — pure markdown, no image references>" --attach "/tmp/<claim-title>.png" --in <project_id> --vault <internal_reports_id> --json`. `--attach` is repeatable for multiple charts; the attachment lands at the END of the content.
2. Re-read the doc and take the SGID from `content_attachments[N].sgid`.
3. Update the doc with the body as **fully rendered HTML** (`<h2>`, `<p>`, `<table>`, `<ul>`), placing `<bc-attachment sgid="<SGID>" content-type="image/png"></bc-attachment>` inline where the chart belongs.
4. Assert on the re-read: one `<bc-attachment>` per chart, inline in position; tables as real `<table>` elements; no raw `|` rows left — **and the plan's contract-mandated tables are all present**: scoreboard and conversions (when conversion data exists) on every plan; top pages and top queries on Growth; appendix when a tracker run exists. A draft that carries a table's numbers only as prose is incomplete, not a style choice — on Foundation, prose carries the traffic distribution qualitatively instead.

**The wall-of-text check — after drafting, count sentences per section against the caps.** Over the cap → cut, do not wrap with `<br>` (that is typesetting, not editing). No character caps — they invite empty padding.

| Section | Cap |
| --- | --- |
| What happened | 3–5 sentences (locked) |
| What I did | one line per task, at most 4 lines |
| Site health | 1 short paragraph, at most 3 sentences, at most 2 named findings |
| Traffic and search | at most 4 short paragraphs — the move, conversions, search/brand, the search surface — 1–3 sentences each |
| Rankings | 1 paragraph for movers, 1 market sentence |
| What's next | 1–3 lines |

One idea per paragraph. If a paragraph has two ideas, split it. A paragraph that needs a scroll on a phone is two paragraphs.

**The rendering rule behind step 3:** `files doc create` and `files update` render pure markdown server-side, but the moment content carries any HTML (the `<bc-attachment>` tag), the whole write goes through as-is — mixed markdown + HTML stores raw. So the chart update is an all-HTML write: render the markdown to HTML yourself (h2/p/table/ul, `dir="auto"`, right-aligned cells via `align="right"`), and **separate every block with `<br>` the way Basecamp stores them** (`</p><br><h2>…`) — block boundaries without the `<br>` render as cramped, un-Basecamp spacing. The chart embed is a block on **both sides**: `</h2><br><bc-attachment …></bc-attachment><br><p>`. **Table captions are `<figcaption>` inside the table's figure wrapper** (`<figure class="lexxy-content__table-wrapper" dir="auto"><table>…</table><figcaption><em>…</em></figcaption></figure>`) — they survive saves, render below the table, and the `<em>` makes them italic (inline `style` attributes are stripped; `<em>` survives). A caveat about a table's data belongs here too — not stapled onto the story prose. Never send `<caption>`: Basecamp's schema strips it and dumps the text as an invalid node inside `<table>`.

**Re-embedding a chart into an existing doc (verified 2026-09-07).** When a chart must be re-rendered after the doc exists (regenerated data, or the tool changed after an earlier embed), `files update` can't attach and `files replace` can't reach content attachments. The working sequence: regenerate the PNG (pingplot's default background is white since v1.1.0 — pass nothing), rename it to the claim-title, then `basecamp -a 6191443 attach "<claim-title>.png" --json` (account-scoped, no project) → take `attachable_sgid` → swap it into the body's existing `<bc-attachment sgid="...">` → `files update`. Verify by re-reading: the doc's `content_attachments` should list the new dimensions/bytes, and the old transparent/stale PNG should drop off the list. **A tool update never re-renders a PNG already embedded in a doc** — regeneration plus re-embed is always explicit.

Confirm the trend PNG exists before drafting when Fathom data exists.

### 5. Draft the report

The bar, every draft: plain language, every line tied to a consequence, ordered by what matters, warm even when the news is bad — warm, not chipper, not clinical.

**The voice.**

Say what happened. Use the words the client already has.

If they cannot tell a partner what the paragraph said, rewrite it. No mission language. No spec-sheet costume.

The stance:

- Short sentences. Common words plus the real nouns (visits, form, rank, deploy, index).
- I / you. Never we, never the team.
- What it means for their business, then the number.
- Quiet months are said out loud.
- Zero asks. Zero upsell. Zero notes-to-self in the body.

The mechanics:

- Plain words: site, page, visits, clicks, forms, calls, rank. Never users, sessions, vertical, funnel, leverage, impactful — and never "conversions" as an abstraction; use the event's name.

The words:

| Write | Do not write |
| --- | --- |
| visits, pageviews, forms, call clicks | users, sessions, goal completions, "traffic" (when you mean visits), "leads" (unless the review qualified them) |
| published, put live | shipped, rolled out, dropped |
| the finding, load time, headers | issue soup, "we ran a health check" |
| tracking, the keyword set, positions as of 2 Sep | program, on the board, visibility journey |
| unknown — I'll watch next month | held steady (next to a 20%+ move), softness, mixed commercially |
| Watch / On track | blocked, at risk, needs love |
| Rankings | the SEO program, how you show up |
- The consequence comes before the metric: "People searching for warehouse robotics can now find that page," not "rank improved 4 positions."
- One idea per sentence. A clause that explains the explanation gets split.
- Em dashes are a tap on the shoulder, not a habit: at most one per sentence, and only when the second half is a turn ("Five forms came in — all direct"). A list pretending to be a sentence is three sentences. If a period or comma does the job, use it. Never stack dashes in one paragraph, and the scoreboard caption gets none. Date ranges use an en dash (August 1–31).
- **I / you / neither.** Matt works solo — "we" reads as a team that doesn't exist. "I" for work Matt did ("I stood up the 13-keyword set"), "you" for their site and their customers. Default is neither: most sentences need no pronoun at all ("Visits were down 36%. Five forms and one call came in direct."). Use "I" only when the point is that the retainer bought Matt's time. Never "the team," and never "Safaii Studio" as an actor.
- Every number carries its window and source in the prose — or the scoreboard caption carries source + window once and the prose stays clean. Never a bare "traffic was down."
- **Tables say exactly; prose says what it means.** If a number is already in a table on the page, the prose never retypes it — no photocopying rows. The one exception is an aggregation the table doesn't show ("six leads" from 5 forms + 1 call), spoken once, in What happened or the conversions prose — never both, never itemized in prose.
- Never narrate the template: no "in the scoreboard below you'll see…" — they can see it.
- No internal asides. The draft body is client-voice only: candidate-list notes, curation asks, and source notes (todo dates, reconstructed splits) go to Matt in-session — never printed inside the draft, not even as an italic aside.
- Never "program." Say tracking, the keyword set, the scan — "program" is consultant furniture.
- No phrase bank, no emoji arrows, no sentence that could appear in a tool export or an agency newsletter. The test: if you'd say it across the table pointing at the scoreboard, keep it — and if the owner couldn't repeat the paragraph to a partner without translating you, rewrite it. Quiet months are said out loud: a flat month is stated plainly, never dressed.

**The frozen body — same skeleton every client, every month.** Headings are unnumbered, in this order, never renamed. A section with no data sits out whole (delete the heading — never print "N/A"), with one conditional exception: **`## Rankings` is standing when the client is on Growth** (`Plan: Growth`) — the heading stays even when tracking is quiet; its body just becomes one line. On a Foundation-only client the heading deletes like any other out-of-scope section — a monthly "rankings aren't set up yet" is noise. The body **never repeats the doc title**: `files doc create` already renders "Site report — <Month Year>", so the body starts at the metadata lines:

```markdown
Prepared: Safaii Studio · Period: <Month 1–last day, Year> · Site: <domain>
Compared with: <previous calendar month> · Scan window: <run-to-run dates>
Status: On track | Watch — <subject>

## What happened
<3–5 sentences, written last>

## Scoreboard
| Metric | <Mon YYYY> | <Prior Mon> | Change |
| --- | ---: | ---: | ---: |

<caption: source + window — add a `<Same month LY>` column between `<Prior Mon>` and `Change` only when the prep script's `ly_available` is true>

## What I did
- <I + verb + object — one line on why it existed. "Ran the monthly scan" is not a What I did>

## Site health
<tribunal diff narrative>

## Traffic and search
<Fathom + GSC narrative, trend chart, conversions table, search prose>

## Rankings
<movers and near-wins + market line; one line when quiet>

## What's next
<one sentence, optional>

## Appendix — full keyword rankings
<optional>
```

Per-block contract:

- **What happened** — the verdict: 3–5 sentences, written last: what moved + why it matters to this business. Never an ask. Ends on the month's own weight — don't pre-echo What's next. The heading is reader-timeless: never a calendar-relative name (This/Last month) — the title carries the month, the heading never points at the reader's desk.
- **Scoreboard** — the locked rows from `Scoreboard metrics:` (or the default: visits, total named-goal conversions, Google clicks). Tokens on the line must be fetchable — `visits`, `pageviews`, `uniques`, an exact Fathom goal name, `Google clicks`, `Google impressions`; an unknown token goes to Matt as a question, never guessed into a row. The LY column (`<Same month LY>`) renders only when the prep script's `ly_available` is `true` (computed from the Fathom site's created date; ~13 months of comparable data) — a site younger than that has no column, not a column of dashes. It appears exactly once in a client's lifetime, at month 13, and stays from then on. When `Fathom goals:` is `not in use`, the conversions row drops — a row that prints zeros forever is noise, not a metric. **Average position never goes on the scoreboard** — it moves the wrong way when page-two impressions grow; it lives in the search prose with its explanation. Impressions only when visibility is the story. Conversions use the client's names, never "goal completions."
- **What I did** — tasks, not findings: what the retainer bought this month. Candidate list from step 1d (diff resolutions + SEO published + Basecamp todo completions), curated by Matt at the review gate.
- **Site health** — the diff, folded into plain narrative. Field CWV (the `crux` engine's SLOW findings) folds in here — "LCP for real users improved from slow to good on your homepage." **Guard rails:**
  - Check `coverage_changes` before calling anything fixed — a category that lost engine coverage went *unchecked*, not fixed. Never report it as progress.
  - Order findings by traffic weight: an issue on a top-10 Fathom page leads; an issue on a page nobody visits gets a line or gets folded.
  - Name carry-over items with why they matter and stop. Scheduling and deferral are internal — the report never assigns homework ("give it a date", "should be formally deferred").
- **Traffic and search** — Fathom + GSC. The **trend chart opens** this section. Conversions as a table ("5 contact forms, 1 call click, vs 0 and 0 last month") — this is the proof-of-value lead for most clients, so lead with it and cross-light with traffic ("visits dipped, and form completions followed anyway"). **Events measure activity, not qualification — never upgrade a conversion count to "leads" on your own.** A form submission becomes a lead only when Matt reads it and says so (at the review gate; he sees every submission). Until then the prose reports events plus the review outcome: "Five forms and a call click arrived; on review, the forms were sales pitches rather than customer leads." When the review qualifies them, the sum may be spoken once in plain words ("two real leads arrived") — the table carries the event breakdown; when the events aren't clearly lead-type (CTA clicks, applications), no total. Top pages and top queries tables ship on **Growth**; on Foundation the traffic prose carries the distribution qualitatively (no numbers — the scoreboard carries the counts). The Fathom pull can surface `/404.html` in the pages table; keep the row and name the dead-end views when present. The query table lists queries that **carried at least one click**; the zero-click tail is one prose line ("visibility without pull"), never rows of zeros. **Brand vs non-brand:** the query pull is the full list (`top_queries` holds every query Google reports — the fetch script caps at 25,000 rows), and the queries table shows the clicks-carried rows, top ten by clicks. Classify every row against the prep script's `brand_terms` (a query is brand when it contains any brand term, case-insensitive); brand clicks = sum of brand rows, non-brand = sum of non-brand rows — **never total minus brand**: queries Google withholds (privacy thresholds) are unattributed, and site-total minus attributed clicks is exactly that, never called non-brand demand. When brand share is ≥50% of clicks, lead the search prose with the brand observation — brand proving the site works is a different story from acquiring demand. Name the withheld bucket plainly when present ("Google doesn't report the searches behind the other 23 clicks (privacy thresholds)"). With no `Brand terms:` line, skip the split. **GSC average position** is explained by its mechanism ("the new impressions are mostly page-two appearances, not lost rankings") — the raw number is optional, never a headline figure, and never printed next to tracker ranks. The tracker's "rank 12" is the live SERP pass; the two systems never blend. **Traffic-move guard:** any scoreboard metric moving beyond ~20% gets one sentence of cause (seasonality, tracking change, lost referrer) or "unknown — I'll watch next month" — never "held steady" beside a −36%. The referrer pulls supply the cause check — **decompose any moved source bucket before writing a cause sentence**: a `Paid/campaign` move means UTM-tagged visits (tracking parameters, not necessarily spend — and never automatically ads), so pull `utm_source`/`utm_medium` for that window and read the tag values (`ig` = an Instagram link, `chatgpt.com` = an AI citation, an outreach/campaign tag = sales email); untagged tool shares (Salesforce, outreach.io) surface only in the hostname view and otherwise sit in Direct. Cite the source-level deltas only when traffic moves ("no source shifted; the drop is diffuse", "Direct held and Organic fell") — silent on quiet months. **Anyone can tag a link to the client's site** (usefathom.com/docs/troubleshooting/utm): UTM values are claims by the link's sender, not proof of ownership — attribute a tagged visit to the client only when its tuple matches the `Owned tagged traffic:` line in the context doc; everything else is neutral ("visits from a tagged link — source not yet identified") until Matt confirms it, then write the confirmed pattern into that line. The hostname view has its own, independent rule: an AI surface (chatgpt.com, perplexity.ai) or a notable new referral gets one line the month it appears — even on a flat month ("4 visits from ChatGPT — the first AI-surface click") — else silent. **AI visits can also arrive UTM-tagged**: ChatGPT tags its citation links `utm_source=chatgpt.com`, which Fathom files under `Paid/campaign` — so a non-zero campaign bucket with no ad spend may be hiding AI citations; a `utm_source=chatgpt.com` value counts as an AI-surface appearance under the same rule. Cross-light with the scan where the story connects ("the two pages I fixed last month are indexed and picking up clicks").
- **Rankings** — standing on Growth (`Plan: Growth`); deleted on a Foundation-only client. Consumed from the Rank Tracker (never re-pulled): movers and near-wins in the body; a first-month table is a **baseline, not a report card** — "tracking set established; two terms already ranking; the rest is the market you're entering." The market line in prose covers who holds the positions ("reddit and Cisco hold most of these") — never a Current #1 column (thirteen hostnames is a competitor dump). The full keyword rankings go in the Appendix (which ships whenever a Rank Tracker run exists — no separate decision). **The appendix grid is frozen at four columns: Keyword · Rank · Page · Change** — no Notes, no Current #1; Page shows the path, not the full URL; Change is an em dash on month one and fills versus the **previous tracker run** from month two (one cycle of dashes keeps the grid comparable; a year-long gap omits the column, the LY rule). Tracker notes never render — they're internal. The caption states it once: positions as of the run date, location, device; Change is versus the previous run, never versus GSC. **Date every borrowed number** — say "positions as of 12 Aug" from the newest run header, never "this month's rankings." Newest run dated more than 35 days before the report run → one line: tracking didn't run this cycle. Market-read line from Competitive Landscape when present ("the services angle is open — nobody selling it the way you do"). Cross-light with published work ("the page I targeted last quarter is climbing"). Tracking quiet → one line, never padded.
- **Zero asks.** The report never mentions asks, approvals, or anything waiting on the client: not a "Needs from you" block, not a status reference, nothing. It also never pitches — no upsell for a Foundation client, no "imagine if you did SEO" framing; an upsell is an ask, and Growth is never pitched inside the monthly. Prospects get the teardown skill; a real upsell goes out as its own note. Approvals go out as their own standalone message when the content is ready; the handoff email may carry one (step 7a). The monthly only reports what is already published.
- **Status** — `On track` or `Watch`, decided by rule, not feel: **Watch iff** (a) any scoreboard metric moved ≥20% (absolute) without a cause sentence — the draft then carries "unknown — I'll watch next month", or (b) the diff has a new finding at high or critical severity. Otherwise On track. There is no "Blocked" — that would be an ask — and no third status: no ladder, no "At risk"/"Concerned"; the binary is the trust, the prose carries the temperature. **A Watch names its subject in three words or fewer** ("Watch — traffic", "Watch — site health") — never a sentence, which would retell What happened; On track stays bare.
- **What's next** — 1–3 priorities for the coming month. I + verb + object. No dates, no counts, no padding. A quiet month can be one line. Work that needs their yes does not belong here; that is the handoff's one ask. This is direction, not a deliverable list. If next month's numbers kill a priority, the following report says so.
- **Sections sit out gracefully:** no Fathom → say the report covers the technical watch and search, one line, move on. Never apologize at length for missing data. No Rank Tracker on a Growth client → the Rankings section is the one-line note (see step 1c); Foundation-only → the heading is deleted, not a standing apology.
- **Month one (baseline mode):** no diff talk at all. Where things start: current health by category, the handful of findings worth fixing early, the scoreboard with whatever history exists, what I did, and what next month's report will start tracking.
- Keep it tight. A prospect teardown persuades; this report **reassures and proves**. If the month was quiet, say so plainly — "a quiet month is the product working."

### 6. Review gate — nothing posts without approval

Show Matt the full draft. Revise in place until he approves. **Ambiguous response ≠ approval.** If he walks away, the draft just waits.

### 7. Create the report doc (Internal > Reports)

On explicit approval, create the report as a **document** in the client's **Internal > Reports** folder (team-only — born hidden, never client-visible at this point):

```bash
basecamp -a 6191443 files doc create "Site report — <Month Year>" "<report body as Markdown>" --in <basecamp_project_id> --vault <internal_reports_id> --json
```

**Content as an argument, never `-` stdin.** Verify content length after create. The chart rides in via `--attach` at create and is positioned inline by the step-4a update; assert one inline `<bc-attachment>` per chart on the re-read.

Resolve the `Internal > Reports` folder id exactly as `seo-project-setup` resolves Internal > SEO (walk Internal, find/create Reports under it). Create the Reports folder if missing.

### 7a. Create the handoff-message draft doc (Internal > Reports)

Create the email-body-style handoff **as its own draft doc** in the same Internal > Reports folder — so Matt reviews and edits the message copy alongside the report, not just inline text:

```bash
basecamp -a 6191443 files doc create "Handoff — <Month Year>" "<handoff text, with placeholder for the report doc link>" --in <basecamp_project_id> --vault <internal_reports_id> --json
```

The handoff draft is the *email body*: the report is the attachment. Short, warm, one paragraph — what you'd write in an email, ending with "the full report is here: <link>". It carries a placeholder link until the report is moved (the final URL isn't known until then). This doc stays in Internal — it's the record of what was sent, never client-visible itself. The handoff email is the **only** place an ask may appear in the monthly flow: if something is genuinely pending on the client (e.g. staged content awaiting approval), one short line here. The report doc itself never mentions it.

### 7b. Matt moves it — the ship gate

Return both doc URLs and tell Matt: **move the report doc from Internal > Reports to Deliverables > Reports** — that move is what flips it client-visible (verified: a doc moved into a client-visible folder reports `visible_to_clients: True`). This is his action, not the skill's. The report stays team-only until he moves it. He can edit the handoff draft doc at this point too.

### 7c. Post the handoff message

After Matt confirms he moved the report doc, post the **handoff draft doc's content** to the client's Message Board — with the real link to the moved report doc swapped into the placeholder:

```bash
basecamp -a 6191443 message "Site report — <Month Year>" "<handoff text from the draft doc, with the real link>" --in <basecamp_project_id> --jq '.data.app_url'
```

If the project has multiple message boards, the CLI errors with "Multiple message boards found" and lists them — add `--message-board <id>` for the main Message Board.

Return the message URL, and remind Matt to tag it with the **📊 Report** message category — the CLI can't set categories on post, so it's a manual step in Basecamp for now.

### 8. Report back

One line to Matt: the report doc URL, the handoff draft doc URL, the message URL, and where the durable artifacts live (`~/.local/share/tribunal/history/<slug>/` — this month's run is next month's baseline). `/tmp` files are scratch; the history is the record. Never delete history.

**Close the loop in the Project Context doc:** the per-cycle record lives in the master `Project Context` doc. Find it at the Internal root (exact title, the master doc built by `project-setup`): append one dated row to its `## Log` table — delivered date + channel (email / Basecamp) + items pending client approval (staged work, transfer asks). Same write loop as every context-doc edit: fresh fetch, splice the row above `</tbody>`, publish with `--content "$(cat file)"`, verify prior rows survived. The log is the project's history — every cycle records itself, never a manual afterthought.

**If the master `Project Context` doc does not exist for this client yet** (built against `SEO — Project Context` before `project-setup` shipped), fall back to the old home: append the same row to `SEO — Project Context` → `## Research log` (Internal → SEO vault). When the master doc is later created, note to Matt that the cycle history moves with the repoint migration.

### 8b. Editing an existing report (post-publish edits)

The mechanic: `files update --content` replaces the **whole body every time** — Basecamp has no partial edit. Drift enters two ways: **regeneration** (an agent rewrites untouched sections, so phrasing drifts) and **stale writes** (publishing a copy fetched before an outside change). The pattern that prevents both:

1. **Canonical file first.** The report's canonical body lives in a stable path outside `/tmp` — `~/Work/client-reports/<project-slug>/report-<YYYY-MM>.html` — written at publish and kept for the cycle. Every edit patches *that file*, then publishes it. Never publish "a fresh fetch plus a small change" unless the fetch is first verified equal to canonical.
2. **Patch, never regenerate.** An edit is a targeted string replacement inside the current content. Untouched sections must come out byte-identical — after any edit, diff the published body against canonical: only the intended lines may differ.
3. **Fresh fetch before every write.** If the live doc differs from canonical (outside edits landed), stop and show Matt the diff — never write over unknown changes.
4. **Verify on re-read — twice.** Content probes (key sentences, table counts, chart count) after every publish; a failed probe stops the run — never "fix it up" by regenerating. Then audit with Basecamp's own diff: every update lands as a version at `/documents/<doc-id>/changes/<version-id>` with an inline green/red diff — open it and confirm **only the intended lines show green/red**. A diff that touches more than the edit intended is a dirty write: stop, restore from canonical, republish.
5. **One doc id per report.** Updates go to the same document; a new doc is only for a new month — same-titled duplicates drift. Version history is native (full log at `/recordings/<doc-id>/events`, reached via the doc's "View change log") — never create duplicate docs to get history, and never assume the log distinguishes authors (CLI writes attribute to the token owner). **After an edit, hand Matt the version's diff URL** — one click shows exactly what changed.
6. **The human side:** ask Matt to close the doc's browser tab before publishing — a stale editor buffer autosaves over newer server content (observed three times in one week).

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Report posted to the wrong project | Trusted a guessed project instead of matching by name | `basecamp_project_id` comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account on publish | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Report doc landed client-visible | Created with `--visible-to-clients` or in Deliverables | Reports are born in Internal > Reports (team-only); the move to Deliverables is Matt's ship gate |
| Report doc empty | Used the `-` stdin form | Pass content as an argument; verify content length after create |
| Message sent before the move | Posted the handoff to a doc still in Internal | The handoff message posts only after Matt confirms the doc is in Deliverables |
| Handoff posted from scratch | Skipped the handoff draft doc | The message uses the drafted handoff doc's content — create it in step 7a, review, then post |
| Client A's numbers appear in client B's report | Reused /tmp scratch files across runs | Scratch files are per-client-per-run keyed by project id; re-fetch, never reuse |
| "Fixed" claim for something never re-checked | Skipped the diff's `coverage_changes` guard | Cross-check every resolved finding against `coverage_changes` before drafting it |
| Diff errors "found 0" for a client reported on before | Prior run made without the `-v` history mount, or the context doc's `Domain:` form changed | Check `ls ~/.local/share/tribunal/history/`; keep the `Domain:` line stable in the context doc |
| Report reads like a scan dump | Drafted from `merge_groups`/API JSON without translating | Re-read the voice rules in step 5; every line needs a consequence, not a metric |
| Index status claims overreach | Presented the inspected top-pages sample as full coverage | GSC API only inspects individual URLs — say "your key pages," never "every page" |
| GSC section silently missing when creds exist | Service account not yet added to that client's property | Add the service-account email as a user on the property in Search Console, once |
| `gsc-fetch.rb` fails with a token/auth error | 1Password session unavailable or service account not on the property | `op signin` once, or verify the service-account email is a user on the GSC property; show the raw error |
| Prep script exits 1 (no project match) | Client named differently than the project | Read the candidate list on stderr, confirm the exact project name with Matt, re-run with it |
| Prep script exits 1 (missing context doc) | No master `Project Context` and no `SEO — Project Context`, or master exists but the SEO doc doesn't | Master missing → `project-setup`; search doc missing → `seo-project-setup`; stop |
| Prep script fails with a CLI error | `basecamp` not installed or account wrong | Show the raw stderr and stop; fall back to the manual steps in step 1/1c |
| Goal numbers look wrong | Prior window wasn't the previous calendar month, or used the site id as `entity_id` for an event | Current = the report's calendar month, prior = the previous calendar month; events use `entity=event&site_id=<SITE_ID>&entity_name=<GOAL>` — the event name, never a goal code (retired) |
| Goal fetch 400s | Still passing `entity_id` for an event | The goal-code form is retired; use `site_id` + `entity_name` (URL-encode the event name) |
| Trend chart missing while Fathom data exists | Pingplot isn't on PATH, or the data file/spec path is wrong | Run `pingplot` and confirm the data file and spec fields match; a missing required chart is a failed step — optional charts may skip |
| Chart renders but labels are truncated | A barX horizontal chart without a wide left margin | Set `marginLeft` (~160 for long query/page labels) in the barX spec |
| Chart renders but looks wrong (all one bar / no labels) | Mismatched `x`/`y` field names vs the source JSON | Check the actual field names in the scratch JSON (e.g. `timestamp` vs `date`, `pathname` vs `page`) and set the spec to match |
| Chart renders but is garbage (alphabetized axis or spaghetti) | Charted Fathom's raw response — numbers-as-strings and/or unsorted rows | Coerce numerics and sort by date before writing the chart data file; treat pingplot's string warning as a failure; vision-verify the PNG before embedding (step 4a) |
| Numbers appear only as prose; the receipts tables are missing | The inverse of a scan dump — the draft narrates conversions without their table (any plan) or pages/queries without theirs (Growth) | Conversions ships on every plan; top pages and top queries on Growth; assert the plan's contract tables on the re-read (step 4a) |
| Prose retypes table rows | The paragraph above a table photocopies it | Tables say exactly, prose says what it means — no retyped rows; a sum the table doesn't show may be spoken once |
| Raw events reported as leads | Conversion counts upgraded to "leads" without qualification | Events measure activity; leads are qualified by Matt's review — report events plus the review outcome, and never count spam as demand |
| Two captions under one chart | Renamed the PNG but kept a caption paragraph too | The claim-title filename IS the caption — one or the other, never both |
| GSC position next to a tracker rank (Appendix notes) | Consumed tracker notes verbatim, blending the two systems | Strip GSC cross-references from tracker notes when rendering the Appendix; GSC lives in Traffic and search |
| Appendix grows extra columns (Current #1, Notes) | Competitor dump and internal notes leaking into the client doc | The appendix is frozen at Keyword · Rank · Page · Change; AI Overview and market context stay a Rankings-prose line the month it matters |
| Withheld queries counted as non-brand demand ("the other 23 clicks are non-brand") | Computed the split as total minus brand over a top-10 export | Non-brand = clicks on classified non-brand rows only; queries Google withholds are unattributed — name them as withheld, never as demand (the full-query pull makes the split exact) |
| What's next grew into a punch list (padded to three, or carried approval-gated work) | Direction written as deliverables the client grades | Only yes-free work, I + verb + object; a quiet month is one line, never a filler third item — an approval-gated item goes out as the handoff's one ask |
| Bare "Watch" in the header | Status routed nothing — the reader didn't know where to look | A Watch names its subject in ≤3 words ("Watch — traffic"); never a context sentence, which retells What happened |
| Untouched sections drifted after an edit | The agent regenerated the document instead of patching it | Patch the current content in place — one section, string replacement, write back; diff against canonical to prove nothing else moved (step 8b) |
| Older content reappeared after an edit | The write came from a stale fetch or a stale editor buffer | Re-fetch before every publish; Matt closes the doc tab; restore from the canonical file and republish (step 8b) |
| Whole doc body replaced with empty content | Published `--content "$(cat missing-file)"` — `cat` failed silently, the empty string was the argument, and `files update` published it (happened 8 Sep 2026, Handoff doc) | `test -s <file> &&` before every publish; on an empty publish, restore from the pre-write fetch, republish, re-verify section probes |
| Whole doc body replaced by the literal string `@filename` | Passed `--content @file` — the CLI has no file-reference shorthand, it published the argument as text and wiped the body | Always pass `--content "$(cat file)"`; on a wipe, restore from the pre-write fetch or canonical, republish, and re-verify section probes |
| Chart missing or broken in the doc | Embedded a `/tmp` path or an upload `download_url` — neither renders | Attach at create with `--attach`, take the SGID from `content_attachments`, place the `<bc-attachment>` element inline via the all-HTML update (step 4a) |
| Tables stored as raw markdown after a chart update | Mixed markdown + `<bc-attachment>` HTML in one write — rendering is skipped when any HTML is present | Send the whole body as rendered HTML (step 4a's rendering rule) |
| An engine missing from the audit output entirely (e.g. crux absent while other engines show) | Docker image predates the engine's source — build-if-missing never rebuilds a stale image | Compare the image's created date to the tribunal repo's last commit; rebuild, then re-run (step 2) |
| CrUX/field CWV never appears even with the key passed | Engine errored silently or the origin has no field data | Check the audit run's stderr; no field data on a low-traffic origin is normal, not a failure |
| Goal name from the context doc matches nothing | The `Fathom goals:` line drifted from what `fathom-analytics` wired | Flag it to Matt in the draft — fix the context doc line, never invent the number or guess the event |
| Re-pulled keyword positions | Ran SERP checks instead of reading the Rank Tracker | Positions come from the newest `## Run —` section; this skill consumes, never re-fetches |
| Read a stale rank snapshot | Grabbed an older `## Run —` instead of the newest | The newest run (top of the doc) is the current one; the config block says which set it covers |
| Draft posted without approval | Treated silence/ambiguity as a yes | Only an explicit yes publishes; anything else waits |
| Approval ask buried in the monthly report | Folded a content/approval ask into the report | Approvals go out as standalone messages; the monthly report only reports what is already published |
| Fathom deltas look wrong | Prior window wasn't the previous calendar month | Current = the report's calendar month; prior = the previous calendar month |
| Chart captions show a working filename | PNG embedded under its scratch name | Rename each PNG to its claim-title before doc create — Basecamp renders the attachment's filename as the visible caption |
| Title appears twice in the report | Body repeated the doc title | The body starts at the Prepared metadata line — `files doc create` already renders "Site report — <Month Year>" |
| Average position on the scoreboard | Copied the GSC position into the locked rows | Avg position never on the scoreboard; it lives in the search prose with its explanation |
| "Not in top 100" rows in the SEO body | Dumped the full tracked set into the section | Body = movers and near-wins; the full set lives in the Appendix |
| Report mentions an ask or approval | Folded a pending ask into the report | Zero asks in the report — standalone message when content is ready, or one line in the handoff email |
| "Held steady" beside a −36% | Skipped the traffic-move guard | Any scoreboard metric moving beyond ~20% gets a cause sentence or "unknown — watching next month" |
| "Paid-campaign traffic" prose implying ad spend | Read Fathom's `Paid/campaign` bucket as ads | That bucket = UTM-tagged visits, not spend — decompose with `utm_source`/`utm_medium` pulls; the tag values name the real source (an `ig` tag is an Instagram link, a `chatgpt.com` tag is an AI citation). Third parties tag links too (usefathom.com/docs/troubleshooting/utm) — match against the `Owned tagged traffic:` line before attributing anything to the client |
| Foundation client gets a monthly "rankings aren't set up" line | Treated Rankings as standing for every client | Delete the heading unless `Plan: Growth` — the standing rule applies only to Growth |
| Upsell framing in a Foundation client's report | Turned the report into a Growth pitch | Zero asks includes zero upsells — Growth is never pitched inside the monthly; prospects get the teardown skill, real upsells ship as their own note |
| Review-gate asides inside the draft ("curate at review") | Internal notes written into the client document | Asides go to Matt in-session; the body is client-voice only |
| Site health ends on homework ("give it a date") | Internal scheduling written as a client ask | Name the finding and stop; deferral decisions stay internal |
| "Program" in draft prose | Consultant vocabulary leaked into the report | Say tracking / the keyword set |
| Costume vocabulary (shipped, rolled out, at risk, needs love, visibility journey, how you show up, mixed commercially) | Dev-speak and consultant furniture standing in for real words | Use the client's words — published, put live, Watch/On track, tracking, the keyword set; if the owner can't repeat the paragraph without translating you, rewrite it |
