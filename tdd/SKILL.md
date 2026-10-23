---
name: tdd
description: Test-driven development — the red → green loop. Use when writing tests, building a feature test-first, fixing a bug test-first, or when /build asks for a slice's `Test:` line. Covers what makes a test worth keeping, where tests attach (seams), and the anti-patterns. Also "tdd this", "test-first", or "red-green-refactor".
---

# Test-driven development

TDD is the red → green loop. This skill keeps the loop honest: what a good test is, where it attaches, and the rules of the loop. Consult it before and during the work, not after.

Read `CONTEXT.md` if the repo has one, so test names and vocabulary match the project's domain language, and respect any ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. The code can change entirely; the test shouldn't. A good test reads like a specification — "user can check out with a valid cart" — and survives refactors because it doesn't care about internal structure.

Good: drives the real interface, asserts on observable behavior, one logical assertion.
Bad: mocks internal collaborators, tests private methods, asserts on call counts or order, breaks when you refactor without a behavior change.

See [tests.md](tests.md) for worked examples and [mocking.md](mocking.md) for where mocking is fair.

## Seams — where tests attach

A **seam** is the public boundary you test at — the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** On a cycle build the PRD names the seam (its *Test seam* line) — use it. Otherwise agree the seam before writing: what's the public interface, and which seams are we testing? No test at an unconfirmed seam. You can't test everything, and agreeing seams up front is how the effort lands on the critical paths and the complex logic instead of every edge case.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`), so it passes by construction and can never disagree with the code. Expected values must come from an independent source — a known literal, a worked example, the spec.
- **Horizontal slicing** — writing all the tests first, then all the implementation. Bulk tests verify *imagined* behavior and go insensitive to real changes. Work in vertical slices instead: one test → one implementation → repeat, each a tracer bullet that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactor at the review, not in the loop.** Cleanup belongs to the review stage (the `code-review` skill), not the red → green cycle.

## By stack

- **Rails:** `bin/rails test` (Minitest); tests in `test/`, mirroring `app/`. Request tests hit the endpoint — the highest seam. Model tests only for real model behavior.
- **Go:** `go test ./...`. Table tests for pure logic; `httptest` for handlers.
- **JS / TS:** the project's runner (`node:test`, vitest, jest). Test the rendered output, not component internals.
- **A CLI:** run it with a fixture input and assert on stdout — that's the seam.

Run typecheck and the suite before committing each slice.
