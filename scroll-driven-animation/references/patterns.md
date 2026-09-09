# Scroll-life patterns

Four recipes, all pure CSS scroll-driven animations. Every recipe ships inside the double gate (`@supports` + `prefers-reduced-motion`) and follows safaii-css: `@layer components` (or `elements` where it styles a bare element), tokens not magic numbers, `@scope` for anything with descendant rules, keyframes at the top of the file.

Two timeline kinds, one mental model:

- **`scroll()`** — progress = how far a *scroller* has scrolled. Use for whole-page position feedback (reading progress).
- **`view()`** — progress = an *element's journey across the viewport*. Use for anything tied to where a thing is while the reader reads. `animation-range` picks the slice of that journey: `entry` (entering), `cover` (crossing), `exit` (leaving).

Scroll-driven animations are **scrubbed, not triggered**: scrolling up plays them backward. That's correct and free — don't fight it.

---

## 1. Reading progress

*When:* long-form pieces (~1,500+ words) where position feedback genuinely helps. Not for short pages — a progress bar on a two-screen page is decoration.

The element exists only for the enhancement, so it's hidden in base CSS and shown inside the gates (Invariant: unsupported browsers must not render a dead bar).

```html
<div class="reading-progress" aria-hidden="true"></div>
```

```css
/* top of file, with the other keyframes */
@keyframes reading-progress-grow {
	to { scale: 1 1; }
}

@layer components {
	.reading-progress {
		display: none; /* enhancement-only element: hidden unless the enhancement runs */
	}

	@supports (animation-timeline: scroll()) {
		@media (prefers-reduced-motion: no-preference) {
			.reading-progress {
				display: block;
				position: fixed;
				inset-block-start: 0;
				inset-inline: 0;
				block-size: 3px;
				background: var(--color-accent);
				transform-origin: 0 50%;
				scale: 0 1;
				animation: reading-progress-grow linear both;
				animation-timeline: scroll(root block);
			}
		}
	}
}
```

Variant: to track one article rather than the whole page, give the article `view-timeline-name: --article` and use `animation-timeline: --article` with `timeline-scope: --article` on a common ancestor (the bar isn't a descendant of the article). Reach for this only when the page has real chrome above/below the article; `scroll(root)` covers the plain document case.

## 2. Reveal on view

*When:* an arrival that deserves a beat — a pull-quote carrying the thesis, a section-opening figure. One or two per page, not every element (a page where everything fades in is a slideshow, not a document).

```html
<blockquote class="reveal">…</blockquote>
```

```css
@keyframes reveal-rise {
	from {
		opacity: 0;
		translate: 0 1.5rem;
	}
}

@layer components {
	@supports (animation-timeline: view()) {
		@media (prefers-reduced-motion: no-preference) {
			.reveal {
				animation: reveal-rise linear both;
				animation-timeline: view();
				animation-range: entry 10% entry 90%;
			}
		}
	}
}
```

The hidden start state (`opacity: 0`) exists **only inside the gates** — in base CSS the element is simply visible. This is the invariant that keeps content readable everywhere; never set the hidden state as a base style.

`animation-range` tuning: `entry 10% entry 90%` completes the reveal by the time the element has fully entered — the reader never waits on it. For a slower arrival that keeps settling as it crosses, `entry 20% cover 35%`.

## 3. Sticky-figure steps (scrollytelling)

*When:* prose that references a figure the reader would otherwise scroll away from — a diagram explained over several paragraphs, a map with narrated stops. The layout (sticky figure) is plain, universally-supported CSS; only the per-step emphasis is the gated enhancement.

```html
<section class="scrolly">
	<figure>…the diagram…</figure>
	<div class="steps">
		<p class="step">First point about the figure…</p>
		<p class="step">Second point…</p>
		<p class="step">Third point…</p>
	</div>
</section>
```

```css
@keyframes step-focus {
	0%, 100% { opacity: 0.45; }
	50% { opacity: 1; }
}

@layer components {
	@scope (.scrolly) {
		:scope {
			display: grid;
			grid-template-columns: minmax(24ch, 40ch) 1fr;
			gap: var(--gutter);
		}

		figure {
			position: sticky;
			inset-block-start: var(--space-4);
			align-self: start; /* without this, the grid stretches the figure and sticky never engages */
			grid-column: 2;
			grid-row: 1;
		}

		.steps {
			grid-column: 1;
			grid-row: 1;
		}

		.step {
			min-block-size: 60vb; /* each step owns enough scroll to read against the figure */
		}
	}

	@supports (animation-timeline: view()) {
		@media (prefers-reduced-motion: no-preference) {
			.scrolly .step {
				animation: step-focus linear both;
				animation-timeline: view();
				animation-range: cover 20% cover 80%;
			}
		}
	}
}
```

Unsupported/reduced-motion: all steps at full opacity beside a sticky figure — still a perfectly good layout, nothing missing. The muted state (0.45) exists only inside the gates, same rule as the reveal's hidden state.

Highlighting *parts of the figure* per step is a named-timeline job (`view-timeline-name` per step + `timeline-scope` on `.scrolly` + one animation per figure part) — real but fiddly; propose it only when the figure genuinely has addressable parts, and budget iteration.

## 4. Scrubbed illustration

*When:* a figure whose meaning unfolds in sequence — a route being traced, a construction line by line, a process diagram that assembles. The reader's scroll draws it; scrolling back undraws it. This is the document-web answer to scroll-cinema's video scrubbing: same reversible time-under-the-reader's-thumb feel, zero video, zero JS.

Works on any inline SVG with stroked paths. `pathLength="1"` normalizes every path so the CSS needs no per-path measurements:

```html
<figure class="figure-scrub">
	<svg viewBox="…" role="img" aria-label="…">
		<path class="draw" pathLength="1" d="…" />
	</svg>
	<figcaption>…</figcaption>
</figure>
```

```css
@keyframes draw-in {
	from { stroke-dashoffset: 1; }
	to { stroke-dashoffset: 0; }
}

@layer components {
	@supports (animation-timeline: view()) {
		@media (prefers-reduced-motion: no-preference) {
			.figure-scrub .draw {
				stroke-dasharray: 1;
				stroke-dashoffset: 0; /* base state stays DRAWN; the keyframes' from-state hides it only while the animation owns it */
				animation: draw-in linear both;
				animation-timeline: view();
				animation-range: entry 25% cover 75%;
			}
		}
	}
}
```

Note the base-state discipline, third time now because it's the pattern people get wrong: `stroke-dashoffset: 0` (fully drawn) is the resting state; the undrawn state lives in the keyframes, inside the gates. Unsupported browsers see the complete illustration.

Multi-stage assembly: stagger parts with `animation-range` offsets per part (`entry 25% cover 50%`, `cover 40% cover 75%`, …) rather than `animation-delay` — ranges stay honest under scrubbing, delays don't.

---

## Proposing well (the judgment layer)

- The reader test, always: **does removing it lose something the reader needed?** "Position feedback on a long read" passes. "The pull-quote lands with weight" passes (barely — one per page). "Sections feel more dynamic" fails.
- **The four named purposes** — every proposal names exactly one; a candidate that fits none is rejected, no matter how good it would look:
  - *position feedback* → reading progress (long content)
  - *referenced figure* → sticky-figure steps (prose pointing at a figure)
  - *sequential meaning* → scrubbed illustration (a figure that unfolds in order)
  - *arrival beat* → reveal on view (a thesis moment)
- **Weigh exposure** (SKILL.md gate): persistent elements get the strictest test; recurring motion (per-paragraph reveals, per-item entrances) is reject-by-default; the once-per-read beat is where the budget lives.
- **Report the rejections** — 2–5 candidates considered and killed, each with the test that killed it. A proposal without rejections is a wishlist.
- Two moments is the usual right answer. Four is the ceiling, and rare.
- Cost stated per proposal: which elements get touched, roughly how much CSS. Honesty here is what makes the approval meaningful.
