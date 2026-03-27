# hw0k-workflow Enhancement — Infrastructure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use hw0k-workflow:implement (recommended) or hw0k-workflow:implement to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the infrastructure layer of the hw0k-workflow enhancement — lefthook git hooks and the new-project-setup skill — as defined in `docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md`.

**Architecture:** Two deliverables: (1) `.githooks/` directory with lefthook config and shell scripts committed to the plugin repo, providing both self-dogfooding hooks and a template for user projects; (2) `skills/new-project-setup/` skill that guides onboarding. All files are either markdown or shell scripts — no compiled code.

**Tech Stack:** lefthook (Go binary, no runtime dependency), bash (POSIX-compatible shell scripts), Markdown (SKILL.md format)

**Prerequisite:** Plan A (content) does not need to be complete before this plan can run — the two plans are independent.

---

## File Map

| Path | Action | Task |
|------|--------|------|
| `.githooks/lefthook.yml` | Create | 1 |
| `.githooks/check-commit-msg.sh` | Create | 1 |
| `.githooks/run-if-exists.sh` | Create | 2 |
| `skills/new-project-setup/SKILL.md` | Create | 3 |
| `skills/new-project-setup/lefthook.yml` | Create | 3 |

---

### Task 1: lefthook Config and Commit Message Validator

**Files:**
- Create: `.githooks/lefthook.yml`
- Create: `.githooks/check-commit-msg.sh`

- [ ] **Step 1: Create `.githooks/lefthook.yml`**

```yaml
# .githooks/lefthook.yml
# hw0k-workflow git hook configuration
# Install: git config core.hooksPath .githooks && lefthook install

commit_msg:
  commands:
    validate-conventional-commit:
      run: .githooks/check-commit-msg.sh {1}

pre_commit:
  parallel: true
  commands:
    lint:
      run: .githooks/run-if-exists.sh lint
      skip:
        - merge
        - rebase
    format:
      run: .githooks/run-if-exists.sh format
      skip:
        - merge
        - rebase
    test:
      run: .githooks/run-if-exists.sh test
      skip:
        - merge
        - rebase
```

- [ ] **Step 2: Create `.githooks/check-commit-msg.sh`**

```bash
#!/bin/bash
# check-commit-msg.sh
# Validates commit message against Conventional Commits 1.0.0
# Usage: check-commit-msg.sh <path-to-commit-msg-file>

set -euo pipefail

MSG_FILE="${1:?Usage: check-commit-msg.sh <commit-msg-file>}"

# Read subject line (first non-empty, non-comment line)
SUBJECT=$(grep -v '^#' "$MSG_FILE" | sed '/^[[:space:]]*$/d' | head -1)

if [[ -z "$SUBJECT" ]]; then
  echo "ERROR: Commit message is empty." >&2
  exit 1
fi

# Exempt git-generated messages
if echo "$SUBJECT" | grep -qE '^Merge '; then
  exit 0
fi
if echo "$SUBJECT" | grep -qE '^Revert "'; then
  exit 0
fi
if echo "$SUBJECT" | grep -qE '^(fixup|squash)! '; then
  exit 0
fi

# Allowed types
TYPES="feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"

# Full pattern: type[(scope)][!]: description
PATTERN="^($TYPES)(\([a-z0-9][a-z0-9._-]*\))?(!)?: [a-z].*[^.]$"

if ! echo "$SUBJECT" | grep -qE "$PATTERN"; then
  # Diagnose which rule was violated for a helpful error message
  TYPE=$(echo "$SUBJECT" | grep -oE '^[a-z]+' || true)
  REASON=""

  if [[ -z "$TYPE" ]]; then
    REASON="Missing type prefix. Subject must start with a type (e.g. feat, fix, chore)."
  elif ! echo "$TYPE" | grep -qE "^($TYPES)$"; then
    REASON="Type \"$TYPE\" is not in the allowed list."$'\n'"  Allowed: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
  elif ! echo "$SUBJECT" | grep -qE "^($TYPES)(\([a-z0-9][a-z0-9._-]*\))?(!)?: "; then
    if echo "$SUBJECT" | grep -qE "^($TYPES)\([A-Z]"; then
      REASON="Scope must be lowercase (e.g. feat(auth): not feat(Auth):)."
    elif echo "$SUBJECT" | grep -qE "^($TYPES)\(.*\s"; then
      REASON="Scope must not contain spaces (e.g. feat(user-service): not feat(user service):)."
    else
      REASON="Missing \": \" separator after type/scope. Expected format: type: description"
    fi
  elif echo "$SUBJECT" | grep -qE "^($TYPES)(\([a-z0-9][a-z0-9._-]*\))?(!)?: [A-Z]"; then
    REASON="Description must start with a lowercase letter."
  elif echo "$SUBJECT" | grep -qE "\.$"; then
    REASON="Description must not end with a period."
  else
    REASON="Does not match Conventional Commits format."
  fi

  echo "" >&2
  echo "ERROR: Invalid commit message." >&2
  echo "" >&2
  echo "  Subject: \"$SUBJECT\"" >&2
  echo "" >&2
  echo "  Reason: $REASON" >&2
  echo "" >&2
  echo "  Expected format: <type>[optional scope]: <description>" >&2
  echo "  Example:         feat(auth): add token refresh logic" >&2
  echo "" >&2
  echo "  See hw0k-workflow:conventional-commit for full rules." >&2
  echo "" >&2
  exit 1
fi

# Advisory: warn if subject exceeds 72 characters (do not fail)
if [[ ${#SUBJECT} -gt 72 ]]; then
  echo "WARNING: Subject line is ${#SUBJECT} characters (recommended max: 72)." >&2
fi

exit 0
```

- [ ] **Step 3: Make scripts executable**

```bash
chmod +x .githooks/check-commit-msg.sh
```

- [ ] **Step 4: Verify `check-commit-msg.sh` manually**

Test valid messages exit 0:
```bash
echo "feat: add login flow" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 0

echo "feat(auth): add login flow" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 0

echo "feat!: remove v1 endpoint" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 0
```

Test exempt messages exit 0:
```bash
echo "Merge branch 'main' into feature/x" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 0

echo 'Revert "feat: add login flow"' > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 0
```

Test violations exit 1 with helpful messages:
```bash
echo "Added login flow" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 1, reason: missing type prefix

echo "update: bump dependency" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 1, reason: type not in allowed list

echo "feat: Add login flow" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 1, reason: uppercase start

echo "feat: add login flow." > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 1, reason: trailing period

echo "feat(Auth): add login" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
echo "Exit: $?"   # Expected: Exit: 1, reason: uppercase scope
```

All 5 violation cases must produce exit 1 with a specific reason message.

- [ ] **Step 5: Commit**

```bash
git add .githooks/lefthook.yml .githooks/check-commit-msg.sh
git commit -m "feat: add lefthook config and commit message validator"
```

---

### Task 2: Project-Aware Pre-Commit Delegator

**Files:**
- Create: `.githooks/run-if-exists.sh`

- [ ] **Step 1: Create `.githooks/run-if-exists.sh`**

```bash
#!/bin/bash
# run-if-exists.sh
# Project-aware hook delegator for hw0k-workflow.
# Detects the project's toolchain and runs the requested task (lint/format/test).
# Exits 0 silently if no matching script is found — enforcement is opt-in.
#
# Usage: run-if-exists.sh <task>
#   task: lint | format | test
#
# Detection priority:
#   1. package.json script matching <task>
#   2. Makefile target matching <task>
#   3. .hw0k-workflow/hooks/pre-commit-<task>.sh
#   4. None found → skip

set -euo pipefail

TASK="${1:?Usage: run-if-exists.sh <task>}"
PLUGIN_PREFIX="[hw0k-workflow]"

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

# ── 3. Escape hatch: .hw0k-workflow/hooks/pre-commit-<task>.sh ───────────────
CUSTOM_HOOK=".hw0k-workflow/hooks/pre-commit-${TASK}.sh"
if [[ -f "$CUSTOM_HOOK" ]]; then
  echo "$PLUGIN_PREFIX Running $TASK via $CUSTOM_HOOK..."
  exec bash "$CUSTOM_HOOK"
fi

# ── 4. Nothing found — skip ───────────────────────────────────────────────────
echo "$PLUGIN_PREFIX No $TASK script found, skipping." >&2
exit 0
```

- [ ] **Step 2: Make script executable**

```bash
chmod +x .githooks/run-if-exists.sh
```

- [ ] **Step 3: Verify `run-if-exists.sh` manually**

Test skip behavior (no package.json, no Makefile, no custom hook):
```bash
# From a temp directory with none of the triggers
cd /tmp && bash /home/hw0k-win11-wsl/workspaces/claude-hw0k-workflow/.githooks/run-if-exists.sh lint
# Expected output: "[hw0k-workflow] No lint script found, skipping."
# Expected exit: 0
```

Test unknown task exits 1 with usage message:
```bash
bash .githooks/run-if-exists.sh
# Expected: "Usage: run-if-exists.sh <task>" and exit 1
```

- [ ] **Step 4: Commit**

```bash
git add .githooks/run-if-exists.sh
git commit -m "feat: add project-aware pre-commit delegator script"
```

---

### Task 3: new-project-setup Skill

**Files:**
- Create: `skills/new-project-setup/SKILL.md`
- Create: `skills/new-project-setup/lefthook.yml`

- [ ] **Step 1: Create `skills/new-project-setup/lefthook.yml`**

This is the template users copy to their project root. Annotated so they know which sections are hw0k-workflow defaults vs project-specific.

```yaml
# lefthook.yml
# hw0k-workflow project template
# Copy to your project root, then run: lefthook install
#
# hw0k-workflow sections are marked # hw0k-workflow
# Project-specific sections are marked # project-specific — customize these

# hw0k-workflow: validates commit message format (Conventional Commits 1.0.0)
# Copy .githooks/check-commit-msg.sh from hw0k-workflow to your .githooks/
commit_msg:
  commands:
    validate-conventional-commit:  # hw0k-workflow
      run: .githooks/check-commit-msg.sh {1}

pre_commit:
  parallel: true
  commands:
    lint:  # hw0k-workflow — detects your toolchain automatically
      run: .githooks/run-if-exists.sh lint
      skip:
        - merge
        - rebase

    format:  # hw0k-workflow — detects your toolchain automatically
      run: .githooks/run-if-exists.sh format
      skip:
        - merge
        - rebase

    test:  # hw0k-workflow — detects your toolchain automatically
      run: .githooks/run-if-exists.sh test
      skip:
        - merge
        - rebase

# project-specific: add your own hooks below
# Example:
# pre_push:
#   commands:
#     run-e2e:
#       run: npm run test:e2e
```

- [ ] **Step 2: Create `skills/new-project-setup/SKILL.md`**

```markdown
---
name: new-project-setup
description: Guides onboarding of a new project to hw0k-workflow standards — installs lefthook git hooks, sets up version-controlled hook config, and optionally configures Claude Code auto-sync
type: workflow
---

# New Project Setup

Follow these steps to apply hw0k-workflow standards to a new project. After setup, every git commit on any tool — VS Code, JetBrains, terminal, any agent — passes through the same enforcement hooks.

## Prerequisites

- `git` installed and repo initialized
- `lefthook` installed (one-time per machine — see Step 1)
- Plugin dir accessible: wherever `hw0k-workflow` is installed (e.g. `~/.claude/plugins/hw0k-workflow/`)

## Steps

### Step 1 — Install lefthook (once per machine)

Choose the method that fits your environment:

```bash
# macOS / Linux via Homebrew
brew install lefthook

# npm (if the project uses Node)
npm install --save-dev lefthook

# Go toolchain
go install github.com/evilmartians/lefthook@latest
```

Verify: `lefthook --version`

### Step 2 — Copy hook files to the project

Copy the `.githooks/` directory from the hw0k-workflow plugin to your project root:

```bash
PLUGIN_DIR=~/.claude/plugins/hw0k-workflow   # adjust to your install path
cp -r "$PLUGIN_DIR/.githooks" ./.githooks
```

This copies:
- `lefthook.yml` — hook orchestration config
- `check-commit-msg.sh` — Conventional Commits validator
- `run-if-exists.sh` — project-aware lint/format/test delegator

### Step 3 — Copy the lefthook template

```bash
cp "$PLUGIN_DIR/skills/new-project-setup/lefthook.yml" ./lefthook.yml
```

If the project already has a `lefthook.yml`, merge only the sections marked `# hw0k-workflow` — do not overwrite the entire file.

### Step 4 — Set the git hooks path and install

```bash
git config core.hooksPath .githooks
lefthook install
```

`core.hooksPath .githooks` points git to the version-controlled hooks directory. This setting persists in the repo's local git config (`.git/config`) — each contributor who clones the repo must run this command once.

To make this automatic for all contributors, add it to an onboarding script or `Makefile`:
```makefile
setup:
	git config core.hooksPath .githooks
	lefthook install
```

### Step 5 — Verify hooks are active

```bash
# Test a bad commit message — should be blocked
echo "bad commit message" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
# Expected: exit 1 with error message

# Test a good commit message — should pass
echo "feat: add initial setup" > /tmp/test-msg.txt
bash .githooks/check-commit-msg.sh /tmp/test-msg.txt
# Expected: exit 0
```

### Step 6 — (Optional) Configure Claude Code auto-sync

Add the `Stop` hook to run `/hw0k-workflow:sync` automatically after each Claude session.

**Team-wide** (commit to repo):
```json
// .claude/settings.json
{
  "hooks": {
    "Stop": [
      { "type": "command", "command": "/hw0k-workflow:sync" }
    ]
  }
}
```

**Personal opt-in** (add `.claude/settings.local.json` to `.gitignore`):
```json
// .claude/settings.local.json
{
  "hooks": {
    "Stop": [
      { "type": "command", "command": "/hw0k-workflow:sync" }
    ]
  }
}
```

## run-if-exists.sh Pattern

The `run-if-exists.sh` script is how pre-commit hooks work without knowing your project's language or toolchain.

When lefthook runs `run-if-exists.sh lint`, the script checks in this order:

1. `package.json` has a `"lint"` script → runs `npm run lint` (or `yarn`/`pnpm` based on lockfile)
2. `Makefile` has a `lint` target → runs `make lint`
3. `.hw0k-workflow/hooks/pre-commit-lint.sh` exists → runs it directly
4. None found → prints skip message and exits 0

The same logic applies for `format` and `test`.

**What this means in practice:**
- A Node project with `"lint": "eslint ."` in `package.json` gets ESLint on every commit automatically — no extra config.
- A Python project with `lint:` in a `Makefile` gets `make lint` automatically.
- A project with neither can add `.hw0k-workflow/hooks/pre-commit-lint.sh` for any custom command.
- A project with none of the above is unaffected — no errors, no blocked commits.

## Customizing Pre-Commit Test Scope

Running the full test suite on every commit is often too slow. Create a targeted test runner:

```bash
# .hw0k-workflow/hooks/pre-commit-test.sh
#!/bin/bash
# Run only tests related to changed files

changed=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|js)$' || true)

if [[ -z "$changed" ]]; then
  echo "[hw0k-workflow] No source files changed, skipping tests."
  exit 0
fi

# Example for Jest: run only tests matching changed file names
echo "[hw0k-workflow] Running tests for changed files..."
npx jest --findRelatedTests $changed --passWithNoTests
```

Adapt the language filter (`\.ts$`, `\.py$`, etc.) and test runner to your project. Commit this file to the project repo at `.hw0k-workflow/hooks/pre-commit-test.sh`.

## Auto-Sync: When to Enable vs Disable

The `Stop` hook runs after **every** Claude response. This is useful for continuous projects but noisy for exploratory sessions.

**Enable team-wide (`settings.json`)** when:
- All contributors use Claude Code with hw0k-workflow
- Standards should be continuously enforced, not just on demand

**Enable per-contributor (`settings.local.json`)** when:
- Not all team members use Claude Code
- Some contributors prefer to run sync manually

**Disable without deleting** (comment out, don't remove — easier to re-enable):
```json
{
  "hooks": {
    "Stop": [
      { "type": "command", "command": "# /hw0k-workflow:sync" }
    ]
  }
}
```

## Global Bypass

To skip all hooks for a single commit (emergency only):
```bash
LEFTHOOK=0 git commit -m "chore: emergency fix"
```

This uses lefthook's standard bypass mechanism — no `--no-verify` needed.
```

- [ ] **Step 3: Verify**

Check `SKILL.md` contains:
- [ ] Prerequisites section
- [ ] 6 numbered steps: install lefthook, copy hook files, copy template, git config + lefthook install, verify hooks active, optional auto-sync
- [ ] `run-if-exists.sh` pattern section (explains 4-step detection, 3 task types)
- [ ] Custom test scope section (example script with `git diff --cached`)
- [ ] Auto-sync enable/disable guidance (team-wide vs personal, how to disable without deleting)
- [ ] Global bypass (`LEFTHOOK=0`)

Check `lefthook.yml` contains:
- [ ] `commit_msg` section with `check-commit-msg.sh {1}`
- [ ] `pre_commit` section with `lint`, `format`, `test` all using `run-if-exists.sh`
- [ ] `skip: [merge, rebase]` on all pre-commit commands
- [ ] `parallel: true` on pre_commit
- [ ] Comments distinguishing `# hw0k-workflow` from `# project-specific` sections

- [ ] **Step 4: Commit**

```bash
git add skills/new-project-setup/
git commit -m "feat: add new-project-setup skill with lefthook onboarding guide"
```

---

## Self-Review Against Spec

### Spec Coverage Check

| Spec requirement | Task |
|-----------------|------|
| `.githooks/lefthook.yml` — commit_msg + pre_commit (lint/format/test) | Task 1 |
| `check-commit-msg.sh` — Conventional Commits validator, exemptions, error messages | Task 1 |
| `run-if-exists.sh` — project-aware delegator (package.json/Makefile/escape hatch) | Task 2 |
| `new-project-setup/SKILL.md` — onboarding steps, run-if-exists pattern, auto-sync guidance | Task 3 |
| `new-project-setup/lefthook.yml` — annotated template for user projects | Task 3 |
| WIP commits not exempt from format enforcement | Task 1 (`check-commit-msg.sh`) |
| `LEFTHOOK=0` global bypass documented | Task 3 (`SKILL.md`) |
| test hook runs scoped tests (custom hook pattern) | Task 3 (`SKILL.md`) |
| `settings.local.json` for personal opt-in | Task 3 (`SKILL.md`) |

All spec infrastructure requirements covered.

### Placeholder Scan

No TBDs, TODOs, or incomplete sections. All shell script content is complete and testable. All SKILL.md sections contain actual guidance, not descriptions of guidance.

### Type Consistency

Shell scripts use consistent variable naming (`TASK`, `PLUGIN_PREFIX`, `MSG_FILE`). The `run-if-exists.sh` task name `lint`/`format`/`test` aligns with the `lefthook.yml` command names. No inconsistencies.
