# AI Context

## Project

- **Purpose**: Convert Viseca credit card text exports to accounting ODS files
- **Status**: Phase 1.2 in progress - Account mapping implementation started

## Build and Test

1. **Standard Validation Flow**: Run `python -m compileall src/ && pylint src/ tests/ && pytest && ./build.sh`
1. **Python Version**: Use Python `3.13` exactly as defined in `pyproject.toml`
1. **Pytest Import Mode**: Tests rely on `src` on the Python path and `--import-mode=importlib`

## Architecture

1. **Pipeline**: `DirectoryParser` -> `TextParser` -> `TransactionGrouper` -> `AccountMapper` -> `OdsGenerator`
1. **CLI Entry Point**: `src/main.py` orchestrates argument parsing and the full processing flow
1. **Configuration**: `src/configuration.py` loads `onecreditcard.json` and validates mapping, ignore rules, and output columns
1. **Parsing**: `src/parsers/` contains the input parsing logic and the `Transaction` dataclass
1. **Grouping and Mapping**: `src/transactionGrouper.py` groups mappable transactions before `src/accountMapper.py` creates booking entries
1. **Logging**: Use `src/logging_config.py` helpers instead of ad-hoc logger setup

## Code Style Rules

1. **Naming**: Follow pylint configuration in pyproject.toml
1. **No Docstrings**: Use single-line comments only, avoid triple-quoted strings
1. **Minimal Comments**: Only comment complex logic, avoid obvious comments
1. **Iterator Pattern**: Return Iterator[T] instead of List[T] for memory efficiency

## Scoped Instructions and Prompts

1. **Tests Rules**: [python-tests.instructions.md](.github/instructions/python-tests.instructions.md)
1. **Parser Rules**: [parsers.instructions.md](.github/instructions/parsers.instructions.md)
1. **Mapping Flow Rules**: [mapping-flow.instructions.md](.github/instructions/mapping-flow.instructions.md)
1. **Parser Refactor Prompt**: [refactor-parser.prompt.md](.github/prompts/refactor-parser.prompt.md)
1. **Validation Prompt**: [validate-workspace.prompt.md](.github/prompts/validate-workspace.prompt.md)
1. **PR Creation Prompt**: [create-pr.prompt.md](.github/prompts/create-pr.prompt.md)

## GitHub Workflow

1. **Authentication**: Use `gh auth login` once per environment and verify with `gh auth status`
1. **PR Creation**: Prefer `gh pr create` over browser-only flows when GitHub CLI is available
1. **PR Quality**: Create PRs with a concise, appropriate title and a structured description that explains summary and key changes
1. **Assignee**: After creating a PR, add the current user as assignee with `gh pr edit <pr> --add-assignee "@me"`
1. **Manual Metadata**: Leave room for follow-up manual updates to labels, projects, and milestone after PR creation
1. **Projects Scope**: If project updates are needed through `gh`, refresh auth with `gh auth refresh -s project`
1. **Merge Flow**: Do not enable auto-merge by default. Prefer manual merge after review, then delete the remote branch when appropriate

## Runtime Constraints

1. **Encoding**: Read and write project files as UTF-8 unless a file already requires something else
1. **Config Validation**: Keep configuration validation strict; invalid or missing config fields should fail fast
1. **Regex Handling**: Validate configurable regex patterns before use and preserve the current fallback behavior only where already implemented

## AI Rules

1. **Context Loading**: When user writes "load AGENTS.md", read this file, [README.md](README.md), then [doc/technical/README.md](doc/technical/README.md), [doc/requirements/README.md](doc/requirements/README.md), and [doc/development/README.md](doc/development/README.md) first. Only read deeper docs when needed.
1. **Development Context**: Reference complete documentation structure for project details
1. **Collaboration Support**: Provide hands-on technical assistance for DevContainer setup to Alexandra
   - **Cross-Platform Awareness**: Consider Ubuntu + Mac + Windows compatibility in all recommendations
1. **Container-First Approach**: Assume Podman + Dev Containers as primary development environment
1. **Context Updates**: Proactively propose updates to AGENTS.md when new information or changes are relevant
1. **AGENTS Change Flow**: Ask for approval before modifying AGENTS.md. After approval, update AGENTS.md directly without a separate proposal document.
1. **Code Proposals**: Show diffs/descriptions only, not full code blocks unless explicitly requested
1. **Short & Concise**: Keep responses brief and to the point. No unnecessary explanations or summaries.
1. **Language Policy**: Communicate with the user in the user's preferred language. Keep project artifacts (code, config, docs, commits, prompts, instructions) in English.
1. **No Repetition**: Don't repeat user instructions or acknowledge with "understood", "you're right", etc.
