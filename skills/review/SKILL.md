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

Use the **track-tasks** capability filtered by prefix `review:`. If open tasks exist from a prior session:
- Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
- If no open tasks: proceed directly

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Step Schedule

Step 1 delegates to `hexis:verify`, which manages its own tasks. Steps 2–4:

| Step | On Start | On Done |
|---|---|---|
| Step 2: Collect git SHAs | **track-tasks**: create "review: collect git SHAs" → mark in_progress | mark completed |
| Step 3: Principles review | **track-tasks**: create "review: principles review" → mark in_progress | mark completed |
| Step 4: Handle results | **track-tasks**: create "review: handle results" → mark in_progress | mark completed |

### On Failure or Abort

Use **track-tasks** to stop the current open task.

## When to Review

**Required:**
- Before merging to main
- After completing a major feature

**Recommended:**
- After each task in subagent-driven development
- When stuck (fresh perspective)

## Process

### Step 1: Verify first

Run `hexis:verify`. Do not proceed if it fails.

### Step 2: Collect git SHAs

```bash
BASE_SHA=$(git merge-base HEAD main)
HEAD_SHA=$(git rev-parse HEAD)
```

### Step 3: Run principles-reviewer

Use the **spawn-subagent** capability to run the `hexis:principles-reviewer` agent (see `hexis:platform-capabilities`). If **spawn-subagent** is unavailable, run the principles review sequentially in the current context.
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
- Spec or plan files in the diff that don't follow `docs/templates/spec.md` / `docs/templates/plan.md`
