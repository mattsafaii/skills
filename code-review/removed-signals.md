# Removed signals

What to look for on the `-` side of a hunk, and which skill owns the judgement. A row here is a lead, never a finding. Route the removal to its owner and report it as a `Regression` only once that owner confirms the interface got worse.

| Removed from the `-` side | Owner | What to check |
| --- | --- | --- |
| `aria-label`, `aria-labelledby`, `aria-describedby`, `aria-live`, `role=` | `safaii-html` | The control or region lost its accessible name, description, or announcement |
| `alt=`, `<label`, `for=`, `scope=` | `safaii-html` | An image, field, or table cell lost its programmatic association |
| `<button>`, `<a>`, `<nav>`, `<main>`, `<ul>` replaced by `div` or `span` | `safaii-html` | Keyboard and assistive-technology behavior traded for styling |
| `:focus-visible`, `:focus`, `outline`, `tabindex` | `safaii-html` | Keyboard users lost the focus indicator, or the element left the tab order |
| `prefers-reduced-motion`, `prefers-contrast` | `safaii-html` | Motion or contrast now ignores the user's system preference |
| `lang=`, `dir=` | `safaii-html` | Language metadata or text direction was dropped |
| Logical properties swapped for `left` / `right` | `safaii-css` | Direction-aware layout was dropped |
| `text-wrap`, `line-clamp`, `overflow-wrap`, `tabular-nums`, `font-feature-settings` | `safaii-css` | Text rendering, wrapping, or numeral alignment silently changed |
| A color token swapped for a literal, or a token swapped for a lighter one | `safaii-css` | The rendered contrast pair may now fail; measure it |
| A user-facing string deleted or shortened | `page-design` | A label, error, or empty state lost the information it carried |

## Equivalent replacements

These clear the signal. Check for them before routing anything, or the report fills with refactors reported as regressions:

- `aria-label` giving way to `aria-labelledby` pointing at visible text.
- An explicit `role` dropped because the element became the native equivalent — `role="button"` going as a `div` becomes a `<button>`.
- `outline` replaced by a `box-shadow` focus ring that still meets the focus-indicator rule.
- `tabindex="0"` dropped from an element that is now natively focusable.
- A color literal replaced by a token that measures the same rendered pair.
- A physical property replaced by its logical counterpart — the fix, not the regression.
- A string moved into the translation catalogue rather than deleted.

## Searching the removed side

Restrict the search to deleted lines so additions do not mask a removal:

```bash
git diff -U0 "$BASE"...HEAD -- '*.tsx' '*.css' | grep -E '^-[^-]' | grep -E 'aria-|role=|alt=|focus|tabindex|prefers-'
```

Read the surrounding hunk before deciding. A removed attribute is meaningless without the element it came from, and `-U0` deliberately hides that context.
