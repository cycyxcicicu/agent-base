#!/usr/bin/env sh
DIR="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$DIR/scripts/setup-skills.py" "$@"
