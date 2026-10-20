#!/usr/bin/env bash
# Link these skills into the places my agents read from.
# Own skills live here; third-party skills stay in ~/.agents/skills
# (managed by the skills.sh CLI) and are NOT touched by this script.
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Pi: registered via the `skills` array in ~/.pi/agent/settings.json
# ("skills": ["~/Code/skills"]) — no symlink needed.
#
# OpenCode: one whole-directory symlink is enough.
mkdir -p ~/.config/opencode
ln -sfn "$SKILLS_DIR" ~/.config/opencode/skills

echo "Skills linked (OpenCode). Pi reads them from $SKILLS_DIR via settings.json."
