---
linked_spec: docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md
---

# hw0k-workflow Enhancement — Infrastructure Plan

> **Historical document.** This plan reflects the initial implementation state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

> **For agentic workers:** Use `hw0k-workflow:implement` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the infrastructure layer of the hw0k-workflow enhancement — lefthook git hooks and the new-project-setup skill — as defined in `docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md`.

**Architecture:** Two deliverables: (1) `.githooks/` directory with lefthook config committed to the plugin repo, providing both self-dogfooding hooks and a template for user projects; (2) `skills/new-project-setup/` skill that guides onboarding. Commit message validation is delegated to `commitlint` + `@commitlint/config-conventional` — no custom validator shell script.

**Tech Stack:** lefthook (Go binary, no runtime dependency), commitlint + @commitlint/config-conventional (Node/npm), bash (POSIX-compatible shell scripts), Markdown (SKILL.md format)

**Prerequisite:** Plan A (content) does not need to be complete before this plan can run — the two plans are independent.

---

## File Map

| Path | Action | Task |
|------|--------|------|
| `.githooks/lefthook.yml` | Create | 1 |
| `.commitlintrc.yml` | Create | 1 |
| `.githooks/run-if-exists.sh` | Create | 2 |
| `skills/new-project-setup/SKILL.md` | Create | 3 |
| `skills/new-project-setup/lefthook.yml` | Create | 3 |
| `skills/new-project-setup/.commitlintrc.yml` | Create | 3 |

---

### Task 1: lefthook Config and commitlint Setup

**Files:**
- Create: `.githooks/lefthook.yml`
- Create: `.commitlintrc.yml`

- [ ] **Step 1: Create `.githooks/lefthook.yml`**

```yaml
# .githooks/lefthook.yml
# hw0k-workflow git hook configuration
# Install: git config core.hooksPath .githooks && lefthook install

commit_msg:
  commands:
    validate-conventional-commit:
      run: bunx commitlint --edit {1}

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

- [ ] **Step 2: Create `.commitlintrc.yml`**

```yaml
# .commitlintrc.yml
# Conventional Commits 1.0.0 enforcement — relaxed subject rules
# type[(scope)][!]: description
#
# subject-case and subject-full-stop are disabled intentionally:
#   - subject-case: English-specific rule (lowercase-start); not imposed
#   - subject-full-stop: No trailing period; not imposed
extends:
  - '@commitlint/config-conventional'
rules:
  subject-case: [0]
  subject-full-stop: [0]
```

- [ ] **Step 4: Verify commitlint works**

Test valid messages exit 0:
```bash
echo "feat: add login flow" | bunx commitlint
# Expected: exit 0

echo "feat(auth): Add login flow" | bunx commitlint
# Expected: exit 0 (uppercase start allowed)

echo "feat!: remove v1 endpoint" | bunx commitlint
# Expected: exit 0

echo "fix: resolve timeout issue." | bunx commitlint
# Expected: exit 0 (trailing period allowed)
```

Test violations exit 1:
```bash
echo "update: bump dependency" | bunx commitlint
# Expected: exit 1, reason: type "update" not allowed

echo "added login flow" | bunx commitlint
# Expected: exit 1, reason: missing type prefix

echo "feat(user service): add login" | bunx commitlint
# Expected: exit 1, reason: scope contains space
```

All 3 violation cases must exit 1 with a reason message.

- [ ] **Step 5: Commit**

```bash
git add .githooks/lefthook.yml .commitlintrc.yml
git commit -m "feat: add lefthook config and commitlint conventional commit enforcement"
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
- Create: `skills/new-project-setup/.commitlintrc.yml`

- [ ] **Step 1: Create `skills/new-project-setup/.commitlintrc.yml`**

This is the template users copy to their project root.

```yaml
# .commitlintrc.yml
# Conventional Commits 1.0.0 enforcement — relaxed subject rules
# type[(scope)][!]: description
#
# subject-case and subject-full-stop are disabled intentionally:
#   - subject-case: English-specific rule (lowercase-start); not imposed
#   - subject-full-stop: No trailing period; not imposed
extends:
  - '@commitlint/config-conventional'
rules:
  subject-case: [0]
  subject-full-stop: [0]
```

- [ ] **Step 2: Create `skills/new-project-setup/lefthook.yml`**

This is the template users copy to their project root. Annotated so they know which sections are hw0k-workflow defaults vs project-specific.

```yaml
# lefthook.yml
# hw0k-workflow project template
# Copy to your project root, then run: lefthook install
#
# hw0k-workflow sections are marked # hw0k-workflow
# Project-specific sections are marked # project-specific — customize these

# hw0k-workflow: validates commit message format (Conventional Commits 1.0.0)
# Requires: commitlint installed in the project (see new-project-setup SKILL.md Step 2)
commit_msg:
  commands:
    validate-conventional-commit:  # hw0k-workflow
      run: bunx commitlint --edit {1}

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

- [ ] **Step 3: Create `skills/new-project-setup/SKILL.md`**

```markdown
---
name: new-project-setup
description: Guides onboarding of a new project to hw0k-workflow standards — installs lefthook git hooks, sets up commitlint commit message validation, and optionally configures Claude Code auto-sync
type: workflow
---

# New Project Setup

Follow these steps to apply hw0k-workflow standards to a new project. After setup, every git commit on any tool — VS Code, JetBrains, terminal, any agent — passes through the same enforcement hooks.

## Prerequisites

- `git` installed and repo initialized
- `lefthook` installed (one-time per machine — see Step 1)
- `bun` installed (commitlint runs via `bunx` — no separate install needed)
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

### Step 2 — Copy the commitlint config

commitlint validates commit messages against Conventional Commits 1.0.0. It runs via `bunx` — no installation required. Copy the hw0k-workflow config to the project root:

```bash
PLUGIN_DIR=~/.claude/plugins/hw0k-workflow   # adjust to your install path
cp "$PLUGIN_DIR/skills/new-project-setup/.commitlintrc.yml" ./.commitlintrc.yml
```

Commit the config:
```bash
git add .commitlintrc.yml
git commit -m "chore: add commitlint config for conventional commit enforcement"
```

### Step 3 — Copy hook files to the project

Copy the `.githooks/` directory from the hw0k-workflow plugin to your project root:

```bash
PLUGIN_DIR=~/.claude/plugins/hw0k-workflow   # adjust to your install path
cp -r "$PLUGIN_DIR/.githooks" ./.githooks
```

This copies:
- `lefthook.yml` — hook orchestration config (inside `.githooks/`, used by lefthook)
- `run-if-exists.sh` — project-aware lint/format/test delegator

### Step 4 — Copy the lefthook template

```bash
cp "$PLUGIN_DIR/skills/new-project-setup/lefthook.yml" ./lefthook.yml
```

If the project already has a `lefthook.yml`, merge only the sections marked `# hw0k-workflow` — do not overwrite the entire file.

### Step 5 — Set the git hooks path and install

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

### Step 6 — Verify hooks are active

```bash
# Test a bad commit message — should be blocked
echo "bad commit message" | bunx commitlint
# Expected: exit 1 with error message

# Test a good commit message — should pass
echo "feat: add initial setup" | bunx commitlint
# Expected: exit 0

# Test that relaxed rules work (uppercase start, trailing period allowed)
echo "feat: Add initial setup." | bunx commitlint
# Expected: exit 0
```

### Step 7 — (Optional) Configure Claude Code auto-sync

Add the `Stop` hook to run `/hw0k-workflow:sync-working-status` automatically after each Claude session.

**Team-wide** (commit to repo):
```json
// .claude/settings.json
{
  "hooks": {
    "Stop": [
      { "type": "command", "command": "/hw0k-workflow:sync-working-status" }
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
      { "type": "command", "command": "/hw0k-workflow:sync-working-status" }
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
      { "type": "command", "command": "# /hw0k-workflow:sync-working-status" }
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

- [ ] **Step 4: Verify**

Check `SKILL.md` contains:
- [ ] Prerequisites section (git, lefthook, bun, plugin dir)
- [ ] 7 numbered steps: install lefthook, copy commitlint config, copy hook files, copy lefthook template, git config + install, verify hooks active, optional auto-sync
- [ ] `run-if-exists.sh` pattern section (explains 4-step detection, 3 task types)
- [ ] Custom test scope section (example script with `git diff --cached`)
- [ ] Auto-sync enable/disable guidance (team-wide vs personal, how to disable without deleting)
- [ ] Global bypass (`LEFTHOOK=0`)

Check `lefthook.yml` template contains:
- [ ] `commit_msg` section with `bunx commitlint --edit {1}`
- [ ] `pre_commit` section with `lint`, `format`, `test` all using `run-if-exists.sh`
- [ ] `skip: [merge, rebase]` on all pre-commit commands
- [ ] `parallel: true` on pre_commit
- [ ] Comments distinguishing `# hw0k-workflow` from `# project-specific` sections

Check `.commitlintrc.yml` template contains:
- [ ] `extends: ['@commitlint/config-conventional']`
- [ ] `subject-case: [0]`
- [ ] `subject-full-stop: [0]`

- [ ] **Step 5: Commit**

```bash
git add skills/new-project-setup/
git commit -m "feat: add new-project-setup skill with lefthook and commitlint onboarding guide"
```

---

## Self-Review Against Spec

### Spec Coverage Check

| Spec requirement | Task |
|-----------------|------|
| `.githooks/lefthook.yml` — commit_msg + pre_commit (lint/format/test) | Task 1 |
| commitlint + `.commitlintrc.yml` — Conventional Commits validator, relaxed subject rules | Task 1 |
| `run-if-exists.sh` — project-aware delegator (package.json/Makefile/escape hatch) | Task 2 |
| `new-project-setup/SKILL.md` — onboarding steps, run-if-exists pattern, auto-sync guidance | Task 3 |
| `new-project-setup/lefthook.yml` — annotated template for user projects | Task 3 |
| `new-project-setup/.commitlintrc.yml` — commitlintrc template for user projects | Task 3 |
| commitlint installation as prerequisite (Don't Reinvent the Wheel principle) | Task 3 (`SKILL.md`) |
| `LEFTHOOK=0` global bypass documented | Task 3 (`SKILL.md`) |
| test hook runs scoped tests (custom hook pattern) | Task 3 (`SKILL.md`) |
| `settings.local.json` for personal opt-in | Task 3 (`SKILL.md`) |
| subject-case and subject-full-stop rules disabled | Tasks 1, 3 (`.commitlintrc.yml`) |

All spec infrastructure requirements covered.

### Placeholder Scan

No TBDs, TODOs, or incomplete sections. All shell script content is complete and testable. All SKILL.md sections contain actual guidance, not descriptions of guidance. All commitlint configs are complete with exact rule names and severity levels.

### Type Consistency

`run-if-exists.sh` task names (`lint`/`format`/`test`) align with `lefthook.yml` command names. commitlint invocation `bunx commitlint --edit {1}` matches between `.githooks/lefthook.yml` and `skills/new-project-setup/lefthook.yml`. `.commitlintrc.yml` rule names (`subject-case`, `subject-full-stop`) are valid commitlint rule identifiers. No inconsistencies.
