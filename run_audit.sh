#!/usr/bin/env bash
# Repo Quality Guard — Convenience Runner for Linux / macOS

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/repo_quality_guard.py" "$@"
