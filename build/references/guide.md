# Build Skill Guide

Start a build cycle. This is the moment the bet is placed — everything needed to go from "card in Up Next" to "build session running in Herdr" happens here, in one command.

**Matt runs `/build` from anywhere inside Herdr** — cwd doesn't matter. The skill looks the project up explicitly and spawns the build agent into the correct Herdr workspace, so it doesn't care where it was launched. It creates the Basecamp project, writes the PRD doc, posts the kickoff, creates the todolist, scaffolds the repo in a new workspace folder, creates (or finds) the project's Herdr workspace, starts an OpenCode agent in it with its first prompt, and moves the card to In Progress. Matt then switches to the project's Herdr workspace where the build session is already working.

Never start coding the build from this session — the build session must live in the project directory so its transcript, memory, and resume stay with the project. (Footnote: avoid launching `/build` from the target repo's *actively-building* agent — it works, but it's a session spawning a sibling into its own project. Anywhere else is fine.)

---

## Fixed IDs

Do not ask Matt for these:

- Account: `6191443` (Safaii Studio)
- Lab Build template: `48254447`
- Lab project: `46824335`
- Card table: `9768185094` (Ideas)
- Up Next column: `9768190777`
- PRD column: `9861998294`
- In Progress column: `9768185099`
- Shipped column: `9768185101`

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

Same handling here as Up Next: if Matt named a project, match it; if multiple unnamed cards are in PRD, show the list and ask which to start.

### 2. Read the card

```bash
basecamp cards show <card_id> --in 46824335 -a 6191443 --md
```

The card body contains the shaped pitch and the PRD (separated by `<hr>`). Read both. The PRD is everything below the `<hr>`.

### 2b. New or existing project?

A card can be a brand-new project or a follow-up cycle on an existing one (existing Basecamp project, existing repo, already in Herdr). Check whether the card/PRD names an existing project or repo; if unclear, ask Matt: "New project, or a cycle on an existing one?"

**Existing project path** — identify the repo (from the card/PRD, or ask Matt which project this cycle is for), then read its Basecamp ids straight from the repo instead of asking Matt to recite them:

```bash
cd <repo_path> && basecamp config show --json
```

This gives `project_id` (and the prior `todolist_id`, which gets repointed in step 8). Then:

- **Skip:** step 4 (project creation), step 8's scaffold/AGENTS.md creation/repo config init, and step 9's workspace creation (still find the existing Herdr workspace there)
- **Keep:** steps 3, 5, 6, 7, 10, 11, 12 — run them against the existing project
- **Adjust:** name things for the cycle, update the existing AGENTS.md, and repoint the Basecamp config — details flagged per step below

### 3. Derive the todolist

**First, check the PRD's vintage.** PRDs written before 2026-07-25 have no `check:` on their acceptance criteria, no "What Can Go Wrong", and no "Gated Decision" — the three things this step reads. Deriving from one anyway produces a build that looks fine and quietly loses the tests, the failure handling, and the spike ordering.

Look for `check:` in the card's acceptance criteria. If it's missing, stop and tell Matt:

> This PRD predates the checks-and-failures format. I can backfill it here — which criteria are provable by command and what proves them, three to five things that can go wrong, and any decision gated on a spike — or you can rerun `/prd`. Backfilling takes a few minutes and I'll write it back to the card.

Default to backfilling: the information is a short conversation, and a full `/prd` rerun redoes work that's already good. Whichever way it goes, **the card gets updated before todos are derived** — the card stays the record, and a build deriving from sections that only ever existed in a chat is exactly the drift this pipeline avoids. Follow the `prd` skill's rules for those three sections; append to the existing PRD rather than rewriting it.

Then, from the PRD, propose a build breakdown to Matt. Present it before creating anything in Basecamp.

**Task derivation rules:**

- **A task is a vertical slice, not a layer and not a screen.** Each slice is the thinnest complete path through part of the core flow — it cuts through every layer it needs (data, logic, the surface the user touches) and runs end to end. "The model" and "the list page" are not tasks; "a job shows on the board and opens its detail" is.
- **The first slice is the tracer bullet: the thinnest path that retires the biggest risk.** Pick the slice that exercises the architecture's riskiest seam — the external API, the auth flow, the awkward data shape, the hardest core-flow step — not the easiest screen. If that path works end to end, the rest is filling in; if it doesn't, you want to know now, before three easy screens sit on a foundation that won't hold. Its `Done when:` names the whole path.
- **A slice may span surfaces and stub what isn't built yet.** When the core flow crosses several surfaces, the first slice can walk all of them with stubbed internals ("board shows a hardcoded job, clicking opens detail"), and later slices replace the stubs with real data. Thinnest complete path, not one screen doing everything.
- **Surfaces are the coverage inventory, not the task list.** Every surface in the PRD must be reached by some slice, but a slice is not one surface and a surface is not one slice. Use the surfaces to check coverage; use the core flow to cut the slices.
- **Every slice ends with the app running and its suite green.** No task leaves the app broken — that is what makes a slice demoable and what keeps each commit a safe checkpoint.
- One task for the data model (schema, migrations) when the PRD has a Data Model section — skip it entirely if the PRD doesn't (see heuristics below). A small shared schema goes up front; for a larger one, a slice may add the tables it needs rather than waiting for a complete model.
- **Cycle builds only — prefactor first.** Open with the task that makes the change easy (extract the method, introduce the seam where the new code plugs in, add the test), before the feature work: *make the change easy, then make the easy change.* A prefactor keeps behavior identical, so it's safe alone; skipping it tangles the refactor and the feature into one risky change.
- **Cycle builds only — one wide mechanical change is not a slice.** A rename or retype whose blast radius spans the codebase can't land green in one step, so sequence it expand → migrate → contract: add the new form beside the old (expand), move call sites over in batches sized by blast radius with the app green after each (migrate), then delete the old form (contract). Each batch is its own task.
- Setup tasks first: scaffold, deploy config
- **A PRD with a Gated Decision section gets a spike task, first in the list after "Scaffold repo"** — before deploy config, before the data model, before any surface. Nothing else in the build is trustworthy until the gate is answered, and a spike run late is just rework. Title it `Spike: [the question]`, with this description:

  ```
  Question: [from the PRD]
  Settled by: [the fixture, measurement, or threshold]
  Fallback: [what gets built if the answer is no]

  Time-box: one session. Throw the spike code away — this answers a question, it
  doesn't start the build.

  Done when: the answer is recorded as a comment on this todo and noted in the
  repo's AGENTS.md, naming which path the build takes. If the fallback wins, say so
  before moving on. If the time-box runs out with no clear answer, stop
  and ask Matt rather than picking a side.
  ```

  The rest of the todolist is written path-independent — that's the point of the PRD naming what holds either way. If the spike's outcome would actually reshape the surfaces or the data model, the pitch wasn't shaped tightly enough; stop and tell Matt rather than deriving todos on top of an unknown.
- Acceptance criteria → split by the kind the PRD assigned them. **Mechanical** criteria (a command proves them) fold into the build todo that implements them, as a `Test:` line — the test gets written with the code. **Visual or interactive** criteria become verification tasks at the end ("Verify: [criterion]"), as before. A PRD whose criteria are all visual — a static site, say — produces no test lines at all, and that's right.
- **Build-section todos (slices, data model) get a description**, passed via `basecamp todo`'s `--description` flag — pulled straight from the PRD, not newly authored: the end-to-end behaviour each slice delivers (drawn from the PRD's Core Flow steps it covers) for slice tasks, the "[Model]: [key fields]" lines for the data model task. Setup and Verify todos stay title-only — the title already says everything ("Scaffold repo", "Verify: [criterion]"); a description there would just restate it.
- **Every build-section description ends with a `Done when:` line** — one sentence naming the observable result, taken from the PRD rather than invented. It tells the build agent when to stop and gives Matt a fixed thing to review against. Then, where a mechanical criterion belongs to that todo, a `Test:` line naming the criterion and the command that proves it:

  ```
  Job board. Lists open jobs, each linking to its detail page.

  Done when: /jobs lists every open job newest first, each row links to its detail page, and an empty board shows the first-run message.
  Test: closed jobs never appear on the board — bin/rails test test/models/job_test.rb
  ```

  The `Done when:` line absorbed the empty-state failure; the `Test:` line covers the one thing you can't confirm by looking at the page.

- Anything in the PRD's **What Can Go Wrong** section attaches to the todo that owns it, as part of `Done when:` — the empty state belongs to the surface that shows it, the bad-input path to the flow that takes the input. Don't make failure handling its own todo; it's part of the work, not a follow-up.
- Add a close-out **"Write QA plan"** task, placed right after the Verify tasks and before "Review against the PRD", with this description:

  ```
  Consolidate every Verify task above into one walkthrough: the exact steps to
  reproduce each (URL to visit, what to click, what input to give) and the
  observable result that proves it. Post it as a comment on this todo, not a
  new doc.

  This isn't a restatement of the acceptance criteria — it's a script Matt can
  follow without re-deriving what "verify X" means. Order the steps so later
  ones don't require redoing earlier setup.

  Done when: the comment lets Matt walk the whole app once, top to bottom,
  checking every Verify criterion, without opening the code.
  ```

  The individual "Verify:" todos stay as the acceptance-criteria record; this task turns them into one ordered script instead of leaving Matt to reconstruct the walkthrough himself. Skip it for a project with one or two Verify tasks — the consolidation isn't worth a todo when there's nothing to order.
- Add a close-out **"Review against the PRD"** task, placed before Finalize README, with this description:

  ```
  Run the `code-review` skill on the diff since the scaffold commit (the PRD is
  its spec source). It reviews on two axes — Standards against this repo's
  conventions, Spec against the PRD — each in its own Herdr reviewer, read-only:
  report gaps, don't fix them. Fix what they find, then commit.

  Done when: both reports are in hand and every finding is fixed or dismissed.
  ```

  Two reviewers reading, not a fleet writing — the build stays single-agent. Skip it for static sites with no application logic.
- Always include a near-the-end **"Finalize README"** task (real usage, install, examples — the scaffold only writes a stub). For open-core-ready or publishable repos, also add a **"Add LICENSE + NOTICE"** task (permissive license; NOTICE for any bundled third-party tools).
- For apps, CLIs, and libraries (anything with real application logic — **not** static/marketing/landing sites), add a final **"Document the codebase (run /document)"** task. The build agent invokes the `document` skill from inside the repo to generate the architecture doc set with inline diagrams into this project's Basecamp Docs. Skip it for static sites.
- Each task should be completable in a focused session (a few hours max) and leave the app running

**Task order:** Scaffold → Spike (if the PRD gates one) → rest of Setup → Prefactor (cycle builds only) → Data model (if applicable) → First slice, end-to-end (the tracer bullet, riskiest path) → remaining slices (each extending the working path) → Verify core flow end-to-end → Verification (per-criterion) → Write QA plan (if there are enough Verify tasks to warrant it) → close-out (Review against the PRD, Finalize README, LICENSE+NOTICE, Document the codebase — whichever apply)

**Proposed format:**

```
Proposed build breakdown for [Project Name]:

Setup
- Scaffold repo
- Spike: [the gated question]          (only when the PRD gates one)
- Deploy config

Data model
- [Schema / migrations]

Build
- [First slice] — end-to-end (tracer bullet)     (cycle: prefactor task(s) come first)
- [Slice 2]
- [Slice 3]

Verify
- Verify: core flow end-to-end
- Verify: [visual/interactive criterion 1]
- Verify: [visual/interactive criterion 2]

Close-out
- Write QA plan          (only when there are enough Verify tasks to warrant consolidating)
- Review against the PRD
- Finalize README
```

Mechanical criteria don't appear as their own line — they ride on the slice that implements them. Say so when presenting, so the breakdown doesn't look like it dropped half the acceptance criteria: "the other three criteria are tested inside the slice todos."

Also confirm the project name is resolved. If the PRD or pitch flags a name as TBD (e.g., "name may collide, decide before publishing"), ask Matt to pick one now — the name determines the folder, repo, and Herdr workspace.

Ask: "Does this look right, or do you want to adjust anything?"

Wait for explicit approval or adjustments before touching Basecamp or the filesystem.

### 4. Create the Basecamp project

Construct from the **Lab Build** template (id `48254447`):

```bash
basecamp templates construct 48254447 --name "<Project Name>" --description "<one-sentence description>" -a 6191443 --json
```

Always include the description — one sentence describing what the project is, drawn from the pitch problem/solution (e.g. "Menu bar app that shows time since your last commit").

Construction is asynchronous — poll until `status` is `"completed"`:

```bash
basecamp templates construction 48254447 <construction_id> -a 6191443 --json
```

When completed, the response includes the new project (`data.project`). Extract the project ID (`data.project.id`) and use it for all subsequent commands.

**Known CLI issue (basecamp CLI 0.7.2, confirmed on this template 2026-07-25):** `templates construct` returns Bad Request regardless of arguments. Root cause confirmed upstream: the SDK's `CreateProjectFromTemplate` request body was missing the `project` envelope Basecamp's API requires (sent flat `{"name":...}` instead of `{"project":{"name":...}}`) — [basecamp-sdk#354](https://github.com/basecamp/basecamp-sdk/issues/354), [basecamp-cli#454](https://github.com/basecamp/basecamp-cli/issues/454). Fixed via SDK PR #396 + CLI PR #554, merged to `main` 2026-07-25 — not yet in a tagged release (latest is still v0.7.2, the one installed here via `brew`). Once a release newer than 0.7.2 ships, retest `templates construct` directly and drop this curl fallback if it works. Until then, use the curl fallback:

```bash
TOKEN=$(basecamp auth token)
curl -s -X POST "https://3.basecampapi.com/6191443/templates/48254447/project_constructions.json" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"project":{"name":"<Project Name>","description":"<one-sentence description>"}}'
```

A `201` response contains the construction `id` — poll it the same way as above.

The template has a placeholder "PRD" doc and an empty "Build" todolist built in (set up by hand in the Basecamp UI, since the API doesn't expose template content). Steps 5 and 7 find and fill those in rather than creating new ones.

**Existing project:** skip — use the existing project id for all subsequent commands.

### 5. Write the PRD doc

The template's placeholder "PRD" doc is already in the new project — find it and fill in the real content instead of creating a new doc:

```bash
basecamp docs list --in <project_id> -a 6191443 --json
```

Match the doc whose `name` field is "PRD" (docs list returns `name`, not `title` — todolists use `title`, see step 7), then update it:

```bash
basecamp docs update <doc_id> --title "PRD" --content "$(cat <<'EOF'
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

Omit Data Model for non-database projects. If no doc named "PRD" is found (e.g. a project constructed before the template had one), fall back to `basecamp docs documents create "PRD" "<content>" --in <project_id> -a 6191443 --json`.

**Existing project:** create a new doc titled for the cycle — `"PRD: [Cycle Name]"` — so it doesn't collide with the original PRD doc. The template's placeholder doesn't apply here; this path never touches the template.

### 6. Post the kickoff message

Post a short message to the project's Message Board summarizing what's being built:

```bash
basecamp messages create "<Project Name>: Cycle Kickoff" "$(cat <<'EOF'
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

The template's placeholder "Build" todolist is already in the new project — find it instead of creating a new one:

```bash
basecamp todolists list --in <project_id> -a 6191443 --json
```

Match the list titled "Build". If it's missing (e.g. a project constructed before the template had one), create it: `basecamp todolists create "Build" --in <project_id> -a 6191443 --json`.

**Existing project:** always create a fresh list named for the cycle — `"Build: [Cycle Name]"` — instead of plain "Build". This path never touches the template's placeholder list.

Extract the todolist ID. Create todos in the approved order. Setup and Verify todos are title-only; Build-section todos (slices, data model) carry a `--description` pulled from the PRD:

```bash
basecamp todo "<setup or verify task>" --list <todolist_id> --in <project_id> -a 6191443 --json
basecamp todo "<first slice> — end-to-end" --description "<the end-to-end behaviour this slice delivers>. Core flow: <the Core Flow steps it covers>. Done when: <the full path from entry point to result>" --list <todolist_id> --in <project_id> -a 6191443 --json
basecamp todo "<next slice>" --description "<the behaviour this slice adds, from the PRD's Core Flow> — extends the working path" --list <todolist_id> --in <project_id> -a 6191443 --json
basecamp todo "Data model" --description "<PRD Data Model '[Model]: [key fields]' lines>" --list <todolist_id> --in <project_id> -a 6191443 --json
```

Keep the returned id for the "Scaffold repo" todo — step 8 needs it. **Existing project:** don't create a "Scaffold repo" todo at all; the repo already exists, so there's nothing for step 3 to have derived it from in the first place.

### 8. Create the workspace and scaffold the repo

**Existing project:** the repo already exists — no scaffold, no `basecamp config init`. Instead:

1. Update the existing `AGENTS.md` with the new cycle's context (summary, surfaces, no-gos) — append or revise, don't blow away what's there. Keep the Basecamp section CLI-based; don't add IDs or URLs. (If the repo predates the AGENTS.md convention and still has a standalone `CLAUDE.md`, migrate it first: `git mv CLAUDE.md AGENTS.md`.)
2. Repoint the Basecamp config at the new list: `cd <repo> && basecamp config set todolist_id <new_todolist_id>`
3. Commit those changes, then skip to step 9

Workspace path: `~/Work/safaii-studio/lab/<kebab-name>`. Confirm with Matt if anything other than the default makes sense.

Don't pre-create the directory — `rails new`, `hugo new site`, and `bundle gem` create it themselves, and a pre-existing dir makes `bundle gem` prompt or fail. Only the stacks that `cd` into the dir below (11ty, Go, static) need the `mkdir` first; each command includes it.

Scaffold for the stack, using the absolute path. If the stack isn't one of the recipes below, don't improvise a command — ask Matt for the exact scaffold command to run.

**Rails:** (creates the dir)
```bash
rails new ~/Work/safaii-studio/lab/<name> --database=sqlite3 --no-skip-test
```

`--no-skip-test` is load-bearing, not noise. `~/.railsrc` carries `--skip-test` and Rails merges it into every `rails new`, so leaving the flag off silently scaffolds a project with no test directory — nowhere for the `Test:` lines from step 3 to go. Verified on Rails 8.1.3: with `--no-skip-test` the `test/` tree is created despite the rc file.

Drop it (and let `--skip-test` win) only for a Rails project that's essentially a static site. Matt's `~/.railsrc` stays as it is for hand-rolled `rails new`.

**11ty:** (deploys to Cloudflare Pages)
```bash
mkdir -p ~/Work/safaii-studio/lab/<name> && cd ~/Work/safaii-studio/lab/<name> && git init && pnpm init && pnpm add @11ty/eleventy
```

**Hugo:** (creates the dir)
```bash
hugo new site ~/Work/safaii-studio/lab/<name> --force && cd ~/Work/safaii-studio/lab/<name> && git init
```

**Ruby gem/CLI:** (creates the dir — do not mkdir first)
```bash
cd ~/Work/safaii-studio/lab && bundle gem <name>
```

**Go:**
```bash
mkdir -p ~/Work/safaii-studio/lab/<name> && cd ~/Work/safaii-studio/lab/<name> && git init && go mod init <module-path>
```

**Static (no framework):**
```bash
mkdir -p ~/Work/safaii-studio/lab/<name> && cd ~/Work/safaii-studio/lab/<name> && git init
```

Then write the project files into the workspace: `AGENTS.md` and `README.md` (plus the Basecamp config below). There is no per-project process file — Solo is gone and Herdr runs commands in panes, not from a config. The project's run and test commands live in AGENTS.md's **Commands** section instead.

**`AGENTS.md`** — the briefing the build session wakes up to. It must stand alone; the build session has none of this conversation's context. Write it with the content below. Include:

- One-paragraph summary of what's being built and why
- Stack, naming the deploy target (Rails → Kamal on VPS, SQLite-only; 11ty → Cloudflare Pages, pnpm). For 11ty/Rails, add a line pointing the build session at the `safaii-css` and `safaii-html` skills for CSS/markup conventions — they auto-trigger, but naming them removes the dependency on that.
- Surfaces and core flow (condensed from the PRD)
- Data model / data contract if applicable
- No-gos
- Commands — how to run it: the dev server, the build, and the test command (`bin/rails test`, `go test ./...`), each on its own line with any port. Assign each project a distinct port; don't leave two apps on the same framework default. This is the run reference the reviewer and Matt use — there is no `solo.yml`.
- How to read a todo — two sentences, because the spawn prompt only reaches the first session and a build runs across several:

  ```markdown
  ## Todos
  Each todo is a vertical slice — when it's done the app runs end to end and its
  tests pass; never leave it broken between todos.

  Work one slice at a time: write the code and its test together (follow the
  `tdd` skill), run typecheck and the test suite, then commit before the next
  todo. Each build todo's description ends with a `Done when:` line — the finish
  line, not your own judgment of done; where it carries a `Test:` line, that test
  is written with the code, not afterwards.

  Basecamp is the record. Close a unit by commenting the commit SHA on the todo,
  then completing it (no flags — the repo's `.basecamp/config.json` supplies
  account, project, and list):

      basecamp comment <todo_id> "<short sha>"
      basecamp todos complete <todo_id>
  ```
- Basecamp section (no IDs or URLs — keeps them out of the committed file): a short paragraph telling the build session that the project config (account/project/todolist IDs) is already set in `.basecamp/config.json` (gitignored), so `basecamp` commands work without flags from this directory. To find the PRD doc, run `basecamp docs list` and match by title (`PRD: [Cycle Name]` for cycles); the pitch lives on the project's card.
- Herdr pointer (short — the build session runs inside a Herdr pane, so this just names the tool for spawning and reading sibling agents):

  ```markdown
  ## Herdr
  This session runs inside a Herdr workspace. Use the `herdr` skill to spawn and read sibling agents (the review step does this): split a pane with `herdr pane split --current --direction right --no-focus`, start an agent with `herdr agent start <name> --kind opencode --pane <pane-id>`, and wait on it with `herdr agent prompt <name> "..." --wait`.
  ```

**`README.md`** — a stub, committed. This guarantees every repo has a README from the first commit; the build session fleshes it out at the end (see the README task in step 3). Generate it from the PRD — don't leave the repo bare:

```markdown
# <name>

<one-line description — the same sentence used for the Basecamp project `-d`>

<1–2 sentences: what this is and who it's for, from the pitch problem/solution.>

**Status:** in development.
```

Keep the stub short — real usage, install, and examples come at the finalize-README task once the commands actually exist.

**Basecamp repo config** — so the build session can run `basecamp` commands without `-a`/`--in` flags. Run the bundled script rather than retyping the sequence:

```bash
@scripts/init-basecamp-config.sh ~/Work/safaii-studio/lab/<name> <project_id> <todolist_id>
```

It runs `basecamp config init` / `set account_id 6191443` / `set project_id` / `set todolist_id` / `trust`, then appends `.basecamp/` to `.gitignore`. (`trust` is only needed for authority keys, but it's harmless and future-proofs the config.) `.basecamp/` stays out of git — it's local session config holding account and project IDs, not project code. Gitignoring `.basecamp/` before the commit keeps the `git add -A` scaffold commit clean — important since these repos are often open-core-ready or public. The build session pulls the PRD/pitch via `basecamp` commands (config above), so no IDs or URLs need to be written into the committed repo.

Commit the scaffold and offer to push to GitHub:

```bash
cd ~/Work/safaii-studio/lab/<name> && git add -A && git commit -m "Scaffold [stack]"
gh repo create <name> --private --source . --push   # creates under the gh-authed account (mattsafaii)
```

Ask before the `gh repo create` — private by default.

`/build` just did the scaffold work itself — close the loop on the "Scaffold repo" todo now, the same way the build agent will later comment a SHA before checking off its own todos:

```bash
basecamp comment <scaffold_todo_id> "Scaffolded in <commit_sha>" --in <project_id> -a 6191443 --json
basecamp todos complete <scaffold_todo_id> -p <project_id> -a 6191443 --json
```

Otherwise the build agent hits "Scaffold repo" as its first todo already done and either redoes it (re-running `rails new`/`git init` into a non-empty dir) or stalls figuring out what's left to do.

### 9. Create or find the project's Herdr workspace

`/build` runs inside Herdr — verify with `test "${HERDR_ENV:-}" = 1` before controlling anything, and never touch a Herdr session from outside a managed pane. The build agent is a separate OpenCode session that lives in the project's Herdr workspace, rooted at the repo.

**New project** — create a workspace for it:

```bash
herdr workspace create --label "<Project Name>" --cwd ~/Work/safaii-studio/lab/<name> --no-focus
```

Read the workspace id from `.result.workspace.workspace_id` and the shell pane from `.result.root_pane.pane_id`. The root pane opens at the repo with an interactive shell — that's the pane the agent starts in.

**Existing project (cycle)** — find the workspace by label instead of creating one:

```bash
herdr workspace list
```

Match `label` to the project name for its `workspace_id`, then list its panes and pick one at a shell prompt:

```bash
herdr pane list --workspace <workspace_id>
```

If the project has no workspace yet, create one as above.

### 10. Spawn the build agent

Start the OpenCode session in the workspace's shell pane, then brief it:

```bash
herdr agent start build --kind opencode --pane <pane_id>   # Herdr agent names are lowercase
```

A successful start returns once Herdr detects OpenCode in that pane and it's ready for input. Then submit the first prompt — it must stand alone, since the session wakes up with none of this conversation:

```bash
herdr agent prompt build "Read AGENTS.md, then start on the first todo in the Basecamp Build list. Work through the todos in order, closing each by commenting its commit SHA on the Basecamp todo and completing it with the basecamp CLI — no flags, since the repo's .basecamp/config.json supplies account, project, and list. Each build todo's description ends with a 'Done when:' line — that's the finish line, not your own judgment of done; where a description carries a 'Test:' line, write that test with the code rather than afterwards; each todo is a vertical slice, so when it's done the app runs end to end and its tests pass — never leave it broken between todos. Once every todo is complete, ask Matt whether to move this project's card on the Lab board to Shipped — don't move it yourself without asking. The card lives in account 6191443, project 46824335, card table 9768185094; find it by matching this project's name, and if Matt confirms, move it to the Shipped column (9768185101)." --wait --timeout 120000
```

Read its progress with `herdr agent read build --source recent-unwrapped --lines 120`.

**Existing project:** always spawn a fresh agent for the cycle (named e.g. `build-<cycle>`, prompt referencing the cycle's todolist) — never send the kickoff to an existing session; its context is full of the previous cycle and the prompt may interrupt it mid-task. Leave existing sessions alone — Matt often runs multiple agents in the same repo, and an idle session may just mean he stepped away. Never close one.

### 11. Move card to In Progress

```bash
basecamp cards move <card_id> --to 9768185099 --card-table 9768185094 --in 46824335 -a 6191443 --json
```

If the move returns `ok: false`, retry once — transient failures happen.

### 12. Confirm and hand off

One line: Basecamp project created, PRD doc written, [N] todos created, repo scaffolded, card moved to In Progress. Share the Basecamp project URL. Then the handoff: "Switch to the **<Project Name>** workspace in Herdr — the build session is already running on the first todo."

**If no agent was spawned** (not running inside Herdr, step 10 skipped): don't claim a session is running. Handoff instead: "Open Herdr, start an OpenCode session in the repo (`~/Work/safaii-studio/lab/<name>`), and tell it: *Read AGENTS.md, then start on the first todo in the Basecamp Build list.*"

**Existing project:** the one-liner is instead: PRD doc written, kickoff posted, [N] todos created on "Build: [Cycle Name]", AGENTS.md updated, cycle agent spawned (or manual-start note if not inside Herdr), card moved to In Progress.

---

## Task derivation heuristics

- **A task is a slice, not a layer or a screen.** It cuts through the layers it needs and runs end to end. "The model" and "the list page" are not tasks.
- **The first slice retires the biggest risk.** The riskiest core-flow path goes first — the API, the auth, the awkward data shape — so the scary part is proven before anything is built on it. Everything after extends something that already runs.
- **A slice may span surfaces and stub what isn't built.** The thinnest complete path, not one screen doing everything.
- **Every slice ends green.** The app runs and its suite passes at each `Done when:`; never leave it broken between tasks.
- **Surfaces are coverage, not the task list.** Every surface must be reached by some slice; the core flow is what you cut slices from.
- **Don't save the wiring for the end.** A separate "Wire core flow" task means nothing is demoable until the last day, and integration surprises land when they're most expensive.
- **Walk the core flow once at the end.** One Verify task exercises the whole flow after all slices land.
- **Prefactor before the feature (cycles).** Make the change easy, then make the easy change — as two tasks, not one.
- **Wide mechanical changes go expand → migrate → contract (cycles).** They aren't slices; forcing them into the per-slice shape produces a todolist that can't land green.
- **Verification tasks are user-facing.** "Verify: user can submit a URL and see a result" — testable by using the app.
- **Setup tasks are real tasks.** Scaffold, deploy config, and env setup take real time.
- **Keep the list short.** 8–15 tasks for small batch. 15–25 for big batch. More means tasks are too granular. Test lines and `Done when:` lines ride inside existing todos, so they don't push the count up.
- **If no data model in PRD, skip data model task.** Don't invent a schema for a CLI tool.
- **Tests follow the PRD, not the code.** Every `Test:` line traces back to a mechanical acceptance criterion. If a test has no criterion behind it, either the PRD missed something — go add it — or the test isn't worth writing.
- **Don't manufacture tests for a screen.** A page that renders a list is checked by looking at it. Forcing a test there costs a session and proves nothing.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 0 | New vs existing resolved before creating anything | Existing project/repo reused, not duplicated | Ask Matt; delete accidental duplicates |
| 1 | PRD read before deriving tasks | Tasks match PRD content | Re-read PRD section of card |
| 1b | PRD carries checks, failures, and any gate | `check:` present on the acceptance criteria | Backfill with Matt and write it back to the card before deriving |
| 2 | Slices cover every surface and flow step | Every PRD surface is reached by some slice and every Core Flow step is reachable | Add the missing coverage |
| 2b | Data model task matches the PRD | Present when the PRD has a Data Model section, absent when it doesn't | Add or remove the task to match |
| 2c | First slice is the tracer bullet | It retires the biggest risk and runs end to end (entry point → result) with its tests; no separate "Wire core flow" task | Pick the riskiest path first; fold wiring into the first slice |
| 2d | Cycle prefactor present (cycle only) | The refactor that makes the change easy is the first build task | Add it |
| 2e | Wide-refactor cycle sequenced expand/contract (when applicable) | Expand → migrate batches → contract, each its own task | Resequence |
| 2f | Tasks are slices, not layers or screens | Each task cuts through the layers it needs and runs end to end | Rework into slices |
| 2g | App green after every slice | The app runs and its suite passes at each task's `Done when:` | Rescope so no task leaves it broken |
| 3 | Every acceptance criterion is accounted for | Visual ones as "Verify:" tasks, mechanical ones as `Test:` lines inside build todos — none dropped | Add the missing ones |
| 3b | Build todos carry a description | Slice and data-model todos have `--description` from the PRD; Setup/Verify todos are title-only | Add missing descriptions |
| 3c | Every build todo has a `Done when:` line | One observable result per todo, from the PRD | Add it |
| 3d | Failure cases assigned | Each What Can Go Wrong item sits in the `Done when:` of the todo that owns it | Attach the orphans |
| 3e | Review task present | "Review against the PRD" in close-out, with both reviewer briefs (Spec + Standards) as its description | Add it (skip only for static sites) |
| 3e2 | QA plan task present when warranted | "Write QA plan" in close-out, after Verify tasks, when there are enough Verify tasks to consolidate | Add it (skip for one or two Verify tasks) |
| 3f | Test framework exists where tests were promised | A todo carrying a `Test:` line is in a project scaffolded with a test setup | Fix the scaffold flags before spawning |
| 3g | Spike task present and first | A PRD with a Gated Decision has `Spike: [question]` immediately after "Scaffold repo", carrying the question, what settles it, and the fallback | Add it; move it ahead of everything else |
| 3h | Core flow verified end-to-end once | A Verify task walks the whole Core Flow after every slice has landed | Add it |
| 4 | Task count reasonable | 8–25 tasks | Merge too-granular or split too-large |
| 4b | Project has a description | Created with `-d`, not title-only | `basecamp projects update --description` |
| 5 | Scaffold matches stack | Command matches PRD stack | Fix scaffold command |
| 6 | Name resolved before scaffold | No TBD or "may collide" name used | Ask Matt before running |
| 7 | AGENTS.md stands alone | Build session can start without this conversation | Add missing context |
| 7b | AGENTS.md is ID-free | No Basecamp IDs/URLs committed — Basecamp section points at the CLI/config | Replace IDs/URLs with the CLI-based section |
| 8b | Basecamp config set | `.basecamp/config.json` has account, project, todolist ids and is trusted | Run config init/set/trust |
| 8c | README stub committed + finalize task exists | `README.md` written in scaffold; a "Finalize README" task is in the list | Write the stub; add the task |
| 8d | AGENTS.md carries a Commands section | Dev server, build, and test commands named (no `solo.yml` anymore) | Add it — it's the run reference |
| 8e | Scaffold repo todo closed before spawn | "Scaffold repo" commented with the scaffold SHA and completed, not left open | Complete it before step 10 |
| 8h | Herdr workspace created or found | New project: a workspace labeled for the project, rooted at the repo; cycle: the existing one reused | Create or find it — step 9 |
| 9 | Agent spawned and briefed | Build session running in its Herdr workspace on the first todo — or, if not inside Herdr, Matt was told to start it manually | Run step 10 |
| 9b | Spawn prompt includes the Shipped-confirmation instruction | Agent is told to ask before moving the Lab card to Shipped once all todos are done | Add it to the spawn prompt |
| 10 | Card moved to In Progress | No longer in Up Next | Run move command |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

If a step fails partway through the build, stop and report exactly which resources already exist (Basecamp project, todos, repo, Herdr workspace, spawned agent) and which don't — don't push on to later steps, and don't delete anything to clean up. Matt decides whether to resume or unwind.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Can't find PRD in card body | PRD skill not run, or card has no `<hr>` separator | Ask Matt to run `/prd` first, or check card body |
| Tasks don't match PRD | Derived from pitch instead of PRD section | Re-read below the `<hr>` |
| Too many tasks | Tasks too granular | Merge related tasks |
| App isn't demoable until the last task | Core-flow wiring deferred to a separate late task | Fold the end-to-end path into the first slice |
| Tasks are layers or screens, not slices | Derived one-per-surface from the PRD | Re-cut from the Core Flow; surfaces are coverage only |
| The first slice is the easiest screen | Risk retired late | Make the riskiest core-flow path the tracer |
| App is broken between todos | A slice didn't end green | Each slice ends with the app running and its tests passing |
| Nobody walks the whole flow | No end-to-end verify task | Add "Verify: core flow end-to-end" |
| Cycle tangles a refactor with the feature | No prefactor task | Add the prefactor first |
| A wide mechanical change can't land green | Forced into the slice shape | Sequence expand → migrate → contract |
| Build coded in the session that ran `/build` | Forgot this is an outside-in command | Hand off to the spawned agent; never code here |
| Gem scaffolded with placeholder name | Skipped name resolution check | Always check for TBD names in pitch/PRD before scaffolding |
| Build session asks basic questions | AGENTS.md too thin | Include stack, data contract, no-gos, and the CLI-based Basecamp section |
| Card stays in Up Next | Forgot move command, or transient `ok: false` | Always run move after todos created; retry once on failure |
| Wrong account on project commands | Missing `-a 6191443` | Always pass account flag |
| Duplicate Basecamp project or repo created | Skipped the new-vs-existing check (step 2b) | Check before step 4; trash the duplicate, rerun against the existing project |
| Build agent works the wrong todolist | Basecamp config still points at the old list | `basecamp config set todolist_id <new_todolist_id>` in the repo |
| Build agent re-runs the scaffold command on its first todo | "Scaffold repo" todo left open after step 8 | Complete it (with SHA comment) before spawning — see step 8 |
| Finished project's Lab card sits in In Progress indefinitely | Spawn prompt didn't include the Shipped-confirmation instruction | Always include it — see step 10 |
| Rails project has no `test/` directory but todos promised tests | Scaffolded without `--no-skip-test`, so `~/.railsrc`'s `--skip-test` won | Rerun the scaffold with the flag before any code is written |
| Build has no tests and no failure handling, and nobody noticed | Derived from a pre-2026-07-25 PRD without backfilling it | Check for `check:` before deriving — see step 3 |
| Backfilled sections live only in the chat | Card never updated after the backfill conversation | Write them to the card first; the card is the record |
| Half the build gets redone after the spike | Spike ordered late, or dropped because the PRD "seemed clear enough" | It runs first, right after the scaffold — nothing built on an unanswered gate is trustworthy |
| Spike turns into the implementation | No time-box, or its code was kept | One session, throwaway code; it answers a question and stops |
| Nobody can tell which path the build took | Spike outcome never recorded | Comment the answer on the todo and note it in the repo's AGENTS.md |
| Build drifts from the Basecamp record | Agent completed a todo without the SHA comment | Comment the SHA and complete it via the basecamp CLI — always as a pair |
| Basecamp todo completed with no SHA comment | The SHA-comment step was skipped | Comment the SHA now; make `basecamp comment` + `basecamp todos complete` the close-out pair |
| Todolist doubles in size | Tests and failure cases were made into their own todos | They ride inside existing todos as `Test:` and `Done when:` lines |
| Build agent stops early or gilds a todo | No `Done when:` line, so "finished" was its own judgment call | Add the line — it's the whole point of the description |
| Reviewer rewrites the code | Reviewer brief omitted read-only scope | Brief says report gaps, don't fix them; the build agent applies the fixes |
| Build agent waits on a reviewer forever | Reviewer spawned with the wrong tool and hit a permission prompt, so it never went idle | Spawn both reviewers with OpenCode (unattended) — see the herdr skill |
| Matt has to re-derive what "verify X" means for each criterion by hand | QA plan task skipped or written as a restatement of the criteria instead of a walkthrough script | Write concrete steps (URL, click, input) and the observable result per step, ordered so setup isn't redone |
| Standards reviewer invents conventions the repo doesn't have | No AGENTS.md or stack-specific skill (safaii-css, dhh-rails-style) to point it at | Fall back to a plain code-smell pass (duplication, naming, dead code) instead of guessing at house style |

---

## Examples

- **Since (2026-06-03):** menu bar Go app; 15 todos (1 setup, 6 build, 8 verify) derived from an 8-criterion PRD. Built before the outside-in rework, so the workspace/Herdr/spawn steps weren't exercised — and it predates the Solo → Herdr switch, so its Solo-era steps are gone entirely. Task derivation and Basecamp steps are the exemplar part.

  **Don't copy its shape wholesale.** Since predates the 2026-07-25 changes: every acceptance criterion became its own verify todo, where mechanical ones now fold into build todos as `Test:` lines. It also predates the tracer-bullet slice model, so its build tasks aren't vertical slices and its first task isn't risk-ordered. A list like Since's — eight verify todos out of fifteen — would be wrong today.

- *(no build has run under the 2026-07-25 rules yet — the first one becomes the example for spikes, `Done when:` lines, the reviewer step, and the tracer-bullet slice model)*
