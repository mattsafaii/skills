# Skills

Matt's own skills. One directory per skill, each with a `SKILL.md` carrying YAML frontmatter (`name`, `description`) and whatever it needs beside it — `references/`, `evals/`, `scripts/`.

This repo is the source of truth. Edit it here; there is nothing to install.

## How it's read

**Pi** loads the whole directory through `~/.pi/agent/settings.json`:

```json
"skills": ["~/Code/skills"]
```

No symlink, no build step. A new skill is available on the next session; a changed one on the next turn. **Third-party skills don't belong here** — they live in `~/.agents/skills` and are managed by the `skills` CLI (`.skill-lock.json` tracks them).

## Adding a skill

Make the directory, write `SKILL.md`, and lead the description with when to use it — that sentence is the only thing an agent sees before deciding to load the file. Mention the skill by name elsewhere in the repo if another skill should hand off to it.
