# Document Skill Guide

Read a codebase and produce documentation — published into that project's own Basecamp project Docs, with inline D2 diagrams — that lets any reader **learn the codebase**: what each part does, how the parts relate, and **why** it's built the way it is. The reader should be able to start knowing nothing and end up understanding the system and the thinking behind it.

The codebase may have been built by AI or by a person. Either way, **the source is the truth** — document what the code actually does, never what a PRD or commit message merely claimed.

## First principle: document what the code can't tell you

A reader can read the code. They get signatures, names, and constants for free. What they *can't* recover from the source is the expensive, valuable part — and that's what these docs exist to capture:

- **Why** — the decisions, the rejected alternatives, the constraints and tradeoffs.
- **How the parts relate** — the architecture, the data and control flow, the boundaries.
- **The mental model** — the few load-bearing concepts that make the rest obvious.
- **The non-obvious** — invariants, gotchas, edge cases, concurrency.

So this skill writes **learning docs** (narrative, the hard part) into Basecamp, and delegates the **symbol-level lookup reference** (every function/type signature) to the language's own doc generator, which is complete and accurate by construction and never rots. Don't hand-transcribe signatures into Basecamp — that restates the code, buries the signal, and goes stale instantly.

**Completeness means: every module/file is accounted for and explained at the right altitude — nothing silently skipped.** It does *not* mean every symbol gets a hand-written entry. Important functions get real narrative depth (what, how, why, gotchas); a trivial one-line getter gets a mention, not a templated stub. Symbol-by-symbol completeness is the generated reference's job.

**This runs inside the repo.** It reads the code, so cwd must be the project directory (`~/Code/personal/<name>`). The build agent runs it there as a finalize step; standalone, Matt runs it from inside the repo. For non-trivial codebases this is a large job — parallelize the Module Guide with subagents (step 3).

---

## Fixed IDs

- Account: `6191443` (Safaii Studio)

The **project's Basecamp project id** comes from `.basecamp/config.json` in the repo (set by `/build`). Read it; don't ask if it's there.

---

## Workflow

### 1. Confirm scope and locate the Basecamp project

**Gate on project type first.** This skill is for codebases with real application logic:

- **Document:** Go apps/CLIs (`go.mod`), Ruby gems/CLIs (`*.gemspec` + `exe/`/`bin/`), Rails apps (`Gemfile` with rails), Node/TS apps, services, libraries.
- **Skip:** static sites, marketing sites, landing pages — 11ty/Hugo projects that are only templates + content + CSS (`.eleventy.js`/`hugo.toml`, `_site/`, only `layouts`/`content`). No architecture to explain.

If it's clearly a static/marketing site, say so and stop. If genuinely ambiguous (an 11ty site with custom build plugins, data pipelines, or serverless functions), ask whether to document the logic parts.

**Document a *stable* codebase, not one mid-build.** These docs are only worth writing when the architecture and decisions have settled — at a build cycle's finish (which is why `/build` runs this as a finalize step) or between cycles. Mid-build, the structure is still moving and the "why" isn't decided, so the docs would be a snapshot that rots immediately and gets re-run anyway.

**Judging done-vs-mid-build (no single signal is airtight — combine, then ask).**

- **In build-finalize mode this question is moot** — the skill is running *because* a build cycle just finished, so it's stable by definition. Skip the check.
- **Standalone:** don't trust `git log` recency — a finished v1 still gets polish commits, so "committed 4 hours ago" means nothing. Instead, read the project's todolists for *completion*, not for a name:

  ```bash
  basecamp todolists list --in <project_id> -a 6191443 --json   # completion of each list
  ```

  Look across **all** lists (don't match the name "Build" — cycles make "Build: <name>", projects vary). Treat the project as stable if the substantive work lists are complete, **ignoring clearly forward-looking lists** — titles like "Next steps", "post-vN", "backlog", "someday", "ideas". Corroborate with other shipped-signals: a version tag / GitHub release (`git tag`), a published package, or a README that reads as shipped (no "WIP"/"in development" banner).
- **When it's genuinely ambiguous, just ask Matt** — "Is this done / between cycles, or still mid-build?" He has the ground truth and it's one cheap question. Prefer asking over guessing.

If it genuinely is mid-build, say so and recommend waiting until the cycle is done — unless the run is deliberately for a real exception: re-orienting on a long-paused project, documenting a *locked* core within a longer build, or a handoff/sale of in-progress work. In those cases, stamp an **"In-progress snapshot — reflects the code as of `<short-sha>` / `<date>`"** line on Start Here so the reader knows it will drift.

**Locate the Basecamp project.** Read `.basecamp/config.json` for `project_id` (and `account_id`). If absent (an older repo `/build` never touched), ask Matt for the Basecamp project or offer to create one. Docs land in **that project's own Docs** — never a shared docs project.

### 2. Understand the codebase

Build a real mental model — this is what makes the docs worth reading. Read, don't skim.

- **Map every module/file.** Walk the tree and list the source files/modules (exclude vendored deps, generated output, `node_modules`, `vendor/`, `_site/`, lockfiles, build artifacts). This list is your completeness checklist (step 3) — every item must end up explained somewhere.
- **Read entry points first** — `main.go`, `exe/<bin>`, `config/routes.rb`, `main.swift`/`@main`/`AppDelegate` (Swift), server bootstrap, the CLI command tree. Then each module.
- **Trace the main flows** end to end, through the real code.
- **Find the data model** — schema (`db/schema.rb`, migrations), structs/models, persisted state, key data structures.
- **Note dependencies** and what each is actually used for; note how the project is configured, built, run, tested.
- **Mine the *why*.** Decisions aren't in the code. Gather rationale from:
  - the code itself (what the structure implies),
  - the project's **PRD and pitch** in Basecamp (`basecamp docs list`/`cards`) — the pitch's **no-gos and rabbit holes are explicit decisions**,
  - **git history** (`git log`, commit messages) for why things changed,
  - reasoning about tradeoffs the code reflects.

  **Rationale honesty (required):** state documented rationale as fact; clearly **label inferred rationale** ("Likely because…", "Inferred:"); **flag genuine unknowns** as open questions. **Never fabricate a plausible-sounding reason.** A flagged unknown is more useful than a confident guess.

Read until non-obvious things are obvious. The docs are only as good as this pass.

### 3. Plan the doc set, manifest, and parallelization

**The doc set** (full spec in **Doc set spec** below) — Basecamp learning docs:

1. Start Here (index)
2. Architecture & Mental Model
3. Decisions & Why
4. Module Guide (complete module/file coverage)
5. Key Flows
6. Data Model (if it persists state)
7. Glossary

Plus an **on-demand symbol reference** (step 5b) — a command in the index, not a persisted file.

**Coverage manifest.** Turn the step-2 module/file list into a checklist — every module/file, with a "covered in the Module Guide?" box. Keep it in the scratch dir (`$WORK/coverage.md`) as a working aid — it's a build-time tracker, not a deliverable. Tick items as you write; verify 100% in step 8b. This guarantees no part of the system is silently skipped. (Completeness is at the module/file level — not every symbol.)

**Parallelize the Module Guide.** Documenting every module is the bulk of the work. For non-trivial codebases, fan it out: spawn one subagent per module/directory (Task tool), each given that module's files, the step-2 understanding, and the Module Guide spec, returning finished doc content. The orchestrator keeps the whole-system docs (Architecture, Decisions, Flows — they need cross-cutting understanding) and assembles + reconciles against the manifest. If you ever cap or sample for size, **say so explicitly in the docs** — never let a silent truncation read as full coverage.

**Standalone mode:** present the plan (doc list + module count + manifest) and confirm before writing. **Build-finalize mode:** derive and write without prompting.

### 4. Create the Documentation folder

Group the whole set in one folder so it doesn't bury the project's other Docs (the PRD, etc.). Use **"Documentation"** — not "Docs," which collides with the "Docs & Files" tool name.

```bash
basecamp docs folders create "Documentation" --in <project_id> -a 6191443 --json
```

Grab the returned folder id (`data.id`) — pass it as `--vault <id>` on every doc create.

**Large codebase → nest the Module Guide.** If the Module Guide runs long (roughly 8+ module docs), create a `"Module Guide"` subfolder inside Documentation so the top level stays scannable — the learning docs you read front-to-back stay visible, the per-module lookup docs tuck one level down:

```bash
basecamp docs folders create "Module Guide" --in <project_id> --vault <documentation_folder_id> -a 6191443 --json
```

Put the per-module docs in that subfolder's id; keep the orientation docs (Start Here, Architecture, Decisions, Key Flows, Data Model, Glossary) in the top "Documentation" folder. For a small project (a few modules), skip the subfolder — flat is fine.

Don't move the build skill's existing PRD doc into the folder — leave it where `/build` put it; the Start Here index just links to it.

### 5. Generate diagrams with D2

**Work in a scratch dir outside the repo — never write generated files into the project.** The deliverable is the Basecamp docs; diagrams, manifest, and reference are byproducts that should never touch the repo (these are often public/open-core). Set a scratch dir once and use it for everything:

```bash
WORK="$(mktemp -d)"   # or the session scratchpad; outside the repo
```

Diagrams go inline in the docs. Author in D2, render to PNG, attach, embed. Write `.d2` source into `$WORK`, validate, format, render:

```bash
d2 validate "$WORK/architecture.d2"
d2 fmt "$WORK/architecture.d2"
d2 --omit-version --pad 20 "$WORK/architecture.d2" "$WORK/architecture.png"
```

**Render flags that matter** (full **D2 reference** below):
- `--omit-version` — strip the D2 version watermark stamped on every image. Always use it.
- `--pad 20` — tighter than the default 100px.
- `--layout elk` — for **ER / data-model** diagrams: ELK points FK connections precisely at the referenced row; default `dagre` doesn't.
- `-t, --theme <id>` — optional; pick one theme ID and use it for *every* diagram so the set is consistent (`d2 themes`; `0` neutral, `303` C4). `--sketch` is fine too — just be consistent.

(First PNG render downloads a one-time headless-render helper, then caches it.)

Make a diagram where it aids understanding:
- **Architecture diagram** (always) — the major pieces and how they connect.
- **ER diagram** (if there's a schema) — tables/models and relationships (`--layout elk`).
- **Sequence diagram** for the top 1–2 flows.

Keep each to one idea — many small beats one hairball. Attach each PNG:

```bash
basecamp attach "$WORK/architecture.png" -a 6191443 --json
```

Returns the embed tag in the `.html` field — a `<bc-attachment sgid="...">…</bc-attachment>` tag. Use it **verbatim, inline** in the doc HTML where the diagram belongs.

### 5b. The symbol reference: link it or make it on-demand

The signature-level lookup layer (every symbol + its signature) is the language's own doc generator. **Never persist it** (not the repo, not Basecamp) — it's regenerable and would only rot. The Start Here index (step 7) handles it one of two ways:

**If the package is published, link the auto-hosted docs.** Published packages already have a free, always-current API reference online — nothing to generate or store, just link it:
- Ruby gem on RubyGems → `https://rubydoc.info/gems/<name>`
- Go module → `https://pkg.go.dev/<module-path>`
- Rust crate → `https://docs.rs/<name>`

**Otherwise (private/unpublished), give the on-demand command** to generate it into a temp dir when wanted:
- **Go:** `go doc -all ./...` (built-in; pipe to a pager or file).
- **Rust:** `cargo doc --no-deps --open` (built-in).
- **Ruby:** `rdoc -o /tmp/<name>-api lib/ exe/` (built-in — point it at a temp dir and let it create that dir; rdoc refuses a pre-existing non-rdoc dir). Use `yard` only if already installed.
- **TS/JS:** `typedoc` if present.
- **Swift:** *no dependency-free generator* — Swift-DocC needs the DocC build-plugin and `swift-doc` is a separate install. For an app or a small/comment-rich package, default to "the source is the reference" (clone pointer); don't add a doc dependency just to generate this. **Worth DocC when** it's a *library with external API consumers* (DocC's actual purpose) or large enough that a browsable, searchable reference beats reading source. **If it's published and hosted on the Swift Package Index** (opt-in via `.spi.yml`), link those DocC docs instead of the source pointer — same as rubydoc.info/pkg.go.dev. The DocC plugin is a build/dev-time dependency only (never linked into the binary), so it doesn't compromise a *runtime* zero-dependency design.

If the only generator would be a **new dependency** (YARD, TypeDoc, gomarkdoc), don't install it — note in the index that the source itself is the reference. This is a convenience pointer; the Basecamp learning docs are the deliverable.

**This skill never modifies the source — it does not add or edit code comments.** The generated reference works with or without comments (comments only enrich it); documenting a codebase here means explaining it in Basecamp, never touching the code. Commenting code is a separate task the user must ask for explicitly.

### 6. Write each doc

**Content format depends on whether the doc embeds a diagram** (verified on Basecamp 5 / CLI 0.7.2):

- **Plain Markdown is converted to rich text** — *only if the body contains no HTML tags*. `# H1`, `**bold**`, `- list`, code fences all render.
- **The moment the body contains any HTML tag** (an inline `<bc-attachment>`), Markdown conversion is skipped for the *whole* doc — `##` renders literally.

So: **any doc with an inline diagram must be authored fully in HTML.** Author diagram-bearing docs in HTML; a diagram-free doc (e.g. Glossary) may be Markdown. When in doubt, HTML always works. HTML tags: `<h1>`/`<h2>`/`<h3>`, `<p>`, `<ul>`/`<ol>`, `<strong>`/`<em>`, `<pre>` for code/signatures/paths, and the `<bc-attachment>` tag inline.

Create each doc in the vault:

```bash
basecamp docs documents create "Architecture & Mental Model" "<h1>Architecture &amp; Mental Model</h1>
<p>…</p>
<bc-attachment sgid=\"…\"></bc-attachment>
<p>…</p>" --in <project_id> --vault <folder_id> -a 6191443 --json
```

For long content, write the HTML to a scratch file and pass via `"$(cat <<'EOF' … EOF)"`. Render the first doc and eyeball it in Basecamp — confirm the diagram embeds inline and the HTML renders — before generating the rest.

### 7. Write the index

Create **"Start Here"**, the front door:

1. **What this is** — two sentences.
2. **Learning path** — the Basecamp docs in reading order (Architecture → Decisions → Module Guide → Flows …), one line each. How a newcomer gets familiar.
3. **Symbol reference** — for every symbol + signature (step 5b): if the package is published, link its auto-hosted docs (rubydoc.info / pkg.go.dev / docs.rs); otherwise give the on-demand command (e.g. "run `rdoc -o /tmp/<name>-api lib/ exe/` to browse every method"). Not a stored file — the source is the canonical reference.
4. **Further reading** — a short list of links: the language's official docs, and the official docs for the main libraries/tools the project depends on (e.g. for a Ruby CLI: Ruby, Thor, the key gems; plus any external tools/APIs it talks to). Link out to the canonical source — don't re-explain languages or libraries in the docs.

**Link to source when the repo has a public remote.** Check `git remote get-url origin` and the default branch. If it's a public host (GitHub/GitLab), add a **Source** line in Start Here linking the repo, and make any commit-SHA references in Decisions & Why clickable (e.g. `https://github.com/<owner>/<repo>/commit/<sha>`). This makes "jump to the actual code" work from Basecamp. Keep it light — link the repo + commit refs, not every file path (that's noise). Skip for private repos. (A public *GitHub* repo is not the same as a *published package* — the symbol reference still uses the on-demand command unless the package is actually on RubyGems/pkg.go.dev/crates.io.)

### 8. Verify coverage and clean up

**The repo stays untouched — nothing to commit.** All working files (diagrams, manifest, reference) live in the scratch dir and are not deliverables. Confirm you wrote nothing into the project:

```bash
git -C <repo> status --porcelain   # should be empty
```

If anything landed in the repo, remove it. Then **reconcile coverage**: every module/file from the manifest (`$WORK/coverage.md`) is accounted for in the Module Guide, or named as a deliberate exclusion in the docs. Walk the list; fill any gap before handoff. A silent gap is the failure this skill exists to prevent. The scratch dir can be discarded once the docs are published.

### 9. Confirm and hand off

One line: Documentation folder created in Basecamp with [N] docs and [M] diagrams; [F] modules/files covered; repo left untouched. Share the Basecamp Docs URL.

---

## Doc set spec

**Start Here (index)** — front door: what this is, the learning path, the symbol-reference pointer, and a short **Further reading** list (official docs for the language and the project's main libraries/tools). Written last, sits first.

**Architecture & Mental Model** — the map. What the system is; the few **load-bearing concepts** that, once understood, make the rest obvious; the major components and their responsibilities; how data and control flow; the boundaries; the stack; where execution starts. Leads with the architecture diagram. If a reader reads one doc, this is it.

**Decisions & Why** — the highest-value layer, the thing the code can't tell you. Each significant decision: **what** was decided, the **alternatives**, **why** this one, the **constraints/tradeoffs**. Cover architectural choices, the stack, key library picks, data-model shape, and the pitch's no-gos/rabbit holes (explicit decisions). Apply the rationale-honesty rule: documented = fact, inferred = labeled, unknown = flagged. Do not fabricate.

**Module Guide** — **complete module/file coverage** (the completeness guarantee). One section (or doc) per module/file from the manifest: its **job**, **why it exists**, its place in the whole, its **key types and functions explained in narrative — with reasoning** (what they do, how, the non-obvious bits), how it **connects to neighbors**, and **gotchas**. Important symbols get real depth; trivial ones get a mention. This is "what each piece does and how they relate," at the altitude where it's learnable — not a flat per-symbol table (that's the on-demand generated reference's job, pointed to from the index).

**Key Flows** — walk the most important end-to-end actions through the *real* code: "user runs X → this entry point → this function → this data → this output," naming the actual symbols at each step. This is where understanding clicks, because it's the system in motion. Sequence diagram for the top flow.

**Data Model** (if it persists state) — each table/model: purpose, key fields, relationships, invariants. Leads with the ER diagram. Skip for stateless tools.

**Glossary** — domain and project-specific terms and concepts a newcomer would trip on.

---

## Writing principles

- **Capture what the code can't say.** Spend the words on why, relationships, mental model, and gotchas — not on restating signatures (the generated reference has those).
- **Document the project, don't teach the language.** The reader is a capable, fast learner who can read the language's own docs. Explain *this codebase* and its decisions; do not write tutorials or course content explaining language/framework concepts in general. When a language idiom or library matters, link its official docs (Further reading) rather than re-explaining it. (No "Learning the Stack" doc — same-language projects would just duplicate it.)
- **Complete at the module level.** Every module/file is explained; nothing silently skipped. If you exclude something (generated/vendored code), name the exclusion — a reader must never mistake an omission for "this doesn't exist."
- **Right altitude.** Architecture is the map; the Module Guide drills in; Flows show motion; the generated reference is for lookup. Don't make the map exhaustive or the modules hand-wavy.
- **Rationale honesty.** Documented rationale = fact. Inferred = labeled. Unknown = flagged as an open question. Never invent a reason that sounds right.
- **Read the truth.** Document what the code does now, from the source — not the PRD, a commit message, or a prior AI build's claims.
- **Teach.** Explain *why* and *how it relates*, in plain language — say what concretely happens. No methodology jargon ("Examples," not "Exemplars").
- **Cite the code.** Real paths, functions, types (`internal/scan/runner.go`, `Runner.Execute`) so the reader can jump to source. **Always repo-relative paths — never absolute local paths** (`internal/adapter/`, not `/Users/matt/Code/personal/.../internal/adapter/`). Absolute paths leak your home-dir layout into public/handoff docs and break for any other reader.

**Sentence-level style** (borrows Simplified Technical English's best habits, not its full controlled-vocabulary standard):

- **Short sentences, one idea each.** Roughly 20-25 words max. Split compound sentences instead of stacking clauses with "and"/"which"/"while."
- **Active voice.** "The router dispatches the request," not "The request is dispatched by the router."
- **One word, one meaning.** Pick a term per concept and reuse it verbatim throughout — don't rotate synonyms ("endpoint" / "route" / "handler") for the same thing.
- **No noun-stacking.** Unpack chains like "the auth token refresh config" into "the config that refreshes the auth token."
- **Concrete verbs over nominalizations.** "Validates input," not "performs input validation."
- **Steps as numbered lists**, not dense prose, when describing a sequence.

This is a style pass, not a vocabulary restriction — domain and code terms (`Runner.Execute`, `sql_table`) stay exactly as-is; nothing gets simplified or substituted.

---

## D2 reference

D2 is text → diagram. Single binary (`d2`). Output: svg, png, pdf, pptx, gif, txt/ascii — we render **png** for Basecamp. Default layout `dagre`; `elk` (bundled) is better for ER. Verified against d2 0.7.1.

**Architecture (containers + arrows).** Nest children to group a subsystem; `->` connects; shapes via `{shape: ...}` (`cylinder` for stores, `queue`, `package`, `person`, …):
```d2
cli: CLI (cobra)
engine: Scan Engine
adapters: Adapters {
  nmap
  zap
  nuclei
}
store: Results Store {shape: cylinder}

cli -> engine: run scan
engine -> adapters.nmap: dispatch
adapters -> store: write findings
engine -> store: merge + reconcile
```

**Data model (ER).** `shape: sql_table`; each row is `name: <type> {constraint: ...}` (`primary_key`→PK, `foreign_key`→FK, `unique`→UNQ). Render with `--layout elk` so FK arrows hit the exact row. (Verified for d2 0.7.1 — the constraint goes in a block *after* the type; the `{type: ..., constraint: ...}` map form on d2lang.com fails here with "columns cannot have children".)
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: varchar {constraint: unique}
}
scans: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
  status: varchar
}
scans.user_id -> users.id
```

**Sequence (flow).** Actors appear in definition order; `actor -> actor: msg`; self-messages allowed; a nested object with no outgoing arrow becomes a note; a container groups a fragment:
```d2
shape: sequence_diagram
user: User
cli: CLI
engine: Engine
user -> cli: run "scan example.com"
cli -> engine: Execute(target)
engine -> engine: dispatch adapters
engine -> cli: merged report
cli -> user: print results
```

**Notes:**
- One idea per diagram. Many small > one huge.
- **Labels can't contain `{` or `}`** — D2 parses braces as an edge/shape map and the compile fails ("edge map keys must be reserved keywords"). Rephrase: `JSON — date, description, postings`, not `JSON {date, description, postings}`. Parentheses in labels are fine.
- Diagrams embed as **static PNGs** — D2 tooltips and links won't work; put that info in the prose.
- You can embed Markdown/code inside a shape (`x: |md ... |`, `x: |go ... |`) to show a key signature on the diagram.
- `d2 validate` before rendering, `d2 fmt` to tidy the source.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 0 | Scope gated | App/CLI/library documented; static/marketing site skipped | Stop; tell Matt it's out of scope |
| 1 | Right Basecamp project | Docs land in the project's own project (from `.basecamp/config.json`) | Read the config; never a shared project |
| 2 | Understanding is real | Docs explain why/relationships, not just restate signatures | Re-read the source and the pitch/git history |
| 3 | Every module covered | Manifest 100%: each module/file explained in the Module Guide | Document the gaps before handoff |
| 4 | Decisions captured | A Decisions & Why doc exists with real rationale | Add it; mine pitch no-gos/rabbit holes + git log |
| 5 | Rationale honest | Inferred is labeled; unknowns flagged; nothing fabricated | Relabel guesses; flag unknowns |
| 6 | Reference pointer in index | Start Here gives the on-demand command to generate the symbol reference | Add the command (or note the source is the reference) |
| 7 | Docs match reality | Describe what the code does, not PRD/AI claims | Re-read source, correct |
| 8 | Exclusions named | Any deliberate omission stated in the docs | Add a note |
| 9 | Diagrams render inline | `<bc-attachment>` tags embed, images visible | Re-attach; tag verbatim in HTML content |
| 10 | Diagram docs are HTML | Any doc with a `<bc-attachment>` is fully HTML | Convert that doc's Markdown to HTML |
| 11 | Repo untouched | `git status` clean — all working files in scratch, nothing committed to the repo | Remove anything written into the project |
| 12 | Index covers both | Start Here has learning path + reference command | Write it |
| 13 | Sentence-level style | Short active sentences; consistent terms; no noun-stacking | Rewrite the offending passage |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Docs just restate signatures | Treated docs as a symbol dump | Capture why/relationships/gotchas; leave signatures to the on-demand generated reference |
| Fabricated-sounding rationale | Guessed at the why | Label inferred, flag unknowns, never invent |
| A module isn't explained anywhere | Skipped the manifest reconcile | Build the manifest in step 2; verify 100% in step 8 |
| Generated files left in the repo | Wrote diagrams/manifest/reference into the project | Work in a scratch dir; `git status` must be clean (step 8) |
| Only an overview, no depth | Skipped the Module Guide | One section per module with narrative depth on key symbols |
| Docs describe features not in the code | Wrote from the PRD/old AI build | Document what the code does; re-read |
| "Important parts only" / silent truncation | Capped coverage without saying so | Cover every module; if you must exclude, name it |
| Markdown renders as literal `#`/`*` in a diagram doc | Embedding a `<bc-attachment>` disabled Markdown conversion | Author diagram docs fully in HTML |
| Diagram doesn't show | Used a link/append instead of the inline `<bc-attachment>` tag | Embed the tag from `basecamp attach` verbatim in the HTML |
| `d2: command not found` | D2 not installed | `brew install d2` |
| D2 fails: "edge map keys must be reserved keywords" | A diagram label contains `{` or `}` | Rephrase the label without braces |
| rdoc: "directory ... isn't an RDoc directory" | Output dir was pre-created | Let the generator make its temp dir; don't `mkdir` it first |
| Wrong/shared Basecamp project | Didn't read `.basecamp/config.json` | Read it; docs go in the project's own project |
| Diagram is an unreadable hairball | One mega-diagram | Split into focused per-subsystem diagrams |
| Docs rot a week after writing | Documented a mid-build codebase | Run at build-finish / between cycles — judge by todolist completion, not git recency; ask if unsure (step 1) |
| Absolute `/Users/...` paths in the docs | Cited local paths instead of repo-relative | Use repo-relative paths everywhere |
| Wrongly called a finished project "mid-build" | Inferred from recent commits | Read todolist completion across all lists (ignore forward-looking ones); polish commits ≠ in progress; ask Matt if ambiguous (step 1) |

---

## Examples

Two clean runs, both source-fact-checked. Use them as the shape to aim for.

**zeni (2026-06-28)** — Ruby gem / CLI (natural-language hledger entry via local Ollama). 8 lib modules + entry point, flat (no Module Guide subfolder). 6 docs: Start Here, Architecture & Mental Model, Decisions & Why, Module Guide, Key Flows, Glossary. 2 diagrams (architecture graph + `log`-flow sequence). Public GitHub but unpublished gem → reference pointer used the `rdoc` one-liner, not rubydoc.info; Start Here got a Source link; Decisions got clickable commit SHAs. The "Decisions & Why" mined the dev log + git history + PRD no-gos, with inferred reasons labeled. No Data Model doc (state is files, not a DB — noted explicitly).

**garp (2026-06-28, run by a separate build session)** — Go static-site generator (single binary; Pongo2 + goldmark + an 11ty-style data cascade). 13 flat files, `package main`. Same 6-doc structure; "module" = file. Reference pointer used `go doc` / pkg.go.dev. Proved the skill holds when run by a different session: repo left untouched (scratch-only), diagrams embedded inline, Further reading + Source + commit links all present. A later source fact-check found **zero inaccuracies** — it correctly captured non-obvious details (exit-2-vs-1, the reference-cycle-avoidance data copy, the custom Pongo2 loader, the `time.Time` date-wrapper trick).

**since (2026-06-28, run by a separate session)** — Swift macOS menu-bar app (AppKit, SwiftPM, ~860 lines / 9 files), a stateful "time since last done" tracker. Exercised two things the others didn't, both handled right:
- **A stack the skill doesn't list (Swift).** Swift-DocC would add a build-plugin dependency this *zero-dependency project deliberately avoids*, so the symbol-reference fell back to "the source is the reference" with a clone pointer — installed nothing, faked no hosted link, respected the project's own no-dependency decision. This is the model for any unlisted language.
- **Persisted state → a Data Model doc** (7 docs, not 6) with an ER diagram, accurate to the one persisted shape (`Item` JSON array at `~/.config/since/items.json`), and correctly separating stored fields from derived-never-stored computed properties.

**What all three got right:** every module accounted for; decisions sourced and honestly labeled (commit-linked when the repo is public *and* a decision traces to a SHA — `since` had none, which was correct); signatures left to the generated/hosted/source reference, not transcribed; the repo left completely untouched.
