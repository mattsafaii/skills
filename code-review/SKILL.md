---
name: code-review
description: Review the changes since a fixed point (commit, branch, tag, merge-base, or PR) along three axes — Standards (does the code follow the repo's conventions?), Spec (does it match the originating PRD?), and Interface (what did a UI change break or leave incomplete?). Standards and Spec always run; Interface runs when the diff touches user-facing code. Spawns the reviews in parallel in sibling Herdr panes and reports them side by side. Use when Matt says "review since X", wants a branch or PR or work-in-progress reviewed, or when /build or /backlog reaches its review step.
triggers:
  - review since
  - code review
  - review this branch
  - review the diff
  - review the pr
---

# Code review

Review the diff between `HEAD` and a fixed point along three axes:

- **Standards** — does the code conform to the repo's documented conventions (and, where it documents none, to a baseline of code smells)?
- **Spec** — does it faithfully implement what the originating PRD asked for?
- **Interface** — when the diff touches user-facing code: what did the change break, and what did it leave incomplete?

Each axis runs as its own reviewer in a sibling Herdr pane, so neither read pollutes the other. This skill reports them side by side, then fixes.

## 1. Pin the fixed point

Whatever Matt named is the fixed point — a commit SHA, branch, tag, `main`, `HEAD~5`, a PR. If none was given, ask. Capture the diff once:

```bash
git diff <fixed-point>...HEAD          # three-dot: diff against the merge-base
git log <fixed-point>..HEAD --oneline
```

Confirm the ref resolves (`git rev-parse <fixed-point>`) and the diff is non-empty before spawning anything. A bad ref or empty diff fails here, not inside the reviewers.

If the change touches a design token, theme value, or shared primitive, its blast radius is wider than the diff — review the consumers too (one hop of importers/callers, two for tokens and primitives), and say how many you did not expand.

For `/build` the fixed point is the scaffold commit; for `/backlog`, the last shipped commit.

## 2. Find the spec

The originating spec, in this order:

1. **The repo's PRD in Basecamp.** From the repo, `basecamp docs list --json`; match the doc titled `PRD` (or `PRD: <Cycle>` for a cycle) and pull its content. This is the usual source.
2. A path Matt passed as an argument.
3. The Lab card (pitch + PRD) — the pitch lives on the project's card.
4. Nothing found: ask. If Matt says there's no spec, the **Spec** reviewer skips and reports "no spec available".

## 3. Find the standards

Anything the repo documents about how code is written — `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`. On top of that, pull the stack skills when they apply: `safaii-css` and `safaii-html` for markup and CSS, `dhh-rails-style` for Ruby and Rails, and `~/.config/opencode/STACKS.md` for the stack's own rules.

Above whatever the repo documents, the Standards reviewer always carries the **smell baseline** below — a fixed set of Fowler code smells (*Refactoring*, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented convention always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

## 4. Read the removed lines

Regressions are invisible in the post-change state. Read the `-` side of every hunk against [removed-signals.md](removed-signals.md) — a change can quietly drop an accessible name, a focus ring, a reduced-motion guard, a text-wrapping rule, or a color token.

A removed signal is a lead, not a finding. Check for an equivalent replacement first (an `aria-label` giving way to `aria-labelledby` is not a regression). Route the unmatched removal to its owner (`safaii-html`, `safaii-css`, `page-design`) and report it as a **Regression** only once that owner confirms the interface got worse.

## 5. Spawn the reviewers in parallel

**Standards and Spec always run. Interface runs when the diff touches user-facing code** — markup, CSS, a component, a style token, or copy. Split a sibling pane per reviewer and start a read-only OpenCode (unattended) agent in each — follow the `herdr` skill. Herdr agent names are lowercase:

```bash
herdr pane split --current --direction right --no-focus      # one per reviewer
herdr agent start review-standards --kind opencode --pane <pane-id>
herdr agent start review-spec --kind opencode --pane <pane-id>
herdr agent start review-interface --kind opencode --pane <pane-id>   # only when UI
```

Then submit each brief with `--wait` (rather than polling), and read them back:

```bash
herdr agent prompt review-standards "<brief>" --wait --timeout 120000
herdr agent prompt review-spec "<brief>" --wait --timeout 120000
herdr agent prompt review-interface "<brief>" --wait --timeout 120000
herdr agent read review-standards --source recent-unwrapped --lines 120
herdr agent read review-spec --source recent-unwrapped --lines 120
herdr agent read review-interface --source recent-unwrapped --lines 120
```

**Standards reviewer brief** — include the diff command and commit list, the standards sources from step 3, and the smell baseline above **pasted in full** (the reviewer has no other access to it):

> Report, per file/hunk where relevant: (a) every place the diff violates a documented convention, citing the file + rule; and (b) any baseline smell you spot, naming it and quoting the hunk. Distinguish hard violations from judgement calls — documented breaches can be hard, but baseline smells are always judgement calls, and a documented convention overrides the baseline. Skip anything tooling enforces. Under 400 words.

**Spec reviewer brief** — include the diff command and commit list, and the spec content from step 2:

> Report: (a) requirements the PRD asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the PRD line for each finding. Under 400 words.

**Interface reviewer brief** — include the diff command and commit list:

> Report what the change broke or left incomplete in user-facing code: (a) a state applied to some cases but not all — hover, focus, active, disabled, loading, selected; (b) a new component with no empty, loading, error, disabled, or narrow-width state; (c) a control added to one surface but not its sibling surfaces; (d) a removal from the `-` side that nothing replaces (accessibility, focus, motion, text, a color token). Name the owning skill for each (`safaii-html`, `safaii-css`, `page-design`). Report only what the diff shows, not taste. Under 400 words.

All reviewers are **read-only** — report gaps, don't fix them. The calling agent applies the fixes.

## 6. Present, then fix

Present under `## Standards`, `## Spec`, and `## Interface` headings, verbatim or lightly cleaned. Do **not** merge or rerank — the axes stay separate (see below). **Status every finding:**

- **Introduced** — the change created it.
- **Regression** — the change weakened something that worked. Fix these first.
- **Pre-existing** — present in touched code but not caused by the change. Report a few at most; don't turn a change review into a full-file audit.

End with a one-line summary: findings per axis, and the worst issue within each axis. Then fix what they found and commit, so the review closes with the change clean.

## Why separate axes

A change can pass one axis and fail another:

- Follows every convention but implements the wrong thing → **Standards pass, Spec fail.**
- Does exactly what the PRD asked but breaks the repo's conventions → **Spec pass, Standards fail.**
- Implements the PRD and follows conventions but drops an accessible name, or ships a component with no error state → **Standards and Spec pass, Interface fail.**

Reporting them separately stops one axis from masking another.

## Failure modes

If something fails in a way this section doesn't cover, show Matt the raw error and stop — don't improvise.

| Symptom | Cause | Fix |
|---|---|---|
| Two `code-review` skills available | Pocock's copy still installed alongside this one | Remove the `~/.agents/skills` copy: `npx skills remove -g -y code-review`. Note the CLI deletes same-named skills from `~/Workspaces/_tools/skills` too, so recreate this file afterward if it vanished. |
| Not running inside Herdr | Skill invoked outside a managed pane | Run the reviews sequentially as sub-agents instead (Task tool, `general-purpose`), still one independent context each |
| Reviewer hangs or never goes idle | It hit a permission prompt | Check `herdr agent get` / `herdr agent read`; spawn reviewers as OpenCode (unattended) and clear the prompt rather than re-sending blind |
| Empty or bad diff | Fixed point didn't resolve | `git rev-parse <fixed-point>`; fix the ref before spawning anything |
| Standards reviewer invents conventions | Repo documents none and the smell baseline wasn't pasted in | Paste the baseline into the brief in full — the reviewer can't see this file |
| Interface axis run when nothing user-facing changed | The trigger didn't check for markup/CSS/component/copy | Skip it; Standards and Spec suffice |
| A removal reported as a new mistake | No status on the finding | Mark it `Regression`, so the author knows it used to work |
