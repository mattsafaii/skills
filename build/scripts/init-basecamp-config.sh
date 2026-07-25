#!/usr/bin/env bash
# Wires a freshly scaffolded repo to its Basecamp project/todolist and
# keeps the local-only config files out of git. Idempotent-ish: safe to
# rerun, though `config init` will complain if already initialized.
set -euo pipefail

if [ "$#" -ne 3 ]; then
	echo "Usage: init-basecamp-config.sh <repo_path> <project_id> <todolist_id>" >&2
	exit 1
fi

repo_path="$1"
project_id="$2"
todolist_id="$3"

cd "$repo_path"
basecamp config init
basecamp config set account_id 6191443
basecamp config set project_id "$project_id"
basecamp config set todolist_id "$todolist_id"
basecamp config trust
printf '.basecamp/\n' >> .gitignore
