# Matt's X voice — spec for drafting clay

What Matt's X posts sound like. Skills (distribute, harvest, jab-hook, x-post-check) consult this before drafting so clay arrives in his voice and needs minimal rewriting. Fiction it isn't: this is a *copy of how Matt actually writes*, distilled from his own posts — not a persona to perform. If a draft reads more like the spec than like Matt, it's wrong.

## The one-line test

If you don't know who @mattsafaii is and read the post with the name hidden, you should be able to guess: short, lowercase-starting, understated, a working indie developer saying something true that he's personally hit.

## Voice traits (in priority order — earlier wins)

1. **Short and plain.** One idea. Cut everything that isn't the point. Most insight posts fit in 1–3 lines. He values deletion ("If it's possible to cut a word out, always cut it out").
2. **Lowercase-starting.** Sentences start lowercase ("the future of endless features…", "it really does not stop"). Not a rigid grammar law, but the natural register is casual, lowercase-leaning, no exclamation-mark shouting.
3. **Understated, dry, unhypey.** Confidence through quiet, not volume. He does not say "This is game-changing 🔥". He says the thing plainly and lets it sit: "every product will look like aws". Irony and deadpan are allowed; screaming isn't.
4. **First-person specificity.** It's *my* server, *my* fix, *this* bug I hit. Concrete numbers and real details over abstractions. "My droplet booted with NOTHING applied" beats "deployment configs can be tricky."
5. **The lesson lives in the anecdote, not the moral.** He tells what happened and what he did; readers pull the takeaway. No "Here are 3 reasons you should…" (that's Grox-slop shape anyway).

## What he doesn't do

- No AI-slop vocabulary: delve, tapestry, crucial, synergy, "in an ever-evolving landscape", "navigating the landscape".
- No intro → 3 bullets → conclusion symmetry. No emoji-per-bullet.
- No engagement-bait or fake questions ("Tell me in the comments!"). The one explicit reframe: his current account farms impressions off-theme; the focused account does not farm at all.
- No manufactured hot takes. An opinion is fine — he has plenty (Hotwire-first, SQLite-not-Postgres, VPS-not-Vercel) — but it has to be a position he actually holds from doing the work, not a contrarian pose.

## Three blendable registers (his own words as templates)

Matt named DHH, levelsio, thdxr as references. Map them to modes, not clones — the underlying voice stays his; he *switches intensity per post type*.

- **Craft/opinion (DHH register)** — confident declarative, principled, no apology. Deployed on the tech-craft essays.
  *Real echo from him:* "You probably don't need that — Hotwire-first." · "I deploy to a cheap VPS, not Vercel." · "SQLite is a real production database."
- **Build-in-public (levelsio register)** — what he shipped, raw and specific, transparent numbers/detail. Deployed on the `[💡 Insight]` build-in-public nuggets. His version is calmer than levelsio — no revenue-ticker dopamine-farming, just "shipped X / hit this bug / learned this."
  *Real echo from him:* "For full code, just check the first link. Free for next 24h." · "Responsive sidebar built with HTML, CSS and JavaScript."
- **Edge/take (thdxr register)** — personality-forward, conversational, in-group dryness, the occasional swipe. Deployed sparingly — the spice, not the meal.
  *Real echo from him:* "it really does not stop."

## The primary shape: Pain → Realization → Build (2026-08, Matt's directive)

Matt's #1 post type and the highest bar: **story-led posts understandable by almost anyone.** "I didn't like the moodboarding software so I set out to build my own. then I realized discovery sucked too and wanted to search my own collections. so I built scry." Formula:

1. **Pain** — a relatable problem, no jargon. "I didn't like X."
2. **Realization** — the second insight that deepens the story. "then I realized Y sucked too."
3. **Build** — the thing, stated plainly. "so I built Z."

**Universal lead, technical follow-up.** The lead post must be understandable by non-devs. Technical detail (how he built it, a bug he hit, a clever fix) is the *second act* — a reply/follow-up thread for the people who stayed, never the opening. A post that starts with "my deploy check polled for a string that already existed on the page" is second-act material misused as a lead; the lead is "deploy scripts lie, and I found out how."

Each project carries an arc: a story lead + a technical follow-up. The existing insight cards are mostly the second act — attach them under their project's story rather than leading with them.

## The trap to avoid

Do **not** turn his understated voice into generic "helpful indie dev" niceness. The account should read like it's built by someone with taste and opinions, not an AI that agrees. Where DHH/levelsio/thdxr are loud, Matt is still — but he is never neutral. If both "authentic Matt" and "algorithm-optimized" call for an edit, authenticity wins (the x-algorithm reference agrees: the slop screen rewards exactly his real voice).

## Draft checklist (before a tweet leaves a skill)

1. Would Matt actually say this? (voice over everything)
2. **Shape-first — Pain → Realization → Build wins.** Which shape is this: a story lead (universal, everyday words) or a technical follow-up (the second act, for people who stayed)? If it's a technical fact with no story attached, it's second-act material — attach it to its project's story, don't open with it.
3. **The "so what?" bar:** would a stranger who never lived it care? A work log is NOT a post. Needs a hook + a payoff. Generic "TIL my tool did X" dies.
4. Is it one idea, cut to the bone?
5. Does it start lowercase / read casual, not corporate?
6. Is there a specific first-person fact, not a generic platitude?
7. Any slop-shape or bait? Kill it.
8. Post-type register: is it the right intensity (craft vs. build vs. edge)?
