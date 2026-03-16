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
1. **Test Naming**: test_\<methodInCamelCase\>_\<inputInCamelCase\>_\<resultInCamelCase\> (use "ctor" for constructor, "error" for exceptions)
1. **Test Structure**: Use AAA pattern (# arrange, # act, # assert) in all test methods - omit "arrange" when nothing needs setup

## Test Conventions

1. **Test Layout**: Use `tests/unit/`, `tests/int/`, and `tests/e2e/`
1. **Fixtures**: Reuse fixtures from `tests/conftest.py`, especially `setupInputDir` and `writeConfig`, for file-based tests
1. **File I/O Tests**: Prefer real temporary directories and fixture copies over mocking file access

## Runtime Constraints

1. **Encoding**: Read and write project files as UTF-8 unless a file already requires something else
1. **Config Validation**: Keep configuration validation strict; invalid or missing config fields should fail fast
1. **Regex Handling**: Validate configurable regex patterns before use and preserve the current fallback behavior only where already implemented

## AI Rules

1. **Context Loading**: When user writes "load AGENTS.md", read this file AND README.md AND all documentation in doc/ directory
1. **Development Context**: Reference complete documentation structure for project details
1. **Collaboration Support**: Provide hands-on technical assistance for DevContainer setup to Alexandra
   - **Cross-Platform Awareness**: Consider Ubuntu + Mac + Windows compatibility in all recommendations
1. **Container-First Approach**: Assume Podman + Dev Containers as primary development environment
1. **Context Updates**: Proactively propose updates to AGENTS.md when new information or changes are relevant
1. **No Context Proposals**: Never provide proposed changes for AGENTS.md context itself - update directly
1. **Code Proposals**: Show diffs/descriptions only, not full code blocks unless explicitly requested
1. **Confirmation Required**: Any changes within the project must be confirmed by the user before execution
1. **Short & Concise**: Keep responses brief and to the point. No unnecessary explanations or summaries.
1. **English Only**: All responses and artifacts must be in English, regardless of chat language used
1. **No Repetition**: Don't repeat user instructions or acknowledge with "understood", "you're right", etc.
1. **No Assumptions**: Always ask for approval before:
   - Creating new files or directories
   - Modifying existing code
   - Installing dependencies
   - Running commands that could affect the project
   - Any other modifications to the workspace
