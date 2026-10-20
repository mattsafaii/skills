# @mattsafaii growth plan

The operating plan for growing Matt's X account as an indie hacker + web designer/developer. Skills and agents reload this when the plan needs context. Config work — not Basecamp-tracked.

## Position
Indie hacker + web designer/developer. Rails, vanilla CSS, plain text, cheap VPS, two businesses. Personality-forward craft voice (see `voice.md`). Profile reads as a working solo maker, not a content account.

## The core problem (diagnosis, 2026-08)
- The account farms impressions, not followers. Off-theme engagement-bait (politics, religion, Lakers, viral drops) spikes to 250–350k impressions but converts to ~zero followers (134 followers / 937 tweets). Scattered topics blur the feed's embedding, so Out-of-Network retrieval never places him in the indie/dev crowd.
- The real pipeline is already built and idle: X Posts queue (124 cards — build-in-public insights + launch threads) and Essays & Videos board (41 essays/videos), essentially none shipped. This is exactly the on-theme content that converts.

## Invariant rules
1. **Go focused.** ~90%+ craft/build-in-public content. No off-theme farming. A rare authentic sidestep (Lakers, Iran, music) is fine, but never as a reach play.
2. **~1 substantive post/day**, mostly from queues. Author-diversity decay means flooding hurts — fewer, stronger.
3. **Don't lead with external links while small** (trips spam scrutiny). Substance in the post; link in a reply or later.
4. **Reply well under bigger in-niche accounts** — the cleanest non-spammy OON path for a small account. Must add a fact/question/counter, never "great post!"
5. **Voice over algorithm.** If authenticity and optimization conflict, authenticity wins (slop gate rewards real voice anyway).

## Phases
- **Phase 0 — Storefront:** fix profile (name/bio/pinned) so a profile-click converts.
- **Phase 1 — Ship the queue (weeks 1–4, ~1/day):** post strongest `[💡 Insight]` cards in voice; start substantive replies; ship launch threads (zeni, Since, Garp…) only when actually postable.
- **Phase 2 — Compounding (months 2–3):** essays from the Essays & Videos board become one-liners + occasional long-form drops; weekly `/content-ideas` tops the insight queue.

## Reference accounts (modes, not clones)
DHH (craft/opinion) · levelsio (build-in-public) · thdxr (edge). Blend registers per post type; underlying voice stays Matt's (see `voice.md`).

## Consumed by
`references/voice.md` — how posts sound. `references/x-algorithm.md` — how the feed ranks. `references/reply-shortlist.md` — accounts to reply under. `references/posting-calendar.md` — the Phase 1 calendar (due-dated). This file — the plan itself.

## Automated weekly content-ideas — not running

**Status (2026-10-20): dead.** The LaunchAgent `com.mattsafaii.content-ideas-weekly` is not in `~/Library/LaunchAgents`, and its script (`~/.config/opencode/scripts/content-ideas-weekly.sh`) doesn't exist — opencode isn't installed either. Nothing fires on a schedule. Until it's rebuilt, run `/content-ideas` by hand each week.

What it was meant to do, so a rebuild doesn't re-litigate it: fire **Fri 14:00**, run `/content-ideas` headless over the past 7 days, and voice-draft client-work (transferable only) + business-growth + build-in-public insights into Distribution Triage as clay, with due dates set, never posting, never drafting essay prose. launchd was the choice because it fires whether or not an agent session is open and survives restarts.

**Note:** the earlier recurring-check-in idea was dropped — the check-in create endpoint is broken in CLI v0.8.1, and check-ins were the wrong tool for a solo reminder anyway (they collect team answers).

**Pivot anchor post (one-off, outside the calendar):** "been quietly shipping for a while and need to start sharing" + GitHub contributions graph — posted 2026-08-20, url https://x.com/mattsafaii/status/2090905571084124439. Pinned (recommended). Establishes the account's craft pivot to the handful of existing followers. Not tracked in Done (calendar measures the queue); metrics can be folded into the monthly report if wanted.

## Automated monthly metrics — not running

**Status (2026-10-20): dead**, same as the weekly job. `com.mattsafaii.metrics-monthly` and `~/.config/opencode/scripts/metrics-monthly.sh` are both gone. Run the aggregation by hand at month end, or rebuild the job.

What it was meant to do: fire **day 1, 7:00**, read the Distribution **Done** column, aggregate the month (posts / impressions / likes / replies / top post / cluster), and post a **Document** to Content's **Docs & Files** titled "Content metrics — <Month Year>". Never posts to X, never creates cards.

**Division of labor (still true when run by hand):** Matt posts + drops the direct status URL onto the card (the only manual bit). The weekly `/content-ideas` fetches live impressions/likes/replies onto Done cards via the X API. The monthly pass reads Done (URLs + gathered metrics) and posts the Doc. A Done card without a URL yields no metrics — see posting-calendar.md "Daily close".

## Ongoing feed loop (keeps the queue full)
Every `/content-ideas` run must also capture, alongside build-in-public: **client-work lessons (transferable, never client-specific)** + **business-growth angles** (what Matt tried to grow the studio/Zonebrite, what happened) + **engagement questions**. Those are on-theme and among his highest-leverage material — the queue must not become pure-dev. Feed them as `[💡 Insight]` / `[🔎 Question]` clay, voice-drafted.

---
**Status checkpoint (Phase 1, story-first rebuild 2026-08-21):** Matt's directive — post about things he builds and WHY + future ideas, not bugs. Queue rebuilt around **8 anchor stories** (scry, calmirror, since, zeni, garp, printnextdoor, whack-a-mullah, hookahhunt) + CLI/daemon pattern thread, dated Aug 21–Sep 06 in Scheduled. ~25 technical cards demoted to **Second act (<project>)** in Triage — attached as reply threads under stories, never standalone leads. Voice spec + content-ideas + distribute guide updated to enforce Pain → Realization → Build. 2026-08-21.
