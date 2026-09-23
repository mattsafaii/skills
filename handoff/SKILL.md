---
name: handoff
description: Compact the current conversation into a handoff document for a fresh agent or session to pick up. Use before ending a session another will continue, or when context is getting long.
triggers:
  - handoff
  - hand this off
  - write a handoff
  - continue in a new session
disable-model-invocation: true
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it as **`HANDOFF.md` at the workspace root** — one file, overwritten each session, never a dated collection. Not inside the repo (it would pollute the source and get committed) and not the OS temp directory (untracked scratch — nothing cleans it reliably, nothing routes to it, so a handoff there sits orphaned rather than read). If the workspace root *is* the repo, temp is the fallback; accept that the file may not be found again.

Include:

- **What's being worked on, and where** — the repo path, the Basecamp project / PRD, the Lab card.
- **Where things stand** — done, in progress, blocked.
- **The next concrete step.**
- **Suggested skills** — the ones the next agent should invoke (e.g. `code-review`, `tdd`, `diagnosing-bugs`, `herdr`).
- **Open questions / decisions pending.**

Rules:

- Don't duplicate what already lives in an artifact — the PRD, the Lab card, `AGENTS.md`, commits, the Basecamp todos. Reference them by path or URL instead.
- The handoff is the tactical "what's in flight" layer, never a source of truth. The durable record is Basecamp and the repo's `AGENTS.md` — say so in a line at the top of the file, so the next agent knows which wins.
- **Date the file** (`Written YYYY-MM-DD` at the top). A persisted handoff is only safe to read later if its age is visible; an undated one reads as current forever.
- **Delete it when the work it describes finishes.** The file exists only while something is in flight — overwrite it when work continues, remove it when it lands. A handoff left behind after completion is the stale document the date line only partly mitigates.
- Redact secrets: API keys, passwords, personally identifiable information.
- If Matt passed arguments, treat them as what the next session will focus on and tailor the doc to that.
