#!/usr/bin/env bash
set -e

echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
python -m build

if ! compgen -G "dist/*" > /dev/null; then
  echo "Build failed — no artifacts found"
  exit 1
fi

read -p "Upload to PyPI? (y/N): " confirm
if [ "$confirm" != "y" ]; then
  echo "Upload cancelled."
  exit 0
fi

echo "Uploading to PyPI..."
twine upload dist/*
