# Fathom API reference

Base URL: `https://api.usefathom.com/v1`. Headers: `Authorization: Bearer <token>`, `Accept: application/json`. Tokens generated at `app.usefathom.com/api`. Every request counts against the site's monthly pageview allowance.

**Tokens have scopes.** `GET /token` returns the current token's permissions — check it before any create/update/delete. The token at `op://Secrets/Fathom API Token/password` (`agent-automation`) has `abilities: ["*"]`, full access. A scoped-down token fails on `POST`/`DELETE` even though the request is otherwise correct.

## Create a site

`POST /sites`

```json
{
  "name": "Client Name",
  "sharing": "none",
  "timezone": "America/Los_Angeles"
}
```

`sharing` is `none` (default), `private` (needs `share_password`), or `public`. Returns the site object: `id`, `object`, `name`, `sharing`, `created_at`, `timezone`. The returned `id` is the `site_id`/`entity_id` used everywhere else.

## Create an event

`POST /sites/{site_id}/events`

```json
{
  "name": "quote request submitted",
  "currency": "dollar"
}
```

`name` up to 255 chars. `currency` is optional (default `dollar`); other values: `pound`, `euro`, `yuan`, `peso`, `shekel`, `yen`, `won`, `hryvnia`, `franc`, `rupee`, `integer`, `none`. Returns `id`, `object`, `name`, `currency`, `created_at`.

**Check for duplicates first** — `GET /sites/{site_id}/events`, match by `name`, skip creating any that already exist. Fathom won't reject a duplicate name; it'll just create a confusing second event with the same label.

## Create a milestone

`POST /sites/{site_id}/milestones`

```json
{
  "name": "Site launched",
  "milestone_date": "2026-07-29"
}
```

`name` up to **30 characters** — the API truncates or rejects longer names, so keep them short before sending. `milestone_date` is `YYYY-MM-DD`. Returns `201` with `id`, `object`, `name`, `milestone_date`, timestamps.

## Aggregations — the main read endpoint

`GET /aggregations`

| Param | Values | Notes |
|---|---|---|
| `entity` | `pageview`, `event` | What you're aggregating |
| `entity_id` | site ID | Required |
| `aggregates` | `visits,uniques,pageviews` or `conversions` (for events) | Comma-separated |
| `date_from` / `date_to` | `YYYY-MM-DD` | Inclusive range |
| `date_grouping` | `day`, `week`, `month` | Omit for a single total row |
| `field_grouping` | `pathname`, `referrer_hostname`, `country`, etc. | Breaks the total into rows |
| `sort_by` | e.g. `pageviews:desc` | Only meaningful with `field_grouping` or `date_grouping` |
| `limit` | integer | Caps rows when grouped |
| `filters` | JSON array, e.g. `[{"property":"pathname","operator":"is","value":"/pricing"}]` | Narrow to a specific page/referrer/etc. |
| `timezone` | IANA name, e.g. `America/Los_Angeles` | Defaults to the site's dashboard timezone if omitted — set explicitly when reconciling against a report generated elsewhere |

Event aggregation swaps `entity=event`. **`entity_id` here is the event's own ID, not the site ID** — passing the site ID 404s (`No query results for model App\Model\Goal`). Add `aggregates=conversions` (or `sum` for `_value` totals on events that carry a monetary value). One call per event — there's no `field_grouping` that breaks a site-wide event query out by event name, and `filters` doesn't accept an `event_id`/`event_name` property either (both error with "Invalid property").

## Other endpoints

| Endpoint | Method | Notes |
|---|---|---|
| `/account` | GET | Requires a `*` scope token |
| `/token` | GET | Introspect the current token's scopes |
| `/sites` | GET | List sites (paginated: `limit`, `starting_after`, `ending_before`) |
| `/sites/{site_id}` | GET/POST/DELETE | Read, update, or delete a site |
| `/sites/{site_id}/events/{event_id}` | GET/POST/DELETE | Manage one event |
| `/sites/{site_id}/milestones/{milestone_id}` | GET/POST/DELETE | Manage one milestone |
| `/current_visitors?site_id=...` | GET | Real-time count, optionally broken down by top pages/referrers |

`DELETE /sites/{id}/data` and `DELETE /sites/{id}/events/{id}/data` (wipe data while keeping the site/event) are deprecated — both return `410 Gone`.

## Pagination

List endpoints (`/sites`, `/sites/{id}/events`, `/sites/{id}/milestones`) use cursor pagination: `limit`, `starting_after`, `ending_before`. Follow the returned cursor rather than paging by offset.
