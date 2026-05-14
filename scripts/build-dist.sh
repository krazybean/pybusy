#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON:-python3}"

if ! "$PYTHON_BIN" -c "import build" >/dev/null 2>&1; then
  echo "Missing build package. Install it with: $PYTHON_BIN -m pip install build twine"
  exit 1
fi

if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-$(git log -1 --format=%ct)}"
fi

echo "Cleaning previous build outputs..."
rm -rf dist/ build/ *.egg-info

echo "Building source distribution and wheel..."
"$PYTHON_BIN" -m build --sdist --wheel

"$PYTHON_BIN" scripts/normalize_sdist.py dist/*.tar.gz

if "$PYTHON_BIN" -c "import twine" >/dev/null 2>&1; then
  echo "Checking package metadata..."
  "$PYTHON_BIN" -m twine check dist/*
else
  echo "Skipping twine check; install twine to validate package metadata."
fi

echo "Writing dist/SHA256SUMS..."
(
  cd dist
  find . -maxdepth 1 -type f ! -name SHA256SUMS -print \
    | sed 's#^\./##' \
    | LC_ALL=C sort \
    | while IFS= read -r artifact; do
        shasum -a 256 "$artifact"
      done > SHA256SUMS
)

echo "Built artifacts:"
ls -l dist
