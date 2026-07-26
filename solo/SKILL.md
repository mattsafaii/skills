---
name: solo
description: How to use Solo's coordination tools — scratchpads for durable context, spawned workers, wake-on-idle timers, locks, and the Basecamp todo bridge. Use when work needs to outlive this session or move between agents — writing down a plan before context compacts, handing off to the next session, spawning a worker to run a slice or review a commit, waiting on a long build/test/scan without polling, or when two agents are editing the same repo. Triggers on "write this down", "save this context", "hand this off", "spawn a worker", "delegate this", "run this in the background", "wake me when it's done", "what was I doing here", or any mention of Solo scratchpads, todos, timers, or locks.
---

# Solo

Solo sits above Claude, OpenCode, and the rest. It doesn't replace them — it adds tools they can call: a place to write things down, a way to start and brief other agents, and a way to sleep until something finishes.

This covers those tools. Solo injects its own getting-started for processes and ports; that side isn't repeated here. `help(topic="...")` in the Solo MCP has the full reference for any tool below.

Every project runs inside Solo, so these tools are always there. Reach for them when work has to outlive the session.

## 1. Write it down

Context dies three ways: compaction, session end, and handoff to another agent. A scratchpad survives all three. Basecamp keeps the record of what was decided; the scratchpad keeps the working state — where the work stands right now.

**One `state` scratchpad per project.** Name it `<Project> — state`, tag it `state`. Read it first in a fresh session; update it at the end of one.

```
scratchpad_list(tags: ["state"])          # find it
scratchpad_read(scratchpad_id)            # returns content + revision
scratchpad_append_section(id, heading, content, expected_revision)
```

Write to it:
- after a plan settles, before any code
- when context is about to compact
- at the end of a session
- before spawning a worker (the worker reads it instead of being re-briefed)

What belongs in it: the decision and why, where the work stands, the next step, open questions, the commands and paths that matter. What doesn't: a copy of the Basecamp todos, or code that belongs in the repo.

Long research or a shaped plan gets its own scratchpad tagged `plan` — keep `state` short enough to read in one gulp.

Use `scratchpad_edit` or `scratchpad_append_section` for changes, not `scratchpad_write` — a full overwrite loses whatever another agent added. Pass `expected_revision`; if it fails, re-read and redo the edit.

At the end of a cycle, `scratchpad_save_to_file` can drop it into the repo or feed a Basecamp doc.

## 2. Delegate

Four agent tools are configured. Resolve ids with `list_agent_tools` — don't hardcode them.

| Tool | Use for |
|---|---|
| **Claude** | Matt's own sessions. Asks before it acts. |
| **Claude (unattended)** | Spawned workers doing real work in a repo. Skips permission prompts — which is also what keeps idle timers honest (see below). |
| **OpenCode** | Medium coding work on the Go plan. Limited budget — don't default to it. |
| **OpenCode (local)** | Free local model, auto-approving. Boilerplate, greps, formatting, high-volume small jobs. |

Smart orchestrator, cheap workers. A review, a scan, a mechanical sweep does not need the expensive model.

Spawn and brief in the same turn — a spawned agent sits there doing nothing until it gets input:

```
spawn_agent(agent_tool_id: <id>, name: "Review: auth", project_id: <id>)
send_input(process_id: <returned>, input: "<brief>")
```

`extra_args` on `spawn_agent` adds flags for one launch without touching the saved tool.

The brief must stand on its own — the worker has none of this conversation:

> You are reviewing <scope> in <repo>. Background: scratchpad <id>. Do not edit files outside <path>. When you're done, report: files changed, checks run and their result, blockers, remaining risk. Don't revert changes you didn't make — other agents are in this repo.

Rules that don't bend:
- **Never send new work into an existing session.** Its context belongs to another task, and the input interrupts it mid-turn. Spawn a fresh one.
- **Never close a session you didn't spawn.** Matt runs several agents per repo; idle often just means he stepped away.
- **A spawned worker stays in its repo.** Never let it edit `~/.claude`, `~/.dotfiles`, or another project.

Close your own workers once you've harvested them.

## 3. Wake

Never poll. No `sleep 60`, no loop that checks output again and again — set a timer and end the turn. Solo injects the timer body as a fresh user turn when it fires, so the agent wakes up with instructions in hand.

```
timer_fire_when_idle_all(processes: [<ids>], max_wait_ms: 1800000, body: "<what to do next>")
timer_fire_when_idle_any(processes: [<ids>], max_wait_ms: 600000, body: "...")
timer_set(delay_ms: 300000, body: "...")
```

Also worth it single-agent: a long Go build, a Rails suite, a docker scan. Start it, set a timer, stop watching.

Four things get this wrong:

1. **Always pass `max_wait_ms`.** Treat it as required. 30 minutes is a sane ceiling.
2. **Schedule after dispatching, never before.** `idle_any` watches for a *transition* — anything already idle when the timer is set is ignored, and the timer decays into a plain sleep.
3. **Read the status that comes back.** `scheduled` means it's really watching. `waiting_for_max_wait` or `already_satisfied` means it isn't — fix it now rather than waking up in half an hour.
4. **An agent stuck on a permission prompt never goes idle**, so the timer never fires. Spawn workers with **Claude (unattended)** or **OpenCode (local)** and it can't happen. If a timer expires on max-wait instead of idle, check the worker for a prompt before assuming it's still working — approve with `send_input` bytes `[13]`.

The body is delivered verbatim as a user turn. Write it as plain instructions with everything needed to act cold: process ids, scratchpad id, next action. Skip XML-ish tags and heavy code fences.

## 4. Lock

Only matters when two agents share a repo — which happens here often enough to be worth the habit.

```
lock_acquire(key: "repo.migrations", lease_ttl_seconds: 1800)
... edit, commit ...
lock_release(key: "repo.migrations")
```

Keys name the area, not the file: `repo.migrations`, `repo.css`, `repo.solo-yml`. Check with `lock_status` before editing something shared. Release when the work lands. Skip locks entirely when you're the only agent writing.

## 5. Todos, and the Basecamp bridge

**Basecamp is the record. Solo todos are the lane board for one run** — blockers so nothing starts too early, locks so it's clear who owns what, comments for handoffs. A Solo todo never stands in for a Basecamp todo.

`/build` imports the todolist as part of setting a project up, so every build has the mirror: progress visible in the sidebar next to the agent, and one command that closes a unit properly in both places. Outside a build — a one-off fix, a spike, a piece of client work — import only when there's real ordering to track.

```bash
python3 ~/.claude/skills/solo/scripts/basecamp-bridge.py import     # open Basecamp todos -> Solo
python3 ~/.claude/skills/solo/scripts/basecamp-bridge.py status     # show the mapping
python3 ~/.claude/skills/solo/scripts/basecamp-bridge.py ship 42 a1b2c3d
```

`import` is one-way and safe to rerun — it skips what's already there. It reads `.basecamp/config.json` in the repo and matches the Solo project by path. Blockers are yours to wire afterwards with `todo_set_blockers`.

`ship` closes one unit properly: comments the SHA on the Basecamp todo, completes it there, completes the Solo copy. It finds the Basecamp id from the Solo todo's `bc-<id>` tag.

Locking a Solo todo (`todo_lock`) before starting it is how a lead keeps two workers off the same lane.

## What not to use

**KV.** It exists for small status values many workers need to discover. One person with a few agents has no discovery problem — a tagged scratchpad does the same job in one mechanism instead of two. Skip it.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Lead waits the full `max_wait_ms` every time | Worker was blocked on a permission prompt, so it never went idle | Spawn workers with the unattended tool; approve a stuck prompt with `send_input` bytes `[13]` |
| Timer fires immediately or acts like a sleep | Scheduled before dispatch, or every watched process was already idle | Dispatch first, then schedule; read the returned status instead of assuming |
| Scratchpad edit wipes another agent's work | `scratchpad_write` used for a partial change | Use `scratchpad_edit` / `scratchpad_append_section` with `expected_revision` |
| Fresh session has no idea where things stand | Nothing was written down before the last session ended | Update the `state` scratchpad at session end, read it at session start |
| A worker interrupted an unrelated task | New work sent into an existing session | Always spawn fresh; never `send_input` a new task into a running session |
| Two agents clobber each other's edits | No lock on a shared area | `lock_acquire` before editing, release after the commit |
| Solo todos drift from Basecamp | Work closed in one place only | Close through `basecamp-bridge.py ship`, not by hand |
| `bridge import` says the repo isn't a Solo project | Repo was never added to Solo | Add it (Cmd+Shift+O), or `create_project` over the MCP |
| Bridge can't reach Solo | Solo restarted and rewrote its port and token | Just rerun — the script re-reads them each call |
