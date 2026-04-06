---
name: setup-new-project
description: Guides onboarding of a new project to hw0k-workflow standards — installs pre-commit git hooks, sets up commitlint commit message validation, and optionally configures Claude Code auto-sync
type: workflow
---

# New Project Setup

Follow these steps to apply hw0k-workflow standards to a new project. After setup, every git commit on any tool — VS Code, JetBrains, terminal, any agent — passes through the same enforcement hooks.

## Prerequisites

- `git` installed and repo initialized
- `uv` installed (one-time per machine — see Step 1)
- `bun` installed (commitlint runs via `bunx` — no separate install needed)
- Plugin dir accessible: wherever `hw0k-workflow` is installed (e.g. `~/.claude/plugins/hw0k-workflow/`)

## Steps

### Step 1 — Install uv (once per machine)

`uv` provides `uvx`, which runs pre-commit without a permanent install:

```bash
# macOS / Linux via Homebrew
brew install uv

# or via the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify: `uv --version`

### Step 2 — Copy the commitlint config

commitlint validates commit messages against Conventional Commits 1.0.0. It runs via `bunx` — no installation required. Copy the hw0k-workflow config to the project root:

```bash
PLUGIN_DIR=~/.claude/plugins/hw0k-workflow   # adjust to your install path
cp "$PLUGIN_DIR/skills/setup-new-project/.commitlintrc.yml" ./.commitlintrc.yml
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
chmod +x .githooks/run-if-exists.sh
```

This copies:
- `run-if-exists.sh` — project-aware lint/format/test delegator

### Step 4 — Copy the pre-commit config

```bash
cp "$PLUGIN_DIR/.pre-commit-config.yaml" ./.pre-commit-config.yaml
```

Commit both:
```bash
git add .githooks .pre-commit-config.yaml
git commit -m "chore: add hw0k-workflow hook infrastructure"
```

### Step 5 — Install hooks

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```

pre-commit installs to `.git/hooks/` directly — no `git config core.hooksPath` needed. Each contributor who clones the repo must run these commands once.

To make this automatic, add to an onboarding script or `Makefile`:
```makefile
setup:
	uvx pre-commit install
	uvx pre-commit install --hook-type commit-msg
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

When pre-commit runs `run-if-exists.sh lint`, the script checks in this order:

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
git commit --no-verify -m "chore: emergency fix"
```

To skip specific hooks only:
```bash
SKIP=lint,test git commit -m "chore: skip lint and test for this commit"
```
