# Design it twice

When exploring alternative interfaces for a chosen deepening candidate, draft several in parallel — your first idea is unlikely to be the best. Based on "Design It Twice" (Ousterhout).

Uses the vocabulary in [SKILL.md](SKILL.md) — **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

### 1. Frame the problem space

Before spawning anything, write a short, user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough illustrative code sketch to ground the constraints — not a proposal, just a way to make the constraints concrete

Show this, then immediately begin step 2. Matt reads and thinks while the drafts are being written in parallel.

### 2. Draft the candidates in parallel

Spawn 3+ sub-agents — the Task tool's `general-purpose` agents work, or sibling Herdr panes if you want them as visible sessions. Each must produce a **radically different** interface for the deepened module.

Prompt each with a separate technical brief (file paths, coupling details, dependency category from [DEEPENING.md](DEEPENING.md), what sits behind the seam). Give each a different design constraint:

- Agent 1: "Minimize the interface — aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility — support many use cases and extension."
- Agent 3: "Optimise for the most common caller — make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Include both this skill's vocabulary and `CONTEXT.md` vocabulary in the brief so each candidate names things consistently.

Each candidate outputs:

1. Interface (types, methods, params — plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [DEEPENING.md](DEEPENING.md))
5. Trade-offs — where leverage is high, where it's thin

### 3. Present and compare

Present the designs sequentially so Matt can absorb each one, then compare in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

Then give your own recommendation: which is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — a strong read, not a menu.
