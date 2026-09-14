---
name: dataforseo
description: "How to use the DataForSEO MCP server (v3) — the api_request and docs tools, the endpoint catalog, the measurement rule, cost awareness, and geo-location handling. Load whenever external SEO data is needed: real SERP positions and rankings, keyword volume and difficulty, backlinks, on-page checks, competitor SEO. Used when Matt says \"check their rankings\", \"keyword research\", \"backlink profile\", \"search volume\", or asks for real search-engine data; also referenced by the prospect and teardown skills. Do not use for general questions that don't need external SEO data."
---

# DataForSEO

External SEO data via the DataForSEO MCP server (v3). The server exposes four tools instead of one per endpoint: discover an endpoint in the docs, then call it through `api_request`. The results are real measurements — and there is a hard rule about what they let you state as fact.

## Setup / availability

- Requires the `dataforseo` MCP server (v3, remote at `https://mcp.dataforseo.com/v3/mcp`). Auth is **OAuth**, set up once with `opencode mcp auth dataforseo` (opens the browser). opencode stores the token in `~/.local/share/opencode/mcp-auth.json` and refreshes it. Check with `opencode mcp list`; run `opencode mcp auth dataforseo` again if the tools go missing or calls return 401.
- `DATAFORSEO_BASIC_AUTH` (resolved from 1Password at shell start, see `~/.zshrc`) is **only** for direct REST calls — `seo-rank-tracking` hits `api.dataforseo.com` with it. The MCP uses OAuth, not this variable.
- **No `dataforseo_*` tools present? Say so and stop** — never fabricate or approximate SEO data from memory. Skip whatever step wanted it.
- Costs are pay-as-you-go against the account balance — no subscription.

## The four tools

- `dataforseo_api_request` — `{ method, path | url, data, noAiMode }`. Makes the authenticated call. `path` is the API path (`/v3/…`); `data` is the task array for POST endpoints.
- `dataforseo_docs_search` — `{ url }`. Returns an endpoint's request/response documentation. Call it when the body isn't in the catalog below.
- `dataforseo_docs_index` / `dataforseo_docs_list_sections` — browse the documentation when you need an endpoint that isn't listed here.

Call pattern:

```
dataforseo_docs_search({ url: "backlinks/summary/live" })         # confirm fields if unsure
dataforseo_api_request({ method: "POST",
                         path: "/v3/backlinks/summary/live",
                         data: [{ target: "example.com" }] })
```

`noAiMode` defaults to `false`, which returns a flattened, AI-optimized subset — results at the top level, some fields dropped. Set `noAiMode: true` for the standard nested schema (`tasks[].result[].items[]`) with every field present, when a call needs specific raw fields (for example `cid`/`place_id` on local listings). It inflates context, so use it only then.

## Rules that don't bend

1. **Measurement, not observation.** MCP calls are real geo-located measurements — the only place an ordinal about rank is allowed. Every claim carries the call's date and location: "as of `<date>`, rank 4 in Google LA results for 'ac repair'." A bare "you rank 4th" is never citable; neither is an un-dated "you don't rank."
2. **Every call charges money.** Think before calling. Prefer a few targeted calls over spraying: group up to 1,000 keywords into one keyword task, batch backlink lookups, and don't re-run the same query twice in a session. (Rough scale: SERP ≈ $0.002/query; keyword-volume tasks ≈ $0.09 each regardless of keyword count; backlink summaries ≈ $0.02.)
3. **Failed call → Unknown, never a guess.** A call that fails or returns nothing goes on the report's Unknown list or is skipped silently. Never hand-wave a rank or backlink count.
4. **A snapshot, not a trend.** One call = one point in time. Don't imply change over time without multiple dated calls.

## Endpoint catalog — question → call

All POST unless marked GET. The task shown is one element of the `data` array — wrap it: `data: [{ … }]`.

**Where does it rank?** (live, geo-locked)
- SERP organic — `POST /v3/serp/google/organic/live/advanced` — `{ keyword, location_name, language_code: "en", depth: 10 }`. Also returns `local_pack`, `related_searches`, `people_also_ask`. `depth` goes to 700; use 100 for rank tracking.
- Locations — `GET /v3/serp/google/locations` (free) — resolves location names to ids. No body.

**Keyword volume / metrics**
- Google Ads volume — `POST /v3/keywords_data/google_ads/search_volume/live` — `{ keywords: [...], location_name, language_code: "en" }` (one task holds up to 1,000 keywords).
- Ads locations — `GET /v3/keywords_data/google_ads/locations` (free).
- Labs keyword overview — `POST /v3/dataforseo_labs/google/keyword_overview/live` — `{ keywords: [...], location_name, language_code: "en" }` → volume, difficulty, CPC, intent.
- Labs bulk difficulty — `POST /v3/dataforseo_labs/google/bulk_keyword_difficulty/live` — `{ keywords: [...] }`.

**Keyword research / ideas**
- Related keywords — `POST /v3/dataforseo_labs/google/related_keywords/live` — `{ keyword, location_name, language_code: "en", depth: 1 }`.
- Keyword ideas — `POST /v3/dataforseo_labs/google/keyword_ideas/live` — `{ keywords: [...], location_name, language_code: "en" }`.
- Keyword suggestions — `POST /v3/dataforseo_labs/google/keyword_suggestions/live` — `{ keyword, location_name, language_code: "en" }`.
- Search intent — `POST /v3/dataforseo_labs/google/search_intent/live` — `{ keywords: [...], language_code: "en" }`.

**What does a domain/page rank for?**
- Ranked keywords — `POST /v3/dataforseo_labs/google/ranked_keywords/live` — `{ target, location_name, language_code: "en" }`.
- Keywords for site — `POST /v3/dataforseo_labs/google/keywords_for_site/live` — `{ target, location_name, language_code: "en" }`.
- Bulk traffic estimation — `POST /v3/dataforseo_labs/google/bulk_traffic_estimation/live` — `{ targets: [...] }`.
- Domain rank overview — `POST /v3/dataforseo_labs/google/domain_rank_overview/live` — `{ target, location_name, language_code: "en" }`.
- Historical keyword data — `POST /v3/dataforseo_labs/google/historical_keyword_data/live` — `{ keywords: [...], location_name, language_code: "en" }`.
- SERP competitors — `POST /v3/dataforseo_labs/google/serp_competitors/live` — `{ keywords: [...], location_name, language_code: "en" }`.

**Backlinks**
- Summary — `POST /v3/backlinks/summary/live` — `{ target }` → `backlinks`, `referring_domains`, `backlinks_spam_score`.
- Backlinks list — `POST /v3/backlinks/backlinks/live` — `{ target, limit: 100 }`.
- Referring domains — `POST /v3/backlinks/referring_domains/live` — `{ target, limit: 100 }`.
- Bulk spam score — `POST /v3/backlinks/bulk_spam_score/live` — `{ targets: [...] }`.
- Competitors — `POST /v3/backlinks/competitors/live` — `{ target, limit: 100 }`.
- Domain pages — `POST /v3/backlinks/domain_pages/live` — `{ target, limit: 100 }`.

**On-page**
- Instant pages — `POST /v3/on_page/instant_pages` — `{ url, enable_javascript: true }`.
- Content parsing — `POST /v3/on_page/content_parsing/live` — `{ url }`.
- Lighthouse — `POST /v3/on_page/lighthouse/live/json` — `{ url }`.

**Broader signals**
- Content analysis — `POST /v3/content_analysis/search/live` and `POST /v3/content_analysis/summary/live` — `{ keyword, location_name, language_code: "en" }`.
- Technologies — `POST /v3/domain_analytics/technologies/domain_technologies/live` — `{ target }`.
- WHOIS — `POST /v3/domain_analytics/whois/overview/live` — `{ limit: 10, filters: [["domain", "=", "example.com"]] }`.

**Business data**
- Business listings — `POST /v3/business_data/business_listings/search/live` — `{ categories: [...], location_coordinate: "lat,lng,km", limit: 10 }` (also `title`, `description`, `location_name`, `is_claimed`).

## Using the tools

- **Geo and language.** Set `location_name` to the real market — city/region for local businesses, country otherwise — and `language_code: "en"`. Use the locations endpoints to resolve a name to an id when a call needs one.
- **local_pack vs organic.** A Maps placement is a different game than a blue link — record which the result is, don't blur them into "a result."
- **Customer vocabulary.** `related_searches` and `people_also_ask` are the words Google itself associates with the query — direct evidence of how customers phrase it.
- **Spam score.** Higher `backlinks_spam_score` = weaker, more toxic link profile. The signal is comparative: a prospect with 12 referring domains and a high spam score against competitors with 200 and clean profiles is a concrete, citable gap.

## Where this is referenced

- `prospect` — step 4b (SERP positions, backlinks, keyword volume for a prospect)
- `teardown` — step 3c (online-presence read for a teardown doc)
- The SEO skills (`keyword-research`, `competitive-landscape`, `competitor-analysis`, `link-prospecting`, `local-seo`, `keyword-clustering`, `seo-audit`, `structure-redirects`) name the endpoint path to call; load this skill for the call pattern and the rules.
