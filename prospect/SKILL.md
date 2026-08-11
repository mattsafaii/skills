---
name: prospect
description: Research a Safaii Studio prospect end to end before a meeting — their business, their competitors, their industry, what their customers actually say — and turn it into a strategy brief with prioritized opportunities and a meeting kit, published as a living "Prospect (internal) — [Company]" doc in Basecamp (Sales project, Deals vault). Steered by Matt's own notes from talking to them, and folds in tribunal/teardown findings when they exist. Use whenever Matt says "research [company]", "prospect research on X", "/prospect", "I'm meeting with X, what should I know", "dig into [company] before the call", or has a second conversation coming up with someone whose business he wants to understand. This is the internal pre-meeting brief — NEVER sent to the prospect. The client-facing site critique is the teardown skill; a generic audit for existing clients is audit-website.
---

# Prospect Skill

Matt meets someone, they talk about their business, they agree to talk again. This skill is what happens in between: real due diligence so he walks into the second conversation understanding their business, their market, and their customers well enough to have a point of view.

The goal is not a pile of facts — the prospect already knows their own revenue. The goal is three things they'd be surprised he knows:

1. **Industry fluency** — how customers in *their category* actually find and choose, what the economics are, what's shifting. Business owners rarely meet a web person who understands their industry.
2. **Competitor specifics** — grounded and dated, not "your competitors are ahead."
3. **A point of view** — a prioritized read on what to do, not a list of questions.

## This document is internal

It contains red flags, a pursue-or-pass verdict, and blunt language about the prospect's business. It lives in the same per-prospect folder as the teardown, which **is** sent to prospects. That co-location is convenient and dangerous, so:

- Title it **`Prospect (internal) — <Company>`**, never just "Prospect — ".
- The document's **first line**, above everything, is:
  `**INTERNAL — Matt's eyes only. Never send. The client-facing document is the Teardown.**`

Write it for Matt — blunt, specific, no client-safe hedging. That bluntness is exactly why it must never leave.

## Fixed IDs

Do not ask Matt for these:

- Account: `6191443` (Safaii Studio)
- Sales project: `46876803`
- Deals vault (root folder for per-prospect folders): `9792703029`
- Pipeline card table: `9782662056`
- Pricing Reference doc: `9792705685`

Durable artifacts go in `~/.local/share/prospect/<slug>/`, matching teardown's convention. Cached industry profiles go in `~/.local/share/prospect/industries/<industry-slug>.md`. Never delete either.

## The one hard rule

**Cite it or mark it Unknown.** Every factual claim carries a source URL. Anything unverified is written as `Unknown` — never inferred, never estimated, never filled in with a plausible number.

Matt walks into a room with these people. A fabricated headcount, a wrong owner's name, or an invented revenue figure costs him the deal. `Unknown` is a perfectly good answer and costs nothing. A confident guess is the only unrecoverable failure this skill has.

**This rule must be repeated verbatim inside every subagent prompt.** Subagents never read this file. A lane agent without it returns a plausible founding year, the main session folds it in having never seen a source, and the rule fails at exactly the point fabrication is most likely.

## Data sources

Follow tribunal's convention: **a source with no key configured sits out silently.** Never block a run on a missing key, never ask Matt to go sign up mid-run. Note in the doc header which sources were unavailable, the same as a skipped lane.

**Always available — no key, no account:**

**Wayback CDX** makes positioning drift exact instead of eyeballed. Get the snapshot timeline:

```bash
curl -s "http://web.archive.org/cdx/search/cdx?url=<domain>&output=json\
&fl=timestamp,original,statuscode,digest&collapse=timestamp:6&limit=60"
```

`collapse=timestamp:6` gives roughly monthly granularity (`:4` yearly, `:8` daily). **The `digest` field is a content hash — consecutive snapshots sharing a digest are re-crawls of an unchanged page, so a digest change is a real edit.** Use it to find the handful of dates the site actually changed, then read those specific snapshots:

```bash
curl -sL "http://web.archive.org/web/<timestamp>/<url>"
```

Two things worth pulling: how long they've been online at all (a 2006 first capture says something different than a 2023 one), and what the homepage promised then versus now. Dropped claims are among the best openers in the brief.

**Optional — free tiers, but each needs a signup and a key.** Use if the environment variable is set, skip if not:

| Source | Env var | Gives | Free tier |
|---|---|---|---|
| TheirStack | `THEIRSTACK_API_KEY` | Job postings — hiring signals, headcount trajectory | 200/mo |
| People Data Labs | `PDL_API_KEY` | Company enrichment — headcount, industry | 100/mo |
| Wappalyzer | `WAPPALYZER_API_KEY` | Tech stack | 50/mo |
| DataForSEO (MCP) | DataForSEO MCP tools present | Real geo-located SERP (rank, local pack, related searches), backlinks, keyword volume | $50 deposit, no subscription |

**If DataForSEO is configured, run step 4b — it replaces the browser search-visibility step** and the observation-only caveat lifts: real geo-located SERP data is a measurement, so rank can be stated as fact with its date and location. Without it, the browser rule in step 5 stands and step 4b is skipped silently.

**Permanently browser-only.** Don't look for an API; none is available to a solo operator: G2, Capterra, TrustRadius (tokens tie to paid vendor plans), and Crunchbase, PitchBook, Harmonic (quote-gated enterprise sales). Meta's Ad Library API excludes US commercial ads, so that's the web UI too.

## Scope

Default is the full run. If Matt says "quick," or the meeting is inside 24 hours, run **short**: recon, Lane A and Lane B, the prospect's own reviews without the competitor comparison, then synthesis. Skip Lane C — a cached industry profile covers most of it.

**Never silently trim.** Skipped lanes are named in the published doc's header, not just in chat. The doc is what Matt opens three days later; a caveat that only existed in the terminal has already scrolled away.

## Workflow

### 1. Intake

**Check what already exists before asking Matt anything.** He may not remember, and the skill can look it up:

```bash
basecamp -a 6191443 cards list --card-table 9782662056 -p 46876803 --md
basecamp -a 6191443 docs list --folder 9792703029 -p 46876803 --md
ls ~/.local/share/tribunal/history/ 2>/dev/null
```

That covers the Pipeline card, whether a prospect folder and prior brief already exist (so a re-run is caught **now**, not after Matt has approved a draft written as if new — step 9), and whether tribunal has scanned them before. Read a prior teardown or tribunal run rather than re-scanning.

Then read the card and its comments:

```bash
basecamp -a 6191443 cards show <card-id> -p 46876803 --md
basecamp -a 6191443 comments list <card-id> -p 46876803 --md
```

The template's fields map onto intake: **COMPANY** and **Website** give the target; **CONTACT** names the decision-maker; **PROJECT** is what they said they want; **NOTES** is the conversation record; **SOURCE**, **BUDGET**, **TIMELINE** calibrate how committed a point of view to bring. Cards are frequently thin — a name and a domain is normal.

**Floor check — stop here if BUDGET already fails it.** If the card states a real number under the **$3,000 project floor**, don't run Recon, the lanes, or the browser pass to find out what the card already told you. Tell Matt in one line — the number, that it's under floor, and that this is a pass unless he wants it run anyway. A vague or absent BUDGET isn't a fail; only gate on a stated number. Every other red flag (no decision maker, procurement, committee) needs research to confirm, so those stay in the fit read at step 6 — this check only fires on the one fact you already have before spending anything.

Confirm four things:

- **Company name** — required.
- **URL** — ask if missing. Never guess it from a company name. If they genuinely have no website, see the no-website branch in step 3.
- **Meeting date** — required, and it sets scope. Ask if not on the card.
- **Matt's notes** — from the card, or ask.

His notes **steer** the research; they are not a section appended at the end. "Referrals are drying up" points the demand and competitor lanes straight at that. "The owner's son built the site" changes what Matt can safely recommend.

**If he has no notes, prompt for recall before giving up.** "Paste your notes" gets a shrug; specific questions get answers:

- What did they say they actually do?
- Did they complain about anything, even in passing?
- Why were you two talking at all — who brought up work?
- Who else was in the room, or did they mention anyone?
- Did they say what they want, or was it vague?

Fragments are worth a lot. One line — "he said summer's dead" — redirects an entire lane.

### 2. Two modes: cold and warm

If there's genuinely nothing, run **cold**. Everything external still works; what changes is what the synthesis is *for*:

| | **Warm** (notes in hand) | **Cold** (no notes) |
|---|---|---|
| Brief is | A strategy brief | A discovery brief |
| Helps Matt | Make the right recommendation | Ask the right questions |
| Section 11 becomes | **Opportunities** — prioritized, committed | **Hypotheses** — ranked guesses, each with the question that confirms or kills it |
| Fit read gives | An offering match and a range | Plausible offerings and a ceiling — **no range, no figure** |
| Main risk | Anchoring on what he was told | Inventing what they care about |

Cold is not a degraded run. For a first real conversation it's arguably the correct shape — five sharp questions with research behind them beat five confident recommendations aimed at a problem nobody confirmed.

**Cold-mode discipline:** never write a guess as a finding. "Reviews mention turnaround six times in a year and competitors don't get this complaint, so speed may be a live problem" is useful. "They're struggling with turnaround" is a fabrication. Same rule as people facts, applied to motives.

**Cold mode never produces a price range.** The whole point of Hypotheses is that the work isn't scoped. A number computed from that state is an anchor Matt may repeat out loud and then be stuck holding. Name the offerings that plausibly map and the ceiling their signals support; say the range comes after discovery.

Note the mode in the doc header. On re-run, notes arriving flips it warm — hypotheses get confirmed, killed, or promoted, and the doc says which.

### 3. Recon — establish the map before fanning out

Do this in the main session. Everything downstream depends on it.

Read their site (`WebFetch` — homepage, about, services, team, careers). Establish:

- What they actually sell, and to whom
- **Their industry** — specific. "Independent HVAC contractor, residential retrofit," not "home services."
- **Their business type** — the routing table below. This decides what the rest of the run looks at.
- **5–10 search terms a real customer would type** — in customers' words, not industry jargon.

**Then find competitors by actually searching.** Run 2–3 of those terms and take the competitor list from what comes back. Do **not** name competitors from reading the prospect's own website first — a pre-named list becomes an anchor that Lane B then goes looking for reasons to confirm. If the prospect's site names competitors, treat those as candidates to discard freely, and require Lane B to say which came from a search and which didn't.

#### Business type routes the whole run

**This is the most important judgment in the skill.** Prospects range from a walk-in restaurant to a Series B SaaS company to an enterprise with a procurement department. They do not share a demand model, a decision process, or a place where evidence lives. Google reviews are close to everything for the restaurant and close to meaningless for the SaaS company. Running the wrong playbook produces a brief that is confident, well-sourced, and useless.

Pick the closest type, or name two if they straddle:

| Type | How they win work | Who decides | Website's actual job |
|---|---|---|---|
| **Local consumer** — restaurant, dentist, salon, retail | Local search, maps, reviews, word of mouth | Owner | Get found, prove trust, convert to a visit |
| **Local B2B / trade** — printer, contractor, supplier | Referral, relationships, repeat accounts, bids | Owner or GM | Credibility proof — closes deals sales started, rarely opens them |
| **Ecommerce / DTC** | Organic, paid, marketplaces, retention | Founder or head of growth | The storefront — it *is* the business |
| **Professional services** — agency, law, accounting, consulting | Reputation, referral, published work | Partner or principal | Credibility and qualification, not conversion |
| **Startup / SaaS** | Product-led growth, content, community, integrations, paid | Founder, or head of marketing/growth once funded | Convert trials or demos; explain the product; carry positioning |
| **Enterprise / established** | Sales teams, channel, brand, incumbency | Committee, plus procurement | Credibility, lead capture, and a signal to partners and investors |

Many businesses are two at once — a printer doing both walk-in cards and commercial contract work, or a SaaS with a self-serve tier and an enterprise motion. **That split is often the single most useful finding**, because the site usually serves one well and neglects the other, and the owner usually wants the neglected half.

**Running a straddle.** Naming two types doesn't mean doubling the run — it means covering both evidence maps inside the same lanes and budgets, then making the gap between them the point.

- **Lanes and browser pass** — pull from both types' evidence maps (step 3 below, and the browser-lane weighting in step 5), but don't split time evenly by default. Weight toward whichever side gets less attention on the prospect's own site or in Matt's notes — that's usually the neglected half, and it's where the finding lives.
- **Word budgets don't grow.** Sections 4, 5, 8, and 9 (customer-finding, positioning, industry model, best-in-class) stay at their normal budget — cover both sides inside it, labeled by type, rather than writing two full sections.
- **State the split up front.** The header (step 8) and the At a glance section name both types, e.g. "Local B2B (contract print) / Ecommerce (storefront)," not just the primary one.
- **Opportunities and the fit read tag which side each item serves.** A recommendation that only makes sense for the neglected half should say so — Matt needs to know if he's pitching the whole business or just the half nobody's serving.

#### Where the evidence lives, by type

Do not go looking for Google reviews on a Series A company. Route the lanes to where this type of business actually leaves a trail:

- **Local consumer / local B2B** — Google Business Profile, Maps reviews, Yelp, local directories, trade associations, local press, bid boards
- **Ecommerce / DTC** — marketplace presence, Trustpilot and on-site product reviews, ad libraries, keyword and category rankings, retention and subscription signals
- **Professional services** — case studies and client lists, Clutch or equivalent directories, published writing, conference talks, awards, team pages
- **Startup / SaaS** — **funding history and stage**, headcount trajectory from job postings, G2 / Capterra / TrustRadius reviews, Product Hunt, Hacker News and Reddit threads, GitHub activity, changelog and blog cadence, docs quality, the pricing page, status page, integrations and marketplace listings
- **Enterprise / established** — annual reports and filings if public, press releases, analyst mentions, careers page scale, subsidiaries and acquisitions, partner and vendor listings, procurement portals

**Funding stage changes everything for a startup** and belongs in the At a glance section: pre-seed has no budget, Series A has budget and moves fast, Series C+ already has a marketing team and an agency and is harder to sell into. Get it from a funding database or announcement, cite it, and mark `Unknown` rather than inferring from headcount or office photos.

#### Customer voice — the source depends on the type

Reading what customers actually say is the highest-value research in this skill regardless of business type. What changes is where they say it:

- Local — Google and Yelp reviews
- Ecommerce — product reviews, Trustpilot, Reddit
- SaaS — G2, Capterra, TrustRadius, Reddit, Hacker News, and their own community or Discord
- Professional services and enterprise — case studies (what the client is quoted praising), win/loss commentary, analyst notes, employee reviews on Glassdoor as a weak proxy

Whatever the source, the extraction is the same: real pain points in customers' own words, **the vocabulary customers use** (which becomes their copy), and what competitors get complained about (the prospect's differentiation, free).

#### If they have no website, or barely one

Common for local businesses running on a GBP listing alone — and a major finding rather than a blocker. Skip the site read, Wayback, and who-built-it; recon comes from the listing, directories, and socials. The brief reframes: the opportunity is **existence**, not optimization.

The startup analogue is different and worth naming when you see it: a site that engineers clearly built as an afterthought — no positioning, feature lists instead of outcomes, a docs site better than the marketing site. That's not absence, it's neglect, and it's usually the easiest sale in the set because the gap between their product and their presentation is obvious to them already.

#### Cached industry profile

```bash
ls ~/.local/share/prospect/industries/
```

If one matches, read it — Lane C starts from it instead of zero. **Check dates before using anything.** Every line in a profile carries the date it was written and its source. Anything over 12 months old gets re-verified before it enters a brief, or goes in with its date visible. An undated cache of "what's changing in the industry" becomes a confident-wrong generator the moment Matt says it out loud.

### 4. Parallel lanes — search and fetch only, no browser

Launch as concurrent `general-purpose` subagents in one message. **No browser automation in these** — see step 5.

Use this prompt frame for every lane, filled in:

```
You are researching a prospect for a solo web/design studio's INTERNAL
pre-meeting brief. Not client-facing.

TARGET: <company> — <url>
INDUSTRY: <industry>
BUSINESS TYPE: <type> — weight your research accordingly
CUSTOMER SEARCH TERMS: <terms>
COMPETITORS (from live searches): <list>
WHAT MATT WAS TOLD: <notes, or "nothing — cold run">

YOUR LANE:
<lane bullets>

TOOLS: WebSearch and WebFetch only. Do NOT load or use any browser
automation tools — other lanes are running concurrently and share one
browser; driving it in parallel corrupts all of our results.

HARD RULE: every claim carries a source URL. Anything you cannot verify
goes in the Unknown list — never infer, estimate, or fill in a plausible
number. A confident guess is worse than a blank. This applies hardest to
people: names, titles, and tenure need a clickable source or they don't
go in.

RETURN — max 400 words, bullets only, no prose preamble:
- <claim> — <evidence: short quote or figure> — <source URL>

Then, required:
Unknown: <what you looked for and could not verify>

The Unknown list is not optional. Silence reads as "not found" when it
may mean "not looked for," and the main session cannot tell the
difference.
```

**Lane A — Company**
- Services, positioning, team, case studies, clients, pricing if public
- Entity age, officers, status — OpenCorporates or a plain-web registry result
- Wayback CDX — how long they've been online, and which dates the homepage actually changed. Use the digest technique in Data sources; positioning drift is one of the best openers in the brief.
- Job postings — what they hire for is what they invest in
- Press, local news, trade press, awards
- Who built the site: footer credit, stack, when last meaningfully touched
- **Who decides, and whether they already have a marketing person or agency** — this changes Matt's entire pitch and is easy to miss

Keep people research to decision-maker identity, role, and the agency check. Skip prior ventures, tenure trivia, and personal history — the meeting kit bars quoting that material anyway (step 6), so collecting it buys nothing and adds fabrication surface on the highest-risk category.

**Lane B — Competitors**
- The list from recon's live searches, plus any the searches surface that recon missed. Say which came from where.
- Per competitor: positioning, what they lead with, site quality, apparent size, how they differ
- What each does better than the prospect, specifically

**Lane C — Industry model**
- How customers in this category buy: impulse or researched, referral or search, price-shopped or trust-led, cycle length
- What a customer is worth — the figure that decides what marketing spend is rational. Ranges with sources, never invented.
- Seasonality; what's changing right now
- Trade associations, publications, where the industry talks to itself
- **Best-in-class reference set** — 2–3 top operators in this category *nationally*. What they do that the prospect doesn't. This is what Matt shows them.

### 4b. DataForSEO measurements — main session, alongside the lanes

**Only if the DataForSEO MCP tools are available.** It's API, not browser, so it runs in the main session **concurrently with the lane subagents** — no Chrome to collide over. Missing MCP? Skip this step silently; the browser observation rule in step 5 stands (and the doc header notes the skipped source, per Data sources).

Run these with the customer terms from recon:

- **SERP positions** — `serp_organic_live_advanced`, one call per customer term, `location_name` set to the prospect's market (city/region for local business types; country otherwise), `language_code: en`, `depth: 10`. **This is a measurement, not an observation** — real geo-locked rank data. Record, per term: where the prospect lands (rank_group / rank_absolute, and `organic` vs `local_pack` — a maps placement is a different game than a blue link), the full result list for the competitor lane, and which `related_searches` / `people_also_ask` items appear (customer vocabulary, direct from Google).
- **Backlink profiles** — `backlinks_summary` for the prospect and top 2–3 competitors. Compare `backlinks`, `referring_domains`, and `backlinks_spam_score`. A prospect with 12 referring domains against competitors with 200 is a concrete, citable gap — stronger than the browser's impression.
- **Keyword volume (optional)** — `kw_data_google_ads_search_volume` for the customer terms, to size the demand each term carries.

**The measurement rule changes what's citable.** From DataForSEO you can state an ordinal with its date and location: "as of `<date>`, rank 4 in Google LA results for 'ac repair'." That's the one place the skill allows it — the step 5 browser rule stays observation-only. Every DataForSEO claim carries the date and location the call used; the data is a snapshot, not a trend.

If a call fails or returns nothing, write the term into the `Unknown` list — don't leave the gap silent and don't hand-wave a rank.

Run **after** the parallel lanes and **alone**. Concurrent agents sharing one Chrome collide and produce garbage.

**Weight by business type** — use the evidence map in step 3. A commercial supplier with 11 Google reviews isn't failing and a Series B SaaS has no Maps listing worth opening; in both cases the time belongs somewhere else. Only run the local block below when the type calls for it.

Load Chrome tools in one `ToolSearch` call, then work the sources this type actually uses:

**Local consumer and local B2B**
- **Google Maps / Business Profile** — prospect and top 3 competitors. Category, completeness, hours, photos, posts.
- **Review velocity** — sort by newest, count reviews dated within the last 90 days, for each of the four businesses. That's the operational definition; use it. If the list won't load or won't sort, mark `Unknown` — never eyeball it. A dead profile and a growing one look identical on total count, which is why the 90-day number matters.
- **Review text** — sort by lowest rating first; complaints carry more information than praise.

**Startup / SaaS**
- **G2, Capterra, TrustRadius** — rating, review count, and the text. Same extraction as local reviews. These are **browser-only, permanently**: none has a self-serve API, tokens are tied to paid vendor plans, and G2 now owns Capterra. Don't look for a programmatic route; there isn't one.
- **Funding and headcount** — a funding database for stage and last round; job postings for what they're staffing and how fast.
- **Product surfaces** — pricing page, docs, changelog cadence, status page, Product Hunt launch, integrations or marketplace listings. A stale changelog and a fast-moving competitor's is a real finding.
- **Community** — Hacker News, Reddit, their own Discord or forum if public.

**Ecommerce, professional services, enterprise**
- Marketplace and Trustpilot presence; Clutch-style directories; case studies and client lists; press releases and analyst mentions; careers page scale. Follow the evidence map rather than defaulting to Maps.

**All types**
- **Search visibility** — run the customer terms and record what comes back. **Report as an observation, never a measurement**: "in a browser search from LA on `<date>`, the top results were X, Y, Z." Never state an ordinal about the prospect — no "you're fourth for emergency AC repair." Browser results aren't geo-locked, personalized, or stable, and they'll pull out a phone and see something different. That's the exact credibility loss the hard rule exists to prevent. *(If DataForSEO is configured, step 4b already replaced this — skip the browser search.)*
- **Ad presence** — Meta Ad Library (`facebook.com/ads/library`), plus whoever is buying the customer terms.
- **Socials** — alive or dead, cadence, engagement. Weight by where this type's buyers actually are.

Stay read-only. Never log in, never submit a form. This is a stranger's public presence, viewed as any customer would.

### 6. Synthesize

The lanes are input. This is the product. Matt's notes decide what matters; the research decides what's true.

- **Positioning read** — what they say they are, what they are, what the market rewards. Where those disagree is usually the opportunity.
- **Opportunities** (warm) or **Hypotheses** (cold) — 3–5, priority ordered by what moves money for *this* business, not what's easiest to sell. Warm: gap, fix, likely impact, rough effort. Cold: the guess, the evidence, and the question that settles it.
- **What not to propose** — what won't move the needle here, and why. A brand refresh for a company losing on review velocity wastes their money and Matt's credibility. Naming this separates a consultant from a vendor.
- **Fit read** — whether they're worth Matt's time, not just what they should do:
  - **Offering match and range.** Read the Pricing Reference live (`basecamp -a 6191443 docs show 9792705685 -p 46876803 --md`) — it moves; don't work from memory. Check against its hard gates: the **$3,000 project floor** (if they can't clear it that's a pass signal, not a discount conversation), the **mandatory 12-month Foundation plan** bundled into every build (so it's in any range quoted), the **plan-client capacity ceiling** (if Matt is near it, this prospect competes with existing clients — say so), and the **on-corner gate** for brand work, taste-driven versus commodity. Cold mode: no range, per step 2.
  - **Ability-to-pay signals** — already buying ads or paying an agency is strongest, because willingness to spend is proven rather than hoped for. Also hiring, expansion, recent investment. For a startup, **funding stage is the signal**: pre-seed rarely clears the floor, Series A has budget and decides fast, Series C+ usually has an in-house team and an incumbent agency.
  - **Red flags, weighted by type** — the ones that matter differ:
    - *Small business* — no clear decision maker, stated budget far under the floor, a family member built the site, a history of cycling through vendors
    - *Startup* — pre-revenue with no raise, a designer or marketer already on staff, a rebrand six months old, the founder wanting to direct pixel-level decisions
    - *Enterprise* — procurement, legal and security review, vendor onboarding, MSAs, net-60 terms, and a committee. Any one of these can cost more unpaid hours than the project earns. **A solo studio is often the wrong vendor for enterprise work, and saying so early is cheaper than discovering it in month three.**
  - **Capacity check** — a large client doesn't just have to be able to pay, it has to fit. One enterprise engagement can consume the capacity of several SMB projects. If it would, say so; that's a real reason to pass on money.
  - **Verdict in one line** — pursue and at what level, pursue but qualify hard on X, or politely pass.

  Flag any Pricing Reference deviation explicitly in one sentence, so it stays a conscious choice.
- **Meeting kit** — 6–8 questions only someone who did the work would ask; 3 facts to drop, with sources; what to lead with; likely objections and handling; **what not to say** (if the owner's son built the site, don't trash the site).

  **Pick facts that show he understands the industry, not that he researched the person.** "Your category lives on repeat accounts, so I looked at how your competitors keep them" lands as prepared. Quoting their filing date or someone's work history lands as a background check. Same research, opposite effect.
- **Walk-in card** — write this **last**, as a compression of everything above. It becomes section 1.

### 7. Audit, then show Matt the draft

**Before printing anything, reread the full compiled draft against the one hard rule.** Every declarative factual sentence needs an adjacent source URL or belongs in the Unknown list — this is the same rule stated at the top of this file and inside every lane prompt, checked one last time now that lane output has been folded into prose. A claim can lose its citation in synthesis even when the lane that found it cited it correctly.

Fix anything that fails — add the source back from the lane's Unknown-adjacent bullet, or convert the claim to `Unknown` — before Matt sees a word of it. Don't publish silently on a failed check.

Print the **walk-in card and the opportunities only**, and ask whether he wants the full text. Printing 3,000 words into the terminal isn't a review he can actually do. Revise in place if he wants changes.

### 8. Publish

Find or create the prospect's folder — shared with teardown, so check first:

```bash
basecamp -a 6191443 docs list --folder 9792703029 -p 46876803 --md
basecamp -a 6191443 docs folders create "<Company>" --vault 9792703029 -p 46876803
```

**Write Markdown.** The CLI converts it — headings, bold, lists, links, tables all render. Verified on create and update. (The bundled basecamp skill claims documents send content "as-is, use plain text or HTML" — that's stale for documents. Don't hand-write HTML on its say-so.)

Write to a file first, then pass by substitution — the brief is long and full of quoted review text and URLs, and inline strings break on escaping and argument length.

```bash
# write to ~/.local/share/prospect/<slug>/<timestamp>-brief.md first
basecamp -a 6191443 docs documents create "Prospect (internal) — <Company>" \
  "$(cat ~/.local/share/prospect/<slug>/<timestamp>-brief.md)" \
  --vault <company-folder-id> -p 46876803
```

That file is the durable local copy — keep it.

**Structure and word budgets.** The budgets are the point: Matt reads this on a phone walking in. Over budget means cut, not spill.

| # | Section | Budget |
|---|---|---|
| — | `**INTERNAL — Matt's eyes only. Never send.**` + header: mode, business type, meeting date, lanes skipped | — |
| 1 | **Walk-in card** — verdict, top 3 opportunities one line each, 3 facts, the questions, what not to say | **300 max** |
| 2 | At a glance — what they do, size, age, entity status, who decides | 120 |
| 3 | What Matt learned directly — his notes, dated per conversation | as needed |
| 4 | How customers find this category | 150 |
| 5 | Where they stand against it | 150 |
| 6 | Competitors — table plus specific gaps | 200 |
| 7 | What their customers actually say — pain points and vocabulary | 250 |
| 8 | Industry model | 200 |
| 9 | What good looks like | 150 |
| 10 | Positioning read | 150 |
| 11 | Opportunities *(cold: Hypotheses)* | 300 |
| 12 | Don't propose | 100 |
| 13 | Fit read | 200 |
| 14 | Meeting kit — the expanded version of the card | 300 |
| 15 | Open questions — unverified, and what only they can answer | 100 |
| 16 | Sources | list |

Sections 2–16 are backup. Section 1 is what gets read.

### 9. Re-runs — this is a living doc

Step 1 already established whether a brief exists. If it does, read it, then:

- Append new notes to section 3 with a date, keeping the old
- Re-run only the lanes the new notes touch
- Revise opportunities, fit read, and walk-in card against what he now knows
- Add `Updated <date> — <what changed>` to the header
- Update the same doc. The command is `docs update`, **not** `docs documents update`:

```bash
basecamp -a 6191443 docs update <doc-id> --type document \
  --title "Prospect (internal) — <Company>" \
  --content "$(cat ~/.local/share/prospect/<slug>/<timestamp>-brief.md)" \
  -p 46876803
```

**Always pass both `--title` and `--content`** — omitting the title wipes it to "Untitled." Content is a full replacement, not a patch.

Then update the cached industry profile, **dating every line and carrying its source**. The second prospect in a vertical should start deeper than the first; that's the part of this skill that compounds, and undated lines are what would rot it.

### 10. Link the Pipeline card

Plain text with a bare URL — Basecamp auto-links it, and comment Markdown handling is unverified. No `[text](url)` syntax.

```bash
basecamp -a 6191443 comment <card-id> "Prospect brief: <doc-app-url> — <one-line headline finding>"
```

**Never rewrite a card's description** even when thin, and **never move a card between columns.** Both are Matt's sales record and his judgment. If the research answered something the card is missing, say so in the report-back and let him decide.

If no card exists, tell Matt. Don't create one.

### 11. Report back

Doc URL, the single strongest finding, the top opportunity, and any skipped lanes. About four lines.

## Failure modes

If something fails in a way this table doesn't cover, show Matt the raw error and stop — don't improvise or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Wrong account / 404 on any basecamp command | Missing `-a 6191443` | Always pass it explicitly |
| Doc title wiped to "Untitled" | `docs update` without `--title` | Always pass both `--title` and `--content` |
| `docs documents update` unknown command | That form doesn't exist | `basecamp docs update <id> --type document` |
| Doc creation fails on escaping or argument length | Built a long string inline | Write to a file, pass `"$(cat …)"` |
| A subagent returned an unsourced fact | Lane prompt omitted the hard rule | The rule goes in every lane prompt verbatim — step 4 |
| A lane returned prose, or nothing about what it couldn't find | Prompt template not used | Use the frame in step 4; the `Unknown` list is required |
| Brief claims the prospect ranks Nth for a term | Treated browser results as rank tracking | Browser results stay observation-only with date and location. Only DataForSEO-measured positions (step 4b) can state an ordinal, and then only with the call's date and location |
| Review velocity stated without a method | Eyeballed instead of counting | Sort by newest, count the last 90 days, or `Unknown` |
| Competitor list is wrong | Named from the prospect's own site instead of live searches | Competitors come from running the customer terms — step 3 |
| Brief is 4,000 words | Ignored the budgets | The table in step 8 is a cap, not a suggestion. Over budget means cut |
| Matt can't find the verdict without scrolling | Walk-in card missing or written first | It's section 1 and written last, compressed from the finished brief |
| Brief judges a B2B, SaaS, or enterprise prospect on Google review count | Ran the local-consumer playbook on the wrong type | Set business type in recon and follow the evidence map — step 3 |
| Startup brief has no funding stage | Treated it as optional | Stage sets budget, speed, and who decides. Cite it or mark `Unknown` — never infer it from headcount or office photos |
| Enterprise prospect assessed on price alone | Fit read ignored procurement, legal review, and capacity | Those costs are the fit question for a solo studio, often more than the fee |
| Customer voice section empty for a SaaS or enterprise prospect | Looked for Google reviews and found none | Customer voice moves by type — G2/Capterra/Reddit for SaaS, case studies and analyst notes for enterprise |
| Cold-mode brief quotes a price | Fit read ran unconditionally | Cold mode gives offerings and a ceiling, never a range — step 2 |
| Cold-mode brief asserts what they want | Guesses written as findings | Motive and priority are labeled hypotheses with evidence |
| Meeting kit facts read like a background check | Chose person-facts over industry-facts | Prove you understand the category, not that you researched the human |
| Cached industry claim is stale | Profile line had no date | Every line dated and sourced; over 12 months gets re-verified |
| Doc published as "Prospect — " without the internal banner | Skipped the titling rule | `Prospect (internal) — <Company>`, banner as the first line |
| Short run presented as full | Trimmed silently | Skipped lanes go in the doc header, not just chat |
| Re-run created a second doc | Didn't check in step 1 | Step 1 lists the Deals vault before anything else |
| Card description overwritten or card moved | Treated the board as skill-writable | Comment only |
| Full pipeline ran on an obviously under-floor prospect | Floor check skipped at intake | Check BUDGET against the $3,000 floor before Recon — step 1 |
| Draft has an uncited factual claim | Synthesis dropped a citation the lane had | Reread the compiled draft against the hard rule before showing Matt anything — step 7 |
| Straddle prospect got a single-type brief, or a doubled-length one | Named two types but ran one playbook, or ran both at full budget | Cover both evidence maps inside normal budgets, weighted toward the neglected side — step 3 |
