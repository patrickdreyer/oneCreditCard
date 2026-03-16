---
description: "Use when creating or modifying pytest tests. Enforces AAA sections, test naming conventions, and fixture-first file I/O testing."
name: "Python Test Conventions"
applyTo: "tests/**/*.py"
---
# Python Test Conventions

- Name tests as `test_<methodInCamelCase>_<inputInCamelCase>_<resultInCamelCase>`.
- Use `ctor` for constructor-focused tests and `error` for exception-focused tests.
- Keep AAA structure with `# arrange`, `# act`, and `# assert`; omit `# arrange` only when there is no setup.
- Reuse fixtures from `tests/conftest.py` before adding new fixtures, especially `setupInputDir`, `writeConfig`, and `fixturesInputsDir`.
- Prefer real temporary directories and fixture copies over mocking file I/O.
- Keep assertions explicit and deterministic.
