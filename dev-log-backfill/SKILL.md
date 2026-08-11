---
name: dev-log-backfill
description: Backfill a dev log in Basecamp from the full git history. Use this skill when the user wants to retroactively create dev log entries, initialize a dev log from past commits, backfill the dev log, generate a dev log from git history, or says something like "init dev log", "backfill the log", "create dev log from history", or "document what's been done so far". This is for projects that don't have a dev log yet and want to reconstruct one from commit history. For logging current session work, use the dev-log skill instead.
---

# Dev Log Backfill Skill

Retroactively generate a dev log by synthesizing the full git history into grouped, dated entries posted to the Basecamp project's message board. This is for projects that don't have a dev log yet and want to bootstrap one from what's already been committed. Dev logs live in Basecamp only — never write them into AGENTS.md.

## Important caveat

Unlike the real-time `dev-log` skill, you don't have session context here — no memory of conversations, decisions, or reasoning that happened during past work. The "why" behind changes has to be inferred from commit messages, diffs, and code context. Be upfront about this: the entries will be less narrative-rich than ones written in the moment. Where commit messages are descriptive, lean on them heavily. Where they're terse ("fix bug", "wip"), do your best to infer intent from the diff, but don't fabricate reasoning you don't actually have.

## Workflow

### 1. Pull the full git history

Run `git log --oneline` to get all commits. For repos with very long histories (hundreds or thousands of commits), this is fine — the grouping step will condense things down.

Also check what dev log messages already exist in the Basecamp project: get the project ID from `.basecamp/config.json` (or `basecamp projects list`, or ask), then `basecamp messages list --in <project>` and look for titles starting with "Dev log —". If entries already exist, the backfill should only cover dates *before* the earliest existing entry to avoid duplicating or conflicting with entries that were written with real session context.

### 2. Group commits by date

Organize commits by their commit date. Use `git log --format="%ad %s" --date=short` to get dates and messages together.

For days with many commits, look at the diffs to understand the bigger picture rather than listing every commit individually. The goal is a readable summary of each day's work, not a commit-by-commit transcript.

### 3. Decide which dates are worth an entry

Not every day needs its own entry. Skip dates with only trivial commits (typo fixes, merge commits, version bumps) unless they're the only activity. Combine adjacent days that are part of the same body of work if that reads better. Use your judgment — the log should be useful to skim, not exhaustive.

### 4. Write entries

For each date or date range worth logging, write an entry using inferred categories and narrative bullets. Follow the same format as the `dev-log` skill — title `Dev log — YYYY-MM-DD: <short summary>` (use `YYYY-MM-DD – YYYY-MM-DD` for a combined range), body in Markdown:

```markdown
**Category Name**

- Narrative bullet explaining what changed and why (as best you can infer)
- Another bullet if needed
```

Where you can confidently infer the *why* from commit messages or code context, write it narratively. Where you can't, stick to a clear description of *what* changed — an honest "what" is better than a fabricated "why".

### 5. Review, then post to Basecamp

Show the user the drafted entries **before posting** — backfill can produce many messages at once, and they should sanity-check the inferred reasoning first. Flag any entries where you were guessing — something like "I inferred the motivation here from the diff, but you'd know better" is helpful.

Once confirmed, post each entry as its own message, oldest first (so the message board reads newest-first like the real-time log):

```bash
basecamp message "Dev log — YYYY-MM-DD: <summary>" "<body>" --in <project> --jq '.data.app_url'
```

Existing dev log messages are immutable — never edit or delete them.

### 6. Confirm

Share the message URLs so the user can spot-check what was posted.

## Handling large repos

For repos with extensive history, don't try to summarize every single day. Focus on meaningful milestones and group related work. A 2-year-old repo doesn't need 400 entries — it needs a readable narrative of how the project evolved. Aim for density over completeness.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Backfilled entries duplicate or conflict with real dev log entries | Didn't check for existing "Dev log —" messages before generating dates | Always check `basecamp messages list` first; only backfill dates before the earliest existing entry |
| Entries read as confidently wrong about motivation | Inferred a "why" the commit message/diff didn't actually support | When intent isn't clear, describe the "what" plainly instead of fabricating a "why" |
| An old repo gets hundreds of noisy entries | Every day treated as worth its own entry | Skip trivial days, combine adjacent related days, aim for density over completeness |
| Matt has to ask for a redo after messages are already live | Entries posted before he reviewed them | Always show drafted entries and wait for confirmation before posting |
| Message board reads out of chronological order | Entries posted newest-first instead of oldest-first | Post oldest first, so the board still reads newest-first overall |
| Backfilled content ends up in AGENTS.md | Confused with a repo-local log | Dev logs are Basecamp-only, same as the real-time `dev-log` skill |

## Status

Behavioral evals live in `evals/evals.json` — they test whether this skill *steers* an agent to the conventions (a test of the skill, not a consumer to keep in sync). Not part of normal backfill work; run them via the skill-crafting tooling when changing the conventions, and add an eval when a new failure mode lands.
