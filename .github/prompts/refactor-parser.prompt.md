---
name: "Refactor Parser"
description: "Refactor parser code while preserving fixture compatibility and regex extraction behavior."
argument-hint: "Target parser file and expected behavior change"
agent: "agent"
---
# Refactor Parser Prompt

Refactor parser-related code with minimal behavior risk.

Workflow:

1. Inspect the target parser module in `src/parsers/`.
2. Inspect related tests in `tests/unit/parsers/`.
3. Inspect relevant fixture exports in `tests/fixtures/inputs/`.
4. Implement the smallest possible change that preserves existing behavior unless explicitly requested.
5. Add or update parser tests first for changed behavior.
6. Run relevant tests and summarize what changed, what stayed stable, and why.

Output requirements:

- List touched files.
- State behavior changes explicitly.
- Report test command(s) run and outcome.
