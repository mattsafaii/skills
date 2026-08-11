---
name: remember
description: Write a durable, curated memory file to the tool-agnostic agent-memory store (~/.agents/memory/curated/, indexed by qmd as the "agent-memory" collection). Two triggers — explicit ("remember this", "save this to memory", "/remember") and proactive: when you notice something memory-worthy (a correction, a confirmed non-obvious decision, an ongoing project fact), offer to save it and wait for a yes before writing. Never write silently.
---

# Remember Skill

Write one durable fact to `~/.agents/memory/curated/`, the tool-agnostic memory store. Deliberately explicit-only: nothing gets written without the user saying yes, either because they asked directly or because they confirmed your offer.

## When to trigger

1. **Explicit** — user says "remember this", "save this to memory", "/remember [thing]". Write immediately, no confirmation needed — asking was the confirmation.
2. **Proactive** — you notice something worth keeping: a correction ("no, don't do X"), a confirmed judgment call that isn't obvious from the code, an ongoing project fact (deadline, decision, who's doing what). Offer it in one line — "Want me to remember that [X]?" — and only write on a yes. If the user is mid-task, don't interrupt; ask at a natural pause or fold it into your next reply.

## What NOT to save

Same exclusions as before: no code patterns/architecture/file paths (derivable from the repo), no git history, no debugging recipes, no ephemeral task state, nothing already in an AGENTS.md. If asked to save something like that, say why it doesn't need saving instead of writing it anyway.

## Memory types

- **user** — who the user is, their role, preferences, knowledge level
- **feedback** — corrections or confirmations about how to work; always include *why*
- **project** — ongoing work, decisions, deadlines, who's doing what; convert relative dates ("Thursday") to absolute ones
- **reference** — pointers to where information lives in other systems (Linear, Slack, a dashboard)

## Writing a memory

1. Check `~/.agents/memory/curated/MEMORY.md` and grep the directory for anything covering the same ground — update the existing file instead of duplicating.
2. Write the file as `~/.agents/memory/curated/<type>_<slug>.md`:

```markdown
---
name: {{short-kebab-case-slug}}
description: {{one-line summary, specific enough to judge relevance later}}
metadata:
  type: {{user, feedback, project, reference}}
---

{{content — for feedback/project, use a rule/fact line then **Why:** and **How to apply:** lines. Link related memories with [[other-slug]].}}
```

3. Add a one-line pointer to `~/.agents/memory/curated/MEMORY.md`: `- [Title](file.md) — one-line hook`. Never write memory content directly into `MEMORY.md` — it's an index, kept under ~150 chars/line.
4. No need to reindex qmd manually — the session-end hook already triggers `~/.agents/memory/reindex.sh` on a throttle.

## Updating vs. creating

If the new fact corrects or extends an existing memory file, edit that file in place rather than creating a near-duplicate. Remove memories that turn out to be wrong.
