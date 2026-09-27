---
name: love-letter
description: "Write and ship a love letter — a hyper-personalized pitch for one named person at one dream client company, so specific it could not be sent to anyone else. Based on Dan Mall's 'The 23-Year Mistake': five signals plus a secret sixth, delivered as a landing page in the client's own branding (the signal that 'we're already working together'). Composes with prospect (research), safaii-css/safaii-html (page craft), and tracks each campaign as a card in the Sales Pipeline. Big-swing, long-game play — gates on the business being in a position to court a dream client for weeks. Use when Matt says \"love letter for [company]\", \"write a love letter to [dream client]\", \"land [company] as a client\", \"shoot my shot at [company]\", or \"/love-letter\". Safaii Studio web design clients by default; the framework is generic."
metadata:
  version: 0.1.0
---

# /love-letter — A pitch for one person, in their brand

Turns a dream client into a landing-page love letter: five signals (Just like you → We did our homework → Bring 10% to life → Don't worry, we've been here before → Let's do this) plus the secret sixth (their brand, not yours). The outcome is a single-file HTML page that could not have been sent to anyone else.

**Read these first — they carry the knowledge this skill applies:**
- `references/signals.md` — the six signals and why each works. The spine.
- `references/scripts.md` — copy frames and the page skeleton.
- `references/examples.md` — the three real love letters and their patterns.
- `references/research.md` — the homework pass (company + person).

**Load `prospect` for the heavy company recon when needed** — this skill is the letter; prospect is the research engine.

**Campaign home:** `~/Workspaces/safaii-studio/love-letters/<client-slug>/` — one folder, one `index.html`, plus a `brief.md` with the research + sourcing.

---

## Step 0 — The phase gate (stop here if it's the wrong play)

Love letters are a big-swing, long-game play. They shine when bills are covered and you can afford to court a dream client for weeks. If Matt is scrambling for this month's revenue, say so in one line and offer faster plays instead (referrals, a `client-report` relationship, a `prospect` meeting already in the pipeline). Not because the strategy is wrong — because the phase is. Don't proceed on a letter until he's clear the swing is affordable.

## Step 1 — Intake

Check what already exists before asking Matt anything:

```bash
ls ~/Workspaces/safaii-studio/love-letters/ 2>/dev/null
basecamp -a 6191443 cards list --card-table 9782662056 -p 46876803 --md
cat ~/.config/makerskills/love-letter/config.md
```

- A past love letter to the same company means a re-run — read it before drafting fresh.
- An existing Pipeline card means the campaign is already tracked; link, don't duplicate.
- The config's dream-client list and case-study inventory seed the letter — check before asking.

Then get from Matt:
- **The dream client** — and why them (the *why* shapes the angle).
- **The target person**, if he has one; otherwise Part B of research finds the one who can hire.
- **Whether public or private fits** — public landing page by default; private (password/link or email) when a public URL is wrong for the target. His call, not the skill's.

## Step 2 — The homework pass

Run `references/research.md`. Company: the four ingredients (owned problem, stat in their units, missed market, FOMO), one opportunity committed to. Person: one quotable line, one true shared ground, their contact path. Everything sourced and dated. Composing with `prospect` is welcome for the company side; the person digging stays light.

## Step 3 — The concept + 10%

Pick the single product area the letter commits to, and the artifact that brings 10% to life: a mockup, a sizzle reel, a sample page in their brand. **Build only the first 10%** — enough of the "what" and "why" that "how" is the only question left, and nothing that they could finish without you or you without them.

## Step 4 — The proof

Hand-pick **2–3 Safaii case studies from the config inventory** at matching scale and stakes — never a portfolio dump. One line each: who, what, at what scale. (The NBA page's "Starting Five" is the exception that proves the rule — five was the right count because the headline was right.)

## Step 5 — Build the page

A single-file `index.html` at the campaign path. **The client's visual identity is mandatory — the Secret Sixth.** Their palette, typefaces, art direction, tone of voice — not Safaii's. Use `safaii-css` for the underlying craft (layers, tokens, fluid type, accessibility) and `safaii-html` for the markup, but the visual identity belongs to the target. Signal 6 is what makes "we're already working together" feel true.

Follow the skeleton in `scripts.md`, written top-down but *built* middle-first:
1. Homework section (the biggest, at least half the page)
2. 10% to life
3. Been here before
4. Then the intro ("Dear [Name]," one strategic sentence), the opportunity summary line, the bridge, and the close
5. Close = closed-ended ask + dynamic next step (~7 days out) + zero-friction contact

## Step 6 — Review gate

Show Matt the draft before anything is sent or tracked. Copy is his to write — the skill frames, he decides the final words and the visual polish. Nothing ships without his approval.

## Step 7 — Send

- **Public:** deploy the single page (Cloudflare Pages — the stack constraint). URL goes in the cover note.
- **Private:** send the page or a private link, or the note + artifact by email — whichever fits the target.
- The **cover note** is the two-sentence move from `scripts.md`: warmth + one honest line ("Congratulations! And honestly? I'm jealous. You have my dream job!"). The page is the artifact; the note is the ask to look.

## Step 8 — Track + follow up

One card in the Sales Pipeline table (`9782662056`, Sales project `46876803`), **Qualifying** column (`9792713218`) by default:

```bash
basecamp -a 6191443 cards create "Love letter — <Company>" --card-table 9782662056 -c 9792713218 -p 46876803
```

Follow the cadence in `scripts.md`: ~3 days of silence → one short follow-up (never a re-send of the whole letter); ~5 more days to hear. Move the card **Follow-up Needed** (`9782662060`) when the follow-up goes out, and comment replies with dates. Never move a card to **Won** (`9782662062`) until it's real; that's Matt's column to call.

## Step 9 — Report back

About four lines: the URL, the target person, the one line that makes it personal, and the next step + when. If it's a public letter, note that the page is live and who it's addressed to.

---

## Failure modes

If something fails in a way this table doesn't cover, show Matt the raw error and stop — don't improvise or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Wrong account / 404 on any basecamp command | Missing `-a 6191443` | Always pass it explicitly |
| Letter reads like it could go to anyone | Skipped the custom-made test | Rerun signals 1 + 6 — one named person, their brand, one committed idea |
| Page uses Safaii's styling | Ignored the Secret Sixth | Rebuild the visual identity in the client's palette/type/tone |
| A stat or person detail is unsourced | Rushed the homework pass | Sourcing + dates are mandatory in `brief.md`; `Unknown` beats a guess |
| Homework section thinner than half the page | Built top-down from the intro | Build middle-first — homework is the load-bearing section |
| 10% artifact is a finished product | Over-built the concept | Cut to what they can't do without you and you can't finish without them |
| Proof is a portfolio dump | Picked too many / wrong stakes | 2–3 cases at matching scale, one line each |
| Card duplicated or moved to Won | Re-tracked or got ahead of the record | Check step 1 for an existing card; Won is Matt's call |
| Follow-up re-sent the whole letter | Misread the cadence | One short nudge at ~3 days; never re-send the letter |
| Sent without Matt's approval | Skipped the review gate | Step 6 is a hard stop — nothing ships without his sign-off |

---

## Related

- `prospect` — the research engine; compose for the company side of the homework pass.
- `references/signals.md` — the six signals; the spine of this skill.
- `safaii-css` / `safaii-html` — page craft underneath the client's visual identity.
- `~/Workspaces/safaii-studio/love-letters/` — campaign archive; read before re-running on the same company.
