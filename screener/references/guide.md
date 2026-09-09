# Screener — Workflow

Classify HEY's first-time senders and recommend decisions. Matt makes every decision; the agent executes only on his word.

## Hard rules

1. **Never deny, approve, clear, or spam without Matt's explicit say-so for that sender** (or an explicit "do all of them" covering the recommendation he just saw).
2. **Never `--spam` unless Matt says the word spam.** It trains HEY's filter and is harder to undo than a plain deny.
3. **Anything that could be a Zonebrite customer lead is surfaced, never denied** — even if it looks like marketing at first glance. Local-service inquiries arrive from personal addresses with odd formatting.
4. **Never auto-approve.** Known sender ≠ approved; it means the recommendation writes itself.
5. Don't touch anything outside the Screener. No moves, no drafts.

## Step 1 — Cheap count, then the queue

```bash
hey screener list --count    # bare number, cheap
hey screener list --json     # clearance IDs + sender + subject + topic_id
```

Empty queue → done, one line. Use `--all` when `total_count` exceeds what came back.

## Step 2 — Classify each sender

For each entry, check in this order (stop at the first hit):

1. **Screening history:** `hey screener history --json` — same sender decided before? Their past decision anchors the recommendation.
2. **Known contacts:** `hey contact list --json` — match name or domain. Also check aliases.
3. **Master Client List:** Basecamp doc `9802376865` in Office (`basecamp docs show 9802376865 -a 6191443`). Domain or company match = Safaii Studio client.
4. **Obvious junk signals:** `noreply@`, `no-reply@`, mailer-daemon, bulk-marketing domains, subject lines selling something.
5. **Lead-shaped:** a person's name + service-sounding subject ("quote", "estimate", "cameras", "installation", "consultation") → treat as a possible Zonebrite lead regardless of polish.
6. Otherwise: **unknown** — read the thread before judging: `hey thread read <topic_id> --markdown`.

Optionally search memory (qmd) for a sender that rings a bell but matches nothing above.

## Step 3 — Recommend

Present a numbered table:

| # | Sender | Subject | Read | Recommendation |
|---|--------|---------|------|----------------|

Recommendations are one word plus a short why: `approve` (known client/contact), `approve --box "The Feed"` (known but not urgent), `deny` (clear junk), `you decide` (lead-shaped or ambiguous — summarize what they sent so Matt can judge).

Wait for Matt's picks. Then execute exactly what he chose:

```bash
hey screener approve <clearance_id>
hey screener approve <id> --box "The Feed"   # one sender at a time
hey screener deny <id>                        # plain deny
```

Bulk flags: several IDs go through HEY's bulk endpoint, which takes no `--box`/`--seen`. `deny id1 id2` works; `approve` takes one ID per call.

## Step 4 — Report

One line per action taken, then the leftovers: anything Matt skipped stays parked in the queue untouched.

If a sender turned out to be a real lead, offer the next step: `/prospect` prep if it's Safaii-sized, or a note to follow up if Zonebrite.
