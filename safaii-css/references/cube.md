# CUBE CSS

The methodology this skill follows, and where we depart from it. Source: [cube.fyi](https://cube.fyi/).

## What it is

CUBE stands for Composition, Utility, Block, Exception — an extension of CSS rather than a replacement for it. It leans on the cascade and inheritance instead of avoiding them, and it is tool-agnostic: as long as the output is CSS, the methodology holds.

| CUBE | Starter | Job |
|---|---|---|
| Composition | `_compositions/` | Flexible, component-agnostic layout |
| Utility | `_utilities/` | A class that does one job and does it well |
| Block | `_blocks/` | A component — a concise group of rules that apply only in that context |
| Exception | in the block's own file | A deviation from a block, driven by a `data-*` attribute |

`reset`, `tokens`, and `base` are ours, not CUBE's. CUBE has no opinion about them.

## Where we follow it exactly

- **Composition is layout only.** No colour, no font style, no shadows, no patterns. A composition rule that sets a visual property belongs in a block instead.
- **Blocks extend, they don't restate.** By the time a block rule runs, the global CSS, composition, and utility layers have already done most of the work.
- **No formal element syntax.** BEM's `.block__element` is not required — a descendant selector inside the block (`.my-block img`) or a simple scoped class is fine. What matters is consistency.
- **Utilities don't fight specificity.** No `!important` as a mechanism — that is a long-run problem, not a shortcut.
- **Hint the browser, don't micro-manage it.** Flexible rules over pixel-perfect ones.

## A block has a ceiling

A block solves **one** contextual problem and stays small. cube.fyi puts the limit at a handful of rules, around 80–100 lines. Styling a card and a button in one file is two blocks, not one. When a variant stops being recognisable as the original block, that is a new block rather than another exception.

## Composition inside blocks

A block's internals get a composition rather than per-element margins — usually `.flow`:

```html
<article class="card">
	<img src="…" alt="…" />
	<div class="flow">
		<h2>…</h2>
		<p>…</p>
	</div>
</article>
```

This is why the starter ships no global block-spacing token. `.flow` composes anywhere, including inside a component, where a page-level rhythm token cannot reach.

## Where we depart

### No utility system generated from tokens

cube.fyi recommends generating utility classes from design tokens — `.bg-primary`, `.color-primary`, one class per token per property. **We don't.** A handful of hand-written utility classes for the things that genuinely vary page to page is fine; that is what `_utilities/` is for. A generated sheet giving every token its own class is a hand-rolled Tailwind, and the folder stops reading as a list of decisions. Colour and background come from blocks and compositions, not from classes sprinkled through the HTML.

### `.wrapper` is a composition, not a utility

cube.fyi's utility page uses `.wrapper` as its example utility. Here it lives in `_compositions/`: it sets `inline-size` and `margin-inline`, which is layout, and layout is the composition layer's job. The line we hold: a utility changes one thing about an element; a composition decides how a group of elements sits together.

### Exceptions live with their block

cube.fyi puts exceptions in their own layer. Here the everyday case — `.button[data-variant="ghost"]` — sits in the block's own file, because a variant that applies to one block belongs next to it: one file to open instead of two.

The `exception` layer is for what doesn't fit that: a rule that must beat everything else, or a genuine one-off that isn't a block's business. It ships empty and should stay that way until something actually needs it.

### Browser support is not classic progressive enhancement

cube.fyi builds the minimum viable experience first, then layers modern CSS on top. We write modern CSS and add fallbacks only where a feature is both recently shipped **and** fails ungracefully — the same instinct, reached from the other end. The policy and its tiers are in `references/browser-support.md`.
