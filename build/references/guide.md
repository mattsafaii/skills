# Build Skill Guide

Start a build cycle. This is the moment the bet is placed — everything needed to go from "card in Up Next" to "build session running in Solo" happens here, in one command.

**Matt runs `/build` from anywhere with the Solo MCP connected** — cwd doesn't matter. The skill looks the project up explicitly and spawns the build agent into the correct Solo project, so it doesn't care where it was launched. It creates the Basecamp project, writes the PRD doc, posts the kickoff, creates the todolist, scaffolds the repo in a new workspace folder, registers it in Solo, spawns a Claude agent inside it with its first prompt, and moves the card to In Progress. Matt then switches to the project in Solo where the build session is already working.

Never start coding the build from this session — the build session must live in the project directory so its transcript, memory, and resume stay with the project. (Footnote: avoid launching `/build` from the target repo's *actively-building* agent — it works, but it's a session spawning a sibling into its own project. Anywhere else is fine.)

---

## Fixed IDs

Do not ask Matt for these:

- Account: `6191443` (Safaii Studio)
- Lab project: `46824335`
- Card table: `9768185094` (Ideas)
- Up Next column: `9768190777`
- PRD column: `9861998294`
- In Progress column: `9768185099`

---

## Workflow

### 1. Find the project to build

List cards in Up Next:

```bash
basecamp cards list --card-table 9768185094 --column 9768190777 --in 46824335 -a 6191443 --jq '.data[] | {id: .id, title: .title}'
```

If Matt named a specific project, match it. If multiple are in Up Next, show the list and ask which to start. If nothing in Up Next matches, also check the PRD column (a card is buildable straight from PRD):

```bash
basecamp cards list --card-table 9768185094 --column 9861998294 --in 46824335 -a 6191443 --jq '.data[] | {id: .id, title: .title}'
```

### 2. Read the card

```bash
basecamp cards show <card_id> --in 46824335 -a 6191443 --md
```

The card body contains the shaped pitch and the PRD (separated by `<hr>`). Read both. The PRD is everything below the `<hr>`.

### 2b. New or existing project?

A card can be a brand-new project or a follow-up cycle on an existing one (existing Basecamp project, existing repo, already in Solo). Check whether the card/PRD names an existing project or repo; if unclear, ask Matt: "New project, or a cycle on an existing one?"

**Existing project path** — confirm the Basecamp project id and repo path with Matt, then:

- **Skip:** step 4 (project creation), step 8's scaffold/solo.yml/CLAUDE.md creation/repo config init, and step 9's registration (still look up the existing Solo project id there)
- **Keep:** steps 3, 5, 6, 7, 10, 11, 12 — run them against the existing project
- **Adjust:** name things for the cycle, update the existing CLAUDE.md, and repoint the Basecamp config — details flagged per step below

### 3. Derive the todolist

From the PRD, propose a build breakdown to Matt. Present it before creating anything in Basecamp.

**Task derivation rules:**

- One task per surface (each view/page/command gets a task)
- One task for the core flow wiring (connecting surfaces end to end)
- Setup tasks first: scaffold, deploy config
- Acceptance criteria → verification tasks at the end ("Verify: [criterion]")
- Always include a near-the-end **"Finalize README"** task (real usage, install, examples — the scaffold only writes a stub). For open-core-ready or publishable repos, also add a **"Add LICENSE + NOTICE"** task (permissive license; NOTICE for any bundled third-party tools).
- For apps, CLIs, and libraries (anything with real application logic — **not** static/marketing/landing sites), add a final **"Document the codebase (run /document)"** task. The build agent invokes the `document` skill from inside the repo to generate the architecture doc set with inline diagrams into this project's Basecamp Docs. Skip it for static sites.
- Each task should be completable in a focused session (a few hours max)

**Task order:** Setup → Data model (if applicable) → Surfaces (simplest first) → Core flow → Verification

**Proposed format:**

```
Proposed build breakdown for [Project Name]:

Setup
- Scaffold repo
- Deploy config

Build
- [Surface 1]
- [Surface 2]
- Wire core flow

Verify
- Verify: [acceptance criterion 1]
- Verify: [acceptance criterion 2]
```

Also confirm the project name is resolved. If the PRD or pitch flags a name as TBD (e.g., "name may collide, decide before publishing"), ask Matt to pick one now — the name determines the folder, repo, and Solo project.

Ask: "Does this look right, or do you want to adjust anything?"

Wait for explicit approval or adjustments before touching Basecamp or the filesystem.

### 4. Create the Basecamp project

```bash
basecamp projects create "<Project Name>" -d "<one-sentence description>" -a 6191443 --json
```

Always include the description — one sentence describing what the project is, drawn from the pitch problem/solution (e.g. "Menu bar app that shows time since your last commit"). Extract the project ID from the response (`data.id`). Use this for all subsequent commands.

**Existing project:** skip — use the existing project id for all subsequent commands.

### 5. Write the PRD doc

Create a doc in the new project with the PRD content:

```bash
basecamp docs documents create "PRD" "$(cat <<'EOF'
# [Project Name] — PRD

## Overview

**Problem:** [from pitch]
**Appetite:** [from pitch]
**Stack:** [confirmed stack]

## Surfaces

- **[Surface]:** [what it is, what the user can do]

## Core Flow

1. [Step]
2. [Step]

## Data Model

- **[Model]:** [key fields]

## Acceptance Criteria

- [ ] [Binary test]
- [ ] [Binary test]

## No-gos

- [Carried from pitch]
EOF
)" --in <project_id> -a 6191443 --json
```

Omit Data Model for non-database projects.

**Existing project:** title the doc for the cycle — `"PRD: [Cycle Name]"` — so it doesn't collide with the original PRD doc.

### 6. Post the kickoff message

Post a short message to the project's Message Board summarizing what's being built:

```bash
basecamp message "<Project Name>: Cycle Kickoff" "$(cat <<'EOF'
[Kickoff message content]
EOF
)" --in <project_id> -a 6191443 --json
```

Use this structure:

```markdown
**Appetite:** [small batch (2–3 days) or big batch (1–2 weeks)]

**What we're building:** [2–3 sentence summary from the pitch problem + solution]

**Pitch + PRD:** [link to the card in the Lab Ideas board]

**Stack:** [confirmed tech stack]

**Scopes:**
- [Surface/task group 1]
- [Surface/task group 2]
- [Surface/task group 3]
```

Keep it short. This is a record of what the cycle is and why, not a spec.

**Existing project:** title it `"<Project Name>: [Cycle Name] Kickoff"`.

### 7. Create the todolist and todos

Create the todolist:

```bash
basecamp todolists create "Build" --in <project_id> -a 6191443 --json
```

**Existing project:** name the list for the cycle — `"Build: [Cycle Name]"` — instead of plain "Build".

Extract the todolist ID. Create todos in the approved order:

```bash
basecamp todo "<task>" --list <todolist_id> --in <project_id> -a 6191443 --json
```

### 8. Create the workspace and scaffold the repo

**Existing project:** the repo already exists — no scaffold, no solo.yml, no `basecamp config init`. Instead:

1. Update the existing `CLAUDE.md` with the new cycle's context (summary, surfaces, no-gos) — append or revise, don't blow away what's there. Keep the Basecamp section CLI-based; don't add IDs or URLs.
2. Repoint the Basecamp config at the new list: `cd <repo> && basecamp config set todolist_id <new_todolist_id>`
3. Commit those changes, then skip to step 9

Workspace path: `~/Code/personal/<kebab-name>`. Confirm with Matt if anything other than the default makes sense.

Don't pre-create the directory — `rails new`, `hugo new site`, and `bundle gem` create it themselves, and a pre-existing dir makes `bundle gem` prompt or fail. Only the stacks that `cd` into the dir below (11ty, Go, static) need the `mkdir` first; each command includes it.

Scaffold for the stack, using the absolute path:

**Rails:** (creates the dir)
```bash
rails new ~/Code/personal/<name> --database=sqlite3 --skip-test
```

**11ty:** (deploys to Cloudflare Pages)
```bash
mkdir -p ~/Code/personal/<name> && cd ~/Code/personal/<name> && git init && pnpm init && pnpm add @11ty/eleventy
```

**Hugo:** (creates the dir)
```bash
hugo new site ~/Code/personal/<name> --force && cd ~/Code/personal/<name> && git init
```

**Ruby gem/CLI:** (creates the dir — do not mkdir first)
```bash
cd ~/Code/personal && bundle gem <name>
```

**Go:**
```bash
mkdir -p ~/Code/personal/<name> && cd ~/Code/personal/<name> && git init && go mod init <module-path>
```

**Static (no framework):**
```bash
mkdir -p ~/Code/personal/<name> && cd ~/Code/personal/<name> && git init
```

Then write two files into the workspace:

**`solo.yml`** — local Solo tooling config; gitignored in the Basecamp repo config step below (stays on disk, not committed). Watch the YAML: `processes` is top-level, NOT nested under `name`:

```yaml
name: <name>
processes:
  Claude:
    command: claude
    auto_start: true
```

**`CLAUDE.md`** — the briefing the build session wakes up to. It must stand alone; the build session has none of this conversation's context. Include:

- One-paragraph summary of what's being built and why
- Stack, naming the deploy target (Rails → Kamal on VPS, SQLite-only; 11ty → Cloudflare Pages, pnpm). For 11ty/Rails, add a line pointing the build session at the `safaii-css` and `safaii-html` skills for CSS/markup conventions — they auto-trigger, but naming them removes the dependency on that.
- Surfaces and core flow (condensed from the PRD)
- Data model / data contract if applicable
- No-gos
- Basecamp section (no IDs or URLs — keeps them out of the committed file): a short paragraph telling the build session that the project config (account/project/todolist IDs) is already set in `.basecamp/config.json` (gitignored), so `basecamp` commands work without flags from this directory. To find the PRD doc, run `basecamp docs list` and match by title (`PRD: [Cycle Name]` for cycles); the pitch lives on the project's card.
- Solo pointer (two lines — the build session runs inside Solo, which auto-injects its own getting-started; this just nudges toward the coordination tools it might not discover):

  ```markdown
  ## Solo
  This project runs inside Solo, which manages its processes. For coordination and follow-up work, call `help(topic="coordination")` and `help(topic="timers")`.
  ```

**`README.md`** — a stub, committed (unlike `solo.yml`). This guarantees every repo has a README from the first commit; the build session fleshes it out at the end (see the README task in step 3). Generate it from the PRD — don't leave the repo bare:

```markdown
# <name>

<one-line description — the same sentence used for the Basecamp project `-d`>

<1–2 sentences: what this is and who it's for, from the pitch problem/solution.>

**Status:** in development.
```

Keep the stub short — real usage, install, and examples come at the finalize-README task once the commands actually exist.

**Basecamp repo config** — so the build session can run `basecamp` commands without `-a`/`--in` flags. Run the bundled script rather than retyping the sequence:

```bash
@scripts/init-basecamp-config.sh ~/Code/personal/<name> <project_id> <todolist_id>
```

It runs `basecamp config init` / `set account_id 6191443` / `set project_id` / `set todolist_id` / `trust`, then appends `.basecamp/` and `solo.yml` to `.gitignore`. (`trust` is only needed for authority keys, but it's harmless and future-proofs the config.) Both `.basecamp/` and `solo.yml` stay out of git — they're local session/tooling config, not project code (`solo.yml` just tells Solo to run `claude` as a process; it stays on disk so Solo keeps working, it's only untracked). Gitignoring them before the commit keeps the `git add -A` scaffold commit clean — important since these repos are often open-core-ready or public. The build session pulls the PRD/pitch via `basecamp` commands (config above), so no IDs or URLs need to be written into the committed repo.

Commit the scaffold and offer to push to GitHub:

```bash
cd ~/Code/personal/<name> && git add -A && git commit -m "Scaffold [stack]"
gh repo create <name> --private --source . --push   # creates under the gh-authed account (mattsafaii)
```

Ask before the `gh repo create` — private by default.

### 9. Register the project in Solo

**Existing project:** already registered — find its project id with `mcp__solo__list_projects` and skip to step 10.

```
mcp__solo__create_project(path: "/Users/matt/Code/personal/<name>", name: "<name>")
```

Note the returned project `id`. (The public Solo docs omit `create_project` — it exists and works; verified on Solo 0.7.1.)

Don't append Solo's MCP docs to CLAUDE.md — the build session runs inside Solo, which auto-injects its own getting-started and exposes its tools live, so a static dump just duplicates that, bloats every repo, and rots as Solo changes. The two-line Solo pointer written in step 8 is all that's needed.

If the Solo MCP isn't connected, tell Matt to add the folder in Solo with Cmd+Shift+O, and skip step 10. Note that no build agent was spawned (see step 12 handoff).

### 10. Spawn the build agent

Start the Claude session inside the new project and brief it:

1. `mcp__solo__list_agent_tools` — find the Claude agent tool id
2. `mcp__solo__spawn_agent(agent_tool_id: <id>, project_id: <solo_project_id>, name: "Build")`
3. If the response includes `agent_instructions`, prepend them to the first prompt
4. `mcp__solo__send_input(process_id: <returned process_id>, input: "Read CLAUDE.md, then start on the first todo in the Basecamp Build list. Work through the todos in order, checking each off in Basecamp as you complete it.")`

**Existing project:** always spawn a fresh agent for the cycle (named e.g. "Build: [Cycle Name]", prompt referencing the cycle's todolist) — never send the kickoff to an existing session; its context is full of the previous cycle and the prompt may interrupt it mid-task. Leave existing sessions alone — Matt often runs multiple agents in the same repo, and an idle session may just mean he stepped away. Never close one.

### 11. Move card to In Progress

```bash
basecamp cards move <card_id> --to 9768185099 --card-table 9768185094 --in 46824335 -a 6191443 --json
```

If the move returns `ok: false`, retry once — transient failures happen.

### 12. Confirm and hand off

One line: Basecamp project created, PRD doc written, [N] todos created, repo scaffolded, card moved to In Progress. Share the Basecamp project URL. Then the handoff: "Open **<name>** in Solo — the build session is already running on the first todo."

**If no agent was spawned** (Solo MCP wasn't connected, step 10 skipped): don't claim a session is running. Handoff instead: "Add **<name>** to Solo (Cmd+Shift+O), then start a Claude session and tell it: *Read CLAUDE.md, then start on the first todo in the Basecamp Build list.*"

**Existing project:** the one-liner is instead: PRD doc written, kickoff posted, [N] todos created on "Build: [Cycle Name]", CLAUDE.md updated, cycle agent spawned (or manual-start note if Solo wasn't connected), card moved to In Progress.

---

## Task derivation heuristics

- **Surfaces first, plumbing second.** Build what the user touches before the internals.
- **Verification tasks are user-facing.** "Verify: user can submit a URL and see a result" — testable by using the app.
- **Setup tasks are real tasks.** Scaffold, deploy config, and env setup take real time.
- **Keep the list short.** 8–15 tasks for small batch. 15–25 for big batch. More means tasks are too granular.
- **If no data model in PRD, skip data model task.** Don't invent a schema for a CLI tool.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 0 | New vs existing resolved before creating anything | Existing project/repo reused, not duplicated | Ask Matt; delete accidental duplicates |
| 1 | PRD read before deriving tasks | Tasks match PRD content | Re-read PRD section of card |
| 2 | One task per surface | Each PRD surface has a task | Add missing tasks |
| 3 | Verification tasks present | Each acceptance criterion has a "Verify:" task | Add them |
| 4 | Task count reasonable | 8–25 tasks | Merge too-granular or split too-large |
| 4b | Project has a description | Created with `-d`, not title-only | `basecamp projects update --description` |
| 5 | Scaffold matches stack | Command matches PRD stack | Fix scaffold command |
| 6 | Name resolved before scaffold | No TBD or "may collide" name used | Ask Matt before running |
| 7 | CLAUDE.md stands alone | Build session can start without this conversation | Add missing context |
| 7b | CLAUDE.md is ID-free | No Basecamp IDs/URLs committed — Basecamp section points at the CLI/config | Replace IDs/URLs with the CLI-based section |
| 8 | solo.yml valid | `processes:` top-level, agent auto-starts | Fix YAML nesting |
| 8b | Basecamp config set | `.basecamp/config.json` has account, project, todolist ids and is trusted | Run config init/set/trust |
| 8c | README stub committed + finalize task exists | `README.md` written in scaffold; a "Finalize README" task is in the list | Write the stub; add the task |
| 8d | solo.yml gitignored, not committed | `solo.yml` in `.gitignore`, absent from `git ls-files` | Add to `.gitignore` before the scaffold commit |
| 9 | Agent spawned and briefed | Build session running in Solo on first todo — or, if Solo wasn't connected, Matt was told to start it manually | Run step 10 |
| 10 | Card moved to In Progress | No longer in Up Next | Run move command |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

If a step fails partway through the build, stop and report exactly which resources already exist (Basecamp project, todos, repo, Solo project, spawned agent) and which don't — don't push on to later steps, and don't delete anything to clean up. Matt decides whether to resume or unwind.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Can't find PRD in card body | PRD skill not run, or card has no `<hr>` separator | Ask Matt to run `/prd` first, or check card body |
| Tasks don't match PRD | Derived from pitch instead of PRD section | Re-read below the `<hr>` |
| Too many tasks | Tasks too granular | Merge related tasks |
| Build coded in the session that ran `/build` | Forgot this is an outside-in command | Hand off to the spawned agent; never code here |
| `create_project` YAML parse error | Malformed solo.yml (`processes` nested under `name`) | Fix indentation, retry |
| Gem scaffolded with placeholder name | Skipped name resolution check | Always check for TBD names in pitch/PRD before scaffolding |
| Build session asks basic questions | CLAUDE.md too thin | Include stack, data contract, no-gos, and the CLI-based Basecamp section |
| Card stays in Up Next | Forgot move command, or transient `ok: false` | Always run move after todos created; retry once on failure |
| Wrong account on project commands | Missing `-a 6191443` | Always pass account flag |
| Duplicate Basecamp project or repo created | Skipped the new-vs-existing check (step 2b) | Check before step 4; trash the duplicate, rerun against the existing project |
| Build agent works the wrong todolist | Basecamp config still points at the old list | `basecamp config set todolist_id <new_todolist_id>` in the repo |

---

## Examples

- **Since (2026-06-03):** menu bar Go app; 15 todos (1 setup, 6 build, 8 verify) derived from an 8-criterion PRD. Built before the outside-in rework, so the workspace/Solo/spawn steps weren't exercised — task derivation and Basecamp steps are the exemplar part.
