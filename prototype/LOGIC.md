# Logic prototype

A tiny interactive terminal app that lets you drive a state model by hand. Use this when the question is about **business logic, state transitions, or data shape** — the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where…"
- "I want to feel out what the API should look like before writing it."
- Anything where you want to **press buttons and watch state change**.

If the question is "what should this look like" — wrong branch. Use `ui-mockup`.

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping — one paragraph, in the prototype's README or a comment at the top of the file. A logic prototype that answers the wrong question is pure waste; make the question explicit so it can be checked later, whether Matt is watching now or returning to it AFK.

### 2. Pick the language

Use whatever the host project uses. If the project has no obvious runtime (e.g. a docs repo), ask. Match the project's existing tooling — don't add a new package manager or runtime just for the prototype.

### 3. Isolate the logic in a portable module

Put the actual logic — the bit answering the question — behind a small, pure interface that could be lifted out and dropped into the real codebase later. The TUI around it is throwaway; the logic module shouldn't be.

The right shape depends on the question:

- **A pure reducer** — `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine** — explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state — just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question, *not* whichever is easiest to wire to a TUI. Keep it pure: no I/O, no terminal code, no `console.log` for control flow. The TUI imports it and calls in; nothing flows the other direction.

This is what makes the prototype useful past its own lifetime: once the question is answered, the validated reducer / machine / function set lifts into the real module on its own.

### 4. Build the smallest TUI that exposes the state

Build it as a **lightweight TUI** — on every tick, clear the screen (`console.clear()`, `print("\033[2J\033[H")`, equivalent) and re-render the whole frame. You should always see one stable view, not an ever-growing scrollback.

Each frame has two parts, in this order:

1. **Current state**, pretty-printed and diff-friendly (one field per line, or formatted JSON). Use **bold** for field names or section headers and **dim** for less important context (timestamps, IDs, derived values). Native ANSI escapes are fine — `\x1b[1m` bold, `\x1b[2m` dim, `\x1b[0m` reset. No styling library unless the project already has one.
2. **Keyboard shortcuts**, listed at the bottom: `[a] add user  [d] delete user  [t] tick clock  [q] quit`.

Behaviour:

1. **Initialise state** — a single in-memory object/struct. Render the first frame on start.
2. **Read one keystroke (or one line)** at a time, dispatch to a handler that mutates state.
3. **Re-render** the full frame after every action — replace, don't append.
4. **Loop until quit.**

The whole frame should fit on one screen.

### 5. Make it runnable in one command

Add a script to the project's existing task runner (`package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`). Run it with `pnpm run <prototype-name>` or equivalent — never a path to remember. If there's no task runner, put the command at the top of the prototype's README.

### 6. Hand it over

Give Matt the run command. He drives it himself; the interesting moments are when he says "wait, that shouldn't be possible" or "huh, I assumed X would be different" — those are the bugs in the *idea*, which is the whole point. If he wants new actions, add them. Prototypes evolve.

### 7. Capture the answer and the prototype

Once it has answered its question, capture the answer, then capture the prototype the way [SKILL.md](SKILL.md) describes. The logic-specific mapping: the validated reducer / machine / function set lifts into the real module (the decision, absorbed); the TUI shell rides along to the throwaway branch that keeps the prototype as a primary source.

## Anti-patterns

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use an in-memory store unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." It answers one question.
- **Don't blur the logic and the TUI.** If the reducer / machine references `console.log`, prompts, or terminal escapes, it's no longer portable. Keep the TUI a thin shell over a pure module.
- **Don't ship the TUI shell to production.** The shell is built to be driven by hand from a terminal. The logic module behind it is the part worth keeping.
