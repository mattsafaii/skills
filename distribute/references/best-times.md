# @mattsafaii — best posting times (to be measured, not guessed)

**Current status (2026-08):** no real time signal exists yet. The 100-post sample pulled 2026-08-20 was off-theme engagement-bait, all from a ~40-min window — unusable for time-of-day or day-of-week analysis, and irrelevant to the craft feed anyway.

## Recommended default until data exists
Post during **US business hours, 7–11am PT**. Reasoning: the indie/dev/webcraft audience (the shortlist + niche) is most active then; it pairs with the morning reply habit; a small account needs its followers actually online when the post drops (win-your-network-first model). **One post/day at ~9–10am PT** matches the calendar.

## How to measure the real answer (after Phase 1 ships)
1. ~2+ weeks of ~1/day on-theme craft posts gives a signal.
2. Pull `users_timeline` (id 1841047934588104706) for on-theme posts (exclude RTs, exclude bait topics) with `public_metrics.impression_count` + `created_at`.
3. Bucket impressions + replies by hour (convert UTC→America/Los_Angeles) and by weekday.
4. Pick the hour/day block with best median impression + reply (reply is the stronger signal — printx check/dwell).
5. Update this file with the finding.

## What counts
Only **on-theme** posts (craft, build-in-public, client-work, business). The off-theme bait impressions are noise and were the old (broken) strategy.

## Caveats
- For a small account, content consistency + reply quality outweigh timing by a large margin. Timing is an edge, not the engine.
- Don't over-rotate on one mega-hit post's hour — use *median* per bucket, not the max.
