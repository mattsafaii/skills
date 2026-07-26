# PRD Skill Guide

Turn a shaped pitch into a build-ready PRD. The output is the PRD appended to the shaped card body — the card becomes pitch + PRD in one place. No project creation, no workspace, no todolist. That happens in `/build`.

---

## What a PRD is

The pitch answers: *what to build and why, at macro level.*
The PRD answers: *what exists, how it works, and what done looks like — specific enough that Claude can build without asking basic questions, rough enough that Claude still makes implementation decisions.*

A PRD that names every field and specifies every UI behavior is a spec — too much. A PRD that just restates the pitch is too little. The right level: Claude reads it and knows exactly what to build, but still has room for judgment on how.

---

## Fixed IDs

Do not ask Matt for these:

- Account: `6191443` (Safaii Studio)
- Lab project: `46824335`
- Card table: `9768185094` (Ideas)
- Shaped column: `9768185098`
- PRD column: `9861998294`

---

## Workflow

### 1. Identify the idea

If Matt named a specific idea, find the card — scoped to the Shaped column so a title match can't accidentally hit a card from another column (Ideas, PRD, Shipped, Graveyard, etc.):

```bash
basecamp cards list --card-table 9768185094 --column 9768185098 --in 46824335 -a 6191443 --jq '.data[] | {id: .id, title: .title}'
```

Match by title. Then fetch the full card:

```bash
basecamp cards show <card_id> --in 46824335 -a 6191443 --md
```

Read the full shaped pitch before asking anything. Don't re-ask what's already answered.

If this is a cycle on an existing project, also read the repo (`~/Code/personal/<name>`) before asking questions — don't re-ask what the code already answers, and verify the pitch's assumptions against what's actually built.

### 2. Work through PRD sections conversationally

Use the shaped pitch as the foundation. Extract what's already specified. Only ask about what's genuinely missing or needs more detail for building.

**Tech stack**

Confirm from the pitch. No question needed unless ambiguous.

**Surfaces**

What views/pages/screens/commands exist? For each one: what's on it, what can the user do?

Keep it breadboard level — not UI layout, just what exists and what affordances are present. If the pitch already names surfaces clearly, confirm and move on.

**Core flows**

Walk the main use case end to end from the user's perspective. Step by step. This is the scenario Claude will make sure works.

- Start from the entry point (URL, CLI command, etc.)
- Walk to the completed action
- Note branches or edge cases that matter for v1

**Data model**

Key models and their important fields. Rough — not a full schema. Skip for non-database projects (CLI tools, static sites).

- What are the models?
- What fields matter? (Not every column — just what isn't obvious)
- What are the key relationships?

**Acceptance criteria**

Binary tests for done. Either this works or it doesn't.

- 5–8 things that must be true when the project ships
- Each testable by running the app, not by reading the code
- **Each one names how it gets checked** — either a command that proves it, or the manual step someone takes. This is what lets `/build` turn the mechanical ones into real tests instead of inventing tests later against finished code.

Two kinds, and the difference matters downstream:

| Kind | Check looks like | Becomes |
|---|---|---|
| Mechanical — parsing, calculations, data flow, CLI output, API shape | a command: `go test ./...`, `bin/rails test`, `zeni "tacos 12 cash"` prints the right entry | an automated test, written with the code |
| Visual or interactive — layout, a browser flow, something you look at | a manual step: "open /jobs, submit the form, see the result" | a manual `Verify:` todo |

Don't force the mechanical kind. A static site's criteria are nearly all visual, and that's correct.

**What can go wrong**

3–5 things, no more. Empty states, bad input, and the one failure path that actually matters for v1.

Code written from a spec that only describes the happy path is happy-path code. Naming the failures here is the cheapest quality fix in the whole pipeline — two questions during this conversation, and the build agent handles them by default instead of being told about them in review.

Ask: what does the user see with no data yet? What happens when the input is junk? What breaks that we can't just let crash?

Carry no-gos over rather than repeating them here — anything deliberately out of scope isn't a failure.

### 3. Check: is this build-ready?

Before presenting:

- **Specific enough?** Could Claude build this without asking "what models exist?" or "what does the main flow do?"
- **Rough enough?** Does it specify button labels, exact field names, or pixel layout? Strip back if so.
- **Complete?** Does every surface have a purpose? Does the core flow work end to end? Are acceptance criteria testable?
- **Checkable?** Does every acceptance criterion name its check — a command or a manual step?
- **Honest about failure?** Does "What can go wrong" name real failures, not restated no-gos?

### 4. Present the full PRD

Show Matt the PRD in readable form. Ask: "Add this to the card and move to PRD?"

Wait for explicit approval before touching Basecamp.

### 5. Update the card and move to PRD column

Append the PRD below the existing pitch HTML using `<hr>` as a separator:

```bash
basecamp cards update <card_id> --body "$(cat <<'EOF'
[existing pitch HTML]
<hr>
<h2>PRD</h2>

<h3>Tech Stack</h3>
<p>[confirmed stack]</p>

<h3>Surfaces</h3>
<ul>
<li><strong>[Surface]:</strong> [what it is, what the user can do]</li>
</ul>

<h3>Core Flow</h3>
<ol>
<li>[Step]</li>
</ol>

<h3>Data Model</h3>
<ul>
<li><strong>[Model]:</strong> [key fields]</li>
</ul>

<h3>Acceptance Criteria</h3>
<ul>
<li>[Binary test] — <em>check:</em> [command that proves it, or the manual step]</li>
</ul>

<h3>What Can Go Wrong</h3>
<ul>
<li><strong>[Situation]:</strong> [what the code should do instead of breaking]</li>
</ul>

<h3>No-gos</h3>
<ul>
<li>[Carried from pitch]</li>
</ul>
EOF
)" --in 46824335 -a 6191443 --json
```

Omit the Data Model section for non-database projects.

Move the card to the PRD column:

```bash
basecamp cards move <card_id> --to 9861998294 --card-table 9768185094 --in 46824335 -a 6191443 --json
```

### 6. Confirm

One line: PRD added to card, moved to PRD column. Done — the card is ready for `/build` when Matt bets on it.

---

## PRD heuristics

- **Derive, don't ask.** If the pitch specifies the stack, surfaces, or flows — extract and confirm, don't re-ask.
- **Surfaces ≠ pages.** A CLI has commands. A static site has sections. Match the terminology to the project type.
- **Data model is optional.** Skip for CLI tools, static sites, scripts.
- **Acceptance criteria are user-facing.** "User can submit a URL and see a result" not "job processes correctly."
- **Every criterion names its check.** A command or a manual step. Without it, `/build` has to guess which criteria deserve tests.
- **Failures are specific.** "Empty library shows a first-run message" beats "handles errors gracefully" — the second one builds nothing.
- **No-gos travel from the pitch.** Always carry them forward.
- **The PRD stands alone.** `/build` reads it without the conversation context. It must be self-contained.
- **No file paths or code snippets.** The PRD outlives them — they go stale fast. Mostly a cycle-PRD risk.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 1 | Tech stack confirmed | Named explicitly | Derive from pitch |
| 2 | All surfaces named | Each has a purpose | Add missing surfaces |
| 3 | Core flow is step-by-step | Numbered sequence | Rewrite as steps |
| 4 | Acceptance criteria are binary | Each is a yes/no test | Rewrite as pass/fail |
| 4b | Each criterion names its check | A command or a manual step per criterion | Add the check |
| 4c | What Can Go Wrong present | 3–5 real failures, not restated no-gos | Ask the three questions in step 2 |
| 5 | No-gos carried from pitch | All pitch no-gos present | Add missing ones |
| 6 | PRD stands alone | Readable without the conversation | Add missing context |
| 7 | Not a spec | No field-level detail, no UI layout | Strip back |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| PRD reads like the pitch | Didn't add implementation detail | Work through surfaces, flows, data model |
| PRD reads like a spec | Too much detail | Strip field names, UI descriptions |
| Acceptance criteria are vague | Written as features not tests | Rewrite: "User can X" not "X is implemented" |
| Every criterion gets a command, including the visual ones | Forced the mechanical kind everywhere | Visual and interactive criteria take a manual step — that's the correct answer, not a gap |
| What Can Go Wrong repeats the no-gos | Confused out-of-scope with failure | No-gos are what we chose not to build; failures are what the built thing must survive |
| Build ships happy-path only | PRD never named the failures | Both are the same miss — fix it here, not in review |
| Card body wipes the pitch | Didn't include existing HTML in update | Always fetch card first, include existing body |
| Forgot Data Model section | Skipped for a project that needs it | Check if it's a database-backed project |

---

## Exemplars

- *(none yet — first PRD written becomes Exemplar 1)*
