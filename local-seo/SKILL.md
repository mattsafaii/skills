---
name: local-seo
description: Audit a Google Business Profile and local-pack visibility for one client — profile snapshot (category, rating, reviews, claimed, hours), competitor comparison from the same market, Maps/local-pack position per keyword, and a prioritized fix list led by one do-this-week action — written to the client's SEO — Local Audit doc in Basecamp (Internal > SEO). Use when Matt says "local SEO for [client]", "/local-seo [client]", "why isn't [client] showing up on Google Maps", "local search audit for [client]", or a client's rankings depend on a physical location or service area. Not national organic work (that's keyword-research / competitive-landscape). Never recreate the doc under a new title.
---

# Local SEO Skill

Works out why a business does or does not show up in Google Maps and the local pack near its customers, and what to fix first. Use when rankings depend on a physical location or service area — storefronts, restaurants, clinics, trades.

## Rules that don't bend

Load the **dataforseo** skill for the full catalog and hard rules. The essentials:

1. **Measurement, not observation.** Every observation carries a date: "as of <date>". **Market is US by default** (the DataForSEO `location_name` / coordinate). A bare rating, review count, or rank is never citable.
2. **The local tools you have.** This skill uses **`business_data_business_listings_search`** (profile fields: category, rating + distribution, review count, photos, claimed, hours, services, `cid`/`place_id`) and **`serp_organic_live_advanced`** (local-pack position per keyword). **Review text, recency, owner replies, Q&A, and posts come from the live Google Maps detail panel via `browser-control`** — no API provides them. Where the browser isn't available or a page won't load, those sections sit out with a one-line note, never fabricated.
3. **Match by `cid` / `place_id`, never name alone.** Name matching collides with chains and similarly named businesses. Once a listing's `cid` is known, reuse it everywhere.
4. **Spend is capped.** One `business_listings_search` for the business, one for competitors (or reuse `people_also_search` rows), and one `serp_organic_live_advanced` per keyword (1–3 keywords). Then ask before any further call. (Listings search ≈ $0.0x; SERP ≈ $0.002 each.)
5. **local_pack ≠ organic.** A Maps placement is a different game than a blue link — record which it is, never blur them.
6. **A missing pack rank is not proof of invisibility.** The position checks cover the storefront, not a service-area sweep — there is no rank grid in this skill. Absence at the storefront means outranked nearby or a sparse SERP; read it against the result count, never as "they don't show up anywhere."
7. **Never recommend review gating, fake reviews, or keyword-stuffed business names.**
8. **Confirm before write.** The audit doc is written only after Matt confirms. An ambiguous response is not confirmation.
9. **Reuse within 30 days.** Same business audited within 30 days → reuse that result and say so. Matt can override with an explicit "run it anyway."

## Fixed context

- Basecamp account: always `-a 6191443` (Safaii Studio), passed explicitly — never rely on the CLI default. This skill only ever runs against the Safaii account.
- Client and project are resolved from Basecamp, never a local file: match the project by name via `basecamp -a 6191443 projects list --json`. Resolve `project_id` and `seo_folder_id` exactly as `seo-project-setup` does — do not invent a second folder walk.
- Inputs: the business name and coordinate come from Matt or the context doc's business overview; the storefront coordinate must be confirmed (a check from the wrong place is worse than no check). The 1–3 customer keywords come from `SEO — Keyword Research`'s dated saved set when it exists (pick the local-intent terms, never brand); only ask Matt for seeds when that set doesn't exist — don't invent a parallel list.
- The doc lives in the client's **Docs & Files → Internal → SEO folder**, team-only, titled **`SEO — Local Audit`** — a stable contract, never recreated.
- **Basecamp 5 renders markdown** — write docs in markdown, GFM tables included.

## Workflow

### 1. Resolve the client and the business

Matt names a client and the business (name, or better a `cid`/`place_id`). Match the client to a project by name: `basecamp -a 6191443 projects list --json`. Ambiguous → show Matt the candidates and ask. **Never guess a project or domain.**

Read `SEO — Project Context` — what the business does and where it operates decides which keywords and radius matter. **Confirm the storefront coordinate:** take it from the context doc's business overview when present, or derive it from the listings row (step 2) when Context has no lat/long — only ask Matt if several pins look plausible. Confirm the coordinate before running the pack SERPs; the whole audit centers on it.

### 2. Find the business

`business_data_business_listings_search` with the business name as `title` (or its `cid`) and a wide radius around the coordinate. Yields the listing's `cid`, `place_id`, coordinate, category, rating, review count, claimed status, hours, and `people_also_search` (nearby competitors).

- **Several locations returned → it's a chain.** Build the profile snapshot table for the whole chain from this one call; then decide the deep-dives (step 6).
- **No match:** widen the radius, drop the category filter, try a variant of the name. If it's genuinely unclaimed/absent, that's a finding, not a failure — the one fix may be "claim/create the listing."

### 3. Run the local-pack position checks

For each of the 1–3 customer keywords, one `serp_organic_live_advanced` call near the coordinate. Record:
- The client's local-pack rank (or not present)
- The top 3–5 competitors' `cid` / `place_id` (collect them once, reuse everywhere)
- Whether the client appears in local_pack vs organic — never blur them

These are storefront checks, not a service-area grid. There is no rank grid in this skill — a 3×3 or 5×5 sweep would be a separate paid add-on, only after Matt explicitly asks for it (every cell is another SERP call).

### 4. Compare against the top competitors

For the top two competitors, pull their listings (via `business_listings_search` on their `cid`, or reuse the `people_also_search` rows which carry rating + review count). Compare, signal by signal:
- Primary category + additional categories
- Review count and average rating
- Claimed status
- Hours completeness
- Photo count
- Website link — **`webfetch` the listed URL** and confirm it deep-links to a location page, not a homepage or stale domain; "should deep-link" needs to be seen, not assumed

### 5. The review gap (browser deep-dive)

From the listing data (review count + rating distribution), note the review gap. Then use **`browser-control`** to open the business's Google Maps detail panel and extract what no API gives:

```js
// open the listing by place URL / cid from step 2
await page.goto("https://www.google.com/maps/place/...", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);
return await snapshot({ maxItems: 120 }); // then read visible review cards
```

**Read the visible review cards, About tab, and posts — never a hardcoded selector.** Google Maps DOM changes with UI tweaks; a frozen class name will die silently. Open the listing URL/cid, read what's on screen, and quote it with the Maps URL as the source. Do this per listing (client + strongest competitor):

- **Review recency** — "7 years ago" vs "last month" is a real gap that count alone hides
- **Review text** — what customers actually say (for the one fix and any reply strategy)
- **Owner replies** — whether the business responds (the About tab and review cards show this)
- **Q&A** — from the About tab; **posts** — via the "See local posts" button

The count/rating comparison from DataForSEO is real and citable; the browser adds recency, text, and reply presence. If `browser-control` isn't available or the page won't load, sit those parts out with a one-line note — never fabricate a review or a reply.

### 6. The one fix to do this week

Prioritize from the evidence. **Category and claim problems outrank posting cadence every time.** A missing/incorrect primary category is the highest-leverage fix; an unclaimed listing is critical. The one thing must be doable this week by a non-technical person, with copy-paste-ready mechanics.

### 7. Multi-location businesses

Always build the profile snapshot table for the whole chain — one call covers it. Deep-dives (position checks, reviews, profile details) are where cost scales:
- **5 locations or fewer:** deep-dive them all.
- **More than 5:** present the snapshot table, then ask Matt which 1–3 locations to deep-dive. Recommend a default — the weakest profile in the densest market.

**One doc vs many locations:** `SEO — Local Audit` suits a single storefront. For a chain, keep the **one snapshot table** and deep-dive 1–3 sites (what the workflow already does) — and **never replace the snapshot rows for locations you didn't re-audit**. If Matt wants per-location history (April's Austin pass vs March's Dallas), that's `SEO — Local Audit — <city-or-cid>`, a separate decision — not v1.

### 8. Confirm the audit with Matt

Present before writing:

- **Profile snapshot** (category, rating, reviews, claimed) — one row per location for chains
- **Where visibility drops off** (per the position checks)
- **The one fix to do this week**
- The signal-by-signal comparison

| Signal | This business | Best competitor | Gap | Action |
| --- | --- | --- | --- | --- |

Cover: categories, reviews (count, rating, recency, text, owner replies — browser-sourced where DataForSEO can't), hours and profile completeness, listing website links, local-pack coverage, claimed status, Q&A and posting hygiene.

**Do not write until Matt confirms.** Revise in place if he changes it. After confirmation, **offer** to merge the local competitors (that have a website) into `SEO — Project Context`'s `## Competitors` — ask, don't silently edit; the context doc is setup-owned.

### 9. Write the doc and log

Write `SEO — Local Audit` (markdown), following the **frozen heading contract** — these headings and columns are exact, never renamed.

```markdown
## Run
Date:
Business:
Coordinate:
## Profile snapshot
| Location | Category | Rating | Reviews | Claimed | Hours | Photos | Website |
## Local-pack position
| Keyword | Rank | Competitors |
## Review & engagement
| Signal | This business | Best competitor | Gap | Action |
## Signal comparison
| Signal | This business | Best competitor | Gap | Action |
## One fix this week
## Data gaps
## Research log
| Date | Summary |
```

- **`## Signal comparison` is the contract** — one row per signal (categories, reviews, hours, photos, claimed, website, coverage).
- **`## Review & engagement`** — the browser-sourced rows: review recency, text, owner replies, Q&A, posts. If the browser wasn't available, that's a `## Data gaps` line, not a blank table.
- **`## Data gaps`** — list what wasn't measured (browser unavailable, page wouldn't load) so nobody reads the missing rows as "no data."
- **Research log** — append an entry: what was audited, the date, the verdict (the gap, the one fix). Never replace prior log rows.

**The write loop (every write, every time):**

1. Find the doc by exact title in the SEO folder — never create a second copy.
2. Read the full markdown into memory.
3. Patch the snapshot and comparison; **replace** the signal comparison with the newly confirmed one; **append** a Research log row — leave prior rows and other sections untouched. **For a chain, never replace snapshot rows for locations you didn't re-audit** — only the deep-dived locations' rows get updated.
4. Upload the **entire** doc as an update of that same file id (`--vault <seo_folder_id>`).
5. Re-read and assert the other sections still exist, the title and vault are unchanged, and the content is non-empty.

First create only if the exact title is missing in the SEO folder. Create: `basecamp -a 6191443 files doc create "SEO — Local Audit" "<markdown>" --in <project_id> --vault <seo_folder_id> --json`. Every later write: `basecamp -a 6191443 files update <document_id> --content "<markdown>" --in <project_id> --vault <seo_folder_id> --json`.

**`files doc create` takes content as an argument, not stdin** — the `-` stdin form silently creates an empty doc. Verify content length after any write.

## Output format

When the run finishes, summarize in-session:

- Profile snapshot (category, rating, reviews, claimed)
- Where visibility drops off
- The one fix this week
- Data gaps (browser unavailable, or page wouldn't load — never a fabricated review)
- Spend note — "reused last 30 days" or "new spend: listings + N position checks"
- Recommended next action: `seo-audit` (broader site work), `keyword-research` (local keywords), or nothing (one-shot)

## Guardrails

- Match by `cid`/`place_id`; name matching collides with chains.
- local_pack ≠ organic — record which, never blur.
- A missing rank reads against the result count — sparse SERP is not invisibility.
- Do not infer local-pack strength from national organic metrics.
- Never recommend review gating, fake reviews, or keyword-stuffed names.
- **The agent never posts to the GBP** — like link-prospecting, this skill produces steps and drafts for Matt to execute; there is no "post the reply / publish the post" step.
- State the data gaps (browser unavailable, page wouldn't load) — never fabricate a review or a rank.
- Spend is capped: one business search, one competitor pull, 1–3 position checks — then ask.
- Confirm before write; nothing posts without Matt's explicit yes.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Doc landed in the wrong project | Guessed a project instead of matching by name | Project id comes from `projects list --json` matching the client's name, nowhere else |
| 404 / wrong account | Relied on the CLI default account | Always pass `-a 6191443` (Safaii Studio) explicitly |
| Compared the wrong business | Matched by name instead of `cid` | Once a `cid` is known, reuse it; name matching collides with chains |
| Storefront coordinate not confirmed | Assumed the coordinate | Confirm the storefront coordinate before any pack SERP; a check from the wrong place is worse than no check |
| Review text / owner replies reported without the browser | Pretended the API gave them | Review text, recency, replies come from `browser-control` on the live detail panel — if it wasn't run, that's a Data gaps line, not a filled row |
| Pack absence read as invisibility | Treated a missing rank as proof | Absence at the storefront means outranked or a sparse SERP — read against the result count, never "they don't show up anywhere" |
| Reviewed keywords are the brand name | Used the wrong query | 1–3 keywords customers actually search, never the brand |
| Invented a parallel keyword list | Ignored a dated saved set | When `SEO — Keyword Research` has a dated saved set, pick the 1–3 local-intent terms from it — never invent a separate list |
| Blurred local_pack with organic | Forgot the placement rule | Record which placement it is, never merge them |
| Recommended review gating | Suggested gaming the reviews | Never; the review gap is earned, not manufactured |
| Doc written without confirmation | Skipped step 8 | Present the audit; only a confirmed yes gets written |
| Duplicate doc over time | Doc title recreated | Find by title first; update, never recreate. Titles are a stable contract |
| Doc created without `--vault` | `--vault` dropped on create, landed at root | Move or delete the root copy; never write the audit onto it |