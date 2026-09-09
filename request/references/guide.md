# Request — Workflow

Client emails a request → discrete Basecamp todos in their project, each carrying the thread's context. Matt confirms before anything is created.

## Hard rules

1. **Never create a todo without Matt's explicit go** on the exact titles, target project, and todolist he just saw.
2. **Never guess the project.** Ambiguous sender → list candidates, let Matt pick. No match at all → ask which project (and note it may need registering in the Master Client List).
3. **One ask = one todo.** Split multi-part emails; don't bury three requests in one todo.
4. **Share links are public URLs** — anyone holding one can read that whole thread and future replies to it. Only link the thread Matt asked about, and say so before using one.
5. Don't touch the email itself beyond reading: no seen/unseen/move/draft unless Matt asks.

## Step 1 — Get the thread

The thread comes from context: Matt names it ("the SPF thread"), points at Imbox/Reply Later, pastes text, or you search:

```bash
hey box view imbox --json          # or laterbox
hey search --from <sender> --json  # or free text
hey thread read <topic_id> --markdown
```

Read the whole thread. The request is usually in the latest entry; earlier entries hold constraints and history.

## Step 2 — Find the project

```bash
basecamp docs show 9802376865 --in 46820187 -a 6191443   # Master Client List: company names
basecamp projects list -a 6191443 --json                  # id + name per project
```

Match the sender (name, email domain, signature block) against the client list, then fuzzy-match onto a project name — "Konnected Concepts" ↔ `46823746`. Confirm the match with Matt in one line: *"Konnected Concepts (project 46823746), right?"*

Zonebrite work lives on its own projects too — same chain works when the sender is Zonebrite-side.

## Step 3 — Extract the asks

List what you pulled out, as proposed todos:

```
1. Fix mobile menu overlap on services page
2. Swap hero photo to the new shoot set
3. "Can we push the launch to October?" → decision needed from you
```

Flag anything that isn't really a todo — questions for Matt, scope creep worth pushing back on, or requests that belong in `/shape`/`/backlog` instead of a quick fix. Let Matt edit the list freely.

## Step 4 — Pick the landing spot

```bash
basecamp todolists list --in <project> -a 6191443
```

Obvious single todolist → use it, say so. Several → show them, ask. No good home → offer `--loose`.

## Step 5 — Create

For each confirmed todo:

```bash
basecamp todos create "<title>" \
  --description "<context>" \
  --list <todolist_id> --in <project_id> -a 6191443
```

Description template (Markdown):

```markdown
Requested by <name> (<email>) on <date>.

> "<short quote of the ask>"

Context: <one or two lines of thread background, if any>
Thread: <hey share link, only if Matt approved sharing>
```

Get the link with `hey share <topic_id>` — but ask first (rule 4). Without a link, quote enough text that the todo stands alone.

## Step 6 — Report

Table: todo title / Basecamp URL. Then offer:

- **Acknowledge to the client:** draft a short reply via the `/replies` pattern (`--draft`, never send) — "Got it, on the board."
- **Mark the thread seen**, if Matt wants it out of sight.
- Anything un-filed stays untouched.
