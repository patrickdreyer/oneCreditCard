# Standalone Executable Build

## Overview

This document describes how to build a standalone executable of oneCreditCard that can run on the host system without requiring Python or dependencies to be installed.

## Requirements

**Development Environment**: DevContainer with Python 3.13+ and all dependencies installed

**Build Tool**: PyInstaller 6.0+

**Target Platform**: Linux x86_64 (executable must be built on same platform as target)

## Why Standalone Executable?

- **Clean Host System**: No need to install Python and dependencies on host
- **Easy Distribution**: Single file that can be copied anywhere
- **Isolated Environment**: Development stays in container, execution on host
- **Version Management**: Each build is self-contained with specific dependency versions
