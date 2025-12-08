# Executable Build Implementation

## Overview

PyInstaller creates standalone executable bundling Python runtime and dependencies.

## Build Tool

**PyInstaller 6.0+**: Packages Python application into single executable

**Configuration**: `--onefile --name onecreditcard --clean --noconfirm`

## Build Process

Script `build.sh` in project root:

```bash
#!/bin/bash
rm -rf build dist
pyinstaller \
    --name onecreditcard \
    --onefile \
    --clean \
    --noconfirm \
    src/main.py
```

**Output**:
- `dist/onecreditcard` - Standalone executable
- `build/` - Temporary artifacts (auto-cleaned before build)
