# Versioning

## Overview

The tool version is derived from git tags using `hatch-vcs`. No manual version bumps are needed.

## Requirements

- **Version Source**: Git tags in `v<major>.<minor>.<patch>` format (e.g., `v0.1.0`)
- **CLI Flag**: `--version`/`-v` prints the current version and exits with code 0
- **Automated Releases**: Pushing a `v*` tag to `main` triggers a GitHub Actions workflow that validates, builds, and publishes a GitHub Release with the standalone binary

## Creating a Release

```bash
git tag v0.1.0
git push --tags
```
