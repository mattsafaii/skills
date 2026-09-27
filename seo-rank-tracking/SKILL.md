---
name: seo-rank-tracking
description: Track keyword positions for one client over time — reads the saved-keyword set from the client's SEO — Keyword Research doc, runs a fresh SERP check per keyword, and appends a dated section to the SEO — Rank Tracker doc in Working on new projects. Basecamp is the record. Pure measurement of an already-confirmed set — no confirmation gate, no judgment calls. Use when Matt says "run rank tracking for [client]", "rank check [client]", "update the rank tracker", "where are we ranking for [keyword]", "/seo-rank-tracking". The saved-keyword set is the contract this skill reads; the appended history is what client-report folds into monthly reports. Never recreate the doc under a new title.
---

# SEO Rank Tracking Skill

Runs a fresh position check on a client's saved keywords and appends it to their Rank Tracker doc. Each run is one dated snapshot; the doc accumulates them so change over time has a real record. This is the one mechanical skill in the chain — the set was already confirmed by `keyword-research`, the output is a factual snapshot, so it writes without a confirmation gate.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** Every position row carries the run's date: "as of 2026-09-01". **Market is US by default** (the DataForSEO `location_name`) — a different market only if the context doc or KR run header says so. A bare "rank 4" is never citable.
2. **Every call charges money.** One SERP check per saved keyword (≈ $0.002 each) — run the full set in one pass, never re-check a keyword twice in a session, and never run the set again "just to confirm".
3. **Failed call → Unknown, never a guess.** A failed SERP call goes in an "Unknown" line, never a fabricated rank.
4. **Append, don't overwrite.** The doc is history. New runs insert on top; they never touch earlier sections.
5. **No rank found is a finding.** "Not in top 100 for 'private lte'" is a real data point — record it, don't treat it as a failure.
6. **One run per day per client.** If the same set was already tracked today, say so and stop — don't re-spend to confirm a number that hasn't moved.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `SEO — Project Context` in Internal → SEO. For research docs, check exact titles in Working and legacy Internal → SEO; stop if both have the same title. Use the existing folder id for updates, or Working for first create (`research_folder_id`).
- The doc lives in **Working on new projects**, or its existing legacy Internal → SEO folder, team-only, titled **`SEO — Rank Tracker`** — a stable contract, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client

Matt names a client. Match it to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous or missing → show Matt the candidates and ask. **Never guess a project or domain.**

### 1b. Read the project context

Find `SEO — Project Context` and read it — the domain, target markets, competitors, positioning. If it's missing, tell Matt to run `seo-project-setup` first and stop.

### 2. Load the saved-keyword set

Find `SEO — Keyword Research` by exact title in Working or legacy Internal → SEO; stop if both exist. Read **only** the `## Saved keywords` table (the tracking contract — keyword, cluster) and the `## Research run` header. **Refuse to run if it's missing or undated:** if the doc is absent, `## Saved keywords` is missing or empty, or the `## Research run` header carries no `Date:`, tell Matt to run `keyword-research` first and stop — never invent keywords to track, and never track a set whose snapshot date isn't recorded.

**Location:** US by default. The SERP `location_name` matches the KR run header's `Location:` when that field is present (it's only set when non-US); otherwise US. If the context doc and KR disagree, stop and ask — don't silently pick one.

### 2b. Check for a same-day run

Find `SEO — Rank Tracker` and read the newest run's date, location, and device. If a run already exists for today **with the same location and device**, say so and stop — the numbers haven't moved since this morning. **Never re-spend to confirm.** A run with a different location or device doesn't block a new one Matt actually asked for (a morning AU-mobile run shouldn't stop an afternoon US run) — but flag it so he knows they're separate snapshots.

### 3. Run the position check

For each saved keyword, one SERP check (Google, `location_name` from step 2, `language_code: en`):

- **Depth 100 via the REST API, not the MCP tool.** Depth-100 `serp/google/organic/live/advanced` responses are ~2000 lines each — through the MCP tool they flood session context and blow up the run. Instead call the DataForSEO REST endpoint directly: `POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced` with body `[{"keyword": "...", "location_name": "...", "language_code": "en", "device": "mobile", "depth": 100}]` for a mobile run (use `"desktop"` for a desktop run), header `Authorization: Basic $DATAFORSEO_BASIC_AUTH`. The API defaults to **desktop** when `device` is omitted. Set `device` explicitly from the requested/tracker-config device on **every task**, including any helper script, and verify the response device before saving the run. Extract only the client's rank/URL, the current #1 domain, and organic-item count per keyword — not the raw payload. Token from the env var if set; only fall back to `op read` if the env is empty.
- Find the client's domain in the organic results.
- Record the **actual organic position through 100** — not just top 10. "Not in top 10" lumps position 11 with position 80, and the striking-distance terms KR cared about (positions 5–20) live right there. Use `not in top 100` when the client isn't found.
- **Ranking URL (client URL only):** the URL the client ranks with — that's what you act on (wrong page, cannibalization, money page never ranking). A competitor URL in this column is a bug — the `#1` column already covers them.
- **Rank = organic only** — an integer (`12`), `not in top 100`, or `unknown`. A local-pack placement goes in the **Notes** column (`pack: 2`), never in `Rank` — a pack slot isn't an organic position, and mixing a note into the Rank column breaks the Change math.
- Note the current `#1` domain for context (cheap, one field — tells you who you're chasing).
- **GSC average position is not a live rank** — never write it into `Rank`. (Optional as a notes field later, not v1.)

Batch the calls in one pass. Do not re-run.

### 4. Append to the Rank Tracker doc

Write `SEO — Rank Tracker` (markdown), following the **frozen heading contract** — the config block and run sections are exact, never renamed.

```markdown
## Tracker config
Domain:
Location: US
Device: mobile
Saved-set date:
Keyword count:
## Run — 2026-09-01
| Keyword | Rank | Ranking URL | Change | Current #1 | Notes |
## Run — 2026-08-01
| Keyword | Rank | Ranking URL | Change | Current #1 | Notes |
```

- **`## Tracker config`** — a stable header above the runs: Domain, Location, Device, Saved-set date, Keyword count. **Replace this block each run**; leave every `## Run —` section alone. Without it, after a few runs nobody remembers the device or which saved set the history is against.
- **Newest run first**, inserted above the previous one.
- **Device: mobile by default** (unless Matt says otherwise) — desktop+mobile doubles spend and splits the history. The choice lives in Tracker config and must match the request and response. If the device cannot be verified, write `unknown`, not `mobile`.
- **Change column** compares to the previous run's row where one exists; "—" on the first run or for keywords not in the prior run.
- **Saved-set fingerprint:** if the saved table changed since the last run (KR replaced it), log "set changed (N added / N removed)" — so a sea of `—` isn't read as a ranking collapse.
- Runs insert; they never replace earlier content.

**The write loop (every write, every time):**

1. Find the doc by exact title in Working and legacy Internal → SEO — stop on duplicates; never create a second copy.
2. Read the full markdown into memory.
3. Update `## Tracker config`; **insert** the new run section above the previous one — leave every existing run untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <research_folder_id>`).
5. Re-read and assert the prior runs still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in both Working and legacy Internal → SEO. Create in Working: `basecamp -a 6191443 files doc create "SEO — Rank Tracker" "<markdown>" --in <project_id> --vault <research_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <research_folder_id> --json`.

**`files doc create` takes the body as an argument, or as `-` to read stdin (CLI v0.10.0+)** — prefer `-` for large or multiline markdown to avoid shell quoting and argument-length limits. Verify content length after any write.

### 5. Report back

One line to Matt: the doc URL, how many keywords tracked, how many moved, how many are still unranked, the market and device used. The history in the doc is the record — `/tmp` scratch is not.

## Output format

When the run finishes, report back in-session:

- Doc URL
- Keywords tracked / moved / still unranked
- Biggest movers (if any worth calling out)
- Spend note — "N SERP checks" or "skipped — ran today"
- Recommended next action: `seo-strategy` (content from the gaps), `competitive-landscape` (if the #1 domains keep winning), or nothing (next run is the cadence)

**client-report contract:** the monthly report reads the **newest** `## Run —` section and the `## Tracker config` block — never an older snapshot.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tracked the wrong keywords | Read the wrong doc, guessed the set, or ran on an undated set | The set comes from SEO — Keyword Research's `## Saved keywords` table, nowhere else; refuse if the set or its `Date:` header is missing |
| Wrote ranks for keywords not in the saved table | Invented or reused rows | Ranks are written only for the saved set; a new keyword first needs `keyword-research` |
| Ran twice the same day | Skipped the same-day check | One run per day per client **per location+device**; the newest run's date, location, and device decide |
| Doc in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Bare ranks in the doc | Forgot the measurement rule | Every rank carries a date in the run header; undated ranks are never written |
| Rank shows only top-10 | Cut the SERP at 10 | Record organic position through 100; `not in top 100` when absent |
| Pack slot in the Rank column | Blurred local pack with organic | Rank is organic only (`12` / `not in top 100` / `unknown`); a pack placement goes in Notes (`pack: 2`) |
| Competitor URL in Ranking URL | Grabbed the wrong row | Ranking URL is the client's URL only; the `#1` column covers competitors |
| Earlier runs wiped | Overwrote content instead of inserting | New runs insert above the previous; they never replace existing content |
| Change column wrong | Compared against a keyword not in the prior run | Compare row-to-row against the previous run only; "—" when absent |
| Re-checked a keyword | Second SERP call "to confirm" | One call per keyword per run; a failed call is recorded Unknown, never re-run |
| One client's history in another's doc | Reused scratch files across runs | Read and append against the client's own Rank Tracker doc, per client |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the ranks onto it |
