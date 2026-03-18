#!/bin/bash

# Build script for cmdbsyncer-inventory PyPI package

set -e

echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

echo "📦 Building package..."
python -m build

echo "🔍 Checking distribution..."
python -m twine check dist/*

echo "✅ Build complete! Files in dist/:"
ls -la dist/

echo ""
echo "To upload to PyPI:"
echo "  TestPyPI: python -m twine upload --repository testpypi dist/*"
echo "  PyPI:     python -m twine upload dist/*"