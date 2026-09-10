# Safaii Studio — Skill index

**Canonical copy:** this file at `~/Work/skills/SKILL-INDEX.md` (agent-facing). The Basecamp mirror (Office → SOPs & Playbooks → **Guide — Skill Index**, id 10290401336) is a copy — update this file first, then re-mirror.

Internal. Agents read this to know what to run and what not to invent.
Site process: Inventory → Structure → Build → Test → Release → Upkeep.

Source of truth for the process: `~/Downloads/safaii-studio-process.md` (the full doc). Skills live in `~/Work/skills/` (opencode loads them through the `~/.config/opencode/skills` symlink). Titles in Basecamp are contracts — skills resolve project → folder → exact title, never hardcode vault ids.

---

## Default order (new client, site + upkeep)

```
1.  Project exists in Basecamp (folders from the project template)
2.  project-setup                 → Project Context
3.  inventory-brief               → Inventory — Brief, Inventory — Current site
4.  Client approves the brief     → Matt copies Brief to Review
5.  seo-project-setup             → SEO — Project Context     [only if they bought search]
6.  keyword-research              → SEO — Keyword Research    [only if search]
7.  keyword-clustering            → terms onto pages          [optional — can assign by hand]
8.  structure-map                 → Structure — Sitemap [, Fields]
9.  structure-copy               → Structure — Template copy
10. Matt approves the map         → copies Sitemap to Review
11. Build / Test / Release        → humans + repo (no skill required)
12. seo-rank-tracking             → after go-live, if search
13. Upkeep work                   → repo + Working files
14. client-report                 → Site report — Month Year
```

If they did **not** buy search: skip 5, 6, 7, 12. Clustering is optional; assign terms by hand on the sitemap.

If Offer in Project Context is `Clear: no`: stop after step 2. No brief, no SEO.

Structure reads: `structure-map` reads the saved set when it exists (`Search — Keyword research` or `SEO — Keyword Research`); `structure-copy` reads the sitemap. They never gate on search being bought.

---

## Skills by job

### Standing facts

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `project-setup` | live | `Project Context` (Internal root) | Project exists. Creates Internal if missing. |
| `seo-project-setup` | live | `SEO — Project Context` (Internal → SEO) | `Project Context`. Search add-on only. |

`project-setup` owns company facts (Business, Contacts, Offer gate, This engagement, Kit, Access, Key pages, Writing, Constraints, Reporting mechanics, Log).
`seo-project-setup` owns GSC property, Plan (Foundation / Growth), brand terms, scoreboard tokens, SERP competitors — and reads company facts from `Project Context` instead of re-asking.

### Inventory

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `inventory-brief` | live | `Inventory — Brief`, `Inventory — Current site` | `Project Context`, Offer clear |
| `seo-audit` | live | one-pager for a **new domain / prospect** | Not for an active job after Inventory |

### Structure

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `structure-map` | live | `Structure — Sitemap`, `Structure — Fields` | Approved brief; saved set if it exists. `Structure — Fields` only if Catalog in v1 ≠ none. |
| `structure-copy` | live | `Structure — Template copy` | Sitemap |

### Search (optional add-on)

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `keyword-research` | live | `SEO — Keyword Research` (saved set) | SEO context doc |
| `keyword-clustering` | live | page assignment / cannibal flags | Saved set |
| `seo-rank-tracking` | live | `SEO — Rank Tracker` | Saved set, live site |
| `competitive-landscape` | live | `SEO — Competitive Landscape` | SEO context; only if Inventory is stuck |
| `competitor-analysis` | live | `SEO — Competitor — <domain>` | Named peer, not default |
| `local-seo` | live | `SEO — Local Audit` | Maps pack actually matters |
| `link-prospecting` | live | `SEO — Link Prospects — <asset>` | Separate paid job + an asset |
| `seo-strategy` | live | opportunities / IA notes | **Do not default.** Structure owns the map. |
| `dataforseo` | tool | nothing | Called by research skills |
| `seo-skills-guide` | router | nothing | Old SEO-only router; this index supersedes it for studio order |

### Build / Test / Release

No skill. Code in GitHub. Staging / Fixes / Checklist are Working files you or a repo agent touch.

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `release-handoff` | later | `Release — Checklist`, `Release — Handoff` | Kit filled in Project Context |

### Upkeep

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| `upkeep-month` | later | `Upkeep — Month YYYY-MM` | Live site |
| `client-report` | live | `Site report — Month Year` in Reports | Domain + Fathom from `Project Context` (falls back to the SEO doc); Plan / GSC / brand terms from `SEO — Project Context` |

### Project shell

| Skill | Status | Writes | Needs first |
|---|---|---|---|
| project template (unnamed) | spec only | folders, stub Working docs, six empty todo lists | New Basecamp project |

See `basecamp-project-template.md`.

### Off the main line (sales / prospect)

| Skill | Status | Job |
|---|---|---|
| `teardown` | live | client-facing audit for a sales prospect |
| `prospect` | live | internal pre-meeting read on a prospect |

---

## Dependency graph

```
project-setup                       [owns Project Context — company facts]
    ├─ inventory-brief              [Working: Brief + Current site]
    │     └─ structure-map          [Working: Sitemap (+ Fields if catalog)]
    │           └─ structure-copy   [Working: Template copy]
    │                 └─ (Build by hand)
    │                       └─ client-report
    │
    └─ seo-project-setup            [search only — owns SEO — Project Context]
          └─ keyword-research
                ├─ keyword-clustering → structure-map (page-to-term)
                └─ seo-rank-tracking → client-report (Rankings on Growth)
```

Off the main line (do not insert unless named):

```
seo-audit              prospects / new domains
competitive-landscape  Inventory stuck on SERPs
competitor-analysis    one domain
local-seo              Maps
link-prospecting       paid extra
seo-strategy           only if you explicitly want opportunity notes
teardown / prospect    sales pipeline, not an active job
```

---

## What reads what

| Artifact | Reader |
|---|---|
| `Project Context` | Every client skill (read first) |
| `SEO — Project Context` | SEO skills + `client-report` (Plan, GSC, brand terms) |
| `Inventory — Brief` | `structure-map`, Matt, client (via Review) |
| `Inventory — Current site` | `structure-map` (redirects later) |
| `Structure — Sitemap` | `structure-copy`, Build |
| `Structure — Fields` | Build (CMS types) |
| `Structure — Template copy` | Build |
| `SEO — Keyword Research` | clustering, rank-tracking, `structure-map` |
| `SEO — Rank Tracker` | `client-report` (Growth only) |
| Fathom + GSC | `client-report` |

---

## Folder map (flat, every client project)

```
Internal          ← Project Context (master) only
Working           ← phase files: Inventory — / Structure — / Build — / Test —
                    Release — / Upkeep — / Search — (one live title per artifact)
Ops
Reports
Archive
Uploads / Review / Handoff / Admin   (client-visible)
```

No `[DRAFT]` / `[Final]` in titles — Basecamp versions are the trail. Do not create per-phase folders; Working stays flat. Live docs still on the older tree (Internal → Strategy/Copy/…/SEO) keep their existing titles until a later migration; new jobs use the flat tree.

---

## Rules for agents

1. If `Project Context` is missing, run `project-setup`. Do not invent the company.
2. If Offer is not clear, stop.
3. Do not run `seo-strategy` as Phase 1.
4. Do not run search skills on a site-only job.
5. Do not write todos from a context skill.
6. Do not create a second doc with a contract title.
7. Do not put sitemaps or reports in `Project Context`.
8. One skill per run unless Matt names a chain.

---

## Status key

- **live** — skill file exists and is in use
- **to build** — prompt written, not shipped
- **later** — wait until the live/to-build chain works
- **spec only** — markdown spec, no skill yet
