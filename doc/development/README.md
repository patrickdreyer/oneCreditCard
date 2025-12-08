# Development Guide

## Branch Naming Convention

Use the following prefixes for branch names:

- **`feature/`** - New features or enhancements
  - Example: `feature/multi-file-support`, `feature/cli-interface`
- **`bugfix/`** - Bug fixes
  - Example: `bugfix/parser-date-format`, `bugfix/currency-conversion`
- **`hotfix/`** - Critical fixes for production
  - Example: `hotfix/security-update`, `hotfix/data-corruption`
- **`test/`** - Test improvements or new test suites
  - Example: `test/integration-tests`, `test/e2e-workflows`
- **`refactor/`** - Code refactoring without changing functionality
  - Example: `refactor/parser-simplification`, `refactor/extract-mapper`
- **`docs/`** - Documentation updates
  - Example: `docs/api-reference`, `docs/user-guide`
- **`chore/`** - Maintenance tasks, dependencies, build configuration
  - Example: `chore/update-dependencies`, `chore/ci-pipeline`

## Commit Message Prefixes

**Format**: `<prefix>: <short description in imperative mood>`

Use the following prefixes for commit messages to provide instant clarity:

- **`feat:`** - Adding a new feature
  - Example: `feat: add multi-file batch processing`
- **`fix:`** - Fixing a bug
  - Example: `fix: correct date parsing for foreign transactions`
- **`chore:`** - Routine tasks (build, config, dependencies)
  - Example: `chore: update odfpy to version 1.4.1`
- **`refac:`** - Code restructuring without changing behavior
  - Example: `refac: simplify transaction grouping logic`
- **`docs:`** - Documentation updates
  - Example: `docs: add configuration examples to README`
- **`test:`** - Adding or updating tests
  - Example: `test: add integration tests for account mapper`
- **`style:`** - Code style changes (formatting, indentation)
  - Example: `style: fix pylint warnings in parser module`

Examples:

- `feat: implement CLI interface with argparse`
- `fix: handle empty directory gracefully`
- `test: add E2E tests for complete pipeline`
- `docs: update branch naming conventions`
