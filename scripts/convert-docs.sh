#!/usr/bin/env bash
# convert-docs.sh
# Cross-platform runner (Linux / macOS / WSL) for Business Analyst document & image conversion.
#
# Usage:
#   ./scripts/convert-docs.sh --all
#   ./scripts/convert-docs.sh --file docs/source/spec.docx
#   ./scripts/convert-docs.sh --file docs/source/mockup.png --enable-ocr
#   ./scripts/convert-docs.sh --all --enable-ocr --model gpt-4o

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/convert-docs.py"

# Find python3 or python
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: Neither 'python3' nor 'python' was found in PATH." >&2
  exit 1
fi

# Run the self-healing Python engine
exec "$PYTHON_BIN" "$PY_SCRIPT" "$@"
