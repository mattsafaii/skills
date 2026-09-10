# Content Ideas Skill Guide

Sweep a time window across everything Matt worked on, distill the insights, and create content idea cards with source attribution. The output is content ideas — for an essay, a tweet, a video, a thread, whatever the insight warrants — each drafted or seeded per Matt's writing rules, each linking back to its source.

**What makes a content-ideas run good:** the cross-cutting connections. A single `/dev-log` run sees one session in one repo. Content Ideas sees *the whole period across every project at once* — so its unique value is patterns like "you reached for a local model in zeni AND constrained-output in CalMirror — same technique, that's one essay." Hunt for those.

---

## Fixed IDs (don't ask Matt)

- **Safaii Studio account:** `6191443`
- **Zonebrite account:** `6060605`
- **Content project:** `46824770` · card table `9768310845` · **Ideas column `9768310846`** (essays/videos land here, prefixed `[Essay]` / `[Video]`)
- **Distribution table:** `10010006453` · **Triage column `10010006454`** (insights/tweets land here, prefixed `[💡 Insight]`)
- **Lab project:** `46824335` (scrapped ideas live in its **Graveyard** column)
- Personal repos: `~/Work/personal/*`

---

## Routing — where an idea goes

Match the idea to the board that already owns that content type (keeps the two-board separation intact):

- **Build-in-public insight / technique / pattern / gotcha from the work** → `[💡 Insight]` card in **Distribution Triage** (`10010006454`). Clay draft.
- **Personal essay or video topic** — a stance, an approach, a philosophy, "me as a person, not a project" → **Essays & Videos table, Ideas column** (`9768310846`), prefixed `[Essay]` or `[Video]`. **Seeds only** (essays are Matt's voice; `develop-essay` owns them).
- When genuinely unsure, default to `[💡 Insight]` in Distribution and note "could be an essay" in the body.

---

## Writing rules (hard — same as the rest of the system)

- **Essays / videos: seeds only.** Capture the angle, never draft the prose. `develop-essay` does the writing with Matt.
- **Tweets / insights: draft clay.** Draft as a starting point; Matt rewrites. Mark every clay card: *"Draft clay — rewrite in your voice. NOT for posting as-is."* When drafting for X, apply the X-algorithm reference at `~/Work/skills/distribute/references/x-algorithm.md` (reply/dwell/share/profile-click positives; never engagement-bait — it's subordinate to the writing rules) **and read `references/voice.md`** (in `distribute/references/`) so clay lands in Matt's voice (short, plain, lowercase-starting, understated, first-person-specific).
- **Gut-check claims.** These are mined from the work — flag any strong claim so Matt confirms he stands behind it.
- **Don't over-produce.** A period of work yields a *few* real insights, not twenty. Most commits are not insights. A high bar beats a wall of filler cards. If a window is thin, say so and produce little.

---

## ⚠ Client-work confidentiality (the #1 guardrail)

Client work (Zonebrite account `6060605`, Safaii client projects) is in scope because the real-world lessons are valuable — but the surface for leaking a client's specifics is large here. Rules:

- Extract only the **generic, transferable** lesson. Never a client's name, situation, data, numbers, or anything that identifies them.
- "Installing cameras taught me X about Y" is fine; "Client Z's site had problem W" is **not**.
- When in doubt, **drop it**. A missed insight costs nothing; a leaked client detail is unrecoverable.
- Surface client-derived cards to Matt explicitly at confirmation so he can veto.

---

## Source attribution (the killer feature)

Every card body ends with a **`🔗 Source:`** line — a **citation, not necessarily a hyperlink**. So Matt can always see *why* it's flagged as an insight, and it doubles as proof the work happened. Multiple sources are fine (that's often the cross-project pattern).

- **Linkable** → hyperlink it: a Basecamp dev-log/message/card URL, or a git commit (link to GitHub if the repo has a remote, e.g. `github.com/mattsafaii/zeni`; otherwise cite as `zeni@a1b2c3d`).
- **Not linkable** → name the provenance in plain words. Be specific and honest:
  - **Cross-project synthesis** (no single link — the insight *is* the connection): "Synthesis across zeni's account-constraining and CalMirror's UID-diffing."
  - **A realization while working:** "Realized building Since's streak-confirm logic."
  - **A conversation / offline:** "Conversation with Mike re: camera installs" (apply the client-confidentiality filter — describe the lesson, not the client).
  - **An outside source** (book, article, tweet): cite it by name, link if a URL exists.
- **Never** fabricate a link, attach a vaguely-related one to look rigorous, or drop the line. An unlinkable source still gets named — "where did this come from?" must always have an honest answer, even if that answer is "a realization, no artifact."

---

## Workflow

### 1. Establish the window

Take the period from Matt (past week / 2 weeks / month / since a date). Default if unspecified: **past 2 weeks**. Convert to an absolute start date for the gathering commands.

### 2. Sweep the sources

Gather raw material from the window across all of these. Verify exact CLI flags with `basecamp <cmd> --agent --help` if unsure.

- **Personal repos (git):** across every repo, commits (and diffs for the meaty ones) in the window. Includes scrapped/abandoned repos — a dead project often has the sharpest lesson.
  ```bash
  for d in ~/Work/personal/*/; do
    [ -d "$d/.git" ] || continue
    log=$(git -C "$d" log --since="<START>" --pretty='%h %s' 2>/dev/null)
    [ -n "$log" ] && printf '### %s\n%s\n\n' "$(basename "$d")" "$log"
  done
  ```
- **Basecamp dev logs:** the narrative "Dev log —" messages (already distilled what+why — prime material). Both accounts.
  ```bash
  basecamp recordings messages --in <project> -a <account> --json   # filter by created_at in window
  ```
- **Basecamp messages / cards / Graveyard:** broader board activity and scrapped ideas (Lab Graveyard) — catches decisions not in git.
- **Latest Activity (timeline):** the cross-account catch-all — surfaces what git and dev logs miss. Run per account.
  ```bash
  basecamp timeline -a 6191443 --json     # Safaii
  basecamp timeline -a 6060605 --json     # Zonebrite
  ```
- **Client work:** Zonebrite + Safaii client projects — under the confidentiality guardrail above.

### 3. Dedupe against what's already captured

Before distilling, list existing insight/idea cards so you don't re-mine what `/dev-log` or a prior content-ideas run already caught:

```bash
basecamp cards list --column 10010006454 --card-table 10010006453 --in 46824770 -a 6191443 --jq '.data[].title'   # existing [💡 Insight] + pieces
basecamp cards list --column 9768310846  --card-table 9768310845  --in 46824770 -a 6191443 --jq '.data[].title'   # existing [Essay]/[Video] ideas
```

Skip anything substantially already there. The run.s job is what's *new* or what only emerges *across* the period.

### 4. Distill

From the raw material, pull genuine insights: things learned, new techniques, patterns tried, an approach to something, a decision and its reasoning, a mistake and the fix, a scrapped idea and *why* it died. Prioritize:

- **Cross-project patterns** — the same idea showing up in two+ places. These are the strongest and most essay-worthy.
- **Non-obvious, transferable** takeaways — useful to someone else, not just a diary entry.
- High bar. Reject the merely-happened. If it wouldn't be interesting to another builder, it's not an insight.

### 5. Draft the cards

For each surviving insight: route it (step: Routing), draft per the writing rules (clay for insights/tweets, seeds for essays/videos), and attach the `🔗 Source:` line. Title:

- `[💡 Insight] <takeaway> (<Project or cross-cutting>)` → Distribution Triage
- `[Essay] <topic>` or `[Video] <topic>` → Essays & Videos table, Ideas column

### 6. Confirm before posting to Basecamp

Show Matt the full list — title, one-line description, target board, and source — grouped by board. **Call out any client-derived cards explicitly.** Get approval; he'll cut/rescope. Only then create them.

### 7. Create the cards

```bash
# Insight → Distribution Triage. Source is linked when linkable...
basecamp cards create -a 6191443 "[💡 Insight] <takeaway> (<Project>)" "<blockquote><draft></blockquote><p><em>Draft clay — rewrite in your voice. NOT for posting as-is.</em></p><p>🔗 <strong>Source:</strong> <a href=\"<url>\"><what></a></p>" \
  --in 46824770 --card-table 10010006453 --column 10010006454 --jq '.data.app_url'

# ...or plain text when it isn't (cross-project synthesis, a realization, an offline source):
#   <p>🔗 <strong>Source:</strong> Synthesis across zeni + CalMirror — same constrain-the-model idea.</p>

# Essay idea → Essays & Videos table, Ideas column
basecamp cards create -a 6191443 "[Essay] <topic>" "<p><strong>Angle:</strong> <seeds, not prose></p><p>🔗 <strong>Source:</strong> <a href=\"<url>\"><what></a></p>" \
  --in 46824770 --card-table 9768310845 --column 9768310846 --jq '.data.app_url'
```

Use a **heredoc** for bodies (shell-escaping; HTML sent as-is for cards). One card per idea.

### 8. Confirm

List created cards grouped by board, with sources. One line on what the period's strongest theme was, if there is one.

---

## Scheduled / recurring use

Content Ideas runs on-demand by default. To run it weekly, set up a routine with `/schedule` (cloud cron) that invokes this skill with a "past week" window — or `/loop` for a session-local recurring run. The skill is the same either way; scheduled mode just passes a fixed window and relies on the step-3 dedupe to avoid repeats. Offer this once after a successful on-demand run; don't set it up unprompted.

---

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---|---|---|
| Wall of low-value cards | Treated every commit as an insight | Raise the bar; most work isn't insight-worthy. Fewer, stronger. |
| Re-created an existing insight | Skipped the dedupe step | Always list existing cards first (step 3) |
| Leaked a client detail | Confidentiality filter too loose | Generic lesson only; when in doubt drop; flag client cards at confirmation |
| Drafted essay prose | Essays are seeds-only | Capture the angle; `develop-essay` writes it |
| Missed the best insight | Only looked at git | Sweep dev logs + timeline too — the connection is often across sources |
| Card has no source | Forgot attribution | Every card ends with a `🔗 Source:` line |
| Dropped a hard-to-link insight (often the best, cross-project one) | Assumed source must be a URL | Source is a citation, not a link — name it in plain words; never skip the insight for lack of a link |
| Attached a vaguely-related link to look rigorous | Forced a hyperlink | If it's not genuinely linkable, write the plain-text provenance instead |
| Body breaks on quotes / posts raw HTML | Shell escaping | Heredoc for the body; HTML is sent as-is for cards |
| Proposed video cards freely | YouTube is deferred | Capture video-worthy ideas as `[Video]` Content cards but note deferred; don't push video as a channel |

---

## Related

- `/distribute` — the forward counterpart: one known project → a full campaign. Content Ideas feeds it (an insight may grow into a project campaign).
- `/dev-log` (step 6) — per-session insight capture. Content Ideas is the periodic cross-source version; dedupe against what dev-log already made.
- `develop-essay` — owns essays end to end. Content Ideas only captures essay *angles*.
- Distribution Playbook (doc `10016763197`) — the rulebook for the card taxonomy and writing rules.
