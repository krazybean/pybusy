#!/usr/bin/env bash
set -euo pipefail

BUMP_TYPE="${1:-patch}"

if [[ ! -f pyproject.toml || ! -f pybusy/__init__.py ]]; then
  echo "Release files not found"
  exit 1
fi

OLD_VERSION="$(sed -n 's/^version = "\([0-9][0-9.]*\)"/\1/p' pyproject.toml | head -n 1)"

if [[ -z "$OLD_VERSION" ]]; then
  echo "Could not determine current version from pyproject.toml"
  exit 1
fi

IFS='.' read -r OLD_MAJOR OLD_MINOR OLD_PATCH <<< "$OLD_VERSION"

NEW_VERSION=""

case "$BUMP_TYPE" in
  patch)
    NEW_VERSION="$OLD_MAJOR.$OLD_MINOR.$((OLD_PATCH + 1))"
    ;;
  minor)
    NEW_VERSION="$OLD_MAJOR.$((OLD_MINOR + 1)).0"
    ;;
  major)
    NEW_VERSION="$((OLD_MAJOR + 1)).0.0"
    ;;
  manual)
    read -r -p "Enter release version: " NEW_VERSION
    if [[ -z "$NEW_VERSION" ]]; then
      echo "No version entered."
      exit 1
    fi
    ;;
  *)
    echo "Usage: $0 [patch|minor|major|manual]"
    exit 1
    ;;
esac

echo "Updating version: $OLD_VERSION -> $NEW_VERSION"

perl -0pi -e "s/version = \"$OLD_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
perl -0pi -e "s/__version__ = \"$OLD_VERSION\"/__version__ = \"$NEW_VERSION\"/" pybusy/__init__.py

echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
python -m build

if ! compgen -G "dist/*" > /dev/null; then
  echo "Build failed - no artifacts found"
  exit 1
fi

read -p "Proceed with release v$NEW_VERSION? (y/N): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Release cancelled."
  exit 0
fi

git add pyproject.toml pybusy/__init__.py
git commit -m "release: v$NEW_VERSION"
git tag "v$NEW_VERSION"
git push
git push origin "v$NEW_VERSION"

echo "Version: $OLD_VERSION -> $NEW_VERSION"
echo "Release prepared. GitHub Actions will publish v$NEW_VERSION to PyPI."
