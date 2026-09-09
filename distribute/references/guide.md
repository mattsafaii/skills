# Distribute Skill Guide

Generate distribution content for something Matt built. Output = cards in the **X Posts** queue (persistent channel) or Reddit strategy docs (one-and-done per project), sized to the project's stage, drafted to Matt's writing rules. The human-readable rulebook is the **Distribution Playbook** (Basecamp doc 10016763197, Content project) — this guide is the operating version of it.

The core idea: **don't force every project into the same mold.** Pick the content types that fit where the project actually is. A just-shipped visual app earns a teaser→reveal launch; an unbuilt idea earns research; a community Matt isn't in yet earns establishing contributions first.

**Channel rule (Matt's architecture, decided 2026-08):** X is the *persistent* channel → lives in the **X Posts** card table (queue, columns, due dates). Reddit is *one-and-done* per project → no card table; a single **“Reddit strategy — <Project>” doc** in that project's own Docs & Files holds the subreddit target, the 1–2 planned posts as draft clay, and the posted links. Don't create Reddit cards in the X Posts table.

---

## Fixed IDs (don't ask Matt)

- Account: `6191443` (Safaii Studio)
- Content project: `46824770`
- X Posts card table (was “Distribution”, renamed in UI): `10010006453`
- Essays & Videos card table (was “Content”, renamed in UI): `9768310845` — Matt-as-person long-form: `[Essay]` / `[Video]` cards, Ideas 9768310846 → Making → Editing → Published
- Triage column (new cards land here): `10010006454`
- Scheduled column (dated/to-post cards): `10224974602` — when a card gets a due date, move it here
- Scheduled→Done standard: posted cards carry `Post: https://x.com/mattsafaii/status/<id>` in the body, move to **Done**; Friday content-ideas run fetches metrics onto them.
- Distribution Playbook doc: `10016763197`
- Reddit strategy docs: one per project, in that project's own Docs & Files, titled **“Reddit strategy — <Project>”** (e.g. Garp 47666267, zeni 47171516, Since 47572591, Whack-A-Mullah 46823899, Decimate 47604827).

**Scheduling workflow:** once a card has a due date (it renders in the Content Calendar / schedule), move it to the **Scheduled** column so the board shows what's queued to post. `basecamp cards move <id> --to "Scheduled" --card-table 10010006453 --in 46824770`.

Per-project plan docs live in each project's **own** build Basecamp project (not the Content project). Get the link from the project's Docs, or from the `📋 Plan:` link on any existing card for that project.

---

## The two modes

Every project can be shared two ways — different jobs:

- **🚀 Launch** — product-first ("here's the thing, go use it"). Needs a shipped, usable product. Teaser → reveal.
- **🔎 Engagement / Research** — problem-first ("how do you deal with X?"). Needs no product; runs anytime, especially *before* launch. Validates demand, builds audience.

---

## Card types (prefixes)

One postable thing per card. Title = `[prefix] <topic> (<Project>)`.

| Prefix | What it is | Stage | Draft style |
|---|---|---|---|
| `[🌱 Establish]` | Contribution that earns standing in a community Matt is **not yet** a member of | Pre-everything | **Seeds only** |
| `[🔬 Research]` | Question that validates an idea still being **shaped** | Pre-build | Clay |
| `[🔎 Question]` | Engagement question for a **built** project | Anytime | Clay |
| `[📊 Poll]` | A poll | Anytime | Clay |
| `[👋 Teaser]` | Single pre-launch teaser | Launch | Clay |
| `[🧵 Thread]` | Launch/reveal thread (one post, multi-tweet) | Launch | Clay |
| `[💡 Insight]` | Build-in-public learning from doing the work | Anytime | Clay |

> **Reddit is not a card prefix anymore.** It's one-and-done per project → a **“Reddit strategy — <Project>” doc** in that project's Docs & Files (title + body clay + posted links). No `[💬 Reddit]` cards in the X Posts table.

`[🌱 Establish]` and `[🔬 Research]` are usually created by `/shape` (its step 7). `[💡 Insight]` is usually created by `/dev-log` (its step 6). This skill can create any of them, but its bread and butter is the **launch + engagement** types for a built project.

---

## Writing rules (hard)

- **Essays: seeds only.** Never draft essay prose — that's `develop-essay`'s job and Matt writes every published essay word. If an essay fits, capture it as an *angle* (seeds), not a draft.
- **Tweets / polls: draft clay.** Draft these as a starting point; Matt rewrites before posting. Mark every clay card: *"Draft clay — rewrite in your voice. NOT for posting as-is."* Reddit drafts go in the project's **Reddit strategy doc** as clay (title + body), not a card.
- **The "so what?" bar + story shape (hard).** Prefer **Pain → Realization → Build** leads — universal, everyday words, understandable by almost anyone. Technical detail is the second act, attached under its project's story, never the opening. A work log is NOT a post; if a mined learning has no reader payoff, fold it into a stronger post or cut it. Shape follows the Scheduled cards in the queue — that's the bar.
- **`[🌱 Establish]`: seeds only, never clay.** These earn standing in a community judging whether Matt belongs. AI-drafted fake expertise gets found out. Surface *openings to contribute* — which threads to answer, what genuine gap he can fill, what of his real work would land — Matt brings the substance.
- **Gut-check claims.** Drafts are mined from the repo. Flag any strong claim ("X is night and day") so Matt confirms he stands behind it before posting.

---

## Engagement discipline (bake into the cards)

- **Real questions, not stealth marketing.** If every "question" is a setup to plug the product, people smell it. Most engagement/research posts should **not** mention the product. Note this on the cards.
- One product-adjacent ask per project ("does this resonate?") is occasional, not a default — flag it as such.
- These need Matt's voice; a canned-sounding question dies.

---

## Channels

- **Active:** X (Safaii) + site essays. **Before drafting any X content (tweets/threads), read `references/x-algorithm.md`** — it maps how the For You feed ranks (reply/dwell/share/profile-click positives, the negatives that suppress slop) onto draft structure. It's subordinate to the writing rules: format guidance only, never a license for engagement-bait.
- **Voice: before drafting ANY X copy (tweets, threads, polls, teasers), read `references/voice.md`** — it's how Matt's posts sound (short, plain, lowercase-starting, understated, first-person-specific) so clay arrives in his voice and needs minimal rewrite. The slop gate in x-algorithm.md is the *why*; voice.md is the *how*.
- **Replies: see `references/reply-shortlist.md`** for build-in-public/webcraft accounts worth substantive replies under (fact/question/counter, never "great post!").
- **Reddit:** one-and-done per project → a **“Reddit strategy — <Project>” doc** in the project's Docs & Files. Name the specific subreddits in the doc (exact-audience subs beat broad reach). Promo-allergic — lead with value, engage before posting.
- **YouTube:** deferred. Do **not** propose video cards unless Matt says he's reopening video.

---

## Workflow

### 1. Identify the project and its stage

Ask (or infer from what Matt said) two things:

- **Which project?** A built one (Decimate, zeni, Garp, Since, Whack-A-Mullah, CalMirror, PrintNextDoor…), or an idea still being shaped.
- **What stage is it actually in?** This decides the content types:
  - **Not a member of the target community yet** → `[🌱 Establish]` (seeds). Hold everything else until standing exists.
  - **Idea still being shaped, not built** → `[🔬 Research]` + maybe `[📊 Poll]`. (This overlaps `/shape` step 7 — if shaping is active, prefer that.)
  - **Built but not launch-ready** (no deploy/notarized build, or pre-launch) → `[🔎 Question]` engagement now; `[👋 Teaser]`/`[🧵 Thread]` drafted but flagged as gated; Reddit strategy goes in the project doc, gated.
  - **Built and launchable** → full launch set + engagement.

Be honest about the stage. A project with no downloadable build can't run a "go get it" launch — say so and draft the gated pieces anyway, marked.

### 2. Read the brief

- **Built project:** read its **plan doc** (in its build project's Docs). It has positioning, channel mix, blockers/gates, raw-facts bank, essay angles. If no plan doc exists, offer to create one first (it's the brief everything links to) — or proceed and link the Playbook instead.
- **Unbuilt idea:** read the **Lab idea card** (the shaped pitch is the brief).
- **Facts:** if the brief is thin, read the repo (README, AGENTS.md) for concrete, accurate details. Wrong technical claims kill credibility — verify, don't guess.

### 3. Draft the cards

For each piece, match draft style to the type (table above). Every card body =

1. A `📋 Plan:` link to the project's plan doc (or `📋 Idea:` to the Lab card for pre-build, or `📋 Playbook:` to doc 10016763197 if neither exists).
2. The draft (clay) **or** the opening (seeds) — wrapped in `<blockquote>` for postable drafts.
3. The mark: clay → *"Draft clay — rewrite in your voice. NOT for posting as-is."*; seeds → *"Seeds — you write the post."*; plus any gut-check / gated / discipline note.

Keep threads as one card (the whole thread in numbered `<blockquote>`s). Reddit drafts as title + body in the project's Reddit strategy doc.

**Scheduled → Done standard:** once a card gets a due date, it renders in the Content Calendar; move it to the **Scheduled** column (`10224974602`). When posted, move to **Done** and append the **status URL + 48h metrics snapshot** (impressions/likes/replies) — this feeds `best-times.md` and content-ideas' what-lands learning. See `references/best-times.md` before making timing claims.

### 4. Confirm before posting to Basecamp

Show Matt the planned cards (titles + a one-line description each). Get explicit approval before creating them — he may cut, reorder, or rescope.

### 5. Create the cards

```bash
basecamp cards create -a 6191443 "[<prefix>] <topic> (<Project>)" "<HTML body>" \
  --in 46824770 --card-table 10010006453 --column 10010006454 --jq '.data.app_url'
```

- Land everything in **Triage** (`10010006454`) — the intake column. Matt moves cards from there.
- HTML body is sent as-is for cards (no Markdown conversion) — use real tags. **Use a heredoc** for the body to avoid shell-escaping pain (see Failure modes).
- One card per postable piece. Don't bundle.

### 6. Confirm

List the created card URLs grouped by type. Note which are postable now vs gated (and on what — a deploy, a notarized build, Phase 2, standing in a community). Point Matt at the lowest-friction next action.

---

## Heuristics

- **Size to the project, not a template.** Visual/fun projects (Decimate, Whack-A-Mullah) earn multi-day teaser→reveal. Niche dev tools (zeni, Garp) earn one sharp thread + the right subreddit, not a slow tease to no one.
- **Lead with the strongest artifact.** For a crowded category (another SSG), the *essay* ("why I built my own") beats a splashy launch — lead with the story.
- **Pre-ship projects are engagement-only.** No launch cards for something nobody can use yet. Engagement validates demand *before* the build finishes.
- **The in-product share loop beats your own posting.** If the thing has a built-in share (Whack-A-Mullah's score button), the campaign's job is to seed and amplify that, not to out-post it.
- **Don't over-produce.** A few strong pieces Matt will actually post beat 15 cards that become backlog. When unsure, fewer.

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---|---|---|
| Drafted essay prose | Forgot essays are seeds-only | Capture the angle, not the draft — that's `develop-essay`'s job |
| `[🌱 Establish]` card has a postable draft | Treated it as clay | Seeds only — give openings to contribute, Matt writes the post |
| Card reads as stealth marketing | Question is a veiled pitch | Make it a real question; usually drop the product mention entirely |
| Launch card with a dead CTA | Project isn't actually launchable | Check for a deploy/notarized build; mark the card gated |
| Wrong technical claim in a draft | Guessed instead of reading the repo | Read README/AGENTS.md; verify before drafting |
| Card body posts as raw HTML or breaks on quotes | Shell escaping | Use a heredoc for the body; HTML is sent as-is for cards |
| Proposed a video card | YouTube is deferred | Don't, unless Matt says he's reopening video |
| 15 cards nobody posts | Over-produced | Fewer, stronger pieces; size to the project |

---

## Related

- `/shape` step 7 — creates `[🌱 Establish]` + `[🔬 Research]` cards during shaping.
- `/dev-log` step 6 — creates `[💡 Insight]` cards from session learnings.
- `develop-essay` — owns essays end to end (this skill only captures essay *angles*).
- `find-community` (minimalist-entrepreneur plugin) — picking/validating the community for the `[🌱 Establish]` stage.
- Distribution Playbook (doc 10016763197) — the human-facing rulebook this guide operationalizes.
