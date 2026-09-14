#!/usr/bin/env bash
set -euo pipefail

# Installs the kryptonite skill by symlinking this repo into
# ~/.claude/skills/kryptonite, so Claude Code picks up SKILL.md, the phase
# skills, modules, references, and scripts as an installed skill. Safe to
# run more than once (idempotent) and works from any working directory.

# Resolve the repo root from this script's own location, following symlinks.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd -P "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"

SKILLS_DIR="$HOME/.claude/skills"
TARGET="$SKILLS_DIR/kryptonite"

mkdir -p "$SKILLS_DIR"
ln -sfn "$REPO_ROOT" "$TARGET"

echo "kryptonite installed: $TARGET -> $REPO_ROOT"
