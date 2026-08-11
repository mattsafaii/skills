# X-Check Skill Guide

Matt wrote a tweet/thread/reply and wants a gut-check before posting. Return **findings** on how it reads against the X "For You" algorithm so he can decide what to change. This is the X equivalent of `develop-essay`'s critique pass.

**Load the algorithm reference first:** `~/Code/skills/distribute/references/x-algorithm.md` is the single source of truth for how the feed ranks. Read it; don't reproduce or re-derive it here. This guide is only the *checking procedure*.

---

## The two hard rules

1. **Findings, not rewrites. Never write his words.** Same rule as `develop-essay`. You may quote his sentence back and name what's off and *what kind of fix* — never supply the replacement wording. He writes every published word; this skill sharpens his judgment, it doesn't ghostwrite. If he says "just fix it," decline and give a sharper finding instead.
2. **Authenticity checker, NOT an engagement optimizer.** Do not suggest hooks, bait, or "do X to boost replies/reach." The only lens is: *does this read like a human Matt wrote it, is it legible, and does it avoid self-inflicted suppression?* The algorithm's slop/spam gates already reward authenticity — so checking for authenticity IS checking for reach. If a finding would push him toward tuning-for-the-algorithm over saying what he means, drop it.

---

## What to check (against the reference)

Run the draft against these. Only raise what actually applies — a clean tweet gets few or zero findings; say so.

1. **Slop tells (the big one).** Does it read AI-generated? Flag: LLM vocabulary (*delve, tapestry, crucial, synergy, "navigating the landscape," "ever-evolving"*), the intro → 3-bullets → conclusion shape, an emoji starting every line, over-polished symmetry, generic hedging. The antidote is his own voice (specific experience, concrete detail, conversational asymmetry) — name the tell, not the rewrite.
2. **Read-aloud / authenticity.** Point at any sentence that doesn't sound like Matt talking to a person across a table.
3. **Topic legibility.** Could a reader (or a classifier) name the subject in ~3 words? Vague musing ("just thinking out loud…") is illegible and sinks. If the point is buried or absent, flag it.
4. **Dwell / substance.** Is there something worth stopping to read — or is it a throwaway line? (Don't push him to pad; flag genuine emptiness, not brevity that works.)
5. **Link-drop while small.** If the post **leads with an external link** (project URL, essay, Substack), flag it — leading with a link from a small account trips spam scrutiny. Fix type: make the post stand on its own; link secondary/in a reply/earned. (Don't flag a link that's incidental, not the lead.)
6. **Reply quality (if it's a reply).** Is it substantive — a specific fact, a genuinely relevant question, a respectful counter that references the parent? Flag dead patterns ("great post!", "this 🔥", "following"), which score ~0 and sink.
7. **Standalone hook (if it's a thread).** Does the first post work with zero context? Flag if it only makes sense after later posts.
8. **Negative-bait.** Flag anything that could trigger not-interested / mute / block / report — engagement-bait ("like if you agree"), ragebait, follow-for-follow, manufactured outrage. These carry negative weight and a single mute can outweigh many likes.

---

## Output format

A short, numbered findings list. For each: **quote the bit**, name **what's off**, and the **fix type** (never the fix wording). Lead with a one-line read: e.g. *"Reads authentic — two small flags"* or *"This would likely trip the slop gate — here's why."* If it's clean, say it's clean and stop; don't invent problems to look useful.

Do **not** post it, create a card, or rewrite it. The skill ends at findings; Matt edits and posts himself.

---

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Supplied replacement wording | Slipped into ghostwriting | Findings only — name the problem + fix type, quote his words back unchanged |
| Suggested a hook / bait to boost reach | Drifted into optimizer mode | Authenticity lens only; drop anything that tunes-for-algorithm over meaning |
| Wall of nitpicks on a clean tweet | Inventing problems to seem useful | Say it's clean; few or zero findings is a valid result |
| Flagged brevity as "low dwell" | Confused short with empty | Brevity that lands is fine; flag genuine emptiness only |
| Re-explained the whole algorithm | Didn't lean on the reference | Read `x-algorithm.md`; this skill is the checking procedure, not the knowledge |

---

## Related

- `x-algorithm.md` (in `distribute/references/`) — the knowledge this skill applies; single source of truth.
- `/distribute`, `/harvest` — generate X content (clay/seeds). This skill checks content Matt wrote himself.
- `develop-essay` — the same findings-not-rewrites discipline, for long-form.
