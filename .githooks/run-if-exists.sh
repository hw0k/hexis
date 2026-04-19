#!/bin/bash
# run-if-exists.sh
# Project-aware hook delegator for hexis.
# Detects the project's toolchain and runs the requested task (lint/format/test).
# Exits 0 silently if no matching script is found — enforcement is opt-in.
#
# Usage: run-if-exists.sh <task>
#   task: lint | format | test
#
# Detection priority:
#   1. package.json script matching <task>
#   2. Makefile target matching <task>
#   3. .hexis/hooks/pre-commit-<task>.sh
#   4. None found → skip

set -euo pipefail

TASK="${1:?Usage: run-if-exists.sh <task>}"
PLUGIN_PREFIX="[hexis]"

# ── 1. package.json ──────────────────────────────────────────────────────────
if [[ -f "package.json" ]] && command -v node &>/dev/null; then
  if node -e "process.exit(require('./package.json').scripts?.['$TASK'] ? 0 : 1)" 2>/dev/null; then
    # Detect package manager from lockfile
    if [[ -f "pnpm-lock.yaml" ]]; then
      PM="pnpm"
    elif [[ -f "yarn.lock" ]]; then
      PM="yarn"
    else
      PM="npm"
    fi
    echo "$PLUGIN_PREFIX Running $TASK via $PM..."
    exec "$PM" run "$TASK"
  fi
fi

# ── 2. Makefile ───────────────────────────────────────────────────────────────
if [[ -f "Makefile" ]] && command -v make &>/dev/null; then
  if make -n "$TASK" &>/dev/null 2>&1; then
    echo "$PLUGIN_PREFIX Running $TASK via make..."
    exec make "$TASK"
  fi
fi

# ── 3. Escape hatch: .hexis/hooks/pre-commit-<task>.sh ───────────────
CUSTOM_HOOK=".hexis/hooks/pre-commit-${TASK}.sh"
if [[ -f "$CUSTOM_HOOK" ]]; then
  echo "$PLUGIN_PREFIX Running $TASK via $CUSTOM_HOOK..."
  exec bash "$CUSTOM_HOOK"
fi

# ── 4. Nothing found — skip ───────────────────────────────────────────────────
echo "$PLUGIN_PREFIX No $TASK script found, skipping." >&2
exit 0
