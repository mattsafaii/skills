# Shape Skill Guide

Shape an idea into a complete pitch using Shape Up methodology, adapted for a solo developer working with AI agents. The output is a pitch that is rough, solved, and bounded — and doubles as a brief for Claude to build from.

---

## Shape Up adapted for solo dev + AI

Shape Up was written for small teams doing human-speed implementation. AI changes the economics:

| Shape Up original | Solo dev + AI adaptation |
|---|---|
| Small batch (1–2 weeks, team) | Small batch (2–3 focused days) |
| Big batch (6 weeks, team) | Big batch (1–2 weeks) |
| Betting table (leadership meeting) | Solo decision: does this earn a cycle? |
| Cooldown (2 weeks) | 1 day: review, cleanup, deploy |
| PRD (planning doc) | Agent brief: surfaces, no-gos, acceptance criteria |

**What doesn't change:** appetite as a forcing function, no permanent backlog, rough/solved/bounded, fixed time/variable scope, shaping as the hardest and most important part.

**What AI changes about shaping:** bad shaping used to produce slow wrong results. With AI it produces fast wrong results. The quality of the shape directly determines the quality of what Claude builds. Shaping is more critical, not less.

**The new primary rabbit hole:** AI adds features you didn't ask for. No-gos are now guardrails for the agent, not just planning discipline. Be explicit.

---

## What shaped work is

Three properties from Shape Up — all three required:

- **Rough** — solution elements are clear but details are left for the builder. No wireframes, no task lists, no pixel specs. Space for creative judgment. Claude fills in the details; the shape sets the direction.
- **Solved** — the main elements connect. The critical unknowns are resolved. Not just a problem statement — there's a real solution at macro level.
- **Bounded** — clear what's NOT included. Fixed appetite, explicit no-gos. Scope shrinks to fit time; time never expands to fit scope.

A pitch that isn't all three isn't shaped yet.

---

## Column contract

The card table columns mean specific things:

- **💡 Ideas** — raw captures, unvetted
- **Shaped** — pitch complete (rough, solved, bounded). Not yet committed. This is a decision queue, not a shelf — shaped ideas that aren't bet on go to Graveyard, not left to pile up here.
- **PRD** — bet placed, PRD written as an agent brief, ready to build
- **Up Next** — committed for the current or next cycle. Only things you've decided to actually build go here.
- **In Progress** — actively building
- **Shipped** — done. Clean break — new requests go back through shaping.
- **Graveyard** — explicitly killed

---

## Fixed IDs

Do not ask Matt for these:

- Account: `6191443` (Safaii Studio)
- Project: `46824335` (Lab)
- Card table: `9768185094` (Ideas)
- Shaped column: `9768185098`
- Ideas triage column: `9768185095`

---

## Workflow

### 1. Identify the idea

If Matt named a specific idea, find the card:

```bash
basecamp cards list --card-table 9768185094 --in 46824335 -a 6191443 --json
```

Match by title. If Matt didn't name one, show the list from the 💡 Ideas column and ask which to shape.

Then fetch the card:

```bash
basecamp cards show <card_id> --in 46824335 -a 6191443 --md
```

### 2. Work through the shaping conversation

Go through each element conversationally. Use the card's existing content as a starting point — don't ask about things already answered.

**Problem**

Shape Up says: the problem should be a specific story or scenario showing why the current situation falls short — not a category of pain. Push for the concrete case.

- What's the specific situation where this falls short?
- Who experiences it?
- Why haven't they been able to solve it already?

If the problem is fuzzy or too broad, narrow it to a specific pain point before proceeding. Vague problems produce vague pitches which produce wrong builds.

**Appetite**

Appetite is a time budget, not an estimate. The number comes first; the scope adjusts to fit.

**Appetite measures human attention, not agent speed.** The agent is always ready. The real constraint is Matt's review time and judgment — how much of his focus does this problem deserve?

Two sizes for solo dev + AI:
- **Small batch** — 2–3 focused days. Simple, well-understood problem.
- **Big batch** — 1–2 weeks. Meaningful product with multiple surfaces.

Ask: "Is this a small batch or big batch?" Help decide based on solution complexity. A two-sided platform with auth is never a small batch. If scope can't fit the appetite, cut scope — never extend time.

**Solution**

Keep it rough. Describe key elements — surfaces, flows, data model shape — without specifying UI details. Think breadboard level: what are the places, what affordances exist, how do they connect.

This pitch will become a brief for Claude to build from. That means: concrete enough for Claude to have a clear direction, abstract enough that Claude can make implementation decisions. Don't write a spec — write a map.

- What's the tech stack? (Rails+Kamal+SQLite, or 11ty+Cloudflare — confirm this)
- What are the core surfaces? (Public browse, owner dashboard, reviewer flow, etc.)
- How does the core use case work end to end? Walk through it.
- What does v1 actually ship?

Stop before it becomes a spec. If you're describing button labels or exact field names, you've gone too far.

**Rabbit holes**

Specific technical or design risks that could blow up the appetite. The shaper's job is to resolve these before handing off.

For AI-assisted builds, pay special attention to:
- Third-party dependencies that need a decision now (maps, auth, storage, payments)
- Data model decisions that are hard to change later
- Features where the "obvious" AI implementation would be wrong

For each rabbit hole: either resolve it in the pitch (make the call) or cut it to a no-go.

**No-gos**

Named features or capabilities explicitly out of scope for this appetite. Not "we'll keep it simple" — specific things that won't be built.

With AI, no-gos serve double duty: they prevent scope creep during planning AND prevent Claude from adding features during building. Be more explicit than feels necessary.

### 3. Check: rough, solved, bounded?

Before presenting the pitch:

- **Rough?** — No wireframes, no task lists, no pixel specs. If the solution reads like a design doc, strip it back.
- **Solved?** — The core use case works end to end. No "we'll figure it out" holes in the main flow.
- **Bounded?** — Appetite named. No-gos explicit. Scope can be cut if needed.

If any fail, keep shaping.

### 4. Present the full shaped pitch

The pitch should be readable by someone (or something) that wasn't in the conversation. It needs to stand alone as a build brief.

---

**[Idea Title] — Shaped Pitch**

**Problem:** [Specific scenario showing why the current situation falls short. 2–3 sentences.]

**Appetite:** [Small batch (2–3 days) or Big batch (1–2 weeks). One sentence on why.]

**Solution:**
[Tech stack. Core surfaces and how they connect. Walk the main use case at breadboard level. Not a spec — a map.]

**Rabbit holes (resolved):**
- [Specific risk + how it's been resolved or scoped away]

**No-gos:**
- [Named feature that won't be built]
- [Named feature that won't be built]

---

Ask: "Update the card and move it to Shaped?"

Wait for explicit approval before touching Basecamp.

### 5. Update the card

Format the pitch as HTML and update the card body:

```bash
basecamp cards update <card_id> --body "<HTML>" --in 46824335 -a 6191443 --json
```

Use this HTML structure:

```html
<h2>Problem</h2>
<p>[specific scenario]</p>

<h2>Appetite</h2>
<p>[small or big batch + reasoning]</p>

<h2>Solution</h2>
<p>[stack + overview sentence]</p>
<ul>
<li><strong>[Surface]:</strong> [breadboard-level description]</li>
</ul>

<h2>Rabbit holes (resolved)</h2>
<ul>
<li>[risk + resolution]</li>
</ul>

<h2>No-gos</h2>
<ul>
<li>[named feature out of scope]</li>
</ul>
```

### 6. Move to Shaped

```bash
basecamp cards move <card_id> --to 9768185098 --card-table 9768185094 --in 46824335 -a 6191443 --json
```

### 7. Pre-build research (optional)

Only when shaping surfaced a real **validation unknown** — demand uncertainty ("would anyone want this?"), an unfamiliar community whose pain you're guessing at, or a problem you can't confirm from your own experience — or when Matt explicitly wants to do user research / get a foot in a community. **Don't force it.** A well-understood itch you're scratching for yourself needs no research.

The job: questions to post on X/Reddit that (a) test the bet and (b) get you known in the community — *before* a build exists. What you learn loops back into the shape (problem, appetite, no-gos).

**First, name the community — and check you're a genuine member (Minimalist Entrepreneur).** Start with the community, not the idea. The strongest pre-build research happens where Matt is *already embedded* — knows the language, already contributes, has heard this exact problem complained about repeatedly. Before drafting questions, run the test:
- **Genuine member?** Contributing, not lurking. If he'd be parachuting in cold, *that is the finding* — either it's the wrong community, or he needs to become a real member first (over weeks, by being useful), not extract research from strangers. Don't fake membership; communities smell it.
- **Painful enough to pay?** Not every gripe is a business.
- **Reachable + right-sized?** He knows where they gather; the niche is big enough to matter, small enough to stand out.

**If he's not a member but genuinely wants in:** the move is *establish first*, not ask. Create **`[🌱 Establish]`** cards — contribution openings that earn standing (answer others, share genuinely useful work, show up consistently) — and hold the `[🔬 Research]` questions until he has standing. Two rules that make or break it:
- **Give, don't ask.** Standing is the byproduct of being useful, over weeks/months. Instrumental contribution (helping only to extract later) gets smelled and backfires worse than silence.
- **Seeds, not clay.** Unlike launch tweets, do NOT draft the posts. Surface the *openings* — which threads are worth answering, what gap he can genuinely fill, what of his real work would land — and he brings the substance. AI-drafted fake expertise gets found out fast in a community judging whether he belongs. Genuine or nothing; if he doesn't actually want to be there for years, it's the wrong community.

If the community itself is unclear, run the **`find-community`** skill first — it's built for exactly this question (and the broader "start from community" framing).

For each genuine unknown, create a **`[🔬 Research]`** card in the Distribution posting queue (NOT the Lab board — the queue is where all postable content lives):

```bash
basecamp card "[🔬 Research] <question topic> (<Idea>)" "<p>🔬 <strong>Idea:</strong> <a href=\"<lab card app_url>\"><Idea> — shaping</a></p><blockquote><draft question></blockquote><p><em>Draft clay — rewrite in your voice. You have zero standing at the idea stage: contribute to the community first, ask second.</em></p>" \
  --in 46824770 --card-table 10010006453 --column 10010006454 -a 6191443 --jq '.data.app_url'
```

- Fixed coordinates: Content project `46824770`, Distribution table `10010006453`, Triage column `10010006454`.
- Link target is the **Lab idea card's** `app_url` (no build project / plan doc exists yet) — the shaped pitch is the brief at this stage. If the idea reaches `/build`, the per-project plan doc takes over and these cards move to Done.
- **Discipline:** the membership test above IS the discipline — if Matt's a real member, asking is natural; if not, participate and be useful *first*. A drive-by "what do you all think of X?" from a stranger gets ignored. Most research posts shouldn't mention he's building anything.
- Rules of the road live in the **Distribution Playbook** (doc 10016763197).

### 8. Confirm

One line: card updated and moved to Shaped (and note any `[🔬 Research]` cards created). Offer to move on to the next idea or write the PRD.

---

## Shaping heuristics

- **Stack defaults:** Rails + SQLite + Kamal for anything with auth, user accounts, or dynamic data. 11ty + Cloudflare Pages for purely read-only/static sites.
- **Two-sided platforms** (owners + users) always need Rails and are always big batch.
- **Map views** need a provider decision up front: Mapbox (styleable, default for custom-designed products), Leaflet+OSM (free, more setup), or Google (hard to style).
- **Don't let a private admin tool scope the public site.** If only Matt uses it locally, it doesn't need to be a web app.
- **Kill criteria belong in appetite.** If the project only works with real-world data collection, name the threshold where you'd abandon it.
- **Appetite measures human attention, not agent speed.** "Lean MVP" isn't an appetite. Small batch or big batch is.
- **No-gos need to be explicit for AI.** Claude will add features that seem reasonable. Name what's out of scope so it can't.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 1 | Problem is a specific scenario | Names a concrete situation, not a pain category | Ask for the specific case |
| 2 | Appetite is a named batch size | "Small batch (2–3 days)" or "Big batch (1–2 weeks)" | Push for a number |
| 3 | Solution is rough | No wireframe-level detail, no task lists | Strip back |
| 4 | Solution is solved | Core use case works end to end | Keep shaping |
| 5 | Rabbit holes are concrete and resolved | Specific risk + a decision made | Resolve or cut to no-go |
| 6 | No-gos are named features | Not "we'll keep it simple" | Name them explicitly |
| 7 | Pitch stands alone | Readable as a build brief without the conversation | Rewrite until it does |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Shaping session never ends | Too many open questions unresolved | Push for a decision; unresolved = rabbit hole or no-go |
| Solution reads like a spec | Gone past rough into wireframe territory | Strip back to surfaces and flows |
| Appetite stays vague | Felt awkward to push | Always get a batch size — appetite is human attention, not agent speed |
| Problem is a category, not a scenario | Accepted the first framing | Ask "what specifically happens when this fails?" |
| AI builds adjacent features during build | No-gos weren't explicit enough | Add more no-gos; be more specific |
| Card body posts as raw HTML | Shell escaping issue | Use heredoc for body content |
| Card stays in Ideas column | Forgot to run move command | Always run move after update |
| Re-asking things already answered | Not reading existing card content | Always fetch and read the card before starting |
| Shaped column accumulates unpicked ideas | Treating Shaped as a shelf | Unselected shaped ideas go to Graveyard, not left in Shaped |

---

## Exemplars

- **Hookah Maps** — shaped May 2026. Big batch (1–2 weeks). Two-sided platform (owners + reviewers). Evolved from static 11ty guide to Rails app mid-session when user accounts entered scope. Mapbox for map. See card 9768317431 in Lab project.
