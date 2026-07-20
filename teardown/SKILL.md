---
name: teardown
description: Generate a full first-draft Teardown for a Safaii Studio sales prospect — reads the prospect's homepage (copy + screenshot) and runs Matt's tribunal website-audit CLI against it, drafts every section of the Full Teardown template (hero read, objection stack, copy, design/hierarchy, technical findings, prioritized fixes), and publishes it as a new "Teardown — [Brand]" doc in Basecamp (Sales project, Deals vault) for Matt to rewrite in his own voice before sending. Use this whenever Matt says "teardown [company/domain]", "full teardown for [prospect]", "/teardown", "run the teardown on X", or wants a first pass at a teardown ahead of a discovery call. This is the deep, written Tier-2 deliverable — NOT the 5-minute Loom light tier (that's a video Matt records himself, this skill doesn't touch it), and not a generic site audit for existing clients (use the audit-website skill for that).
---

# Teardown Skill

Drafts every section of Matt's Full Teardown template — a full first pass, not just the technical section. Sections 1–5, 7, 8 are design/copy judgment — the template calls this "a sample of judgment, not a 20-page audit" and warns "demonstrate the taste, don't claim it" — so those sections come back **flagged as an AI first pass** for Matt to rewrite in his own voice, never sent as-is. Section 6 ("Under the hood") is different: it's grounded in tribunal's actual scan data, so it's not flagged the same way, though Matt can still edit it.

This exists so Matt starts from a draft instead of a blank template on every qualified prospect.

Background, if you want it: "The Homepage Teardown — Offer" (Basecamp doc 9993402077) describes the whole two-tier system this fits into.

## Fixed IDs

Do not ask Matt for these — they are fixed for this skill:

- Account: `6191443` (Safaii Studio)
- Sales project: `46876803`
- Deals vault (root folder for per-prospect folders): `9792703029`
- Full Teardown template doc: `9994887966` ("Teardown — Full (Template)")
- Pipeline card table: `9782662056`

tribunal lives at `~/Code/personal/tribunal` (module `github.com/mattsafaii/tribunal`).

This skill has its own bundled dependency: `scripts/capture-homepage.mjs` (Playwright, headless — no visible browser tab). If `node_modules` isn't present in this skill's directory, run `pnpm install` here once; if `~/Library/Caches/ms-playwright` has no chromium build, run `pnpm exec playwright install chromium` once.

## Workflow

### 1. Collect the target

Need a **brand/prospect name** and a **URL**. Ask for whichever is missing — don't guess a URL from a company name.

### 2. Read the homepage

Sections 1–5 need an actual read of the page, not just tribunal's technical facts — the hero's four jobs, the objection stack, copy quality, and visual hierarchy are all judgment calls about what a visitor sees and feels.

```bash
cd ~/.claude/skills/teardown
mkdir -p ~/.local/share/teardown/<slug>
node scripts/capture-homepage.mjs <url> \
  ~/.local/share/teardown/<slug>/<timestamp>-desktop.png \
  ~/.local/share/teardown/<slug>/<timestamp>-mobile.png \
  > ~/.local/share/teardown/<slug>/<timestamp>-page.json
```

`<slug>` is the brand name, lowercased and hyphenated (matches tribunal's own target-slug convention); `<timestamp>` is UTC, e.g. `20260702T140205Z`. This mirrors where tribunal saves its own run history (`~/.local/share/tribunal/history/`) so nothing from a teardown run lives only in `/tmp` — these are the only durable copies of the screenshots, since tribunal itself has no idea they exist.

This headlessly renders the page (so JS-only content shows up, unlike a plain fetch) and produces three things: a full-page desktop screenshot, a full-page mobile screenshot, and a JSON file with the rendered title, meta description, and visible text. Read the JSON for copy — headline, subhead, CTA text, section order. **Read both screenshots with the `Read` tool** before drafting Section 5 — that's what grounds the design/hierarchy read in what the page actually looks like instead of a guess from markup.

Don't also run `WebFetch` on the same URL "just to check" — it's the same static page either way, so a second fetch won't reveal anything Playwright's rendered DOM didn't already capture; it'd just be redundant work. `WebFetch` only comes in if the script above actually fails (site blocks headless browsers, times out) — then fall back to `WebFetch` for text-only, draft Sections 1–4 from whatever you get, and flag Section 5 as needing Matt's own look since there's no screenshot to ground it.

### 3. Run tribunal — via the Docker image, not the bare binary

Most of tribunal's engines (axe, Lighthouse, pa11y, retire, whatweb, nuclei) only ship inside the bundled Docker image — a bare `go build` binary only picks up the API-based engines (SSL Labs, Observatory) plus whatever happens to already be on PATH, silently degrading to a fraction of the coverage. Always run it through Docker:

```bash
docker image inspect tribunal >/dev/null 2>&1 || (cd ~/Code/personal/tribunal && docker build -t tribunal .)
mkdir -p ~/.local/share/tribunal/history
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal audit <url> --format json > /tmp/teardown-<brand-slug>.json
```

The first build takes a few minutes (installs Chromium + Lighthouse/axe/pa11y/retire); after that it's cached and fast. Restricted engines (squirrelscan, WPScan) are never bundled by design — they'll still show `unavailable`/`skipped`, and that's correct, not a bug.

The `-v` flag is a volume mount — it points the container's history path at the same real directory on Matt's Mac (`~/.local/share/tribunal/history`), so tribunal's own built-in history feature (every run auto-saves to `<root>/<target-slug>/<timestamp>.json`, which is what backs `tribunal diff`) actually lands on disk. Without it, `--rm` deletes the container — and the run it just saved — the instant the command finishes, silently. The `/tmp` JSON above is just this session's scratch copy for drafting from; the durable copy is the one tribunal itself writes into history.

Stay passive — never pass `--authorized`. This is a prospect's live site, not one Matt has explicit permission to intrusive-scan. Passive is also tribunal's default, so just don't add the flag.

If tribunal errors or an engine comes back `unavailable`/`failed`, that's fine — tribunal is built to degrade gracefully and still produce a `Run`. Work with whatever `merge_groups` came back; don't treat a partial run as a failure.

### 3b. Diff against the last run, if this prospect has been audited before

After the audit, run `tribunal diff` — it compares the two most recent runs in history, so the audit you just ran is the "to" side and the prior teardown's run is the baseline:

```bash
docker run --rm -v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history \
  tribunal diff <url> --format json > /tmp/teardown-<brand-slug>-diff.json
```

Pass the **same URL you gave `audit`** — tribunal slugs it identically to find the right history folder (its slug comes from the target URL, not the brand name, so don't substitute the brand slug here).

If it errors with "need two saved runs … found 1", this is the first teardown of this prospect — that's the normal case, not a failure. Skip the diff and move on.

When a diff does come back, it has `summary` counts and per-finding changes (`new` / `resolved` / `regressed` / `improved`), score deltas, and `coverage_changes`. **Check `coverage_changes` before trusting any "resolved"** — a finding whose whole category simply lost engine coverage between runs wasn't fixed, it went unchecked, and tribunal flags exactly this so you don't present it as progress.

**The diff is for Matt, not the doc.** It surfaces only in the report-back (step 8) — the teardown doc itself always reads as a fresh look. Whether to tell a prospect "we've looked at this before" is a sales call Matt makes deliberately, not something the draft should decide for him (the prior teardown may never have been sent).

### 4. Draft every section

Fetch the template first so you're filling its exact structure:

```bash
basecamp -a 6191443 docs show 9994887966 -p 46876803 --md
```

**Section 6 ("Under the hood") — grounded in tribunal, written in Matt's voice, not flagged as a draft.** Read the JSON `Run`:

- `scores.overall` / `scores.categories` — context, not the point. Don't lead with a number.
- `coverage` — per category, which engines checked it (`many` / `one` / `none`). A `none` is a real gap worth naming if it matters (e.g. no security engines succeeded), not a technical footnote.
- `merge_groups` — the reconciled findings to work from. Each has `kind` (`corroborated` = multiple engines independently agree, the strongest signal; `single-source` = one engine only, hold more loosely; `conflicting` = flag if you use it at all), `severity`, `confidence`, `category`, and the underlying `findings[]` with `evidence`.

If step 3b produced a diff, don't write it into this section — the doc reads as a fresh look regardless (see step 3b for why). The diff goes to Matt in the report-back instead.

Write it the way Matt actually writes it — read Basecamp doc `10032725076` ("Marathon Power Website Review (to send)") as the reference for tone before drafting. That document is the bar: plain language, zero jargon, each issue tied to a real consequence (Google ranking, security exposure, lost trust, a visitor bouncing) instead of a metric name, ordered by what actually matters rather than by raw severity, and warm even when the news is bad ("Good news here", "Nothing here requires changing the site you just built"). Keep it tight — surface the handful of things that matter, fold near-duplicates together, skip anything a prospect would shrug at. If nothing significant turned up, say that directly.

**Sections 1–5, 7, 8 — drafted from the homepage read, flagged as a first pass.** Use the template's own bracketed instructions as the spec for each section (the 10-second test, the hero's four jobs, the objection-stack walk, the copy read, design/hierarchy, the prioritized fix list pulling from everything above including Section 6, and the close). Give it a real, specific attempt — not a hedge-everything placeholder — since a concrete draft is what makes editing faster than writing from scratch. Right under each of these section headings, add one line:

```
*— AI first pass, rewrite in your voice before sending —*
```

Remove that line yourself once you've rewritten a section; the skill always includes it fresh.

### 5. Show Matt the draft before publishing anything

Print the full draft and wait for a go-ahead, same as any other skill that posts to Basecamp on Matt's behalf. Revise in place if he wants changes.

### 6. Publish the doc

Find or create the prospect's folder under the Deals vault:

```bash
basecamp -a 6191443 docs list --folder 9792703029 -p 46876803
```

If a folder matching the brand name doesn't exist:

```bash
basecamp -a 6191443 docs folders create "<Brand>" --vault 9792703029 -p 46876803
```

Build the new doc's content from the template's structure and boilerplate, with the drafts from step 4 dropped into each section (flag lines included on 1–5/7/8). Title it "Teardown — &lt;Brand&gt;". Then:

```bash
basecamp -a 6191443 docs documents create "Teardown — <Brand>" "<content>" --vault <brand-folder-id> -p 46876803
```

### 7. Link back to the Pipeline card, if one exists

Check whether the prospect already has a card:

```bash
basecamp -a 6191443 search "<Brand>" -p 46876803
```

If a card turns up on the Pipeline board (card table `9782662056`), add a dated comment linking to the new doc — don't touch the card's description, that's the template's territory:

```bash
basecamp -a 6191443 comment <card-id> "Teardown drafted: <doc-app-url>"
```

If no card exists yet, just tell Matt — don't create one. Whether a prospect is qualified enough for a Pipeline card is his call, not this skill's.

### 8. Report back

Give Matt the doc URL and a one-line summary (e.g. "3 corroborated findings surfaced, overall score 75 — mostly performance; sections 1-5/7/8 are a first-pass draft to rewrite"). If a diff ran, add one line of deltas (e.g. "vs the March run: 2 new, 1 resolved, overall −4") — this is the only place the diff surfaces; the doc doesn't mention prior runs. Mention where the durable artifacts landed (`~/.local/share/tribunal/history/<slug>/` for the scan, `~/.local/share/teardown/<slug>/` for the screenshots) in case Matt wants to look at them later. Nothing more beyond that.

Never delete anything under either of those two directories — they're the durable record, not scratch space. `/tmp` files created along the way (redirected stdout, etc.) are fine to leave or clean up; they're not the source of truth for anything.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Wrong account / 404 on any basecamp command | Missing `-a 6191443` | Always pass it explicitly — never rely on the CLI's global default |
| Section 6 reads like a scan report | Wrote straight from `merge_groups` without translating | Re-read the Marathon Power reference doc; every line needs a consequence, not a metric |
| Sections 1-5/7/8 read generic, could be any company's homepage | Drafted from assumption instead of the actual captured copy/screenshot | Re-read the JSON text and screenshots before drafting — quote or reference specifics from the real page |
| Draft published without the "AI first pass" flag on 1-5/7/8 | Skipped adding the flag line under each heading | Always add it fresh per section 4 — never rely on it carrying over from the template |
| Section 5 (design/hierarchy) invents a visual read with no screenshot | Screenshots weren't actually opened with `Read`, or the capture script failed | Always `Read` both PNGs before drafting Section 5; if the script failed, say so rather than guessing at layout/color from markup alone |
| `capture-homepage.mjs` fails with a missing module / browser error | `pnpm install` or the chromium download was never run in this skill's directory | `cd ~/.claude/skills/teardown && pnpm install && pnpm exec playwright install chromium` |
| Most engines come back `unavailable`, only ~4 of 13 ran | Ran the bare `tribunal` binary instead of the Docker image | Always run via `docker run --rm tribunal audit ...` per step 3 — the bare binary only has the API-based engines |
| Performance/accessibility score looks alarmingly low | Lighthouse/axe are lab (synthetic) data — can read much harsher than real-user field data | Frame it as lab vs. field (tribunal's own distinction), not a contradiction of anything Matt already knows about the site — see Section 6 guidance |
| Run never shows up in `~/.local/share/tribunal/history/` | Ran `docker run --rm tribunal` without the `-v` volume mount — the save happened, then `--rm` deleted the container (and the file) with it | Always include the `-v ~/.local/share/tribunal/history:/home/node/.local/share/tribunal/history` mount from step 3 |
| tribunal build fails | Go toolchain mismatch or stale `go.sum` | Run `go build` from `~/Code/personal/tribunal` directly and surface the real error to Matt rather than guessing a fix |
| `diff` errors "need two saved runs … found 1" | First teardown of this prospect | Not a failure — skip the diff (step 3b) and draft Section 6 from this run alone |
| `diff` errors "found 0" even though this prospect was torn down before | Prior run was made without the `-v` history mount (so it never persisted), or a different URL form was passed than last time (slug mismatch) | Check `ls ~/.local/share/tribunal/history/` for the actual slug folders; pass the same URL form the prior audit used |
| Report-back presents a "resolved" finding as a fix the prospect made | Its category lost engine coverage between runs — unchecked, not fixed | Cross-check resolved findings against the diff's `coverage_changes` before reporting them |
| Doc mentions "since we last looked" / a prior audit | Diff data leaked into Section 6 | The diff is report-back-only (step 3b) — the doc always reads as a fresh look |
| Duplicate prospect folder created in Deals vault | Didn't check `docs list` first | Always list the Deals vault (`9792703029`) before creating a folder |
