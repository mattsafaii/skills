# Distribute Skill Guide

Generate distribution content for something Matt built. Output = prefixed cards in the **Distribution** posting queue, sized to the project's stage, drafted to Matt's writing rules. The human-readable rulebook is the **Distribution Playbook** (Basecamp doc 10016763197, Content project) — this guide is the operating version of it.

The core idea: **don't force every project into the same mold.** Pick the content types that fit where the project actually is. A just-shipped visual app earns a teaser→reveal launch; an unbuilt idea earns research; a community Matt isn't in yet earns establishing contributions first.

---

## Fixed IDs (don't ask Matt)

- Account: `6191443` (Safaii Studio)
- Content project: `46824770`
- Distribution card table: `10010006453`
- Triage column (new cards land here): `10010006454`
- Distribution Playbook doc: `10016763197`

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
| `[💬 Reddit]` | Reddit post draft (title + body) | Launch/engagement | Clay |
| `[💡 Insight]` | Build-in-public learning from doing the work | Anytime | Clay |

`[🌱 Establish]` and `[🔬 Research]` are usually created by `/shape` (its step 7). `[💡 Insight]` is usually created by `/dev-log` (its step 6). This skill can create any of them, but its bread and butter is the **launch + engagement** types for a built project.

---

## Writing rules (hard)

- **Essays: seeds only.** Never draft essay prose — that's `develop-essay`'s job and Matt writes every published essay word. If an essay fits, capture it as an *angle* (seeds), not a draft.
- **Tweets / Reddit / polls: draft clay.** Draft these as a starting point; Matt rewrites before posting. Mark every clay card: *"Draft clay — rewrite in your voice. NOT for posting as-is."*
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
- **Reddit:** per-project subreddit targeting (exact-audience subs beat broad reach). Promo-allergic — lead with value, engage before posting. Name the specific subreddits in the cards.
- **YouTube:** deferred. Do **not** propose video cards unless Matt says he's reopening video.

---

## Workflow

### 1. Identify the project and its stage

Ask (or infer from what Matt said) two things:

- **Which project?** A built one (Decimate, zeni, Garp, Since, Whack-A-Mullah, CalMirror, PrintNextDoor…), or an idea still being shaped.
- **What stage is it actually in?** This decides the content types:
  - **Not a member of the target community yet** → `[🌱 Establish]` (seeds). Hold everything else until standing exists.
  - **Idea still being shaped, not built** → `[🔬 Research]` + maybe `[📊 Poll]`. (This overlaps `/shape` step 7 — if shaping is active, prefer that.)
  - **Built but not launch-ready** (no deploy/notarized build, or pre-launch) → `[🔎 Question]` engagement now; `[👋 Teaser]`/`[🧵 Thread]`/`[💬 Reddit]` drafted but flagged as gated.
  - **Built and launchable** → full launch set + engagement.

Be honest about the stage. A project with no downloadable build can't run a "go get it" launch — say so and draft the gated pieces anyway, marked.

### 2. Read the brief

- **Built project:** read its **plan doc** (in its build project's Docs). It has positioning, channel mix, blockers/gates, raw-facts bank, essay angles. If no plan doc exists, offer to create one first (it's the brief everything links to) — or proceed and link the Playbook instead.
- **Unbuilt idea:** read the **Lab idea card** (the shaped pitch is the brief).
- **Facts:** if the brief is thin, read the repo (README, CLAUDE.md) for concrete, accurate details. Wrong technical claims kill credibility — verify, don't guess.

### 3. Draft the cards

For each piece, match draft style to the type (table above). Every card body =

1. A `📋 Plan:` link to the project's plan doc (or `📋 Idea:` to the Lab card for pre-build, or `📋 Playbook:` to doc 10016763197 if neither exists).
2. The draft (clay) **or** the opening (seeds) — wrapped in `<blockquote>` for postable drafts.
3. The mark: clay → *"Draft clay — rewrite in your voice. NOT for posting as-is."*; seeds → *"Seeds — you write the post."*; plus any gut-check / gated / discipline note.

Keep threads as one card (the whole thread in numbered `<blockquote>`s). Keep Reddit as title + body.

### 4. Confirm before posting to Basecamp

Show Matt the planned cards (titles + a one-line description each). Get explicit approval before creating them — he may cut, reorder, or rescope.

### 5. Create the cards

```bash
basecamp -a 6191443 card "[<prefix>] <topic> (<Project>)" "<HTML body>" \
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
| Wrong technical claim in a draft | Guessed instead of reading the repo | Read README/CLAUDE.md; verify before drafting |
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
