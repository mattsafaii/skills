---
name: domain-modeling
description: Build and sharpen a project's domain model — the CONTEXT.md glossary and the docs/adr/ decision record. Use when pinning down terminology or a ubiquitous language, recording an architectural decision, or when another skill (codebase-design, tdd, diagnosing-bugs) needs the model maintained. Also "glossary", "ubiquitous language", "record a decision", or "ADR".
---

# Domain modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary isn't this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

The skills that read what this writes: `codebase-design` (the domain names good seams; existing ADRs are decisions it shouldn't re-litigate), `tdd` (test names match the domain language), and `diagnosing-bugs` (a mental model of the modules involved).

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When a term is used in a way that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When a vague or overloaded term comes up, propose a precise canonical one. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe the edge cases and force precision about the boundaries between concepts.

### Cross-reference with code

When someone states how something works, check whether the code agrees. If you find a contradiction, surface it: "The code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. It is a glossary and nothing else — not a spec, not a scratch pad, not a home for implementation decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and one was picked for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](ADR-FORMAT.md).
