---
name: review
description: Use when completing a task or feature — triggers principles review before merge
type: workflow
---

# Review

## Overview

Catch principle violations and quality issues before merge.

**Core principle:** Review is the last gate before merge.

## $ARGUMENTS

If `$ARGUMENTS` contains a PR number or scope description, use it. Otherwise infer from current branch/changes.

## Task Tracking

### On Start

Call `TaskList` filtered by prefix `review:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

Step 1 delegates to `hw0k-workflow:verify`, which manages its own Tasks. Steps 2–4:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Collect git SHAs | `TaskCreate("review: collect git SHAs")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 3: Principles review | `TaskCreate("review: principles review")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Step 4: Handle results | `TaskCreate("review: handle results")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.

## When to Review

**Required:**
- Before merging to main
- After completing a major feature

**Recommended:**
- After each task in subagent-driven development
- When stuck (fresh perspective)

## Process

### Step 1: Verify first

Run `hw0k-workflow:verify`. Do not proceed if it fails.

### Step 2: Collect git SHAs

```bash
BASE_SHA=$(git merge-base HEAD main)
HEAD_SHA=$(git rev-parse HEAD)
```

### Step 3: Run principles-reviewer

Run the `hw0k-workflow:principles-reviewer` agent:
- Changed files: `git diff --name-only $BASE_SHA $HEAD_SHA`
- Scope: the implementation delivered

### Step 4: Handle results

- Core principle violations: must fix before merge
- Other violations: handle by severity
- If reviewer is wrong: push back with technical justification

## Red Flags

**Never:**
- Request review while verify is failing
- Ignore principle violations
- Skip review because "it's simple"
