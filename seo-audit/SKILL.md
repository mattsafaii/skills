---
name: seo-audit
description: Audit a website and deliver a one-page, plain-language SEO report anyone can act on, centered on a single do-this-week action. Runs Matt's tribunal audit CLI against the domain, verifies findings against the live site, derives the one thing from the data, and drafts the report for Matt's review before it's posted to that client's Basecamp project. Use when Matt says "audit [domain] for a client", "/seo-audit [domain]", "one-page SEO report for [domain]", or wants a fresh-domain audit for a client not yet on a maintenance plan. Not a teardown (that's for sales prospects), not a maintenance report (that's client-report), not a raw findings dump (that's audit-website). Nothing posts without Matt's explicit approval.
---

# SEO Audit Skill

Audits a domain and produces a one-page, plain-language report centered on a single do-this-week action. The whole report exists to support ONE action the owner can take this week; everything else is supporting detail. Engine is **tribunal**; the report is a Basecamp markdown message to the client's project, reviewed by Matt before anything reaches a client.

## Rules that don't bend

Load the **dataforseo** skill for the catalog and hard rules. The essentials:

1. **The one thing drives everything.** The report's only job is to make one action obvious and doable this week. Derive it from the data, never from generic advice. If the report doesn't have a one thing, it's not done. **Every number carries a date** — "around 40 searches a month (as of <date>)" — never a bare figure; **market is US by default**, different only if the context doc says so.
2. **Verify before you claim.** Report nothing you have not seen evidence for. Cross-check every finding against the live page HTML yourself (`webfetch` the page) — a tool's output is a lead, not proof. Separate what the tools reported from what you verified, and say both in the method footer.
3. **Plain language, no drama.** No exclamation points, no drama words, no filler. Gloss every term of art in plain English on first use (canonical, meta description, crawler, 301, structured data). Severity words only where literally true — a down site is critical; a long title is not. **The tone doc is the single voice authority** — when a mechanical rule here conflicts with how the tone doc writes, the tone doc wins.
4. **Skip nitpicks that don't matter.** A beginner report with twenty findings has failed. Five to ten fixes max, ordered by impact. Missing backlink or ranking data means "no recorded data," not a penalty.
5. **Stay passive.** Tribunal runs passive engines by default. Never `--authorized` on a site you don't own or aren't authorized to test.
6. **Spend is modest and capped.** One audit (tribunal, no cost), one `backlinks_summary`, at most one `dataforseo_labs_google_domain_rank_overview`, and at most one `dataforseo_labs_google_keyword_overview` (for the focus-area keywords). Only the DataForSEO calls spend — keep total to that. (Backlink summary ≈ $0.02; domain overview ≈ $0.02; keyword overview ≈ $0.09.)
7. **Nothing posts without Matt's approval.** The report is drafted, reviewed, revised, then posted only on explicit yes. Ambiguous response ≠ approval.
8. **Reuse within 30 days.** Same domain audited within 30 days → reuse that result and say so instead of re-running. **Matt can override** — an explicit "run it anyway" re-runs despite the recent audit; say "re-running per your override" and go.

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- **The report is an artifact, not a message body.** The flow: create the audit doc in the client's **Internal > Reports** folder (team-only, born hidden), Matt reviews and manually moves it to **Deliverables > Reports** (client-visible — the move flips visibility), then a short message posts to the client's Message Board with a link to the moved doc.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- **Which project?** If the audited domain is an existing client, match it to their project and create the report there. If it's a prospect or unknown, ask Matt which project it belongs to — never guess. (Prospects normally get a `teardown`; if Matt says audit a prospect instead, this skill still runs and the report doc goes wherever Matt directs.)
- The domain to audit is the one Matt names — if it's a client, confirm it matches the context doc's `Domain:` line.
- tribunal lives at `~/Work/personal/tribunal`; it runs via its Docker image (see step 2) or the local binary.
- Tone reference for client-facing prose: Basecamp doc `10032725076` ("Marathon Power Website Review (to send)") — read it before drafting, every time.
- **Basecamp 5 renders markdown** — the report doc is markdown, not HTML. GFM tables render.

## Workflow

### 1. Resolve the domain and project

Matt names a domain. Resolve the client and project by name via `basecamp -a 6191443 projects list --json` — if it's an existing client, confirm the domain matches their context doc's `Domain:` line. If it's a prospect or unknown, ask Matt which project (or none) this report belongs to. **Never guess a project or domain.**

Read `SEO — Project Context` if it exists — what the business does decides which findings matter and what the one thing should be. Missing context doc → still audit (this is a fresh-domain audit; the domain itself is the subject), but note what you're inferring about the business.

### 2. Run tribunal: audit

Same mechanics as teardown/client-report — Docker image, history volume mount (so a later `client-report` diff can use this run as its baseline):

```bash
docker image inspect tribunal >/dev/null 2>&1 || (cd ~/Work/personal/tribunal && docker build -t tribunal .)
mkdir -p ~/.local/share/tribunal/history
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal audit <domain> --format json > /tmp/seo-audit-<domain>-run.json
```

Pass the domain verbatim. Passive engines only — never `--authorized`.

- Engines coming back `unavailable`/`failed` are fine; work with the findings that exist. Record what wasn't covered in the method footer.
- **Dead domain handling:** if the audit comes back broken or nearly empty (certificate errors, 5xx, one page crawled), investigate before writing — check the certificate and redirect variants yourself, and search the web for the business. A dead domain often has a live successor site, which flips the whole recommendation to "redirect the old domain."

### 2b. Pull the supporting data (capped)

Three DataForSEO calls max, in this order:
- **`backlinks_summary`** for the domain — the backlink/referring-domain picture is usually the deciding data for the one thing (clean site + no backlinks → outreach; strong links → focus elsewhere). Skip when the site is clearly dead.
- **`dataforseo_labs_google_domain_rank_overview`** — estimated organic traffic and keyword count. Skip when the site is clearly dead.
- **`dataforseo_labs_google_keyword_overview`** — only for the focus-area keywords in step 5 (to check they're actually winnable). One batched call.

That's the whole budget. If a call fails or returns nothing, it goes in the method footer as "no recorded data" — never a penalty, never a second attempt to re-buy it.

### 3. Verify the findings you'll report

For every finding you plan to include, `webfetch` the live page and confirm the evidence (the quoted tag, the missing meta, the broken link, the redirect). Report nothing you have not seen evidence for. Findings that don't survive verification are dropped silently.

### 4. Decide the one thing

Derive it from the data, never from generic advice. **When the context doc exists, its `current_goal` and money pages constrain the choice** — "start writing blog posts" loses to "the goal is quote requests, so fix the contact page's indexability" when that's what the data shows. Common patterns:
- **Clean site, no backlinks:** outreach to guests, partners, or directories, with a ready-to-send message.
- **Dead domain, live successor site:** permanent redirect via hosting support, with the exact sentence to send them.
- **Blocked or noindexed pages:** remove the block.
- **Healthy site:** a starting focus area (see step 5).

It must be doable this week by a non-technical person, with copy-paste-ready mechanics included.

### 5. Propose a starting focus area (healthy sites only)

**If `SEO — Keyword Research` already has a dated saved set, defer to it** — point at that set or skip "where to focus first." Never invent a parallel 3–5 keyword list when the research exists. The focus area is a fresh-domain-only feature.

For a fresh domain: propose one topic area and 3–5 specific, low-difficulty keywords the site can realistically rank for, each with the page or post to make. **Seeds come only from the site's visible on-page headings / `webfetch` language** — not from `keyword_ideas` (that's the consumer-junk path KR banned). Then one `dataforseo_labs_google_keyword_overview` call (volume/difficulty) to verify they're winnable. Drop any term that's off-positioning. Label the section a **starting direction**, and **don't write these terms into `SEO — Keyword Research`** — this isn't research, it's a pointer. **Skip this entirely when the site is down** — the one thing is all that matters there.

### 6. Draft the report

Read the tone reference doc first (`basecamp -a 6191443 docs show 10032725076 -p 46876803 --md`). The Marathon Power bar applies: plain language, every line tied to a consequence, ordered by what matters, warm even when the news is bad.

The report structure (markdown message, mirroring the OpenSEO template's section order):

- **Header** — the domain as the title, the review date on its own line under it, then a 2–3 sentence summary of the whole report (overall state; the main gap and the one thing; what the report covers).
- **Where the site stands** — the verdict in one or two plain paragraphs: what's working, and the main gap the one thing addresses.
- **If you only do one thing** — the one sentence action, why it matters, then 2–3 concrete steps (copy-paste message included in italics, and a way to check it worked).
- **Small fixes, in order** — 5–10 max, ordered by impact. Each fix shows the exact evidence (a quoted tag or number in `code`) and concrete steps a non-technical person can follow, with a severity tag (`low` / `medium` / `high`) only where literally true.
- **Where to focus first** (healthy sites only) — one topic area and 3–5 keywords, each with its volume in plain words and dated ("around 40 searches a month, as of <date>") and the page or post to make. Omit when the site is down.
- **Already working** — what the site does well, each with why it matters in one clause.
- **Method footer** — the review date; what the tools reported vs. what you verified yourself; what wasn't covered; backlinks/domain data or "no recorded data."

### 7. Review before delivering

Run an adversarial pass on your own draft. Attack four things: claims beyond the verified facts, unglossed jargon, anything overwhelming for a beginner, and dramatic language. Fix what the pass surfaces.

### 8. Review gate — nothing posts without approval

Show Matt the full draft. Revise in place until he approves. **Ambiguous response ≠ approval.** If he walks away, the draft just waits.

### 9. Create the report doc (Internal > Reports)

On explicit approval, create the audit as a **document** in the client's **Internal > Reports** folder (team-only — born hidden, never client-visible at this point):

```bash
basecamp -a 6191443 files doc create "SEO review — <Domain>" "<report body as Markdown>" --in <basecamp_project_id> --vault <internal_reports_id> --json
```

**Content as an argument, never `-` stdin.** Verify content length after create.

Resolve the `Internal > Reports` folder id exactly as `seo-project-setup` resolves Internal > SEO (walk Internal, find/create Reports under it). Create the Reports folder if missing.

### 9a. Create the handoff-message draft doc (Internal > Reports)

Create the email-body-style handoff **as its own draft doc** in the same Internal > Reports folder — so Matt reviews and edits the message copy alongside the report:

```bash
basecamp -a 6191443 files doc create "SEO review — <Domain> — handoff message" "<handoff text, with placeholder for the report doc link>" --in <basecamp_project_id> --vault <internal_reports_id> --json
```

The handoff draft is the *email body*: the audit report is the attachment. Short, warm, one paragraph — ending with "the full review is here: <link>". It carries a placeholder link until the report is moved. This doc stays in Internal — the record of what was sent, never client-visible itself.

### 9b. Matt moves it — the ship gate

Return both doc URLs and tell Matt: **move the report doc from Internal > Reports to Deliverables > Reports** — that move flips it client-visible (verified: a doc moved into a client-visible folder reports `visible_to_clients: True`). His action, not the skill's. The audit stays team-only until he moves it. He can edit the handoff draft doc at this point too.

### 9c. Post the handoff message

After Matt confirms he moved the report doc, post the **handoff draft doc's content** to the client's Message Board — with the real link to the moved report doc swapped into the placeholder:

```bash
basecamp -a 6191443 message "SEO review — <Domain>" "<handoff text from the draft doc, with the real link>" --in <basecamp_project_id> --jq '.data.app_url'
```

If the project has multiple message boards, the CLI errors with "Multiple message boards found" and lists them — add `--message-board <id>` for the main Message Board.

Return the message URL, and remind Matt to tag it with the appropriate message category (the CLI can't set categories on post).

### 10. Report back

One line to Matt: the report doc URL, the handoff draft doc URL, the message URL, and the one thing the report centers on. The report is the record — the audit JSON in /tmp is scratch (but the tribunal history mount, if used, is next month's baseline).

## Output format

When Matt reviews the draft, summarize in-session:

- Domain + project
- The one thing (the do-this-week action)
- Fix count
- Where to focus first (healthy sites) or the redirect/outreach call
- Recommended next action: `keyword-research` (fresh healthy site — turn the starting direction into a real saved set), `client-report` (maintenance plan), `teardown` (if this was a prospect), or nothing (one-shot audit). Keep this list out of the client-facing body — it's a Matt-only next step.

## Guardrails

- The one thing drives the report; no one thing = not done.
- Verify before claim — report nothing without live-page evidence.
- Plain language, no drama, glossed terms.
- Skip nitpicks; 5–10 fixes max, ordered by impact.
- Passive only — never `--authorized` on a site you don't own.
- Nothing posts without explicit approval.
- Missing backlink/ranking data = "no recorded data," not a penalty.
- The audit is an **artifact** — a doc born in Internal > Reports, moved to Deliverables > Reports by Matt (the ship gate), with a short handoff message linking to it. Unlike the Internal > SEO research docs, this one is client-facing — but only after the move.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Report posted to the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Claimed a finding never verified | Reported a tool's output as fact | Cross-check against the live page HTML before drafting; drop what doesn't survive |
| The one thing is generic | Derived from advice instead of data | Re-derive from the audit + verified pages; a real finding always yields a real action |
| Twenty findings in the report | Included every nitpick | Cut to 5–10 by impact; a beginner report with twenty findings has failed |
| Jargon left unglossed | Skipped the plain-language pass | Gloss every term of art on first use |
| Ran an active scan | Used `--authorized` | Passive engines only; active scans are a separate, explicit conversation |
| Blew the data budget | Re-ran failed calls or added overviews | One backlinks + at most one domain overview + one keyword overview; a failed call is "no recorded data," never a re-buy |
| Backlink claim without evidence | Reported a summary number as fact | Verify the backlink read against the summary and the live context; drop what doesn't hold |
| Wrote focus keywords into `SEO — Keyword Research` | Treated the starting direction as research | The focus area is a pointer, never a saved set — research lives in keyword-research's own doc |
| Report doc landed client-visible | Created with `--visible-to-clients` or in Deliverables | Reports are born in Internal > Reports (team-only); the move to Deliverables is Matt's ship gate |
| Report doc empty | Used the `-` stdin form | Pass content as an argument; verify content length after create |
| Handoff message sent before the move | Posted a link to a doc still in Internal | The handoff posts only after Matt confirms the doc is in Deliverables |
| Handoff posted from scratch | Skipped the handoff draft doc | The message uses the drafted handoff doc's content — create it in step 9a, review, then post |
| Draft posted without approval | Treated silence/ambiguity as a yes | Only an explicit yes publishes; anything else waits |
| Re-ran an audit from last month | Skipped the reuse check | Same domain audited < 30 days ago → reuse and say so; only an explicit "run it anyway" re-runs |