---
name: backlog
description: Plan and work a post-launch change on an already-shipped project — scope it briefly, break it into cards on the project's Backlog table, work through them normally, and close out with a review. Use when Matt wants to add a feature, do a refactor, or make some other non-trivial change to a project that's already been built, after /build's original cycle is done. Not for brand-new projects — that's /build's job.
---

# Backlog

The gap this fills: `/build` plans and ships a project's first cycle, but once it's live there's no structured way to plan the next change — a feature, a refactor, whatever comes up a week or a month later. This skill is that: deliberately lightweight, no interviews, no formal spec, no ceremony beyond what a normal small project needs.

## Workflow

### 1. Find the project and its Backlog table

Get the project from `.basecamp/config.json` in the repo root. If there's no config, find it with `basecamp projects list` or ask Matt.

Check the project's dock for a card table tool: `basecamp projects show <project> --json`, look for a `kanban_board` entry. **Don't rely on `basecamp cards columns` alone to decide whether one exists** — it can return data for a card table that isn't actually enabled in the dock (learned the hard way testing on Hookah Hunt).

If there's no `kanban_board` in the dock, this project needs the Card Table tool added once — the `basecamp` CLI can't add a new dock tool, only manage one that already exists. Ask Matt to add it via the Basecamp UI (project → "+ Add a tool from the dock" → Card Table). Basecamp seeds a default set of columns (Triage/Not now/Figuring it out/In progress/Done, roughly) — rename the first (Triage-type) column to "Backlog" if it isn't already, and use whatever "in progress"/"done" columns exist. Don't force it down to exactly three columns; the extra default ones are harmless sitting empty.

### 2. Scope the change

Talk it through briefly — what's changing, what's explicitly not. This is a short conversation, not an interview. Post-launch changes are usually clearer-cut than a brand-new feature, so don't manufacture ambiguity that isn't there — if Matt already said what he wants, confirm and move on rather than asking a checklist of questions.

One exception: when the approach itself is unsettled — two plausible ways to build it and no clear winner — don't scope on top of the guess. Run `grilling` to work the options down, `codebase-design` when the question is where the seam goes, or `prototype` to check whether a data shape or interface feels right. Scope from the answer. The card carries the outcome — no research doc, no new artifact.

### 3. Break it into cards

Create one card per session-sized chunk of work in the **Backlog** column:

```bash
basecamp cards create "Title" "<p>What this delivers.</p>" --in <project> --column <backlog_column_id>
```

Each card describes the end-to-end behavior it delivers, not a layer-by-layer task list. If one card genuinely can't start before another finishes, say so in the card body ("Blocked by: <other card title>") — plain prose, not a formal mechanism. Don't invent dependencies that aren't real; most small changes have none.

### 4. Work through the cards

Move a card to **In Progress** when starting it (`basecamp cards move <id> --to <in_progress_column_id> --in <project>`). Write the code and its tests the normal way — no enforced test-first discipline, no special process. One card at a time.

### 5. Close out each card

Comment the commit SHA, then mark it done:

```bash
basecamp comments create <card_id> "Commit <sha>: <message>" --in <project>
basecamp cards done <card_id> --in <project>
```

Same convention as todos elsewhere — comment before complete, never complete silently.

### 6. Review the whole change

Once every card for this change is done, run the `code-review` skill on the full diff for this change: Spec against the step-2 scoping conversation (pass it as the spec), Standards against the repo's conventions. Both reviewers are read-only — report gaps, don't fix them. Fix what it finds.

### 7. Confirm

One line: which cards were completed, and a link to the Backlog table. Mention anything the reviewers flagged that's still open.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cards post to the wrong project | No `.basecamp/config.json` in the repo root | Always check config first; if missing, run `basecamp projects list` or ask Matt — never guess |
| Can't find the Backlog table | Project never had the Card Table tool added | Ask Matt to add it once via the Basecamp UI — the CLI can't create a card table, only manage one that exists |
| Scoping turns into a full interview | Treated a clear-cut change like an ambiguous new feature | Post-launch changes are usually clearer-cut — confirm what Matt already said and move on |
| Card scoped as if clear-cut, then the approach shifts mid-build | The change was genuinely uncertain about approach, but scoping skipped straight to cards | Run `grilling` (or `codebase-design`/`prototype`) first, then scope from the answer |
| Cards accumulate fake dependencies | Invented a "Blocked by" note for ordering preference, not a real gate | Only note a real blocker; most small changes have none |
| Reviewer rewrites the code | Reviewer brief omitted read-only scope | Brief says report gaps, don't fix them; apply the fixes yourself after |
| Build agent (or you) waits on a reviewer forever | Reviewer spawned with the wrong tool, so it never went idle | Spawn both reviewers as read-only Pi one-shots (`pi --tools read,grep,find,ls --print`) — see the herdr and code-review skills |
| Standards reviewer invents conventions the repo doesn't have | No AGENTS.md or stack-specific skill to point it at | Fall back to a plain code-smell pass instead of guessing at house style |
| Card completed with no SHA comment | Marked done directly instead of commenting first | Comment the SHA now; comment before complete from here on |
