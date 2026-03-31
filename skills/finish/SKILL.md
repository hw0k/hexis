---
name: finish
description: Use when implementation is complete — guides branch completion with commit, PR creation, or merge
type: workflow
---

# Finish

## Overview

Verify → commit → choose integration method → execute → clean up.

**Announce at start:** "I'm using the hw0k-workflow:finish skill to complete this work."

## $ARGUMENTS

If `$ARGUMENTS` contains a branch or feature description, use it as context.

## Process

### Step 1: Run verify

Run `hw0k-workflow:verify`. Do not proceed to Step 2 if it fails.

### Step 2: Handle uncommitted changes

If uncommitted changes exist, commit them following `hw0k-workflow:conventional-commit` rules.

### Step 3: Present options

Use `AskUserQuestion`:

```
Implementation complete. How should we integrate?

1. Merge locally into <base-branch>
2. Push and create a PR
3. Keep the branch (handle manually later)
4. Discard the work
```

### Step 4: Execute

#### Option 1: Local merge

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>
git branch -d <feature-branch>
```

#### Option 2: Push + PR

**P2 gate:** Show the exact push command and wait for explicit approval. Do not push without approval.

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
- <2–3 lines of changes>

## Test Plan
- [ ] <verification step>
EOF
)"
```

PR title and body follow `hw0k-workflow:conventional-commit` type rules.

#### Option 3: Keep

Report branch location. No further action.

#### Option 4: Discard

**Confirm first:**
```
The following will be permanently deleted:
- Branch: <name>
- Commits: <list>
- Worktree: <path> (if applicable)

Type 'discard' exactly to confirm.
```

After confirmation:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

### Step 5: Clean up worktree

For Options 1, 2, and 4:
```bash
git worktree list | grep <branch>
git worktree remove <worktree-path>
```

Option 3: keep the worktree.

## Red Flags

**Never:**
- Proceed while verify is failing
- Push without explicit approval
- Delete work without confirmation
- `--force-push` without an explicit request
