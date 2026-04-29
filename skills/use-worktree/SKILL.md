---
name: use-worktree
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans
type: workflow
---

# Use Worktree

## Overview

Set up an isolated git worktree for feature work.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

## Directory Selection

Follow this priority order:

### 1. Check for Existing Directory

```bash
ls -d .worktrees 2>/dev/null
ls -d worktrees 2>/dev/null
```

If found, use it. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

If a preference is specified, use it.

### 3. Ask the User

If neither of the above applies, ask the user:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/hw0k/worktrees/<project-name>/ (global)
```

## Safety Verification

For project-local directories (`.worktrees` or `worktrees`), verify gitignore before creating:

```bash
git check-ignore -q .worktrees 2>/dev/null || echo "NOT IGNORED"
```

**If not ignored:** Add to `.gitignore` and commit, then proceed with worktree creation.

Global directories (`~/.config/hw0k/worktrees`) do not need verification.

## Creation

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

Auto-detect and run project setup:

```bash
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f go.mod ] && go mod download
```

## Install git hooks

```bash
uvx pre-commit install
uvx pre-commit install --hook-type commit-msg
```

## Baseline Verification

```bash
<project test command>
```

If tests fail: report failures and ask whether to proceed or investigate.

## Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Red Flags

**Never:**
- Create project-local worktree without verifying gitignore
- Proceed without baseline test verification
- Assume directory location — always follow the priority order

**Always:**
- Ask the user for directory selection when no config exists
