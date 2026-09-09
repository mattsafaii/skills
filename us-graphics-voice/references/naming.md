# Naming — U.S. Graphics Company

## The rule (Neil's CLAUDE.md, 2026-09-07)

Every name you choose, for files, scripts, directories, functions, variables, classes, commits, branches, anything, must use precise professional vocabulary. Choose the word a 1972 IBM engineer would write in a specification. No slang, no casual shorthand, no cute or clever names, no words borrowed from chat culture.

Illustration — `deploy_dashboards.sh`, not `push_dashboards.sh`. One illustration, not the extent of it.

## House catalog grammar

| Kind | Pattern | Examples |
|---|---|---|
| Company | Formal name + short + LLC | U.S. Graphics Company / USGC / U.S. Graphics, LLC |
| Typeface | Place + duty + ™ | Berkeley Mono™, Houston Mono™, Los Alamos Mono, Chicago Corporate |
| Type catalog | TX-nn | TX-02 Berkeley Mono |
| Bundle / stock | FX-nnn | FX-600, FX-102 |
| Document | DX-nnn | DX-102 datasheet, DX-201 doctrine poster |
| Bulletin | BT-nnn | BT-001, BT-002 |
| Release change | RC-nnn | RC-159 |
| Module | MX-nnn | MX-005 Standard Fonts |
| Collection | CL-nnn | CL-002 Standard |
| Theme | NAME + part | RETICLE 5201-010 |
| Program | spelled-out + acronym | Customers Are Really Everything (CARE) |

Place names in type (Berkeley, Houston, Los Alamos, Chicago) are geographic or civic, not vibe. Duty words (Mono, Corporate) say what the face is for.

## Slogans

Verb/noun triads, periods, lowercase after the name if they do it that way:

- AB&R® identify. track. manage.
- Anthropic, speculative — Machines. Mind. Mankind.
- House line already on the site — Engineering graphics for professionals.

Refuse mission-statement sludge.

## Apex exhibits

- Sun — Ultra 60, UltraSPARC II, A23-Deuterium. "Your product names will never be this cool."
- Cognex — Cognition Experts; DataMan, VisionPro, In-Sight, DataMatrix.
- RAMTRON + F-RAM + FM18L08-70-SG — mark, family, device.
- Western Acoustics — a shipped USGC brand name (consignments now closed).

## File and git hygiene (apply the IBM test)

| Instead of | Write |
|---|---|
| push_dashboards.sh | deploy_dashboards.sh |
| wip-stuff | incomplete-layout or the actual object |
| fix-oops | restore-metrics-alignment |
| yeet-old-api | remove-deprecated-endpoint |
| ship-it | release-v2.003 |
| nits | typographic-corrections |

Commit messages are specifications of what changed, not moods.

## When the user asks for names

Offer two or three, not twelve. Each should pass the IBM test and, if it is a product, the RAMTRON lockup test (name works next to a mark and a part number). State what was refused and why (slop, cute, chat-culture, generic "labs/ai/hub").
