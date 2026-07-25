#!/usr/bin/env python3
"""Move work between a Basecamp todolist and this repo's Solo todos.

Basecamp stays the record. Solo todos are the lane board for one build run:
blockers so a lead doesn't dispatch too early, locks so you can see who owns
what. This script keeps the two in step without turning Solo into a second
tracker.

  import   Basecamp todolist -> Solo todos (one way, run at the start of a run)
  ship     one Solo todo -> SHA comment on Basecamp + both marked done
  status   show the mapping

The Basecamp todo id rides along as a Solo tag (bc-<id>), so the mapping
survives restarts and needs no state file. Stdlib only.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

DISCOVERY = os.path.expanduser("~/.config/soloterm/http-api.json")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


# --- Solo -------------------------------------------------------------------


def solo_bootstrap():
    """Port and token for the local Solo HTTP API. Rewritten on app restart."""
    try:
        with open(DISCOVERY) as f:
            d = json.load(f)
        return f"http://127.0.0.1:{d['port']}", d["token"]
    except FileNotFoundError:
        die("Solo is not running (no http-api.json). Start Solo and retry.")
    except (KeyError, ValueError):
        die(f"{DISCOVERY} is unreadable — start Solo and retry.")


def solo(method, path, body=None):
    base, token = solo_bootstrap()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)["data"]
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        die(f"Solo API {method} {path} failed ({e.code}): {detail}")
    except urllib.error.URLError as e:
        die(f"cannot reach Solo API: {e.reason}")


def solo_project_for(path):
    projects = solo("GET", "/api/projects")["projects"]
    real = os.path.realpath(path)
    for p in projects:
        if os.path.realpath(p["path"]) == real:
            return p
    die(f"{real} is not a Solo project — add it in Solo (Cmd+Shift+O) first.")


def solo_todos(project_id, tags=None):
    q = "?limit=200" + (f"&tags={','.join(tags)}" if tags else "")
    return solo("GET", f"/api/projects/{project_id}/todos{q}")["todos"]


# --- Basecamp ---------------------------------------------------------------


def bc_config(repo):
    """Read .basecamp/config.json — same file the basecamp CLI uses."""
    cfg_path = os.path.join(repo, ".basecamp", "config.json")
    if not os.path.exists(cfg_path):
        die(f"no .basecamp/config.json in {repo} — run `basecamp config init` there.")
    with open(cfg_path) as f:
        cfg = json.load(f)
    for key in ("account_id", "project_id", "todolist_id"):
        if not cfg.get(key):
            die(f"{cfg_path} is missing {key}.")
    return cfg


def bc(args, repo):
    proc = subprocess.run(
        ["basecamp", *args], cwd=repo, capture_output=True, text=True
    )
    if proc.returncode != 0:
        die(f"basecamp {' '.join(args)}\n{proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def bc_json(args, repo):
    out = bc([*args, "--json"], repo)
    try:
        return json.loads(out)
    except ValueError:
        die(f"basecamp {' '.join(args)} returned no JSON:\n{out[:300]}")


def strip_html(text):
    text = re.sub(r"<br\s*/?>|</p>", "\n", text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return "\n".join(line.strip() for line in text.split("\n")).strip()


def repo_root(start):
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start, capture_output=True, text=True,
    )
    return proc.stdout.strip() if proc.returncode == 0 else os.path.realpath(start)


# --- commands ---------------------------------------------------------------


def cmd_import(args):
    repo = repo_root(args.repo)
    cfg = bc_config(repo)
    project = solo_project_for(repo)

    payload = bc_json(
        ["todos", "list", "--all", "--status", "incomplete",
         "-l", cfg["todolist_id"], "--in", cfg["project_id"], "-a", cfg["account_id"]],
        repo,
    )
    open_todos = payload.get("data") or []
    if not open_todos:
        print("Nothing to import — no open todos on the Basecamp list.")
        return

    already = set()
    for t in solo_todos(project["id"], tags=["basecamp"]):
        already.update(tag for tag in t["tags"] if tag.startswith("bc-"))

    created = skipped = 0
    for t in open_todos:
        tag = f"bc-{t['id']}"
        if tag in already:
            skipped += 1
            continue
        body = strip_html(t.get("description"))
        body = (body + "\n\n" if body else "") + f"Basecamp: {t['app_url']}"
        made = solo(
            "POST",
            f"/api/projects/{project['id']}/todos",
            {"title": t["content"][:200], "body": body, "tags": ["basecamp", tag]},
        )
        print(f"  solo #{made['id']}  {t['content'][:60]}")
        created += 1

    print(f"\nImported {created} todo(s) into Solo project {project['name']}"
          f"{f', skipped {skipped} already there' if skipped else ''}.")
    if created:
        print("Blockers are yours to wire: todo_set_blockers in the Solo MCP.")


def cmd_ship(args):
    repo = repo_root(args.repo)
    cfg = bc_config(repo)
    project = solo_project_for(repo)

    todo = solo("GET", f"/api/projects/{project['id']}/todos/{args.todo_id}")["todo"]
    bc_ids = [tag[3:] for tag in todo["tags"] if tag.startswith("bc-")]
    if not bc_ids:
        die(f"solo todo #{args.todo_id} has no bc-<id> tag — it did not come from Basecamp.")
    bc_id = bc_ids[0]

    note = args.note or f"Shipped in {args.sha}"
    bc_json(["comment", bc_id, note, "--in", cfg["project_id"], "-a", cfg["account_id"]], repo)
    bc_json(["todos", "complete", bc_id, "-p", cfg["project_id"], "-a", cfg["account_id"]], repo)
    solo("POST", f"/api/projects/{project['id']}/todos/{args.todo_id}/complete", {"completed": True})

    print(f"Basecamp #{bc_id} commented + completed; Solo #{args.todo_id} completed.")
    print(f"  {todo['title']}")


def cmd_status(args):
    repo = repo_root(args.repo)
    project = solo_project_for(repo)
    todos = solo_todos(project["id"], tags=["basecamp"])
    if not todos:
        print(f"No imported todos in Solo project {project['name']}.")
        return
    print(f"{project['name']} — {len(todos)} imported todo(s)\n")
    for t in sorted(todos, key=lambda x: x["id"]):
        bc_id = next((tag[3:] for tag in t["tags"] if tag.startswith("bc-")), "?")
        mark = "x" if t["completed"] else ("!" if t["isBlocked"] else " ")
        owner = f"  [{t['lockedBy']}]" if t.get("lockedBy") else ""
        print(f"  [{mark}] solo #{t['id']:<5} bc {bc_id}  {t['title'][:52]}{owner}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--repo", default=".", help="repo path (default: cwd)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("import", help="copy open Basecamp todos into Solo").set_defaults(fn=cmd_import)

    ship = sub.add_parser("ship", help="close one todo in both places")
    ship.add_argument("todo_id", type=int, help="Solo todo id")
    ship.add_argument("sha", help="commit SHA that shipped it")
    ship.add_argument("--note", help="comment text (default: 'Shipped in <sha>')")
    ship.set_defaults(fn=cmd_ship)

    sub.add_parser("status", help="show the Basecamp <-> Solo mapping").set_defaults(fn=cmd_status)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
