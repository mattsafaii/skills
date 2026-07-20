---
name: client-report
description: Generate the monthly maintenance report for a Safaii Studio client — runs Matt's tribunal audit CLI against the client's site, diffs against last month's run, pulls Fathom Analytics and Google Search Console data for the same window, and drafts a ready-to-send month-over-month report ("what we watched, what changed, what it did") for Matt's review before posting it to that client's Basecamp project. Use whenever Matt says "client report for [client]", "/client-report [client]", "monthly report for [client]", "run the monthly audit for [client]", or it's report time for a maintenance-plan client. Clients only — prospects get the teardown skill; ad-hoc audits get audit-website. Nothing ever posts without Matt's explicit approval.
---

# Client Report Skill

Turns tribunal's run history + Fathom + Google Search Console into the monthly proof-of-value report for maintenance-plan clients. The scan diff says what changed; analytics and search data say what it did. One report, in Matt's client voice, reviewed by Matt before anything reaches a client.

## Fixed context

- Basecamp account: `6191443` (Safaii Studio). Each client's report posts to **that client's own Basecamp project** (from the registry) — never anywhere else.
- tribunal lives at `~/Code/personal/tribunal`; it runs via its Docker image (see step 2).
- Tone reference: Basecamp doc `10032725076` ("Marathon Power Website Review (to send)") — read it before drafting, every time.
- This skill bundles a GSC helper: `scripts/gsc-fetch.mjs` (service-account auth via `google-auth-library`). If `node_modules` is missing here, run `pnpm install` in this skill's directory once.

## The client registry

`~/.config/client-report/clients.json` — local only, never in any repo. Shape:

```json
{
  "fathom_token_file": "~/.config/client-report/fathom-token",
  "gsc_key_file": "~/.config/client-report/gsc-service-account.json",
  "clients": {
    "acme": {
      "name": "Acme Co",
      "url": "https://acme.com",
      "fathom_site_id": "ABCDE",
      "gsc_property": "sc-domain:acme.com",
      "basecamp_account_id": 6191443,
      "basecamp_project_id": 12345678,
      "notes": ""
    }
  }
}
```

- **`url` must be the same form every month** — tribunal slugs the target URL to find its history folder; a changed URL form orphans the history.
- A missing/empty `fathom_site_id` or `gsc_property` means that section **sits out** of the report with a one-line note. It never fails the run.
- `basecamp_account_id` says which Basecamp account the client's project lives in — `6191443` (Safaii Studio) for client work, `6060605` (Zonebrite) for Zonebrite's own site. If the field is absent, default to `6191443`.
- Not every entry is a paying client — Zonebrite is Matt's own company, reported on with the same machinery. Use `notes` to flag an internal site; the report for those is for Matt (and Mike), so the reassure-the-client framing can relax into a plain internal health report.
- One Fathom API token and one GSC service account are shared across clients. GSC setup per client: add the service account's email as a (restricted) user on the client's Search Console property once.
- If the registry file doesn't exist, help Matt create it from the shape above — then continue.

## Workflow

### 1. Resolve the client

Matt names a client. Look it up by key or `name` in the registry. Unknown → list the registered clients and stop. **Never guess a domain.**

### 2. Run tribunal: audit, then diff

Same mechanics as the teardown skill — Docker image, history volume mount (without the mount, `--rm` silently deletes the run tribunal just saved):

```bash
docker image inspect tribunal >/dev/null 2>&1 || (cd ~/Code/personal/tribunal && docker build -t tribunal .)
mkdir -p ~/.local/share/tribunal/history
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal audit <url> --format json > /tmp/client-report-<client>-run.json
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal diff <url> --format json > /tmp/client-report-<client>-diff.json
```

Pass the registry `url` to both, verbatim.

- `diff` errors with "need two saved runs … found 1" → **month one**. Switch to baseline mode (step 5) — that's normal, not a failure.
- Stay passive — never `--authorized`. Maintenance clients consented to monitoring, not intrusive scanning; if Matt ever wants an active scan, that's a separate, explicit conversation outside this skill.
- Engines coming back `unavailable`/`failed` are fine; work with the `merge_groups` that exist.

**The reporting window** = the previous run's `finished_at` (from the diff's baseline) → now. Month one: last 30 days.

### 3. Fetch Fathom (skip if no `fathom_site_id`)

Token is the contents of `fathom_token_file`. Two calls — current window and the equivalent preceding window (same length, immediately before) for deltas:

```bash
TOKEN=$(cat ~/.config/client-report/fathom-token)
# totals: visits, uniques, pageviews
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=visits,uniques,pageviews&date_from=<FROM>&date_to=<TO>"
# top pages
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=<SITE_ID>&aggregates=pageviews&field_grouping=pathname&sort_by=pageviews:desc&limit=10&date_from=<FROM>&date_to=<TO>"
```

The top-pages list does double duty: report content AND the traffic weight used to order findings in step 5.

### 4. Fetch GSC (skip if no `gsc_property`)

```bash
cd ~/.claude/skills/client-report
node scripts/gsc-fetch.mjs \
  --key <gsc_key_file> --property "<GSC_PROPERTY>" \
  --start <FROM> --end <TO> --prev-start <PREV_FROM> --prev-end <PREV_TO> \
  --inspect "<url1>,<url2>,..." \
  > /tmp/client-report-<client>-gsc.json
```

Returns search analytics (clicks/impressions/position, current vs previous window, top queries, top pages) plus per-URL index inspection results. Note: a `sc-domain:` property includes **all subdomains** — top_pages can surface subdomain sites (e.g. a product/tool subdomain) picking up search traffic the main site doesn't see. That's report-worthy signal, not noise. For `--inspect`, pass the client's top pages from Fathom (up to ~10) mapped to full URLs — inspection is per-URL and quota-limited, so top pages are the ones worth checking.

**API honesty:** GSC's API has no site-wide index-coverage report and no CWV data (CWV is CrUX — a future tribunal engine, not this skill). Never present the inspected sample as "we checked every page's index status."

If the script fails (auth, property not shared with the service account yet), the GSC section sits out with a one-line note — same as a missing config field.

### 5. Draft the report

Read the tone reference doc first (`basecamp -a 6191443 docs show 10032725076 -p 46876803 --md`). The Marathon Power bar applies: plain language, every line tied to a consequence, ordered by what matters, warm even when the news is bad.

Structure — *what we watched, what changed, what it did*:

- **Open** with the one-paragraph month in review: overall health, the single most important thing (good or bad).
- **What changed** from the diff: new / resolved / regressed / improved, folded into plain narrative. **Guard rails:**
  - Check `coverage_changes` before calling anything fixed — a category that lost engine coverage went *unchecked*, not fixed. Never report it as progress.
  - Order findings by traffic weight: an issue on a top-10 Fathom page leads; an issue on a page nobody visits gets a line or gets folded.
- **What it did** from Fathom + GSC: visits/pageviews vs the prior window, search clicks/impressions trends, top queries, index status of the pages that matter. Cross-light with the scan where the story connects ("the two pages we fixed last month are indexed and picking up clicks").
- **Sections sit out silently gracefully:** no Fathom → say the report covers the technical watch only, one line, move on. Never apologize at length for missing data.
- **Month one (baseline mode):** no diff talk at all. Structure becomes *where we're starting, what we'll watch*: current health by category, the handful of findings worth fixing early, and what next month's report will start tracking.
- Keep it tight. A prospect teardown persuades; this report **reassures and proves**. If the month was quiet, say so plainly — "a quiet month is the product working."

### 6. Review gate — nothing posts without approval

Show Matt the full draft. Revise in place until he approves. **Ambiguous response ≠ approval.** If he walks away, the draft just waits.

### 7. Publish

On explicit approval, post to the client's own Basecamp project, in the account the registry names:

```bash
basecamp -a <basecamp_account_id> message "Monthly site report — <Month Year>" "<report body as Markdown>" --in <basecamp_project_id> --jq '.data.app_url'
```

If the project has multiple message boards, the CLI errors with "Multiple message boards found" and lists them — add `--message-board <id>` for the main Message Board (not Meeting Notes or other secondary boards), and save the id to the client's registry entry as `basecamp_message_board_id` so future runs pass it directly.

Return the message URL, and remind Matt to tag it with the **📊 Report** message category — the CLI can't set categories on post, so it's a manual step in Basecamp for now. (Existing projects may not have the category yet — it was added account-wide for *new* projects; Matt adds it per existing project as needed.)

### 8. Report back

One line to Matt: the message URL, and where the durable artifacts live (`~/.local/share/tribunal/history/<slug>/` — this month's run is next month's baseline). `/tmp` files are scratch; the history is the record. Never delete history.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Report posted to the wrong project | Trusted a guessed project instead of the registry | `basecamp_project_id` comes from the registry entry, nowhere else |
| 404 / wrong account on publish | Used the default account for an entry that lives elsewhere (e.g. Zonebrite = `6060605`) | Always pass the entry's `basecamp_account_id` to `-a`; default `6191443` only when the field is absent |
| Client A's numbers appear in client B's report | Reused /tmp scratch files across runs | Scratch files are per-client-per-run; re-fetch, never reuse |
| "Fixed" claim for something never re-checked | Skipped the diff's `coverage_changes` guard | Cross-check every resolved finding against `coverage_changes` before drafting it |
| Diff errors "found 0" for a client reported on before | Prior run made without the `-v` history mount, or the registry `url` form changed | Check `ls ~/.local/share/tribunal/history/`; keep the registry URL form stable |
| Report reads like a scan dump | Drafted from `merge_groups`/API JSON without translating | Re-read the Marathon Power doc; every line needs a consequence, not a metric |
| Index status claims overreach | Presented the inspected top-pages sample as full coverage | GSC API only inspects individual URLs — say "your key pages," never "every page" |
| GSC section silently missing when creds exist | Service account not yet added to that client's property | Add the service-account email as a user on the property in Search Console, once |
| `gsc-fetch.mjs` fails with missing module | `pnpm install` never run in this skill's dir | `cd ~/.claude/skills/client-report && pnpm install` |
| Draft posted without approval | Treated silence/ambiguity as a yes | Only an explicit yes publishes; anything else waits |
| Fathom deltas look wrong | Compared windows of different lengths | Previous window must be the same number of days, immediately preceding |
