# Client reports — state

**August cycle (Konnected Concepts) — closed 8 Sep 2026.** First end-to-end run through the frozen pipeline. Delivery: HEY email scheduled 6am 9 Sep (handoff letter pasted + report PDF attached — Mehari is not on Basecamp; delivery channel recorded in the context doc). Report doc "Site report — August 2026" awaits Matt's move to Deliverables > Reports. Five review items staged on branch `review-content-pass` (Access-protected preview) pending Mehari's approval, then merge to master.

**Next:** Oct 3 2026 — launchd `com.mattsafaii.client-monthly` first run (Site report — September 2026, Konnected). Prep script + full-query pull ready. Lead-gate build queued as Backlog card 10280166755 (design done). Guru Packaging context doc + Mercury Net 10 still open on Matt.

**Contract changes since the freeze (all Matt/Grok-directed):**
- Heading "This month" → **"What happened"** (reader-timeless; never This/Last month)
- **What's next** = 1–3 priorities, I + verb + object, no padding, yes-free work only (Grok contract)
- Doc title **"Site report — <Month Year>"** (was "Monthly site report"); handoff doc = "Handoff — <Month Year>"
- **Events ≠ leads**: submissions become leads only at Matt's review gate; withheld GSC queries are unattributed, never non-brand
- Billing: Net 10 from Sep 2026 (memory file)
- Business overview now carries `Site launched:` (Konnected: June 25, 2026 — April Fathom install tracked the old site)
- What I did cap (≤4 lines) bent to 5 for August (Pages CMS bullet added at Matt's request)

**Pipeline changes:**
- `gsc-fetch.rb` now pulls the FULL query list (25k cap) — brand/non-brand split is exact; tested on Konnected Aug (217 rows, 32 brand / 0 non-brand / 23 withheld)
- Scoreboard figcaption carries the pull date + settle note
- Handoff = a doc in Internal > Reports ("Handoff — <Month>"), NO Message-board post; client delivery = email
- Step 8 closes the loop: one dated Research-log row in the context doc per cycle (delivered date + channel + pending approvals)

**Wipe incidents (3× on 8 Sep, all recovered from pre-write fetches):** `--content @file` is not supported (×2); publishing `"$(cat missing-file)"` sends empty content. Rules: always `--content "$(cat file)"`, `test -s` before publish, verify stored == canonical after. Anchors must match Basecamp's stored markup (`<li value="N">`, auto-linked URLs, `<p><br></p>` separators).

**Migration architecture (supersedes the pre-project-setup plan agreed 8 Sep):** the master client doc is now a **separate** `Project Context` built by the new `project-setup` skill (`~/Workspaces/_tools/skills/project-setup/`) — one doc per client at Internal root, 11 frozen headings (Business, Contacts, Offer, This engagement, Kit, Access, Key pages, Writing, Constraints, Reporting, Log). The old plan to "promote" `SEO — Project Context` into the master doc is dead: no title/folder move happen.

- **Split of ownership:** company facts (domain, offer, contacts, kit, Fathom, writing rules) live in master `Project Context` (owner: `project-setup`). Search facts (GSC property, Foundation/Growth, brand terms, scoreboard tokens) stay in `SEO — Project Context` (owner: reworked `seo-project-setup` — search add-on, reads Project Context first, never re-asks company facts).
- **No doc moves → no breakage:** `SEO — …` titles and the Internal → SEO path stay until a later migration, so `client-report-prep.rb` walks Internal → SEO unchanged and the Oct 3 run is safe.
- **`seo-project-setup` is already patched** (reads Project Context at Internal root first, missing → run `project-setup` and stop; default next = keyword-research).
- **Later migration (not now):** point `client-report` / `client-report-prep.rb` at `Project Context` for domain + Fathom, this SEO file only for Plan / GSC / brand terms; extend read-first to non-SEO skills (copywriting/branding/design); eventually drop duplicated Business overview.
- **Resolved (client-report step 8):** the per-cycle log row's home is the master `Project Context` → `Log` (master doc is the standing record per the process doc rule 11). Implemented in client-report with a fallback: until Matt runs `project-setup` on the client, the row still lands in `SEO — Project Context` → `Research log` (Konnected's Oct 3 run is covered either way).
- **Guru Packaging (line 5):** run `project-setup` first, then `seo-project-setup` as the search add-on — not the old single-doc interview flow.
