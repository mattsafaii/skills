# Video-scrub ledger — the tier above CSS (reference only)

Everything worth knowing about **scroll-scrubbed video** (the Apple/Emons technique: pre-rendered camera footage, scroll drives `video.currentTime`), extracted from the scroll-world skill teardown (July 2026). This is the **last-resort tier** — reach for it only when a page genuinely needs cinematic camera motion that CSS can't express, and only as its own explicit, costed ask. This file exists so the cost is known *before* choosing it. It is documentation, not an implementation to copy blindly; snippets are illustrative.

**Sources:** [oso95/scroll-world](https://github.com/oso95/scroll-world) and the hardened fork [cth9191/scroll-world](https://github.com/cth9191/scroll-world) (both MIT). Their production knowledge, verified in their engine code; our conventions disagree with their architecture (client-rendered copy, injected CSS, AI assets) but the video mechanics are sound.

## When it's warranted at all

- The moment needs a *camera* — travel through space, a product orbit, a reveal that is genuinely filmic. If the meaning is "a figure assembles" or "a thing arrives", the CSS patterns already do it for free.
- Budget exists for real asset production (footage, 3D render, or paid AI generation) — the technique is only as good as the footage.
- One hero moment, not a page of them. The page must remain a complete document without the video (poster + copy), per house invariants.

## The physics (why naive implementations fail)

1. **Seekability, not keyframe density, makes scrubbing work.** Many static hosts don't serve HTTP byte-range requests → `video.seekable` stays `[0,0]` → every seek clamps to frame 0 and the video looks frozen. Fix: fetch the clip as a **Blob** and play the object URL (blobs are always fully seekable). Corollary: you do not need all-intra encodes.
2. **Seek cost scales with frames-since-last-keyframe.** Encoding recipe that scrubs smoothly without bloat: native resolution, `crf ~20`, **GOP 8** (`-g 8 -keyint_min 8 -sc_threshold 0`), `-an`, `+faststart`, light `unsharp` (video reads softer than stills). All-intra is ~3× the bytes for no visible gain once blob-loading removes the range-request problem.
3. **Never queue seeks.** Setting `currentTime` every frame while the decoder is still seeking piles up and freezes the clip on fast flicks (worst on phones). Coalesce: skip while `video.seeking`, lerp toward the latest target when free.
4. **Multi-clip chains must be frame-identical at seams.** Every generated/rendered clip renders slightly differently, so a chain only reads as continuous if each clip's first frame is *the previous clip's actual extracted last frame* (ffmpeg out, feed in as the next render's start frame) — never a shared source still. Verify mechanically: SSIM across each boundary from the encoded files (≥0.90 pass, <0.75 means an endpoint wasn't a real frame). And camera *velocity* must not reverse across a seam — a frame-matched seam still reads as a rewind stutter if the motion direction flips.
5. **Posters must be extracted first frames of the encoded clip**, not the source still — a still is a different render/crop and pops on the first paint.

## The device traps (each cost someone a debugging day)

- **iOS: a muted video that has never played won't paint a seeked frame.** Keep the poster up until the clip actually paints (`seeked` event), and prime each video (muted `play()`→`pause()`) on first touch. Don't strip `playsinline`/`muted` attributes.
- **iOS Low Power Mode rejects even muted `play()` — and `currentTime` scrubbing doesn't work either.** No video technique survives it. Detect the rejected prime promise on first touch and fall back to stills. (Our CSS patterns are immune — another reason they're the default tier.)
- **Phones need lighter encodes** — 720p, `-g 4` — but tier by **screen short side (≤600 CSS px)**, not pointer type: an iPad Pro has a coarse pointer and a desktop-class decoder; serving it the phone encode makes it blurry for nothing.
- **Data-saver / slow network:** Chromium exposes `saveData`/`effectiveType`; iOS exposes nothing. So the *default* must be conservative (posters first, lazy fetch near viewport) and network signals used only to downgrade further — never a heavy default with downgrade-on-signal, because the devices most on cellular can't signal.
- **Mobile URL bar `resize` events:** re-running layout on height-only resizes yanks the scroll position. Gate layout re-runs on width change.
- **Memory:** blob-loading a whole chain holds every clip in memory (~8 MB × N at GOP 8/1080p) with no release. Budget it; release object URLs when leaving video mode.

## Costs, honestly

- **Assets:** footage or renders per moment; AI generation (if used at all — against house defaults for client-facing craft) runs real money per attempt with re-roll rates that spike on interiors (content-filter false positives).
- **Weight:** ~8 MB per 8s 1080p clip; a multi-scene chain is 50–90 MB fetched into memory. This alone disqualifies it for most document sites.
- **QA surface:** desktop + phone + iPad + Low Power Mode + data-saver + reduced-motion, portrait crops of 16:9 framing, seam checks after every asset change.
- **The upgrade path when even this isn't smooth:** a pre-extracted **image sequence drawn to `<canvas>`** (what Apple actually ships) — deterministic paint, no decoder seeks, progressive loading; more build tooling. Same scrub math carries over.

## House adaptation requirements (if ever built)

Non-negotiables that differ from scroll-world's engine: copy server-rendered in the document (never a hidden SEO mirror — the document IS the page); CSS in the project stylesheet, not injected; stills mode (reduced-motion, data-saver, LPM) is the same complete document, not a degraded mirror; one moment, not a full-page film. Approval flows through the document-alive proposal step like any other motion — with this file attached as the cost sheet.
