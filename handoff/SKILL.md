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

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to the OS temporary directory, not the workspace.

Include:

- **What's being worked on, and where** — the repo path, the Basecamp project / PRD, the Lab card.
- **Where things stand** — done, in progress, blocked.
- **The next concrete step.**
- **Suggested skills** — the ones the next agent should invoke (e.g. `code-review`, `tdd`, `diagnosing-bugs`, `herdr`).
- **Open questions / decisions pending.**

Rules:

- Don't duplicate what already lives in an artifact — the PRD, the Lab card, `AGENTS.md`, commits, the Basecamp todos. Reference them by path or URL instead.
- Redact secrets: API keys, passwords, personally identifiable information.
- If Matt passed arguments, treat them as what the next session will focus on and tailor the doc to that.
