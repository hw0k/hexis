# Issues #2 + #3 + #4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Relocate plan mode to executing task skills, add sync-working-status calls at completion, and migrate git hooks from lefthook to Python pre-commit (uvx).

**Architecture:** Issues #2 and #3 are pure markdown edits to skill files — no code, no tests, verification is reading the changed files. Issue #4 is a config migration that replaces lefthook.yml with .pre-commit-config.yaml and rewrites the setup-new-project and use-worktree skills.

**Tech Stack:** Markdown skill files, Python pre-commit (uvx), bash (.githooks/run-if-exists.sh unchanged)

---

## Issues #2 + #3: Skill File Updates

Covers five skill files. Issues are combined because they overlap on the same three files (write-test, implement, verify).

### Files Modified

- Modify: `skills/specify/SKILL.md`
- Modify: `skills/plan/SKILL.md`
- Modify: `skills/write-test/SKILL.md`
- Modify: `skills/implement/SKILL.md`
- Modify: `skills/verify/SKILL.md`

---

### Task 1: Update `skills/specify/SKILL.md` — remove plan mode

**Files:**
- Modify: `skills/specify/SKILL.md`

- [ ] **Step 1: Remove `EnterPlanMode` call in `$ARGUMENTS` section**

Remove line 21:
```
Call `EnterPlanMode` immediately after reading $ARGUMENTS.
```

- [ ] **Step 2: Remove plan mode checklist items**

Replace:
```markdown
## Checklist

- [ ] EnterPlanMode
- [ ] Identify what is blurry — list specific ambiguities
- [ ] Ask clarifying questions (AskUserQuestion, one at a time)
- [ ] ultrathink before writing the spec
- [ ] ExitPlanMode (draft spec in plan file → user approves)
- [ ] Write spec to docs/specs/
- [ ] Commit
- [ ] Hand off to hw0k-workflow:plan
```

With:
```markdown
## Checklist

- [ ] Identify what is blurry — list specific ambiguities
- [ ] Ask clarifying questions (AskUserQuestion, one at a time)
- [ ] ultrathink before writing the spec
- [ ] Write spec to docs/specs/
- [ ] Commit
- [ ] Hand off to hw0k-workflow:plan
```

- [ ] **Step 3: Rewrite Step 3 — remove plan file and ExitPlanMode**

Replace:
```markdown
### Step 3: Draft and Approve

**ultrathink** before writing — identify any remaining ambiguities and surface them as questions first.

Draft the spec in the plan file (`~/.claude/plans/`). A good spec answers:
- What exactly does this do? (behavior)
- What are the inputs and outputs?
- What is explicitly out of scope?
- What does "done" look like?

**Self-review before ExitPlanMode:**
1. **Ambiguity scan:** Any phrase open to two interpretations? Pick one and make it explicit.
2. **Scope check:** Anything still undefined?
3. **Placeholder scan:** TBD, TODO → fix.

Call `ExitPlanMode`. User approves the draft.

> The plan file (`~/.claude/plans/`) is a **temporary approval draft only** — it is NOT the spec artifact. The real output is `docs/specs/YYYY-MM-DD-<topic>-design.md`, written in Step 4.
```

With:
```markdown
### Step 3: Draft

**ultrathink** before writing — identify any remaining ambiguities and surface them as questions first.

A good spec answers:
- What exactly does this do? (behavior)
- What are the inputs and outputs?
- What is explicitly out of scope?
- What does "done" look like?

**Self-review before writing:**
1. **Ambiguity scan:** Any phrase open to two interpretations? Pick one and make it explicit.
2. **Scope check:** Anything still undefined?
3. **Placeholder scan:** TBD, TODO → fix.
```

- [ ] **Step 4: Remove ExitPlanMode rejection rule**

Remove from Rules section:
```
- If ExitPlanMode is rejected: return to Step 3 and re-draft. Do NOT skip to implementation.
```

- [ ] **Step 5: Verify**

Read `skills/specify/SKILL.md` — confirm no `EnterPlanMode`, `ExitPlanMode`, or plan file references remain.

- [ ] **Step 6: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "refactor(specify): remove plan mode — specify is planning, not executing"
```

---

### Task 2: Update `skills/plan/SKILL.md` — remove plan mode

**Files:**
- Modify: `skills/plan/SKILL.md`

- [ ] **Step 1: Remove `EnterPlanMode` call in `$ARGUMENTS` section**

Remove line 19:
```
Call `EnterPlanMode` immediately after loading the spec.
```

- [ ] **Step 2: Remove plan file draft + ExitPlanMode in File Structure section**

Replace:
```markdown
**ultrathink** before decomposing tasks — never skip this.

Draft the full plan in the plan file (`~/.claude/plans/`). Call `ExitPlanMode` for user approval before writing to `docs/plans/`.
```

With:
```markdown
**ultrathink** before decomposing tasks — never skip this.
```

- [ ] **Step 3: Verify**

Read `skills/plan/SKILL.md` — confirm no `EnterPlanMode`, `ExitPlanMode`, or plan file references remain (except in the Step Structure example which is illustrative).

- [ ] **Step 4: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "refactor(plan): remove plan mode — plan is planning, not executing"
```

---

### Task 3: Update `skills/write-test/SKILL.md` — add plan mode + sync

**Files:**
- Modify: `skills/write-test/SKILL.md`

- [ ] **Step 1: Add Complexity Check section after `$ARGUMENTS`**

Add after the `$ARGUMENTS` section (before `## The Iron Law`):
```markdown
## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Changes span multiple files
- Approach is unclear (multiple valid approaches exist)
- Test design is non-obvious or requires architectural decisions

**Complex task** → call `EnterPlanMode`. Design the test approach and get user approval via `ExitPlanMode` before writing any code.
**Simple task** → proceed directly.
```

- [ ] **Step 2: Add sync-working-status after Pre-completion Checklist**

Add after `## Pre-completion Checklist` section (before `## When Stuck`):
```markdown
## Completion

After all checklist items pass:

Invoke `hw0k-workflow:sync-working-status`.
```

- [ ] **Step 3: Verify**

Read `skills/write-test/SKILL.md` — confirm Complexity Check section is present after `$ARGUMENTS`, and sync-working-status call is present after the checklist.

- [ ] **Step 4: Commit**

```bash
git add skills/write-test/SKILL.md
git commit -m "feat(write-test): add plan mode gate and sync-working-status at completion"
```

---

### Task 4: Update `skills/implement/SKILL.md` — add plan mode + sync

**Files:**
- Modify: `skills/implement/SKILL.md`

- [ ] **Step 1: Add Complexity Check section after `$ARGUMENTS`**

Add after the `$ARGUMENTS` section (before `## Process`):
```markdown
## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Plan spans multiple files with cross-task dependencies
- Execution approach is unclear (inline vs. subagent decision is non-obvious)
- Architectural or structural decisions required

**Complex task** → call `EnterPlanMode`. Review the plan, clarify execution strategy, get user approval via `ExitPlanMode` before writing any code.
**Simple task** → proceed directly.
```

- [ ] **Step 2: Add sync-working-status before `hw0k-workflow:finish` in Step 4**

Replace:
```
After all tasks done, invoke `hw0k-workflow:finish`.
```

With:
```
After all tasks done, invoke `hw0k-workflow:sync-working-status`. Then invoke `hw0k-workflow:finish`.
```

- [ ] **Step 3: Verify**

Read `skills/implement/SKILL.md` — confirm Complexity Check section is present, and sync-working-status precedes finish invocation.

- [ ] **Step 4: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "feat(implement): add plan mode gate and sync-working-status at completion"
```

---

### Task 5: Update `skills/verify/SKILL.md` — add plan mode + sync

**Files:**
- Modify: `skills/verify/SKILL.md`

- [ ] **Step 1: Add Complexity Check section after `$ARGUMENTS`**

Add after the `$ARGUMENTS` section (before `## The Iron Law`):
```markdown
## Complexity Check

Before starting, assess scope complexity against these criteria (any one is sufficient):
- Verification spans multiple subsystems
- Success criteria are ambiguous
- Multiple verification strategies are applicable

**Complex scope** → call `EnterPlanMode`. Define verification commands and expected outputs, get user approval via `ExitPlanMode` before running anything.
**Simple scope** → proceed directly.
```

- [ ] **Step 2: Add sync step to Gate Function**

Replace the Gate Function:
```markdown
## Gate Function

```
Before claiming completion:
1. IDENTIFY: which command proves this claim?
2. RUN: full command (fresh, complete)
3. READ: full output, exit code, failure count
4. VERIFY: does the output confirm the claim?
   - NO: state actual status with evidence
   - YES: make the claim with evidence
5. ONLY THEN: claim
```
```

With:
```markdown
## Gate Function

```
Before claiming completion:
1. IDENTIFY: which command proves this claim?
2. RUN: full command (fresh, complete)
3. READ: full output, exit code, failure count
4. VERIFY: does the output confirm the claim?
   - NO: state actual status with evidence
   - YES: proceed to step 5
5. SYNC: invoke hw0k-workflow:sync-working-status
6. ONLY THEN: claim
```
```

- [ ] **Step 3: Verify**

Read `skills/verify/SKILL.md` — confirm Complexity Check section present, Gate Function has 6 steps with SYNC before claim.

- [ ] **Step 4: Commit**

```bash
git add skills/verify/SKILL.md
git commit -m "feat(verify): add plan mode gate and sync-working-status at completion"
```

---

## Issue #4: Migrate lefthook to Python pre-commit (uvx)

### Files Modified/Created/Deleted

- Create: `.pre-commit-config.yaml`
- Delete: `lefthook.yml`
- Delete: `.githooks/lefthook.yml`
- Delete: `.githooks/pre-commit.old` (untracked cleanup)
- Delete: `.githooks/commit-msg.old` (untracked cleanup)
- Modify: `CLAUDE.md`
- Modify: `skills/setup-new-project/SKILL.md`
- Modify: `skills/use-worktree/SKILL.md`
- Modify: `.gitignore` — remove entries for lefthook-generated scripts

---

### Task 6: Create `.pre-commit-config.yaml`

**Files:**
- Create: `.pre-commit-config.yaml`

- [ ] **Step 1: Create the config file**

```yaml
# .pre-commit-config.yaml
# hw0k-workflow — git hook configuration via pre-commit (https://pre-commit.com)
# Install: uvx pre-commit install && uvx pre-commit install --hook-type commit-msg

repos:
  - repo: local
    hooks:
      - id: lint
        name: lint
        language: system
        entry: .githooks/run-if-exists.sh lint
        stages: [pre-commit]
        pass_filenames: false

      - id: format
        name: format
        language: system
        entry: .githooks/run-if-exists.sh format
        stages: [pre-commit]
        pass_filenames: false

      - id: test
        name: test
        language: system
        entry: .githooks/run-if-exists.sh test
        stages: [pre-commit]
        pass_filenames: false

      - id: commitlint
        name: commitlint
        language: system
        entry: bunx commitlint --edit
        stages: [commit-msg]
        pass_filenames: true
```

- [ ] **Step 2: Verify**

Read `.pre-commit-config.yaml` — confirm 4 hooks: lint, format, test (pre-commit stage), commitlint (commit-msg stage).

- [ ] **Step 3: Commit**

```bash
git add .pre-commit-config.yaml
git commit -m "chore: add pre-commit config (replaces lefthook)"
```

---

### Task 7: Delete lefthook config files and old hook backups

**Files:**
- Delete: `lefthook.yml`
- Delete: `.githooks/lefthook.yml`
- Delete: `.githooks/pre-commit.old`
- Delete: `.githooks/commit-msg.old`

- [ ] **Step 1: Delete lefthook configs and old backups**

```bash
rm lefthook.yml .githooks/lefthook.yml
rm -f .githooks/pre-commit.old .githooks/commit-msg.old
```

- [ ] **Step 2: Update `.gitignore` — remove lefthook-generated entries**

Remove these lines from `.gitignore`:
```
# Generated by lefthook install --force — not version-controlled
.githooks/commit-msg
.githooks/pre-commit
```

Also add pre-commit bypass note comment if desired. The `pre-commit` tool installs to `.git/hooks/` (already outside git tracking), so no new gitignore entries are needed.

- [ ] **Step 3: Commit**

```bash
git add -u
git commit -m "chore: remove lefthook config files and old hook backups"
```

---

### Task 8: Update `CLAUDE.md` — replace lefthook references

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Replace Git Hooks section**

Replace:
```markdown
## Git Hooks

This repo self-dogfoods its own hooks:

```bash
git config core.hooksPath .githooks
lefthook install --force
```

`lefthook install --force` generates `.githooks/commit-msg` and `.githooks/pre-commit` — these are gitignored artifacts, not tracked files. Run this command once after cloning.

Commit messages are validated by `bunx commitlint` against `.commitlintrc.yml`. Conventional Commits 1.0.0 with relaxed subject rules (no lowercase-start enforcement, no trailing-period enforcement).

When using `claude --worktree`, the generated hook scripts are automatically copied to the new worktree via `.worktreeinclude`. For manual `git worktree add`, run `lefthook install --force` inside the worktree.
```

With:
```markdown
## Git Hooks

This repo self-dogfoods its own hooks:

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```

Run these once after cloning. Hooks install to `.git/hooks/` — no `core.hooksPath` configuration needed.

Commit messages are validated by `bunx commitlint` against `.commitlintrc.yml`. Conventional Commits 1.0.0 with relaxed subject rules (no lowercase-start enforcement, no trailing-period enforcement).

When creating a git worktree, run `uvx pre-commit install && uvx pre-commit install --hook-type commit-msg` inside the worktree.
```

- [ ] **Step 2: Verify**

Read `CLAUDE.md` — confirm no lefthook references remain. Git Hooks section uses uvx pre-commit.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md git hooks section for pre-commit migration"
```

---

### Task 9: Update `skills/setup-new-project/SKILL.md`

**Files:**
- Modify: `skills/setup-new-project/SKILL.md`

This is a large rewrite of the skill's steps. The overall structure stays the same; content changes are in Steps 1–5 and the Global Bypass section.

- [ ] **Step 1: Update frontmatter description**

Replace:
```yaml
description: Guides onboarding of a new project to hw0k-workflow standards — installs lefthook git hooks, sets up commitlint commit message validation, and optionally configures Claude Code auto-sync
```

With:
```yaml
description: Guides onboarding of a new project to hw0k-workflow standards — installs pre-commit git hooks, sets up commitlint commit message validation, and optionally configures Claude Code auto-sync
```

- [ ] **Step 2: Update Prerequisites**

Replace:
```markdown
## Prerequisites

- `git` installed and repo initialized
- `lefthook` installed (one-time per machine — see Step 1)
- `bun` installed (commitlint runs via `bunx` — no separate install needed)
- Plugin dir accessible: wherever `hw0k-workflow` is installed (e.g. `~/.claude/plugins/hw0k-workflow/`)
```

With:
```markdown
## Prerequisites

- `git` installed and repo initialized
- `uv` installed (one-time per machine — see Step 1)
- `bun` installed (commitlint runs via `bunx` — no separate install needed)
- Plugin dir accessible: wherever `hw0k-workflow` is installed (e.g. `~/.claude/plugins/hw0k-workflow/`)
```

- [ ] **Step 3: Replace Steps 1–5a with new pre-commit steps**

Replace everything from `### Step 1 — Install lefthook (once per machine)` through `### Step 5a — (Optional) Configure worktree hook propagation` with:

```markdown
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
```

- [ ] **Step 4: Update run-if-exists.sh Pattern section**

Replace the introductory sentence:
```
When lefthook runs `run-if-exists.sh lint`, the script checks in this order:
```

With:
```
When pre-commit runs `run-if-exists.sh lint`, the script checks in this order:
```

- [ ] **Step 5: Update Global Bypass section**

Replace:
```markdown
## Global Bypass

To skip all hooks for a single commit (emergency only):
```bash
LEFTHOOK=0 git commit -m "chore: emergency fix"
```

This uses lefthook's standard bypass mechanism — no `--no-verify` needed.
```

With:
```markdown
## Global Bypass

To skip all hooks for a single commit (emergency only):
```bash
git commit --no-verify -m "chore: emergency fix"
```

To skip specific hooks only:
```bash
SKIP=lint,test git commit -m "chore: skip lint and test for this commit"
```
```

- [ ] **Step 6: Verify**

Read `skills/setup-new-project/SKILL.md` — confirm no lefthook references remain. Steps use uv/uvx and pre-commit.

- [ ] **Step 7: Commit**

```bash
git add skills/setup-new-project/SKILL.md
git commit -m "feat(setup-new-project): migrate from lefthook to pre-commit (uvx)"
```

---

### Task 10: Update `skills/use-worktree/SKILL.md` — add pre-commit install step

**Files:**
- Modify: `skills/use-worktree/SKILL.md`

- [ ] **Step 1: Add hook install step after auto-setup block**

The skill's Creation section ends with an auto-detect setup block. After it (before `## Baseline Verification`), add:

```markdown
## Install git hooks

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```
```

- [ ] **Step 2: Verify**

Read `skills/use-worktree/SKILL.md` — confirm hook install step is present before Baseline Verification.

- [ ] **Step 3: Commit**

```bash
git add skills/use-worktree/SKILL.md
git commit -m "feat(use-worktree): install pre-commit hooks after worktree creation"
```

---

### Task 11: Unset `core.hooksPath` and install pre-commit hooks

This task applies the migration to the current repo.

- [ ] **Step 1: Unset the leftover git config**

```bash
git config --unset core.hooksPath
```

- [ ] **Step 2: Install pre-commit hooks**

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```

- [ ] **Step 3: Verify commit-msg hook**

```bash
echo "bad commit message" | bunx commitlint
# Expected: exit 1 with error
echo "feat: add test" | bunx commitlint
# Expected: exit 0
```

- [ ] **Step 4: Verify pre-commit hook**

```bash
uvx pre-commit run --all-files
# Expected: lint/format/test skipped (no scripts found), exit 0
```

---

## Verification

After all tasks complete:

1. `git log --oneline -10` — confirm 10 focused commits
2. `grep -r "EnterPlanMode\|ExitPlanMode" skills/specify skills/plan` — expect no matches
3. `grep -r "EnterPlanMode\|ExitPlanMode" skills/write-test skills/implement skills/verify` — expect matches
4. `grep "sync-working-status" skills/write-test/SKILL.md skills/implement/SKILL.md skills/verify/SKILL.md` — expect 1 match per file
5. `cat .pre-commit-config.yaml` — confirm file exists with 4 hooks
6. `ls lefthook.yml` — expect: No such file
7. `uvx pre-commit run --all-files` — expect: hooks run, exit 0
8. `echo "bad" | bunx commitlint` — expect: exit 1
