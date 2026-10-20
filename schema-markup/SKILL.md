---
name: schema-markup
description: Emit JSON-LD schema markup into a client's 11ty site repo — the Build step that turns the mapped entities into structured data. Reads Project Context (org facts), Structure — Fields (objects → Product/Service), and Structure — Sitemap (page types → BreadcrumbList, WebSite); writes a shared src/_includes/partials/schema.html include emitted in the base layout's head, driven by page front-matter, covering Organization/LocalBusiness, WebSite, BreadcrumbList, Product, Service, and FAQPage only where a visible FAQ exists. Marks up only what is visible on the page; never invents ratings, reviews, prices, or availability; never edits Structure — Fields. Skips when schema is not in scope for the job. Use when Matt says "schema for [client]", "/schema-markup", "add structured data", "add JSON-LD", or after the templates render the catalog.
---

# Schema Markup

## Goal

Emit valid JSON-LD structured data into a client's site, matching what each page actually shows, so search engines can read the mapped entities.

This is a Build step: the markup lives in the repo, in the templates. Nothing goes to Basecamp. The types come from `Structure — Fields` (the objects) and `Structure — Sitemap` (the page types); the org facts come from `Project Context`. The markup describes the page; it never describes a page the site does not have.

## Tone

Direct, precise. Mark up only the truth on the page. When a required value is missing, flag it — do not fill it to make the markup valid.

## Gate

Schema is optional per job — the process says "schema for the objects you mapped, if you are doing that on this job." If Structure's technical choices / the entity map do **not** put schema in scope, say so and stop.

## Required reads, in order

1. **`Project Context`** — at the root of Internal. Read **Business** (legal name, domain, address, phone, email, social profiles) for the org node. **Missing → stop; tell Matt to run `project-setup`.**
2. **`Structure — Fields`** — in Working. The mapped objects decide which entity types apply (`Product`, `Service`). **Missing → stop; run `structure-map`.**
3. **`Structure — Sitemap`** — in Working. The page types decide `WebSite`, `BreadcrumbList`, and where `Product` / `Service` / `FAQPage` attach.
4. **The templates and the loaded catalog** — in the client's repo under `~/Code/` (`~/Code/<slug>/`), to read the real values each page shows.

## Where the markup goes (repo)

- **`src/_includes/partials/schema.html`** — one shared include, emitted in the base layout's `<head>`. It builds the JSON-LD from global data (`site.json`), page front-matter, and the loaded catalog.
- **Page front-matter** carries what the include cannot infer — the page's type, its breadcrumb trail, and any page-specific fields.
- Keep **one consistent shape** — a single `@graph` per page, or discrete blocks; pick one and use it everywhere.
- Org facts live in **one place** (from `Project Context` → `site.json`), referenced by `@id` — never duplicated across pages.

## The type set

Emit only the types a page actually is:

- **`Organization`** — site-wide. Legal name, URL, logo, contact, `sameAs` social profiles.
- **`LocalBusiness`** — **only** when the client has a real public address and service area; include `address` (PostalAddress), `telephone`, `areaServed`, hours if recorded. If the address is missing, fall back to `Organization` and flag it — do not invent a location.
- **`WebSite`** — site-wide. Name, URL; a `SearchAction` `potentialAction` **only if the site has search**.
- **`BreadcrumbList`** — per page, from the path.
- **`Product`** — product pages. `name`, `sku` (the catalog number), `description`, `image`, `brand`. An `offers` block **only if the price is public** per Structure's catalog rules — never invent price, currency, or availability.
- **`Service`** — service pages. `name`, `description`, `areaServed`, `provider` (the org node).
- **`FAQPage`** — **only** where a visible FAQ exists on the page, with answers drawn from that visible copy. No FAQ section → no `FAQPage`.

## Rules

- **Visible only.** Mark up what a visitor can see on the page. Never mark up hidden content, and never describe something the page does not show.
- **Real values only.** Every value comes from `Project Context`, `Structure — Fields`, the loaded catalog, or the page's own copy. Never invent ratings, reviews, prices, availability, or a location.
- **Valid JSON-LD.** `@context` is `https://schema.org`; every block parses; required fields per type are present.
- **Reference, don't repeat.** Site-wide nodes (org, WebSite) are defined once and referenced by `@id`; page-level nodes point at them (`provider`, `publisher`).
- **Never edit `Structure — Fields`.** A missing field for a type is a finding for Matt, not a field to add here.

## What Schema Markup is not

- **Not `structure-map`.** It never changes the object/field contract; it reports what it needs.
- **Not page content or copy.** It describes existing visible content; it does not add an FAQ or a product to a page.
- **Not a rich-result guarantee.** It emits correct markup; whether a search engine shows a rich result is outside its control.
- **Not an invented entity.** No fake reviews, aggregate ratings, or offers.

## Checklist

1. **Gate.** Schema in scope for this job, or stop.
2. **Read in order.** Project Context (missing → `project-setup`); Structure — Fields (missing → `structure-map`); Structure — Sitemap; the templates and loaded catalog.
3. **Choose the type set.** Org type (`LocalBusiness` only with a real address), `WebSite`, `BreadcrumbList`, plus `Product` / `Service` / `FAQPage` per page type. Only what each page is.
4. **Map the values** from Project Context / Structure — Fields / the catalog / the page's visible copy.
5. **Write** `src/_includes/partials/schema.html` and the page front-matter / layout wiring.
6. **Validate.** Each emitted block parses; required fields per type are present; nothing describes invisible content.
7. **Report and recommend next.** Types emitted per page; any type missing required values (flagged, with the fallback taken). Next: `test-site`.

## Output format

Checklist with statuses:

| Step | Status | Notes | Next action |
| --- | --- | --- | --- |

Then summarize: gate result, types emitted and on which pages, missing-value findings and fallbacks, files written, and next step.

## Guardrails

- Mark up only visible content.
- Never invent ratings, reviews, prices, availability, or locations.
- Never edit `Structure — Fields`; flag missing fields.
- One source of truth for org facts, referenced by `@id`.
- One consistent graph shape across pages.
- No Basecamp doc — the markup lives in the repo.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Markup describes content the page hides | Invisible content marked up | Mark up only what is visible |
| Invented rating, review, or price | Filled a required field to make it valid | Use the real value or omit the block; flag the gap |
| `LocalBusiness` with no real address | Type chosen without an address | Fall back to `Organization`; flag it |
| `offers` on a gated-price product | Public/gated rule ignored | Omit `offers` unless the price is public |
| `FAQPage` on a page with no FAQ | Type added to look richer | Only mark up an FAQ that is visibly on the page |
| Org facts repeated per page and drifting | Defined inline instead of referenced | Define the org node once; reference it by `@id` |
| Invalid JSON-LD | Unescaped values or a stray block | Parse-check every block; `@context` = `https://schema.org` |
| `structure-map` edited here | Missing field "fixed" in the contract | Flag it to Matt; `structure-map` owns the field list |
