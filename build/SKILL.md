---
name: build
description: Start a build cycle for a project in the Up Next column. Run it from anywhere with the Solo MCP connected — cwd doesn't matter; it spawns the build agent into the correct Solo project. Reads the PRD, derives a todolist, creates the Basecamp project and todos, scaffolds the repo in a new workspace, registers it in Solo, spawns a fresh build agent inside it, and moves the card to In Progress. For a cycle on an existing project, reuses the project, repo, and Solo registration instead of creating them. Use when Matt says "let's build", "start building", "kick off the build", "start the cycle", or "/build".
triggers:
  - let's build
  - start building
  - kick off the build
  - start the cycle
  - ready to build
---

# Build Skill

Place the bet. Reads the PRD, derives and confirms a todolist, creates the Basecamp project + todos, scaffolds the workspace, registers it in Solo, spawns the build agent with its first prompt, and moves the card to In Progress. If the card is a cycle on an existing project, the existing Basecamp project, repo, and Solo registration are reused — only the cycle's PRD doc, kickoff, and todolist are created.

Run this from anywhere with the Solo MCP connected — cwd is irrelevant, since it spawns the build agent into the project looked up explicitly. The actual build happens in the spawned agent's session inside the project directory — never code the build here. (Footnote: avoid running it from the target repo's actively-building agent — that works but is a session spawning a sibling into its own project.)

Open `@references/guide.md` and follow it. Do not proceed without it.
