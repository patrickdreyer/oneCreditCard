---
name: "Validate Workspace"
description: "Run the repository validation flow and report concise, actionable results."
argument-hint: "Optional scope hint, e.g. parser, mapping, full"
agent: "agent"
---
# Validate Workspace Prompt

Run the standard repository validation flow and provide an actionable summary.

Validation order:

1. `python -m compileall src/`
2. `pylint src/ tests/`
3. `pytest`
4. `./build.sh`

Guidance:

- Use Python 3.13 environment expectations from project configuration.
- Stop only when blocked by a failing step that prevents later steps.
- Summarize errors with file locations and likely root cause.
- If all steps pass, provide a short pass summary.
