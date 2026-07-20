# New Client Skill Guide

Start a new Safaii Studio client. One run: construct the Basecamp project from the chosen client template, verify its structure, optionally drop the repo config, register the client in the Master Client List, and print the hand-off checklist of the things this skill deliberately does not do.

This skill creates a real Basecamp project. It always shows what it's about to create and waits for explicit approval first.

---

## Fixed IDs

Do not ask Matt for these — they are fixed for this skill. Always pass `-a 6191443` explicitly; never trust the global default account.

- Account: `6191443` (Safaii Studio)
- Template — Client — Website: `46823738`
- Template — Client — Web App: `46824526`
- Office project: `46820187`
- Master Client List doc (the client register): `9802376865`

---

## Workflow

### 1. Collect inputs

Gather from the conversation; ask only for what's missing:

- **Client name** (required) — used as the Basecamp project name
- **Template** (required) — Client — Website or Client — Web App
- **Maintenance plan** (required) — yes/no; recorded in the register so `/client-report` knows who's due
- **Repo path** (optional) — if the client repo already exists, the skill drops `.basecamp/config.json` there. Client repos live under `~/Code/_safaii-studio/clients/`.

### 2. Duplicate guard

Before creating anything, check both:

```bash
basecamp projects list -a 6191443 --jq '.data[].name'
basecamp docs show 9802376865 --in 46820187 -a 6191443 --md
```

If the client name (or an obvious variant) already appears as a project or register entry, **stop and ask** — never create a possible duplicate. This skill is for new clients only; retrofitting an existing client project is out of scope.

### 3. Confirm

Show Matt exactly what will happen — project name, template, plan status, repo path (or none) — and wait for explicit approval. Do not construct on an ambiguous response.

### 4. Construct the project

```bash
basecamp templates construct <template_id> --name "<Client Name>" \
  --description "<one-line description of the engagement>" -a 6191443 --json
```

**Known bug (basecamp CLI 0.7.2, found 2026-07-15):** `templates construct` returns `Bad Request` no matter the arguments — the API itself works. Until the CLI is fixed, hit the endpoint directly:

```bash
TOKEN=$(basecamp auth token)
curl -s -X POST "https://3.basecampapi.com/6191443/templates/<template_id>/project_constructions.json" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"project":{"name":"<Client Name>","description":"<one-line description>"}}'
```

A `201` response contains the construction `id`. Construction is asynchronous — poll until `status` is `"completed"`:

```bash
basecamp templates construction <template_id> <construction_id> -a 6191443 --json
```

Poll every few seconds; when completed the response includes the new project (`data.project`). If polling misbehaves, fall back to finding the project by name: `basecamp projects list -a 6191443 --jq '.data[] | select(.name == "<Client Name>")'` (construction typically completes within seconds). If the project hasn't appeared after ~a minute, stop and tell Matt to check Basecamp before retrying — retrying blind risks a duplicate project.

### 5. Verify structure

Compare the constructed project against the canonical snapshot in `references/structure.md` for the chosen template:

```bash
basecamp projects show <project_id> -a 6191443 --json   # dock tools
basecamp todolists list --in <project_id> -a 6191443 --json
```

Report anything missing or unexpected as **drift** — a short list, nothing more. **Never patch the project or the template**; fixing templates is a human job. If `structure.md` still holds a placeholder for this template, snapshot the freshly constructed project's structure into it now (first-run bootstrap) and tell Matt that this construction is now the canonical reference.

### 6. Config drop (only if a repo path was given)

From inside the repo:

```bash
cd <repo_path>
basecamp config init
basecamp config set account_id 6191443
basecamp config set project_id <project_id>
basecamp config set todolist_id <todolist_id>
basecamp config trust
grep -qx '.basecamp/' .gitignore || echo '.basecamp/' >> .gitignore
```

For `todolist_id`, pick the project's primary working todolist from the step-5 listing; if it's not obvious which list code work belongs on, ask Matt. This is the entire filesystem footprint — the skill never scaffolds repos.

### 7. Register the client

The Master Client List (doc `9802376865` in Office) is the client register. Target format:

- **Active Clients** — one entry per client: name, project link, maintenance plan (yes/no), start date
- **Past & Historical** — the plain list of company names

Fetch the current doc, append the new client to Active Clients, and update. Rules:

- **Always pass both `--title "Master Client List"` and `--content`** — omitting title wipes it to "Untitled".
- Never drop existing names; every company in the doc stays in the doc.
- First run only: if the doc is still a flat list, restructure it into the two sections above (all existing names go under Past & Historical) as part of the same update.

```bash
basecamp docs update 9802376865 --title "Master Client List" --content "<HTML>" --in 46820187 -a 6191443 --json
```

### 8. Hand-off checklist

End every run by printing the new project URL and the manual follow-ups the skill deliberately does not do:

- Invite the client as a guest (when the project is ready to show)
- First invoice via Mercury
- Kickoff message on the project's Message Board

---

## Testing constraint

Never construct real projects or write to the real register as a test. Acceptance runs use a throwaway project Matt approves by name (e.g. "ZZ Test Client"), trashed afterward, and a scratch copy of the register doc — never doc `9802376865`.

---

## Eval checks

| # | Check | Pass | If fail |
|---|-------|------|---------|
| 1 | Approval gate | Nothing created before Matt's explicit yes | Add the confirm step back |
| 2 | Project constructed from template | New project exists, correctly named, from the chosen template | Check construction status; don't blind-retry |
| 3 | Drift reported, not patched | Missing todolist → reported; project untouched | Remove any auto-fix behavior |
| 4 | Flag-free CLI from repo | `basecamp todos list` works in the repo with no flags; `.basecamp/` absent from `git status` | Re-run config steps; check .gitignore |
| 5 | Register intact | After update: title unchanged, all prior names present, new entry readable with plan status | Restore from doc history; always pass --title and --content |
| 6 | Duplicate guard | Existing client name → skill stops and asks | Run guard before construct, not after |
| 7 | Checklist printed | Every run ends with project URL + the three manual follow-ups | Add to the final output |

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `construct` returns Bad Request | basecamp CLI 0.7.2 payload bug (API works) | Use the curl fallback in step 4; retest the CLI after upgrades |
| Duplicate project created | Guard skipped, or construct retried while a construction was still pending | Always guard first; on slow constructions check Basecamp before retrying |
| Register title becomes "Untitled" | `docs update` without `--title` | Always pass both `--title` and `--content` |
| Register loses historical names | Content rebuilt from scratch instead of from the fetched doc | Always fetch current content and append |
| Wrong account / 404 | Missing `-a 6191443` | Always pass the account flag explicitly |
| `construct` errors immediately | `--name` omitted (it's required) | Pass `--name` |
| basecamp commands need flags in the repo | Config not trusted or todolist_id unset | `basecamp config trust`; set all three ids |
| Drift check flags a lived-in project | Skill run against an existing client project | New clients only — stop; this is out of scope |
| Test entries in the real register | Eval ran against doc 9802376865 | Use a scratch doc for testing, then delete it |

---

## Examples

- Acceptance run 2026-07-15: throwaway "ZZ Test Client" from the Website template — all seven eval checks passed; produced the structure snapshot in `structure.md` and surfaced the CLI construct bug. The first real client onboarded with this skill becomes Example 1.
