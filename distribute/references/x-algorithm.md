# X "For You" Algorithm — content reference

How X ranks the For You feed, distilled into what it means for drafting X content. Sources: the open-source [`xai-org/x-algorithm`](https://github.com/xai-org/x-algorithm) repo (release dated May 15, 2026), read from the actual scorer code — not the 2023 Twitter release — plus a community source-level breakdown (`codebreaker77/X-Algo-Breakdown`) for the Grox content-understanding pipeline. **Caveat on the breakdown:** its specific multipliers (decay 0.5, OON 0.75, etc.) are *illustrative examples*, not values from source — the real weights are withheld upstream. Don't cite numbers.

**Read this before drafting any X content (tweets, threads) in `/distribute` or `/content-ideas`.**

---

## ⚠ The one rule this is subordinate to

Matt's authenticity rules win, always. This reference shapes **structure and format** to give *genuine* content its best chance — it never licenses engagement-bait, ragebait, follow-farming, or slop. The happy truth below: the algorithm rewards the same things Matt already values (real conversation, substance, usefulness, a clear point of view) and actively suppresses the things he already refuses to make. So "algorithm-aligned" and "authentic" point the same way here. If they ever conflict, authenticity wins and we skip the post.

---

## How the feed works (just enough)

- **Two candidate sources:** in-network (Thunder — posts from accounts you follow) and out-of-network (Phoenix retrieval — a two-tower model that finds posts semantically similar to what the user engages with). For a small account, **OON retrieval is the growth lever** — it's how non-followers see you.
- **Ranking:** a Grok-based transformer predicts the probability of many actions per post, then a weighted sum produces the score.
- **Multi-action weighted score** (`home-mixer/scorers/weighted_scorer.rs`):
  - **Positive:** favorite, reply, retweet, quote, click, profile_click, share, share-via-DM, share-via-copy-link, photo_expand, video-quality-view, **dwell + continuous dwell-time**, quoted_click, follow_author.
  - **Negative (push the post DOWN):** not_interested, block_author, mute_author, report.
  - **Exact weights are NOT published** in the open-source release — don't cite or invent numbers. Reason qualitatively: effortful/intentful actions (reply, repost, quote, share, follow, profile-click, sustained dwell) are the meaningful positives; a bare like is weak signal.
- **OON attenuation:** out-of-network posts get their score multiplied by an `OON_WEIGHT_FACTOR` (< in-network). So OON content must be genuinely strong to surface.
- **Author diversity:** repeated posts from the same author in one feed are decayed (`author_diversity_scorer.rs`). Flooding hurts; your single best post beats five mediocre ones.
- **Candidate isolation:** each post is scored independently of the others — every post must stand on its own.
- **Content understanding (Grox):** spam detection, category classification, policy enforcement run over content. Spammy/policy-tripping posts get filtered before ranking.
- **Filters:** old posts are dropped (recency matters), already-seen/already-served posts are removed (no value in reposting the same thing in a session), muted-keyword and blocked-author filtering apply.

---

## What this means for drafting (apply when the channel is X)

1. **Optimize for replies, not likes.** A post that invites a genuine response — a real question, a position worth pushing back on, a "how do you handle X" — scores on reply probability, the strongest honest positive. This is identical to the engagement discipline already in the Playbook: ask real questions.
2. **Earn the dwell.** Dwell and continuous-dwell-time are scored. Substance that makes someone *stop and read* — a concrete story, a useful detail, a thread that pays off — beats a throwaway one-liner. Don't pad; do give something worth the seconds.
3. **Make it profile-click / follow-worthy.** profile_click and follow_author are scored. A post strong enough that someone checks who you are — then a coherent, niche-consistent profile that rewards the click (ties to the studio positioning/worldbuilding).
4. **Write for the share, not the broadcast.** share / share-via-DM / share-via-copy-link are all scored. A genuinely useful insight gets sent to a friend. This is literally what `[💡 Insight]` cards are — lean into "useful enough to forward."
5. **Hook must stand alone (candidate isolation + threads).** The first tweet of a thread is scored on its own; it has to work with zero context. Front-load the point or the tension.
6. **Stay in your niches (feeds OON retrieval).** The two-tower model builds an embedding of you from what engages with your posts. Consistency across your real topics — vanilla CSS / web craft, local-first, solo-dev process, plain-text, field-utility software — makes you retrievable to the right out-of-network audiences. Scattered topics blur that signal.
7. **Replying well is a real OON path — and replies are now VLM-quality-scored.** The `ReplyScorer` (a Grok vision model) reads the parent post and your reply and assigns a quality score *with a written reason*. "Great post!" / "following" is dead — it scores ~0.1 and sinks. To rank near the top, the reply must **add a specific fact, ask a genuinely relevant question, or respectfully counter**, referencing concrete concepts from the parent (give the model something to write a reason about). A substantive reply under a larger account in your niche can surface to their audience — the cleanest non-spammy discovery path for a small account. (Maps directly to `[🌱 Establish]` / `[🔎 Question]` behavior.)
8. **Never trip the negatives.** not_interested / block / mute / report carry negative weight and reflect lasting user intent. Engagement-bait, ragebait, follow-for-follow, reply-guy spam, and repetitive posting *actively* suppress you. This is the algorithmic reason Matt's no-slop rule is also the winning strategy.
9. **Cadence over volume.** Author-diversity decay + already-served filtering mean flooding is counterproductive. Space posts; make each one count. (Matches "don't over-produce.")
10. **Recency.** Old posts are filtered out — post when the audience is active, and treat timeliness as part of the draft.
11. **Media where it's genuine.** photo_expand and video-quality-view are scored — a real before/after (Decimate), a gameplay GIF (Whack-A-Mullah), a terminal recording (zeni) earns that surface. Don't bolt on media for its own sake.

---

## Pre-publish AI screening (the Grox gate — biggest addition)

Before any human sees a post, a Grok vision model screens it. This is the algorithmic enforcement of Matt's no-slop, write-in-my-voice rules — and the reason AI clay that *isn't* rewritten gets punished. Three gates:

- **`slop_score` (AI-slop detection).** The classifier is explicitly trained to catch low-effort AI-generated text and throttle its reach. Tells it flags: LLM vocabulary (**delve, tapestry, crucial, synergy, "navigating the landscape," "in an ever-evolving…"**), the **intro → 3 bullets → conclusion** shape, an **emoji at the start of every bullet**, and over-polished symmetry. Antidote = exactly Matt's voice: specific personal experience, concrete numbers, conversational/asymmetrical phrasing, a real anecdote. **This is the mechanism that makes the seeds-vs-clay rule load-bearing — draft clay MUST be rewritten in his voice or it trips the slop gate.**
- **`quality_score` / "banger" screen (~0.4 threshold).** The VLM must be able to **tag the post's topic in ~3 words and write a description**; posts it can't classify ("just thinking out loud today…") score low. So make the topic legible — a defined subject, a clear claim — not vague musing. (This also feeds topic-cluster retrieval: a clearly-tagged post gets matched into the right adjacent communities.)
- **Image quality.** The VLM checks whether an image is parseable (clear subject / readable text). Deep-fried memes or text-crammed images tank the score. If a card suggests media, suggest *clear* media (a clean before/after, a legible terminal capture).

## Small / new-account constraints (directly limits launch tactics)

A dedicated `SpamEapiLowFollowerClassifier` treats small accounts (the breakdown cites ~<500 followers) as suspicious. For Matt — a small account who wants to share projects — this is the most practically important finding:

- **Don't lead a post with an external link** (project URL, essay link, Substack, etc.) while the account is small — link-dropping from low-follower accounts trips spam scrutiny and suppresses reach. Put the substance in the post; the link is secondary (a reply, or later in a thread), and earned by the post being good.
- **No repetitive tagging of large accounts** to get attention, and **no copy-paste replies** across threads — both are spam signals.
- Build trust with native, substantive text/image posts first; route to off-platform links more freely once established. (Dovetails with `[🌱 Establish]`: earn standing before extracting.)

## Win your network first (the 2-phase reach model)

Followers see your post un-penalized and recency-sorted (via Thunder) — that's your proving ground. Their early engagement builds the raw score high enough to survive the OON penalty when the feed tests you on non-followers. Practical: post when your audience is active, and make the post genuinely worth your *existing* followers' engagement before worrying about reach. No initial in-network traction → no OON distribution.

## Video / GIF on X (note even though YouTube-as-channel is deferred)

Matt still posts GIFs/short clips on X (Whack-A-Mullah gameplay, terminal recordings):
- **Very short clips may get no video credit** — the video-quality-view weight only applies above a minimum duration, so a 2–4s GIF can score zero as video. If a clip is the point, make it substantive (a longer loop / real demo), not a 3-second blip.
- **The embedder reads the audio/subtitles**, not just frames — a talking-head clip with no captions is opaque to topic retrieval. Add a clear descriptive text caption (and captions/clear speech if there's audio) so the model knows what it's about.

## What NOT to do with this

- Don't add "engagement hooks," fake questions, "comment X below," manufactured hot takes, or thread-bait. They read as slop, and the negatives (not_interested/mute) are weighted to catch exactly that.
- Don't cite specific weight numbers (withheld) or the old 2023 multipliers (different release).
- Don't let algorithm-fit override Matt's voice or the seeds-vs-clay rules. Format guidance only; the substance and the words are still his.
