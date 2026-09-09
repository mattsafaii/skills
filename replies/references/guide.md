# Replies — Workflow

Draft replies for every thread Matt parked in HEY's Reply Later box. Every reply is saved with `--draft`. HEY's drafts folder is the review lane: an agent writes, a person decides.

## Hard rules

1. **Never send.** No `hey draft send`, no `hey reply` without `--draft`, no `hey compose` without `--draft`. The send belongs to Matt.
2. **Don't invent facts.** Never fabricate a date, price, availability, estimate, or commitment. If a good reply needs one and it isn't in the thread or context, stop and ask Matt first.
3. **Don't touch box state.** No move, seen/unseen, trash, label, bubble. The only write is the draft itself.
4. **Skip bundles with no `topic_id`** (a bundle row names its sender, not a thread) — list them at the end as "needs you in HEY."
5. Sensitive threads (legal, disputes, invoices in question, anything emotional): flag them to Matt and ask how he wants to handle them rather than drafting cold.

## Step 1 — Read the queue

```bash
hey box view laterbox --json
```

Each posting carries `id` (box item), `topic_id` (thread), `name` (subject), `contacts`, `summary`, `created_at`, `seen`. If the queue is empty, say so and stop.

Show Matt a numbered list:

```
1. Jane Doe <jane@client.com> — "Re: homepage feedback" — parked 2d
2. ...
```

Ask which to work: all, or numbers. Don't draft without his pick.

## Step 2 — Understand each thread

For each chosen thread:

```bash
hey thread read <topic_id> --json
```

Bodies come back as Markdown, oldest entry first. Read the whole thread before writing anything — replies answer the latest entry.

Then gather context, cheaply and only as needed:

- **Sender's private note:** find the contact ID from the posting's `contacts`, then `hey contact show <contact_id> --json` — the note may hold history ("prefers text", "invoice on net-30").
- **Past discussions:** if the sender or their company rings a bell but the note is empty, search memory (`qmd`) before asking Matt.
- **Project context:** if the thread is clearly about a build, check that project's Basecamp todolist or dev log for current state. Don't go fishing otherwise.

## Step 3 — Draft in Matt's voice

Write like Matt writes email:

- Short and direct. Lead with the answer, then the detail they need.
- Plain words, active voice. Cut filler ("just wanted to", "I hope this finds you well", "circling back").
- Match the sender's register — clients get warm and casual, vendors get brief and businesslike.
- Know which hat he's wearing: Safaii Studio (design/build talk) vs Zonebrite (service, scheduling, no fear-selling).
- Run the draft against the reader-first test (does it give this person a reason to care and a clear next step?) and strip AI tells (no em dash pileups, no rule-of-three padding).

If any fact is missing — when he's free, what something costs, whether he'll take the job — ask Matt before saving the draft.

## Step 4 — Save as draft

```bash
hey reply <topic_id> -m "<markdown>" --draft
```

The command works out addressing itself (like HEY's own reply) and returns the draft id. Show Matt each draft in chat as you save it: sender, subject, draft body, draft id.

## Step 5 — Report and revise

End with a table: thread / draft id / one-line summary of what the draft says. Then offer:

- **Revise:** "tweak #2" → `hey draft edit <draft_id> -m "<new markdown>"` (an edit replaces the body; other fields are kept)
- **Discard:** `hey draft delete <draft_id>`
- **Read back:** `hey draft show <draft_id> --json`
- Anything left unworked stays parked in Reply Later untouched.

Matt sends from HEY — web, phone, or TUI — whenever he's ready.

## Notes

- Redoing a draft: if an older draft for the same thread exists, ask before deleting it (`hey draft delete`) and drafting fresh.
- Replies use the thread's own linked mail account automatically; no `--account` needed.
- If auth fails mid-run: `hey auth status`, then tell Matt to run `hey login`.
