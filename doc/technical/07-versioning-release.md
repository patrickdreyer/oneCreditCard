# Versioning and Release

## Overview

Version is derived from git tags via `hatch-vcs`. The file `src/_version.py` is generated at install/build time and must not be committed.

## hatch-vcs Setup

`pyproject.toml` configures `hatch-vcs` as the version source:

```toml
[tool.hatch.version]
source = "vcs"

[tool.hatch.build.hooks.vcs]
version-file = "src/_version.py"
```

Running `pip install -e .` generates `src/_version.py` from the current git tag.

## GitHub Actions Release Workflow

`.github/workflows/release.yml` triggers on `v*` tag pushes:

1. Checks out with full git history (`fetch-depth: 0`) so hatch-vcs can derive the version
2. Installs dependencies and runs `pip install -e .` to generate `src/_version.py`
3. Validates with `python -m compileall src/ && pylint src/ tests/ && pytest`
4. Builds the standalone executable with `./build.sh`
5. Verifies the binary with `./dist/onecreditcard --version`
6. Publishes a GitHub Release with the binary attached and auto-generated release notes

## Creating a Release

```bash
git tag v0.1.0
git push --tags
```
