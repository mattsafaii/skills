---
name: document
description: Document an app, CLI, or library codebase so a reader can learn it deeply — what each part does, how the parts relate, and WHY it's built that way (the decisions behind the code) — published into that project's own Basecamp project Docs with inline diagrams. Writes narrative learning docs (architecture, decisions, complete module guide, key flows) and delegates symbol-level signature lookup to the language's own doc generator. Reads the actual source (AI-built or human-built); never fabricates rationale. Skips static/marketing/landing sites. Runs inside the repo (the build agent's finalize step, or standalone anytime). Use when Matt says "document the codebase", "document this project", "write the architecture docs", "generate docs", "explain this codebase", or "/document".
---

# Document Skill

Produce documentation that lets a reader **learn a codebase** — start knowing nothing, end up understanding what each part does, how the parts relate, and **why** it's built the way it is. Works on code built by AI or by a person; the source is the truth.

**First principle:** document what the code *can't* tell you. A reader gets signatures and names for free by reading the source. The valuable, expensive part — the *why* (decisions, alternatives, tradeoffs), the *relationships* (architecture, flows), the *mental model*, the *gotchas* — is what these docs capture. So:

- **Learning docs → Basecamp** (narrative, the hard part): Architecture & Mental Model, Decisions & Why, a complete Module Guide, Key Flows, Data Model, Glossary — with inline diagrams.
- **Symbol reference → linked or on-demand** (the lookup part): for published packages the index links the auto-hosted API docs (rubydoc.info / pkg.go.dev / docs.rs); otherwise it gives a one-line command to generate signatures with the language's own doc tool (`go doc`, `cargo doc`, rdoc) into a temp dir. Never persisted, never hand-transcribed into Basecamp. The skill never edits the source (no adding comments).

**Completeness** = every module/file is accounted for and explained at the right altitude (nothing silently skipped) — *not* a hand-written entry per symbol. Important functions get narrative depth; trivial ones get a mention; per-signature completeness is the generated reference's job.

**Rationale honesty:** documented reasons are stated as fact, inferred reasons are labeled, genuine unknowns are flagged. Never fabricate a plausible-sounding why.

**Scope:** apps, CLIs, libraries, services. **Not** static/marketing/landing sites — gate first.

**Where it runs:** inside the repo (it reads the code). The build agent runs it as a finalize todo, or Matt runs `/document` standalone anytime. Large codebases: fan the Module Guide out to subagents.

Open `@references/guide.md` and follow it. Do not proceed without it.
