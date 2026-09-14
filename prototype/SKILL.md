---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when Matt wants to sanity-check whether a state model, data shape, or API feels right. For "what should this look like?", use variant (real page) or ui-mockup (standalone HTML) instead.
triggers:
  - prototype this
  - throwaway prototype
  - does this state model
  - feel out the API
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). A tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper. This is the branch this skill owns.
- **"What should this look like?"** → not here. Use the `ui-mockup` skill to explore a few variations in one standalone HTML file.

If the question is genuinely ambiguous, default by the surrounding code — a backend module → logic, a page or component → the UI tools — and state the assumption at the top.

## Rules that apply to any prototype

1. **Throwaway from day one, clearly marked.** Put it near where it will be used, named so a reader sees it's a prototype, following the project's existing structure.
2. **One command to run.** Wire it into the project's task runner (`pnpm <name>`, `make <name>`) so Matt can start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is usually the thing being checked, not a dependency. If the question involves the database, use a scratch DB or a clearly-marked throwaway file.
4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions.
5. **Surface the state.** After every action, print the full relevant state so the change is visible.
6. **Capture it when done.** Fold the validated decision into the real code, then commit the prototype itself to a throwaway branch (out of main) and leave a context pointer on the relevant todo. Capture the answer — the verdict and the question it settled — too. Main keeps only the validated decision.
