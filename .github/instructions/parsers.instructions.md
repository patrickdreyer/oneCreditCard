---
description: "Use when changing parser logic in src/parsers. Preserves regex-first extraction style, iterator-based outputs, and fixture-driven parser tests."
name: "Parser Area Conventions"
applyTo: "src/parsers/**/*.py"
---
# Parser Area Conventions

- Preserve regex-first extraction patterns and keep parsing behavior explicit.
- Prefer compiled regular expressions and stable matching order when parsing transaction blocks.
- Return iterator-based outputs (`Iterator[Transaction]`) instead of materializing full lists unless strictly required.
- Keep text handling UTF-8 safe and avoid hidden normalization changes.
- When parser behavior changes, update parser unit tests in `tests/unit/parsers/` and relevant fixture inputs in `tests/fixtures/inputs/`.
- Keep parsing changes minimal and avoid unrelated refactors.
