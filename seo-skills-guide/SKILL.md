---
name: seo-skills-guide
description: The map for Matt's SEO skill chain — which skill to run when, in what order, and why. A reference router, not a workflow: it answers "which SEO skill should I use", "what's next in SEO", "/seo-skills-guide", "how do I do SEO for a client", "what order do the SEO skills go in", or "which skill does X". It carries the spine, the routing decisions, the doc-contract inventory, and the tool/secret map. Load it when deciding what to run next; the individual skills do the actual work and have their own confirm gates.
---

# SEO Skills Guide

The map of Matt's SEO skill chain. This skill never produces a deliverable — it routes. It tells you which skill to run next and why; the individual skills carry their own rules, frozen contracts, and confirm gates.

> For the whole studio site pipeline (project-setup → inventory-brief → structure-map → structure-copy, plus where search plugs in), see `SKILL-INDEX-STUDIO.md` at `~/Work/safaii-studio/_config/` — it supersedes this guide for studio order. This guide still owns the SEO-only detail.

## The spine

The default path for any client with SEO work:

```
seo-project-setup → keyword-research → seo-rank-tracking
```

- **`seo-project-setup`** is the search gate. It itself reads the **master `Project Context`** doc first (Internal root, built by the `project-setup` skill) — company facts come from there, never re-interviewed; missing master doc → run `project-setup` first. Nothing runs without the client's `SEO — Project Context` doc — every research skill refuses to start if it's missing. Run it first, always.
- **`keyword-research`** finds the saved-keyword set (the tracking contract).
- **`seo-rank-tracking`** tracks positions on demand (dated position snapshots, same-day cap) — it only needs a dated `## Saved keywords`, not a page map. The monthly cadence belongs to `client-report`.

**Insert `keyword-clustering` when the question is pages, not positions.** Clustering maps the set onto the site (IA/content planning). If you're measuring first, setup → research → tracking is the whole path.

## Routing by situation

| Situation | Run | Why |
| --- | --- | --- |
| Any client, first time | `project-setup` → `seo-project-setup` | `project-setup` creates the master `Project Context` at the Internal root (company facts, Offer gate); the search add-on fills GSC / plan / brand terms |
| Greenfield build, no site yet | `seo-project-setup` → `keyword-research` | Seeds come from positioning (no GSC, no site to fetch); KR defines the saved set — clustering + `seo-strategy` Entity Map define the page structure for copywriting |
| Launched site, never did SEO | `seo-project-setup` → `keyword-research` | "Never did SEO ≠ new site" — GSC striking-distance is the advantage; harvest it |
| Bad / wrong information architecture | `keyword-research` → `keyword-clustering` → `seo-strategy` | Seeds come from positioning, not the broken site; clustering + strategy output the corrected IA to rebuild against |
| Local business (Maps matters) | `seo-project-setup` → `keyword-research` if no saved set → `local-seo` | GBP + local-pack audit; local-seo takes its keywords from the saved set when it exists |
| Want to know who owns the market | `competitive-landscape` | After keywords exist; feeds strategy gaps |
| One competitor to study | `competitor-analysis` | After landscape names the domain |
| Content ideas / entity map / IA | `seo-strategy` | Consumes research + page map + landscape |
| Link prospects for an existing asset | `link-prospecting` | Needs a live linkable asset (content comes before links) |
| Fresh-domain client-facing audit | `seo-audit` | One-page, one-action report — not a teardown, not maintenance. If Context exists it binds the one thing; if a dated saved set exists, don't invent a focus list |
| Monthly maintenance report | `client-report` | Consumes tribunal + Fathom + GSC + the SEO docs' newest data |

## Decision trees

**"I need to know X"**

- What keywords to target → `keyword-research`
- Where keywords map to pages → `keyword-clustering`
- Who's winning the market → `competitive-landscape`
- What one competitor does → `competitor-analysis`
- Where we rank now → `seo-rank-tracking`
- What content to make → `seo-strategy`
- Who should link to an asset → `link-prospecting`
- Why a business isn't on Maps → `local-seo`
- Is a fresh domain healthy → `seo-audit`

**"What's the state of the client"**

- Prospect, pre-meeting → `prospect` (internal), `teardown` (client-facing)
- Existing client, monthly → `client-report` (consumes the Rank Tracker's newest run + config, optional Landscape `## Market read`; positions older than ~35 days → say so, don't re-SERP)
- Existing client, first SEO work → `seo-project-setup` first, then the spine

## The doc inventory (contracts)

Every doc lives in the client's **Docs & Files → Internal → SEO folder** unless noted. Each has one owner — the skill that writes it — and other skills consume it, never re-create it.

| Doc | Owner | Consumed by |
| --- | --- | --- |
| `Project Context` *(Internal root, not the SEO folder)* | `project-setup` | company facts for every skill — read first, never re-asked |
| `SEO — Project Context` | `seo-project-setup` (search add-on) | every research skill (the search gate) |
| `SEO — Keyword Research` | `keyword-research` | rank-tracking, clustering, strategy, landscape, local-seo |
| `SEO — Page Map` | `keyword-clustering` | strategy |
| `SEO — Competitive Landscape` | `competitive-landscape` | strategy, link-prospecting, client-report (optional `## Market read`) |
| `SEO — Competitor — <domain>` | `competitor-analysis` | strategy, link-prospecting |
| `SEO — Rank Tracker` | `seo-rank-tracking` | client-report (newest run + config), strategy (optional striking distance) |
| `SEO — Content Opportunities` | `seo-strategy` | (the deliverable) |
| `SEO — Entity Map & IA` | `seo-strategy` | (the deliverable) |
| `SEO — Link Prospects — <asset-slug>` | `link-prospecting` | (the deliverable) |
| `SEO — Local Audit` | `local-seo` | (the deliverable) |

**Non-doc deliverables — the report-artifact flow:** `seo-audit` and `client-report` produce client-facing **report docs**, not Internal > SEO docs. The flow: skill creates the report doc **and** a handoff-message draft doc in the client's **Internal > Reports** (team-only, born hidden) → Matt reviews both (edits either in place) and manually moves the **report doc** to **Deliverables > Reports** (the move flips it client-visible) → the handoff message posts to the Message Board from the drafted copy, with the real link to the moved report. The handoff draft stays in Internal as the record of what was sent. `teardown` posts to the Sales project's Deals vault.

**The folder map (every client project):**

```
Docs & Files
- Internal (team-only)
  - Strategy / Copy / Design / Development / SEO (research docs live here) / Site Ops / Reports (report docs are born here)
- Admin (client-visible)
- Assets (client-visible)
- Review & Feedback (client-visible)
- Deliverables (client-visible)
  - Reports (moved report docs land here — the ship gate)
```

**Title families:** `SEO — Competitor — <domain>` and `SEO — Link Prospects — <asset-slug>` are patterns, not fixed titles — one doc per competitor / per asset. **`SEO — Local Audit — <city-or-cid>` is not v1** — don't invent per-location local docs from the guide; a single chain audit is the current shape.

## The tool and secret map

| Tool | What it does | How it's reached | Secrets |
| --- | --- | --- | --- |
| DataForSEO MCP | real SERP/keyword/backlink/domain data | the `dataforseo` skill's catalog | `DATAFORSEO_BASIC_AUTH` via 1Password → `~/.zshrc` |
| GSC | first-party search data (clicks, impressions, striking distance) | `~/Work/scripts/gsc-fetch/gsc-fetch.rb` (one shared script) | service-account JSON via `op read 'op://Secrets/GSC Service Account JSON/notesPlain'` |
| Basecamp resolution | resolve a client + read its Context / Rank Tracker / Landscape docs in one pass | `~/Work/scripts/client-report-prep.rb` (client-report step 1) | none |
| Fathom | analytics | direct API calls (client-report) | token via `op read 'op://Secrets/Fathom API Token/password'` |
| tribunal | audit engine (technical, passive; incl. field CWV via the crux engine) | Docker image at `~/Work/safaii-studio/lab/tribunal` | CrUX key via `GOOGLE_CrUX_API_KEY` (wired in `~/.zshrc`) |
| Browser-control | live Maps detail panel (review text, Q&A, posts) | browser-control skill / MCP | runs in Matt's browser |

**Basecamp:** always `-a 6191443` (Safaii Studio), passed explicitly. Documents are markdown (Basecamp 5 renders GFM tables). `files doc create` takes content as an argument, never `-` stdin.

## Rules that apply across the chain

- **The search doc gates everything.** Missing `SEO — Project Context` → run `seo-project-setup` first. The master `Project Context` gates company facts — `seo-project-setup` requires it (missing → run `project-setup`).
- **Split of ownership.** Company facts (domain, offer, contacts, kit, Fathom, writing rules) belong to the master `Project Context` doc; the SEO doc holds only search facts (GSC property, plan, brand terms, scoreboard tokens). `client-report` reads both: master doc first for domain + Fathom (falls back to the SEO doc when the master doc doesn't exist yet), SEO doc for Plan / GSC / brand terms.
- **Consume, never re-research.** Each skill reads what the previous one wrote; re-deriving is a failure.
- **Measurement, not observation.** Every number carries a date; market is US by default unless the context doc says otherwise.
- **Confirm gates are per-skill, not universal.** Research / landscape / analysis / local / strategy write only after Matt confirms their doc. **Rank-tracking writes with no confirm gate** — it appends a factual snapshot of an already-confirmed set. Client-report and seo-audit confirm **create** (the report doc in Internal) and **handoff** (the message, after Matt's move) — the move itself is Matt's ship gate.
- **One owner per doc.** No skill writes another's doc except the asked merges into `SEO — Project Context` (competitors, key pages) on Matt's explicit yes.
- **Reuse rules vary by cadence:** research / landscape / analysis / local / audit / strategy reuse within **30 days** (same inputs); `seo-rank-tracking` is **one run per calendar day** (a 30-day reuse there means stale positions); `client-report` is **monthly by definition**. Matt can override research reuse with "run it anyway."
- **Spend is capped everywhere.** Each skill states its default batch; anything beyond asks first.