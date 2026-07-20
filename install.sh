#!/usr/bin/env bash
# Link these skills into the places my agents read from.
# Own skills live here (~/Code/skills); third-party skills stay in ~/.agents/skills
# (managed by the skills.sh CLI) and are NOT touched by this script.
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# OpenCode: one whole-directory symlink is enough.
mkdir -p ~/.config/opencode
ln -sfn "$SKILLS_DIR" ~/.config/opencode/skills

# Claude Code: reads only ~/.claude/skills/, and that dir is shared with the
# skills.sh symlinks, so link each own-skill individually and leave the rest alone.
mkdir -p ~/.claude/skills
for d in "$SKILLS_DIR"/*/; do
  ln -sfn "${d%/}" ~/.claude/skills/
done

echo "Skills linked (OpenCode + Claude Code)."
