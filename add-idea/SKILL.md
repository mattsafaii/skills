---
name: add-idea
description: Add a new idea card to the 💡 Ideas triage column of the Ideas card table in Matt's Safaii Studio Lab project on Basecamp. Use this skill whenever Matt wants to capture, save, or file an idea — triggers on phrases like "new idea", "add idea", "capture this idea", "save this as an idea", "put this in the ideas board", or the explicit slash-style "/add-idea". The skill drafts an HTML-formatted card body (inspiration/source, concept, open questions), shows it to Matt for confirmation, then posts via the basecamp CLI and returns the card URL.
---

# Add Idea Skill

Capture a new idea as a card in the 💡 Ideas triage column of the Lab project's Ideas card table. Matt reviews the draft before it's posted.

## Fixed IDs

Do not ask Matt for these — they are fixed for this skill:

- Account: `6191443` (Safaii Studio)
- Project: `46824335` (Lab)
- Card table: `9768185094` (Ideas)
- Column: `9768185095` (💡 Ideas — triage)

## Workflow

### 1. Collect the idea

Gather these fields from the conversation. Ask only for what's missing — don't re-prompt for anything Matt has already said.

- **Title** (required) — short, specific. Lead with the concrete thing, not a vague category. "Web app: generate a 'decayed' version of any website" beats "Decay tool idea".
- **Inspiration / source** (optional) — the article, tweet, conversation, or observation that sparked the idea. Include a URL if there is one.
- **Concept** (required) — 1–3 sentences describing what the idea actually is.
- **Details** (optional) — features, effects, dimensions, examples to explore. Bullet list.
- **Open questions** (optional) — things to figure out. Bullet list.

If Matt gave you a URL as inspiration, fetch it first (WebFetch) so the card body can summarize *why* that source was relevant — not just link to it.

### 2. Draft the card body as HTML

Basecamp card bodies accept HTML. Use this structure, omitting any section Matt didn't supply:

```html
<div>
<p>Inspired by <a href="URL">source name</a> — one-line summary of the relevant idea from the source.</p>

<p><strong>Concept:</strong> the concept in 1–3 sentences.</p>

<p><strong>Details to explore:</strong></p>
<ul>
<li>Detail one</li>
<li>Detail two</li>
</ul>

<p><strong>Questions to figure out:</strong></p>
<ul>
<li>Question one</li>
<li>Question two</li>
</ul>
</div>
```

Keep it tight. This is a capture, not a PRD — shaping happens in the next column.

### 3. Show the draft and wait

Before posting, show Matt the proposed **title** and **body** (rendered as readable text, not raw HTML — he can infer the markup). Ask: "Post this?"

Wait for explicit approval. Do not post on ambiguous responses.

### 4. Post the card

Run:

```bash
basecamp -a 6191443 cards create "<TITLE>" "<HTML_BODY>" \
  -p 46824335 \
  --card-table 9768185094 \
  --column 9768185095
```

Quote the title and body safely — prefer a heredoc for the body to avoid shell-escaping issues with HTML.

### 5. Return the URL

Pipe the JSON output through `python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('app_url'))"` and show Matt the card URL. Short confirmation, nothing more.

## Failure modes

If a command fails in a way this table does not cover, show Matt the raw error and stop — don't improvise a workaround or retry variations.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Card posts to wrong column | Omitted `--column` flag | Always pass `--column 9768185095` |
| Shell escaping breaks HTML body | Quoting the body as a single-line string | Use a heredoc: `"$(cat <<'EOF' ... EOF)"` |
| Wrong account / 404 | Missing `-a 6191443` — CLI falls back to global default | Always pass `-a 6191443` explicitly |
| Card body shows raw `<div>` tags | Basecamp decoded content vs. source HTML confusion | HTML is correct; Basecamp renders it. Don't switch to Markdown. |
| Idea is actually code work | Ideas card table is for concepts, not tickets | Redirect Matt to To-dos on the relevant project per his Basecamp workflow |
