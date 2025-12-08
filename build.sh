#!/bin/bash
# Build standalone executable with PyInstaller

set -e

echo "Building onecreditcard executable..."

# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller \
    --name onecreditcard \
    --onefile \
    --clean \
    --noconfirm \
    --specpath build \
    src/main.py

echo "Build complete! Executable available at: dist/onecreditcard"
echo ""
echo "To install on host system:"
echo "  sudo cp dist/onecreditcard /usr/local/bin/"
echo ""
echo "To test:"
echo "  ./dist/onecreditcard --help"
