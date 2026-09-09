# Content Ideas Zonebrite Skill Guide

Sweep a time window of Zonebrite's Basecamp activity, distill **content ideas**, and create idea cards routed to the right content board with source links. This is the Zonebrite version of `/content-ideas` — same shape, but it mines Basecamp (not git repos), produces *content ideas* (not build-in-public insights), and carries a stronger confidentiality guardrail because the raw material is real customers' security work.

**What makes it good:** the cross-job patterns. One install is a job; the same customer question showing up across five jobs is a blog post, a GBP answer, or a resource. Hunt for the recurring thing.

This skill is governed by the **Content Playbook (Zonebrite)** (doc 10021739130) and subordinate to the **Brand Strategy** (anti-fear voice). Read those rules; this guide is the content-ideas procedure.

---

## Fixed IDs (don't ask Matt)

- **Zonebrite account:** `6060605`
- **Marketing project:** `46771824`
- Content boards (route ideas to the **Ideas** column of the matching board):
  - **GBP Posts** — table `9821916129`, Ideas column `9821916131`
  - **Website Content** (blog + resources) — table `10022351438`, Ideas column `10022351440`.
  - (No social board. Instagram is a passive job-photo habit Mike keeps, not an idea pipeline — don't route or create cards for it.)
- Reference docs (point at, don't duplicate): Content Playbook `10021739130`, Brand Strategy `10003942350`, Marketing Channel Stack `9989596907`, Copy Bank `10012817406`, Street-Level Sales `9996077012`.

---

## Routing — which board / format

The deciding question: **is the idea evergreen-and-deep, or timely-and-short?**

- **Evergreen, in-depth answer to a buyer question** → **Website Content** (ranks in search, compounds). `[✍️ Blog]` for an article; `[📋 Resource]` for a checklist/guide/downloadable.
- **Timely, short, conversion-focused** → **GBP Posts**. GBP posts are officially **Updates / Offers / Events** — short, with a CTA button, a visual, ~1–2×/week:
  - `[📰 Update]` — news, a quick tip, a recent job, OR a teaser linking to a published blog/resource
  - `[📣 Offer]` — a promo with start/end dates + CTA (+ optional coupon)
  - `[📅 Event]` — a dated happening (rare for ZB)
- **A recent-job / before-after** → a GBP `[🏠 Showcase]` Update (a flavor of Update). The Instagram photo is Mike's passive habit, not a tracked card — don't create one for it.

| Idea is… | Board (table) | Prefix |
|---|---|---|
| Evergreen article answering a buyer question | Website Content (10022351438) | `[✍️ Blog]` |
| Checklist / guide / downloadable | Website Content (10022351438) | `[📋 Resource]` |
| Timely news / quick tip / blog teaser | GBP Posts (9821916129) | `[📰 Update]` |
| Recent job / before-after | GBP Posts (9821916129) | `[🏠 Showcase]` |
| Promo with dates + CTA | GBP Posts (9821916129) | `[📣 Offer]` |
| Dated event | GBP Posts (9821916129) | `[📅 Event]` |

**The repurpose chain (don't make duplicate cards):** a strong topic is usually *one blog/resource* (the deep, canonical version) that then *spins off* a short GBP `[📰 Update]` teaser (and, if there's a relevant install, an IG photo — Mike's passive habit, not a card). Capture the topic **once** in its deepest format (usually Blog), and note the GBP-teaser repurpose **on that card** — do not create separate disconnected cards for the same topic. Only make a standalone GBP card when the idea is genuinely GBP-native (a recent job, an offer, a timely tip with no article behind it).

---

## Draft depth

- **GBP:** draft **clay** in the company voice — short, ready for Matt/Mike to refine. Mark: *"Draft clay — refine in the Zonebrite voice. Not final."*
- **Blog / resource:** capture **seeds** — the angle, who it's for, the buyer question it answers, and a rough outline / the checklist items. Don't write the whole article; these are substantial and SEO-considered, written by Matt/Mike. Mark: *"Seeds — angle + outline; write in the Zonebrite voice."*

---

## ⚠ Customer-security confidentiality (the hard guardrail — stronger than Safaii's)

The raw material is real customers' security installations. This rule overrides every content goal.

- Extract only the **generic, transferable** lesson — "a question we keep getting," "a placement mistake we see a lot." **Never** a specific client's name, address, business, system, camera positions, blind spots, or access points.
- A source link on a card may point at an internal client project **for your own tracking**, but the **content idea itself must already be anonymized and generic** — assume the card could be read by anyone.
- Never propose content that reveals how any real client's property is secured.
- When unsure, **drop it.** A missed idea costs nothing; a leaked customer security detail is unrecoverable and brand-ending.
- Surface any idea derived from a specific client job explicitly at confirmation so Matt can veto.

---

## Voice (from Brand Strategy)

Anti-fear, always — never exploit anxiety, imply imminent danger, or position the buyer as helpless. Sell uncertainty → confidence. "Peace of mind" is banned. Plain English, benefits over features, calm-craftsman. CTA (for `[📣 Offer]`) is "Schedule Your Free Site Survey." Pull phrasing from the Copy Bank.

---

## Workflow

### 1. Establish the window
Take the period from Matt (past week / month / since a date). Default: **past 2 weeks**. Convert to an absolute start date.

### 2. Sweep the sources (Basecamp only — no repos)
Verify flags with `basecamp <cmd> --agent --help` if unsure. Both Matt's and Mike's activity.

- **Chats / messages:** `basecamp chat messages` and `basecamp recordings messages -a 6060605` across projects — filter to the window. Customer questions and field notes live here.
- **Timeline (activity):** `basecamp timeline -a 6060605 --json` — the cross-project catch-all.
- **Client-job projects + Field Ops + Support:** the individual job projects, `Field Ops`, `Support` — what came up on real jobs (apply the confidentiality guardrail hard).
- **Zonebrite.com dev logs / Sales & Biz Dev:** site dev logs and sales activity for site-content and FAQ-shaped material.

### 3. Dedupe against existing cards
List what's already on the boards so you don't re-propose it:
```bash
basecamp cards list --card-table 9821916129 --in 46771824 -a 6060605 --jq '.data[].title'    # GBP
basecamp cards list --card-table 10022351438 --in 46771824 -a 6060605 --jq '.data[].title'   # Website Content
```
Skip anything substantially already captured.

### 4. Distill content ideas
Pull genuine, useful ideas: a recurring buyer question, a confusion worth a guide, a job lesson generalized, an FAQ that should be a resource, a seasonal/timely GBP angle. **High bar** — most activity isn't a content idea. A thin window yields few; say so. Prioritize the cross-job recurring patterns.

### 5. Draft + route the cards
For each idea: route by format (table above), draft to the right depth (clay vs seeds), tag with the prefix, and attach a `🔗 Source:` line (internal link or plain-text provenance — a citation, not necessarily a hyperlink; the same rules as `/content-ideas`'s source attribution). Keep public content anonymized regardless of the source.

### 6. Confirm before posting to Basecamp
Show Matt the list — title, one-line description, target board, source — grouped by board. **Call out any idea derived from a specific client job explicitly** for veto. Get approval, then create.

### 7. Create the cards
```bash
basecamp cards create -a 6060605 "[<prefix>] <title>" "<HTML body: idea + angle + draft/outline + 🔗 Source + confidentiality-safe note>" \
  --in 46771824 --card-table <board table id> --column <board Ideas column id> --jq '.data.app_url'
```
Land in each board's **Ideas** column. Use a heredoc for the body (shell escaping; HTML sent as-is for cards). One card per idea.

### 8. Confirm
List created cards grouped by board with sources. Note the strongest recurring theme of the window, if there is one.

---

## Scheduled / recurring use
On-demand by default. For a weekly cadence, set a `/schedule` reminder (a cloud routine can't reach Matt's local `basecamp` auth, and the confidentiality veto needs a human — so it nudges, it doesn't auto-run). Offer it once after a successful run; don't set it up unprompted. (Mirror of `/content-ideas`'s 🌾 weekly reminder.)

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---|---|---|
| Leaked a customer's security detail | Confidentiality filter too loose | Generic transferable only; never client setup; flag client-derived ideas at confirmation; when unsure drop |
| Fear-based angle | Ignored the anti-fear voice | Sell confidence, not anxiety; "peace of mind" banned; re-read Brand Strategy |
| Wrote a full blog post | Wrong draft depth | Blog/resource = seeds + outline, not finished prose; Matt/Mike write it |
| Wall of weak ideas | Treated every message as an idea | High bar; few strong ideas beat many filler cards |
| Routed everything to one board | Skipped format routing | Match idea → board by the routing table; tag the prefix |
| Re-proposed an existing card | Skipped dedupe | List board cards first (step 3) |
| Card body breaks on quotes | Shell escaping | Heredoc for the body |

---

## Related
- `/content-ideas` — the Safaii sibling (mines repos for build-in-public insights). This one mines Zonebrite's Basecamp for content ideas. Different account, sources, boards, guardrails — keep them separate.
- Content Playbook (Zonebrite) doc `10021739130` — the rulebook this skill serves.
- Brand Strategy doc `10003942350` — the voice this skill obeys.
