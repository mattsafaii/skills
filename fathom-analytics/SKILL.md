---
name: fathom-analytics
description: Analyze a site's codebase to figure out what's worth tracking, then create those events and milestones in Fathom Analytics via the API and wire the fathom.trackEvent() calls into the code. Also the general reference for installing the script, excluding traffic, debugging, and querying the API directly. Use when Matt says "set up Fathom tracking for this", "what should we track on this site", "instrument this site with Fathom", "add Fathom events", "/fathom-analytics" while working in a project repo — or for narrower asks like adding one event, excluding traffic, or pulling stats. For the monthly client report that already consumes Fathom data, see client-report — this skill sets tracking up, that skill reads it back.
---

# Fathom Analytics

How to instrument a site with Fathom Analytics (usefathom.com): figure out what's worth tracking, create it in Fathom, wire the code, and how to query/debug it afterward.

Fathom is the default analytics choice — no cookies, no consent banner required (GDPR/CCPA/ePrivacy/PECR compliant by not collecting PII or IP addresses). Reach for it before suggesting GA4 or anything cookie-based.

## Workflow: instrument a site

Run this when asked to set up or improve tracking on a repo. **Nothing gets created in the client's Fathom account or committed to their code until Matt approves the plan** — same review gate as every other skill that touches a client's live account.

### 1. Resolve the site

Layered, cheapest-first:
1. Grep the repo for an existing embed (`data-site="..."` in any HTML/template file). Already-live sites have this.
2. If none, check `~/.config/client-report/clients.json` for a `fathom_site_id` matching this project (by `url` or key).
3. If still nothing, ask Matt for the site ID, or offer to create one: `POST /sites` with `{"name": "..."}` — only do this on explicit go-ahead, it's a real object in the account.

State which path found it (or that none did) when you present the plan — don't silently guess.

### 2. Analyze the codebase for what's worth tracking

Read the templates/views/components for genuine decision points, not every clickable thing. The filter is **track for decisions, not data** — an event only earns a place if it answers a question Matt or the client would actually ask ("did the redesign lift signups," "which CTA converts"). Look for:

- Forms: contact, quote/estimate request, newsletter signup, booking
- High-intent CTAs: "buy," "book," "subscribe," "request a quote," "call now," "get a demo" — not every nav link or ghost button
- Checkout / payment completion (candidate for a monetary `_value`)
- File downloads (resource PDFs, spec sheets)
- Outbound links to booking tools (Calendly, SavvyCal, Cal.com) or a phone/`tel:` link on a service business site
- A 404 page, if the site has a distinct one

Skip: pageviews (Fathom already tracks these automatically), generic nav clicks, anything with no decision behind it.

**One event per distinct action, not per UI instance.** Three phone links in the header/footer/CTA are one `call now clicked` event with one delegated listener — not three. Fathom events carry **no custom properties**, only an optional monetary `_value` in cents — there's no way to tag one event with a location/source dimension, so the only way to distinguish "which phone link" would be forking the event name, which fragments the one number that actually answers a question. Only split by location if the locations genuinely answer *different* questions on their own (e.g. a sticky mobile CTA you specifically want to compare against the nav link) — say so explicitly when proposing that split, since it's the exception.

Name events lowercase, human-readable, no special characters or emoji — `"quote request submitted"`, `"pricing cta clicked"`, `"booking link clicked"`. Consistent tense across the set (past-tense completions read best in a dashboard list).

**If analysis turns up an unrelated bug** (a dead form handler, a broken CTA override, anything that undercuts what an event would actually measure) — surface it in the plan, don't silently fix it and don't silently ignore it. It's real signal for whoever reviews the plan, and fixing code that wasn't asked for is out of scope for this workflow.

### 3. Draft the plan and get approval

Show Matt a table: event name | trigger (file:location) | value in cents if monetary | one-line why. Include any milestone worth backfilling — typically just a launch date (ask if unknown, don't guess a date from `git log` without checking, since a repo's first commit isn't necessarily the go-live date). Milestone names are capped at **30 characters** by the API — keep them short (`"Site launched"`, `"Redesign shipped"`).

If the analysis surfaced an unrelated bug, list it separately from the tracking plan, clearly labeled as a finding rather than something included in scope.

Wait for explicit approval. Revise in place if Matt wants changes — don't create or edit anything on an ambiguous response.

### 4. Execute

On approval, in order:
1. Create the site first if step 1 didn't find one (`POST /sites`).
2. `GET /sites/{site_id}/events` and diff against the plan — **skip any event that already exists by name** rather than creating a duplicate. Create the rest with `POST /sites/{site_id}/events` (see [references/api-reference.md](references/api-reference.md) for the exact body).
3. Create approved milestones with `POST /sites/{site_id}/milestones`.
4. Wire the `trackEvent()` calls into the code — see [references/instrumentation.md](references/instrumentation.md) for the delegated-listener pattern. Prefer it over hand-writing a listener per event; it's less code to drift out of sync later, and it doesn't assume any particular framework.

### 5. Report back

List what was created (event/milestone name + Fathom's returned ID) and which files changed. Point at the dashboard's Events tab so Matt can see them land. If any event was skipped as a pre-existing duplicate, say so — don't let it look silently omitted.

---

## Reference: script setup

Every site gets one script tag, in `<head>`:

```html
<script src="https://cdn.usefathom.com/script.js" data-site="SITE_ID" defer></script>
```

`SITE_ID` comes from the Fathom dashboard → Settings → your site's row in "My sites" (click the Site ID to copy it). Source it from a template variable or env var, not a hardcoded literal.

**Client-side router / SPA-style navigation** (Turbo, Turbolinks, Next.js router, htmx boost, or anything else that swaps content without a full page load): Fathom's automatic pageview tracking fires at the wrong time and double-counts or mistimes. Disable auto-tracking and fire it manually on the router's own navigation event:

```html
<script src="https://cdn.usefathom.com/script.js" data-site="SITE_ID" data-auto="false" defer></script>
<script>
  document.addEventListener('<router-nav-event>', function () {
    if (window.fathom) window.fathom.trackPageview()
  })
</script>
```

Swap `<router-nav-event>` for whatever the site's router actually fires (`turbo:load`, `turbolinks:load`, a route-change hook, etc.). `data-auto="false"` is required — without it, the first pageview fires twice. A site with normal full-page navigation doesn't need any of this — the plain script tag already tracks correctly.

### Framework-specific setup

Fathom has first-party guides for essentially every platform — WordPress, Shopify, Webflow, Next.js, Astro, Gatsby, Remix, SvelteKit, Vue, React, Angular, Ghost, Squarespace, Wix, WooCommerce, GTM, and more — full list at `usefathom.com/docs/integrations`. Check there for the exact embed mechanics of whatever the site is actually built on rather than assuming the plain `<script>` tag drops in unmodified — a page builder, CMS, or component framework often needs its own injection point.

**Google Tag Manager** (script injected via GTM instead of directly): use a Custom HTML tag, not GTM's own script-tag type:

```html
<script>
  var script = document.createElement('script')
  script.id = 'fathom'
  script.dataset.site = 'SITE_ID'
  script.src = 'https://cdn.usefathom.com/script.js'
  script.defer = true
  document.getElementsByTagName('head')[0].appendChild(script)
</script>
```

## Reference: firing an event manually

For a one-off ask outside the full workflow — after the Fathom script has loaded:

```js
fathom.trackEvent('newsletter signup')
```

Monetary value (cents):

```js
fathom.trackEvent('purchase', { _value: 4900 }) // $49.00
```

Assign the event a currency afterward in Site settings → Events (Fathom doesn't infer it). `trackGoal()` is the deprecated predecessor to `trackEvent()` — never use it for anything new.

## Excluding traffic

Two different problems, two different mechanisms — don't conflate them:

**Site-wide firewall** (Settings → Sites → [site] → Firewall tab, takes ~10 min to propagate, ~60s for IP blocks): allowed domains, blocked pages (pathnames/wildcards), blocked IPs, blocked countries, blocked referrers. Blocked traffic doesn't consume the pageview allowance.

**Excluding your own visits** (so Matt's own browsing doesn't inflate a client's numbers) — run once in the browser console on the live site:

```js
fathom.blockTrackingForMe()
```

Persists in that browser's local storage indefinitely. Reverse with `fathom.enableTrackingForMe()`. Don't reach for IP blocking instead — IPs change, this doesn't.

## Querying the API directly

Base URL: `https://api.usefathom.com/v1`. Bearer token auth — generate a token at `app.usefathom.com/api`. **Every API call counts against the site's monthly pageview allowance** — don't poll in a loop.

Store the token at `~/.config/client-report/fathom-token` (shared with the client-report skill — one token, don't create a second file) unless the task is outside that context, in which case ask where Matt wants it kept.

```bash
TOKEN=$(cat ~/.config/client-report/fathom-token)

# Totals for a window
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=SITE_ID&aggregates=visits,uniques,pageviews&date_from=2026-07-01&date_to=2026-07-31"

# Top pages in that window
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.usefathom.com/v1/aggregations?entity=pageview&entity_id=SITE_ID&aggregates=pageviews&field_grouping=pathname&sort_by=pageviews:desc&limit=10&date_from=2026-07-01&date_to=2026-07-31"
```

Full endpoint + request/response schemas (create site, create event, create milestone, aggregations parameters): [references/api-reference.md](references/api-reference.md).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No data at all | Script missing on some pages, or wrong `data-site` | Diff the embed against every template/layout; verify Site ID matches dashboard exactly |
| Data only for the homepage | Canonical tag pointing everywhere at `/` | Check `<link rel="canonical">` on other pages, or set `data-canonical="false"` |
| SPA/Turbo site under-counts or double-counts | Router fires navigation events at the wrong time for Fathom's auto-tracking | `data-auto="false"` + manual `trackPageview()` on the framework's own navigation event |
| Numbers look right but Matt's own testing inflates them | Forgot to self-exclude | Run `fathom.blockTrackingForMe()` in console on that site |
| Script 404s or is blocked | Caching/minify/JS-combine plugin (WordPress: WP Rocket, SiteGround Optimizer) stripped or bundled it, or CSP blocks `cdn.usefathom.com` | Exclude the Fathom script from the plugin's optimization; add `cdn.usefathom.com` to CSP `script-src` |
| Firewall change didn't take | Propagation delay | Wait ~10 min (domains/pages/countries/referrers) or ~60s (IP blocks) before assuming it failed |
| Report/API numbers don't match dashboard | Comparing windows of different lengths, or timezone mismatch | Match window length exactly; pass explicit `timezone` param if the dashboard's site timezone isn't UTC |
| Created event never fires | Event exists in Fathom but no code calls `trackEvent()` with that exact name | Grep the codebase for the event name string; names must match exactly, case-sensitive |

## Privacy note (for client-facing copy)

Fathom collects no cookies, no IP addresses, and doesn't fingerprint or build cross-site profiles — it hashes a visitor signature that can't be reversed. That's why Safaii Studio sites don't need a cookie consent banner for analytics. Useful line for a privacy policy; don't overstate it into "fully anonymous" — say "doesn't track individuals or store PII."

## Related skills

- **client-report** — the monthly client report workflow that reads back what this skill sets up (Fathom aggregations + GSC data)
- **safaii-html** — event handler placement conventions (delegated listeners / behavior layers over inline `onclick`), behind the instrumentation patterns this skill wires in
- **build** — new sites get instrumented as part of the build, not as an afterthought
