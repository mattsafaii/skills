---
name: project-setup
description: Create or update a client's master Project Context doc — one Basecamp document titled exactly "Project Context" at the root of the project's Internal folder (not Working, not the Search/SEO folder), with frozen headings for the business, contacts, Offer gate, engagement scope, kit, access, key pages, writing rules, constraints, reporting mechanics, and a change log. Interview Matt in small batches, confirm inferences, and never invent. Search-only facts (GSC property, Foundation/Growth plan, brand terms, scoreboard tokens, rankings) stay in the Search/SEO context doc. Use when Matt says "set up [client]", "/project-setup", "start a new client [name]", "create the Project Context for [client]", or when another skill reports the Project Context doc is missing or lacks a fact it needs.
---

# Project Setup

## Goal

Create or update ONE Basecamp doc per client, titled exactly **`Project Context`**, at the **root of the project's Internal folder** in Docs & Files (not Working, not the Search/SEO folder). It is the standing record of client facts: what the business sells, who buys, what this engagement includes, the kit, access, key pages, writing rules, constraints, and reporting mechanics. Every skill reads this title first; it stops them re-deriving what is already known and stops them inventing facts.

## Tone

Be direct, practical, and structured. Ask questions in small batches. Confirm inferences. Never invent: if a fact is not given or verifiable on the site or in a doc, ask Matt — a placeholder stays "not set" until real.

## What does NOT go in this doc

Search-only facts stay in the SEO context doc (`SEO — Project Context`):

- GSC plan / property
- Foundation/Growth plan tier
- Brand terms
- Scoreboard tokens
- Rankings / keyword data

The `## Reporting` heading here is delivery mechanics only (client-visible, where it posts, folders, title). `Scoreboard events` reads from the Fathom goals in `## Access` rather than duplicating a list.

## Client project folders — the contract

Every client project carries this **flat tree** in Docs & Files. Never invent other folders.

```
Internal          ← Project Context only
Working
Ops
Reports
Archive
Uploads  /  Review  /  Handoff  /  Admin
```

Rules: no `[DRAFT]` / `[Final]` in titles — Basecamp versions are the trail. One live file per artifact, prefix = phase for phase files in Working (`Inventory —`, `Structure —`, `Build —`, `Test —`, `Release —`, `Maintenance —`, `SEO —`). Code and catalog data live in GitHub, not Basecamp.

**v1 scope:** this skill creates **Internal only** if missing. It does not build the rest of the skeleton — that is the template skill's job — and it does **not** dump a sitemap into Context; phase work belongs to Working via other skills.

## Where the answers go

One doc titled **`Project Context`**, **Internal root**. Get the folder id before doing anything else:

1. `basecamp -a 6191443 projects list --json` — match the project by exact name Matt gave. Ambiguous or missing → show candidates and ask; never guess.
2. `basecamp -a 6191443 files folders --in <project_id> --json` — find the **Internal** vault id.
3. Find the doc with `files list --vault <internal_vault_id>` — never create the doc until the Internal id is known.

Skills resolve project id → folder name → exact title; they do not hardcode vault ids.

### Frozen heading contract

These headings are exact. **Do not rename them.** Formats only, no real client data in the examples.

```markdown
## Business

Domain: https://example.com
Site launched: YYYY-MM-DD
Markets: <countries / service area>
What they sell: <products and the service around them, as they sell it today>
Who buys: <role: facilities, procurement, contractor, IT, …>
Locations: <offices / warehouses if it matters>
Previous site: same domain | <old URL>

## Contacts

| Name | Role | Email | Notes |
|---|---|---|---|
| | Owner | | |
| | Point of contact | | Approves brief / map / go-live |

## Offer

Clear: yes | no
How they sell today: <one short paragraph, their words, not a new framework>

## This engagement

Main job: site + maintenance | site only | maintenance only
Maintenance: monthly | none
Secondary in scope: none | portal | integration | other: <name>
Inquire path: <RFQ / contact / call / service ticket>
Catalog in v1: <families / "none">
Pricing on site: public | gated | mixed
Brief: <title> — draft | approved YYYY-MM-DD | none yet

## Kit

Workspace: ~/Work/safaii-studio/clients/<slug>
Site root: <workspace>/site
Repo: <GitHub org/repo or "not yet">
Cloudflare: <account / Pages project or "not yet">
Production URL: same as Domain | <url>
Resend: domain authenticated yes | no | not yet
Catalog store: json | sqlite | none
PagesCMS: yes | no
Owner of GitHub / Cloudflare / Resend: client | not yet
Secrets: 1Password vault <name> | not set

## Access

Domain registrar: <who holds it>
GitHub: invited | pending
Cloudflare: invited | pending
Resend: invited | pending
Search Console: wired | not wired
Analytics: Fathom site id: <id or "not in use">
Fathom goals: <exact event names, comma-separated, or "not in use">
Logo / photos: in Uploads | not received

## Key pages

| URL | Role | Topic | Notes |
|---|---|---|---|
| https://example.com/ | money | Home | |

## Writing

Audience: <who reads the site>
Voice: clear, specific, no slogan layer
Do not claim: <regulated or sales claims they cannot stand behind>
Banned phrases: <or "none">

## Constraints

Industry notes: <medical / security / government / none>
Topics they will not put on the site: <or "none">

## Reporting

Client-visible monthly: yes | no
Where it posts: Message Board | email | both
Draft folder: Reports
Shipped folder: Handoff
Title: `Site report — Month Year`

Scoreboard events: use the Fathom goals in Access.
Search plan, brand terms, and rankings appendix live in `SEO — Project Context`. Do not duplicate them here.

## Log

| Date | Summary |
|---|---|
| YYYY-MM-DD | Project Context created. |
```

**Reading the contract:**

- **Contacts** — at least owner and point of contact. Same person → one row, both roles in Role. No extra rows for people you do not work with.
- **Offer → `Clear:`** is the gate. If `Clear: no`, stop and say so: the offer needs a separate advisory job, or Matt walks away. Do not start Structure, do not invent positioning and call it context.
- **Access: Fathom site id / Fathom goals** — event names exactly as they exist in Fathom (lowercase, human-readable, matching what `fathom-analytics` created). A title-cased guess won't match the API.
- **Key pages roles:** `money` | `hub` | `other`. Shortlist (10–30), not a sitemap — the sitemap lives in Working as `Structure — Sitemap`.
- **Voice / Writing** — record only what the site stands behind; no slogan layer.
- Leave a heading in place even when the body is "not set" — never delete a heading.

## Rules (from the studio process)

- This skill is for Safaii Studio site work: **site + maintenance for B2B product-and-service companies** — an operating company that already sells, where the offer is usually clear. Not a brand-led world-building job. Not a single-location storefront (favor or referral only).
- The doc is the **standing record**. Phase work is prefixed files in Working. Do not dump the sitemap, punch lists, or strategy artifacts into Context.
- GSC property, plan tier, brand terms, scoreboard, rankings stay in the Search/SEO context doc — this skill never writes them here.

## The write loop (every write, every time)

Basecamp docs are full-document replace. The procedure, copied from `seo-project-setup`:

1. Find the doc by exact title **in the Internal root** — never create a second copy.
2. Read the full markdown into memory.
3. Patch only the target heading's body. Leave every other section and every log row untouched.
4. Upload the **entire** doc as an update of that same file id (`--vault <internal_vault_id>`).
5. Re-read and assert the other sections still exist, the title and folder are unchanged, and the content is non-empty.

Without file-id + full-replace + re-read, "never recreate" is a wish. The post-write check applies to **every** write — create and update.

### First create (only when the doc doesn't exist)

If the title is missing in the Internal root, create it **once with every heading present and empty tables** — never a partial doc:

1. Build the full markdown: every heading in the frozen contract, Contacts / Key pages / Log tables empty with correct column headers, and the fact lines filled from this run's answers ("not set" where unknown).
2. `basecamp -a 6191443 files doc create "Project Context" "<full markdown>" --in <project_id> --vault <internal_vault_id> --json` — **must carry `--vault`**, or the doc lands at project root.
3. Log the first row: `YYYY-MM-DD | Project Context created.`
4. Enter the write loop from then on — same file id, full-document updates.

### Canonical CLI shapes

The verified basecamp CLI commands — do not invent flags:

```text
# resolve the Internal folder id
basecamp -a 6191443 files folders --in <project_id> --json

# find the doc by exact title, ONLY in the Internal root
basecamp -a 6191443 files list --vault <internal_vault_id> --in <project_id> --json

# read the current doc
basecamp -a 6191443 files show <file_id> --in <project_id> --json

# first create (only if title absent in the Internal root)
basecamp -a 6191443 files doc create "Project Context" "<full markdown>" --in <project_id> --vault <internal_vault_id> --json

# every later write
basecamp -a 6191443 files update <file_id> --content "<full markdown>" --in <project_id> --vault <internal_vault_id> --json
```

`files doc create` takes content as an argument, never `-` stdin — the stdin form silently creates an empty doc. Publish with `--content "$(cat file)"` from a written file, `test -s` the file before publish, and verify stored content == canonical after.

## Checklist

### 1. Verify the connection and resolve the client

1. Basecamp CLI, account `6191443` (Safaii Studio) — always passed explicitly; this skill never runs on another account.
2. `projects list --json`, exact-name match. Ambiguous → ask.
3. CLI unavailable → stop; nothing can be saved without it.

### 2. Read what is already there

Find `Project Context` only in the Internal root (listing the whole project risks grabbing a root-level namesake). Read it if present and summarize what's known vs missing; confirm or correct entries rather than re-asking. Also read the Search/SEO context doc if it exists — the Fathom site id and goal names already answered there flow into `## Access`, and the GSC row here becomes `wired` only when that doc has a real `Property:` line (the property string itself never comes over). Never re-ask what's recorded.

### 3. Collect the business (Business, Contacts)

Ask for, in small batches:

- Primary website/domain, previous site if the domain changed
- When the current site launched (ask; if analytics or GSC tracking predates the launch, note it — pre-launch data describes a different site)
- Markets: countries or service area
- What they sell — products and the service around them, **as they sell it today**. Never a new framework; their words.
- Who already buys (facilities, procurement, contractor, IT…)
- Locations that matter (offices, warehouses)
- Owner and point of contact (owner approves; point of contact approves brief / map / go-live). Billing / IT / catalog people only when you actually work with them.

### 4. The Offer gate

Ask how they sell today — one short paragraph in their words. Then set the gate:

- Offer is clear → `Clear: yes`, continue.
- They cannot say what they sell or who pays → `Clear: no`. **Stop.** Tell Matt: settle the offer as a separate advisory job, or walk away. Do not continue the interview into Structure-adjacent topics; do not invent positioning here.

### 5. This engagement

Ask:

- Main job: site + maintenance | site only | maintenance only
- Maintenance: monthly | none
- Secondary in scope: none | portal | integration | other: <name> — only what this brief includes; a portal is never hidden inside Maintenance
- Inquire path: RFQ / contact / call / service ticket — what a stranger does today
- Catalog in v1: which families, or "none"
- Pricing on site: public | gated | mixed
- Brief status: draft / approved + date / none yet

### 6. Kit (default kit unless the brief names an exception)

Record what exists, planned state vs "not yet":

- Workspace: derive `<slug>` from the Basecamp project name — lowercase, spaces to hyphens, strip other punctuation (e.g. "Guru Packaging" → `guru-packaging`) — and confirm the slug with Matt once. Write the full path on the `Workspace:` line: `~/Work/safaii-studio/clients/<slug>`, and the website repo root on the `Site root:` line: `<workspace>/site` (the folder pushed to GitHub). If the workspace directory does not exist, create it with `mkdir -p`. If **mkdir fails**, record the path anyway, tell Matt, and do not abort the Basecamp write. This step creates the workspace folder only — it does **not** create `site/`, does not `git init`, does not scaffold, and does not copy Basecamp docs into the workspace; Build makes `site/` and runs `git init`.
- Repo: GitHub org/repo
- Cloudflare: account / Pages project
- Production URL
- Resend: domain authenticated
- Catalog store: json | sqlite | none — smallest store that fits
- PagesCMS: yes | no — only if they edit pages themselves
- Owner of GitHub / Cloudflare / Resend: **client** — they create the accounts (or their IT does) and invite you; never create an account owned by you that later needs handover. If you must create them, the owner email is theirs from the first minute.
- Secrets: 1Password vault name or "not set"

### 7. Access

- Domain registrar (who holds it)
- GitHub / Cloudflare / Resend: invited | pending — per the ownership rule above
- Search Console: `wired | not wired` only — the property string is a search fact and stays in the Search/SEO context doc. Don't duplicate the `sc-domain:` line here until that skill is migrated.
- Analytics: `Fathom site id:` line (exact id, or "not in use") and `Fathom goals:` line with exact event names — same lowercase-as-in-Fathom rule as the SEO context skill
- Logo / photos: in Uploads | not received (they supply; you do not invent a brand)

### 8. Key pages

Curated shortlist (10–30 URLs), one row each with role (`money` | `hub` | `other`) and topic where known. If the site doesn't exist yet, record the planned money/hub pages from the interview — grounded in what they sell, not invented. This is not a sitemap; sitemap work belongs to Structure in Working.

### 9. Writing and constraints

- Audience: who reads the site
- Voice: clear, specific, no slogan layer — plus any voice notes Matt gives
- Do not claim: regulated or sales claims they cannot stand behind
- Banned phrases or "none"
- Industry notes (medical / security / government / none) and topics they will not put on the site

### 10. Reporting (delivery mechanics only)

- Client-visible monthly: yes | no
- Where it posts: Message Board | email | both
- Draft folder: Reports; Shipped folder: Handoff
- Title: `Site report — Month Year` (frozen)
- Scoreboard events come from the Fathom goals in `## Access` — nothing duplicated, no plan tier, no brand terms, no rankings here

### 11. Log and recommend next

Append a one-line Log row per run — created on first run; one-line diff on re-runs ("added contacts, corrected engagement scope") so the log records change, not just "updated". Merge new answers into existing prose; never overwrite.

**After first write, recommend next: Inventory brief — not seo-strategy.** If Inventory brief isn't built yet, say so plainly and stop there rather than naming a substitute.

Then **stop**. The run ends with: find or create Project Context → fill it from the interview + template → return the doc URL. Do not migrate `seo-project-setup` in the same run. Do not create phase folders. Do not write todos. The report itself (`Site report — Month Year` — drafted in Reports, shipped via Handoff) is a different skill (`client-report`); this skill only records Reporting yes/no and the Fathom goals in Access.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: client resolved, sections filled, Offer gate result, what's still "not set", and the recommended next workflow. Return the doc URL. Tell Matt he can read and edit everything saved in the doc directly in Basecamp.

## Guardrails

- Confirm facts with Matt before writing them. Inferences from the site are fine to propose, but they get saved as agreed answers, not guesses — distinguish source evidence from inference.
- Never re-ask what's already recorded. Merge new answers into existing prose on a re-run; preserve every section and log row.
- The doc is context only — no strategy, no sitemap, no copy drafts. Phase artifacts live in Working.
- One owner: this skill writes only `Project Context`. Search-only fields belong to the Search/SEO context skill.
- Re-run fills gaps; it does not discard.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| Doc in the wrong folder | Created at project root, in Working, or in a Search/SEO subfolder | Doc must live at the **Internal root**; move or update there, never treat a stray copy as canonical |
| Create succeeded but vault is wrong | `--vault` dropped or wrong id | Delete the misplaced doc and re-create with `--vault <internal_vault_id>`; never start the write loop on that file id |
| Second doc with the same title | Created instead of found | Find by exact title in Internal first; update that file id, never recreate |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443`; never another account |
| Empty doc after create | Used the `-` stdin form | Pass content as an argument; verify content length after create |
| Earlier sections clobbered | Full-doc replace without re-reading first | Write loop: read → patch one heading → upload entire doc → re-read and assert |
| Headings drift between runs | Renamed a section | Follow the frozen heading contract; other skills parse these names |
| Facts invented | Proposed inferences as facts without confirming | Ask Matt; placeholders stay "not set" until real |
| Fathom goal names wrong | Title-cased / guessed event names | Copy event names exactly as they exist in Fathom (verify on the API if unsure) |
| Offer unclear but work continued | Skipped the gate | `Clear: no` → stop, present the advisory/walk-away choice, do nothing else |
| Context lost on re-run | Overwrote instead of merged | Merge new answers into existing prose; preserve every section and log row |
