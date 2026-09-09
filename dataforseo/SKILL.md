---
name: dataforseo
description: How to use the DataForSEO MCP tools — the tool catalog, the measurement rule, cost awareness, and geo-location handling. Load whenever external SEO data is needed: real SERP positions and rankings, keyword volume and difficulty, backlinks, on-page checks, competitor SEO. Used when Matt says "check their rankings", "keyword research", "backlink profile", "search volume", or asks for real search-engine data; also referenced by the prospect and teardown skills. Do not use for general questions that don't need external SEO data.
---

# DataForSEO

External SEO data via the DataForSEO MCP server (89 tools). The MCP returns real measurements — and there is a hard rule about what those measurements let you state as fact.

## Setup / availability

- Requires the `dataforseo` MCP server to be connected. Auth is the `DATAFORSEO_BASIC_AUTH` token resolved from 1Password at shell startup (`~/.zshrc`): it prefers the interactive `op` session and falls back to the service-account token (`~/.config/op/sa.token`), so it stays available even when the CLI session is signed out/expired. If BOTH paths fail, `.zshrc` prints a visible warning at shell start ("could not resolve DATAFORSEO_BASIC_AUTH") — the var is empty, the MCP server won't connect, and the fix is `op signin --account safaiistudio.1password.com` or checking the service account token in 1Password admin. It's basic auth over the hosted MCP endpoint, so no local process.
- **No DataForSEO MCP tools present? Say so and stop** — never fabricate or approximate SEO data from memory. Skip whatever step wanted it.
- Costs are pay-as-you-go against the account balance — no subscription.

## Rules that don't bend

1. **Measurement, not observation.** MCP calls are real geo-located measurements — the only place an ordinal about rank is allowed. Every claim carries the call's date and location: "as of `<date>`, rank 4 in Google LA results for 'ac repair'." A bare "you rank 4th" is never citable; neither is an un-dated "you don't rank."
2. **Every call charges money.** Think before calling. Prefer a few targeted calls over spraying: group up to 1,000 keywords into one keyword task, batch backlink lookups, and don't re-run the same query twice in a session. (Rough scale: SERP ≈ $0.002/query; keyword-volume tasks ≈ $0.09 each regardless of keyword count; backlink summaries ≈ $0.02.)
3. **Failed call → Unknown, never a guess.** A call that fails or returns nothing goes on the report's Unknown list or is skipped silently. Never hand-wave a rank or backlink count.
4. **A snapshot, not a trend.** One call = one point in time. Don't imply change over time without multiple dated calls.

## Tool catalog — question → tool

**Where does it rank?** (real-time, geo-locked)
- `serp_organic_live_advanced` — organic results for a keyword; also returns `local_pack` placements, `related_searches`, `people_also_ask`
- `serp_locations` — resolve location names to ids

**Keyword volume / metrics**
- `kw_data_google_ads_search_volume` — search volume, CPC, competition (one task holds up to 1,000 keywords)
- `kw_data_google_ads_locations` — location ids
- `dataforseo_labs_google_keyword_overview` — volume, difficulty, CPC, intent per keyword
- `dataforseo_labs_bulk_keyword_difficulty` — difficulty scores in bulk

**Keyword research / ideas**
- `dataforseo_labs_google_related_keywords` — "searches related to"
- `dataforseo_labs_google_keyword_ideas` — ideas from a product/service category
- `dataforseo_labs_google_keyword_suggestions` — queries from a seed keyword
- `dataforseo_labs_search_intent` — intent behind keywords

**What does a domain/page rank for?**
- `dataforseo_labs_google_ranked_keywords` — keywords a domain or page ranks for
- `dataforseo_labs_google_keywords_for_site` — keywords relevant to a target domain
- `dataforseo_labs_bulk_traffic_estimation` — estimated monthly traffic
- `dataforseo_labs_google_domain_rank_overview` — domain rank and core metrics
- `dataforseo_labs_google_historical_keyword_data` — volume/CPC/competition over time

**Backlinks**
- `backlinks_summary` — overview: `backlinks`, `referring_domains`, `backlinks_spam_score`
- `backlinks_backlinks` — individual backlinks list
- `backlinks_referring_domains` — the referring domains
- `backlinks_bulk_spam_score` — spam scores in bulk
- `backlinks_competitors` / `backlinks_domain_pages` — competitive context

**On-page**
- `on_page_instant_pages` — single-page on-page audit (live)
- `on_page_content_parsing` — structured content extraction (links, anchors, headings, text)
- `on_page_lighthouse` — Lighthouse audit run on DataForSEO's infrastructure

**Broader signals**
- `content_analysis_search` / `content_analysis_summary` — where a brand/keyword is mentioned across the web
- `domain_analytics_technologies_domain_technologies` — tech stack
- `domain_analytics_whois_overview` — WHOIS / registration data

## Using the tools

- **Geo and language.** Set `location_name` to the real market — city/region for local businesses, country otherwise — and `language_code: en`. Use the `*_locations` tools to resolve a name to an id when a call needs one.
- **local_pack vs organic.** A Maps placement is a different game than a blue link — record which the result is, don't blur them into "a result."
- **Customer vocabulary.** `related_searches` and `people_also_ask` are the words Google itself associates with the query — direct evidence of how customers phrase it.
- **Spam score.** Higher `backlinks_spam_score` = weaker, more toxic link profile. The signal is comparative: a prospect with 12 referring domains and a high spam score against competitors with 200 and clean profiles is a concrete, citable gap.

## Where this is referenced

- `prospect` — step 4b (SERP positions, backlinks, keyword volume for a prospect)
- `teardown` — step 3c (online-presence read for a teardown doc)

Load this skill from either for the full catalog and rules.
