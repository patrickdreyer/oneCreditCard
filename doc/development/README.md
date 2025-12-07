# Development Overview

Development guidance for the oneCreditCard project.

## Status

**Ready to implement** - Requirements and architecture complete

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

## Documents

- **[Implementation Guide](01-implementation-guide.md)** - Development phases and testing strategy  
- **[Parsing Implementation](02-parsing-implementation.md)** - Text parsing patterns and regex implementation
- **[ODS Generation](03-ods-generation.md)** - OpenOffice Calc file generation technical details
