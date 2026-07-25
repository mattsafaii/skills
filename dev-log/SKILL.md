---
name: dev-log
description: Post a dated dev log entry to the project's Basecamp message board. Use this skill whenever the user asks to log what was done, update the dev log, write a dev log entry, record today's work, or says something like "devlog", "log this session", "what did we do today", or "add to the changelog". Also trigger when the user wraps up a coding session and wants to capture what happened. This skill pulls recent git history, combines it with session context, and writes narrative bullet points explaining what changed and why.
---

# Dev Log Skill

Post a narrative dev log entry to the Basecamp project's message board. The entry captures what changed and — more importantly — why it changed, drawn from both git history and what happened during the current session. Dev logs live in Basecamp only — never write them into AGENTS.md or CLAUDE.md.

## Workflow

### 1. Gather context

Run `git log --oneline -20` to see recent commits. Combine this with your memory of what was worked on in the current session — the problems discussed, decisions made, and reasoning behind changes. The git log is raw material, not the final product; your session context is equally important.

Also read the project's Solo `state` scratchpad if it has one — `scratchpad_list(tags: ["state"])`, then `scratchpad_read`. Git shows what changed; the scratchpad holds why, including reasoning from earlier sessions this one never saw. It's the best source for the narrative bullets in step 3 and for anything worth capturing in step 6. Skip it if the project has no scratchpad — most of the log still comes from git and this session. See the `solo` skill for the convention.

### 2. Determine categories

Look at the changes and group them into natural categories. Don't force a fixed taxonomy — let the work dictate the grouping. Common categories include things like **Features**, **Bug Fixes**, **Refactoring**, **Infrastructure**, **Tests**, **Docs**, but use whatever labels actually describe the work. If everything falls under one category, that's fine — don't invent categories just to have more than one.

### 3. Write the entry

Each bullet point should be a short narrative sentence that captures the *why*, not just the *what*. A reader skimming the log months later should understand the motivation, not just the diff.

**Good:** "Added rate limiting to the /api/search endpoint because load testing showed it was vulnerable to burst traffic that could starve other routes."

**Bad:** "Added rate limiting middleware."

The why might come from the git history, from the conversation during the session, or from your understanding of the codebase. Use all of it.

### 4. Format the entry

Title: `Dev log — YYYY-MM-DD: <short summary>` using today's date.

Body (Markdown — the basecamp CLI converts it to HTML):

```markdown
**Category Name**

- Narrative bullet explaining what changed and why
- Another bullet if needed

**Another Category**

- More bullets as needed
```

### 5. Post to Basecamp

Get the project ID from `.basecamp/config.json` in the repo root. If there's no config, find the project with `basecamp projects list` (or ask which project).

```bash
basecamp message "Dev log — YYYY-MM-DD: <summary>" "<body>" --in <project> --jq '.data.app_url'
```

Past entries are immutable — always post a new message; never edit or delete earlier dev log messages.

### 6. Capture insights (optional — only if something quotable came out of the session)

Scan the session and the dev log you just wrote for any **generic, non-obvious, transferable** learning — a technical gotcha, a design or product decision, a "I got this wrong twice" lesson. Most sessions produce zero; that's fine. **Do not force it.** A high bar beats a steady drip of filler. One idea per insight.

For each genuine insight, create a card in the Safaii Studio **Distribution** card table so it joins the build-in-public tweet queue:

```bash
basecamp -a 6191443 card "[💡 Insight] <takeaway> (<Project>)" "<blockquote><draft tweet></blockquote><p><em>Draft clay — rewrite in your voice; gut-check the claim before posting.</em></p>" \
  --in 46824770 --card-table 10010006453 --column 10010006454 --jq '.data.app_url'
```

- Coordinates are fixed: account `6191443`, Content project `46824770`, Distribution table `10010006453`, **Triage** column `10010006454`. These never change regardless of which repo the dev log is for.
- Title carries the takeaway + source project so the board is scannable. Body = a draft tweet (clay Matt rewrites) + the gut-check note.
- Board taxonomy (for context — dev-log only ever creates `[💡 Insight]` cards): postable pieces in Triage are prefixed `[💡 Insight]`, `[🔎 Question]`, `[👋 Teaser]`, `[🧵 Thread]`, `[💬 Reddit]`, `[📊 Poll]`. Stay in the insight lane.
- Each project's **distribution plan/brief is a Doc** (`<Project> — Distribution Plan`) in *this* build project's own Docs — not in the Distribution table. If one exists for the current repo, append a `📋 Plan:` link to it in the insight card body so the card points back to the brief.
- If the insight is **cross-cutting / not tied to a single project** (no plan doc to link), instead link the **Distribution Playbook** (the cross-cutting rulebook): `<p>📋 <strong>Playbook:</strong> <a href="https://app.basecamp.com/6191443/buckets/46824770/documents/10016763197">Distribution Playbook</a></p>`. A card with neither is also fine — the link is optional.
- This is **draft clay, not seeds-only** — the no-AI-writing rule is for essays, not throwaway tweet drafts. Still: write it as a starting point, never as final copy.
- **Client work:** only capture if the insight is generic and non-confidential — never leak a client's specifics into the public tweet queue.

### 7. Confirm

Share the dev log message URL — and list any insight cards created — so Matt can sanity-check what was posted.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Message posts to the wrong Basecamp project | No `.basecamp/config.json` in the repo root, so the wrong project got guessed | Always check `.basecamp/config.json` first; if missing, run `basecamp projects list` or ask Matt which project — never guess |
| Dev log history has gaps or contradictions | An earlier entry was edited or deleted instead of superseded | Entries are immutable — always post a new message, never edit or delete a past one |
| Distribution board fills with low-value cards | Step 6 forced an insight out of a session that didn't produce one | Most sessions produce zero insights; skip step 6 entirely rather than manufacture one |
| Client specifics leak into the public tweet queue | An insight card captured a client-identifiable detail | For client work, only capture insights that are generic and non-confidential — skip anything that names or fingerprints the client |
| Insight card lands under the wrong account/project | Coordinates improvised instead of using the fixed ones | Insight cards always use Safaii Studio account `6191443`, Content project `46824770`, Distribution table `10010006453`, Triage column `10010006454` — regardless of which repo (including Zonebrite work) the dev log itself is for |
| Dev log content ends up in AGENTS.md/CLAUDE.md | Confused with the daily/repo-level logging habit | Dev logs are Basecamp-only; AGENTS.md/CLAUDE.md is a separate, repo-local log this skill never touches |
| Entry lists what changed but not why | Only git history was read; the reasoning was in the scratchpad | Read the `state` scratchpad in step 1 before writing bullets |
