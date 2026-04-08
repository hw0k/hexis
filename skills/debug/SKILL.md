---
name: debug
description: Use when encountering any bug, test failure, or unexpected behavior — before proposing fixes
type: workflow
---

# Debug

## Overview

Random fixes waste time and create new bugs.

**Core principle:** Always find the root cause before fixing. Fixing symptoms is failure.

## $ARGUMENTS

If `$ARGUMENTS` contains an error message, stack trace, or symptom description, use it as Phase 1 input. Otherwise use `AskUserQuestion` to collect it.

## Task Tracking

### On Start

Call `TaskList` filtered by prefix `debug:`. If open Tasks exist from a prior session:
- Use `AskUserQuestion`: **Resume** (use `TaskGet` to verify state, continue from the last open phase) or **Start fresh** (call `TaskStop` on all open Tasks)
- If no open Tasks: proceed directly

### Step Schedule

| Phase | On Start | On Done |
|---|---|---|
| Phase 1: Root Cause Investigation | `TaskCreate("debug: root cause investigation")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 2: Pattern Analysis | `TaskCreate("debug: pattern analysis")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 3: Hypotheses and Verification | `TaskCreate("debug: hypotheses and verification")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |
| Phase 4: Implementation | `TaskCreate("debug: fix implementation")` → `TaskUpdate(in_progress)` | `TaskUpdate(completed)` |

### On Failure or Abort

Call `TaskStop` on the current open Task.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Do not propose any fix before Phase 1 is complete.

## Phase 1: Root Cause Investigation

**Before attempting any fix:**

1. **Read the error completely** — do not skip. Full stack trace, line numbers, file paths, error codes.

2. **Reproduce consistently** — exact steps to reproduce. If unreproducible → do not guess, collect more data.

3. **Check recent changes** — `git diff`, recent commits, config changes, environment differences.

4. **Collect evidence in multi-component systems** — add diagnostic logging at each component boundary, run once, identify where it breaks.

5. **Trace data flow** — where does the bad value originate? Trace upstream.

**Logging principle:** Before claiming "cannot reproduce", check existing logs. If no logs at the failure boundary, add them, run once, then form hypotheses.

## Phase 2: Pattern Analysis

Find similar working code. Compare against the reference implementation. List the differences.

## Phase 3: Hypotheses and Verification

**ultrathink** before generating the hypothesis list. Then:

1. State a single hypothesis: "I believe X is the root cause because Y."
2. Minimal change to verify the hypothesis. One at a time.
3. Verify before continuing.

**P3 requirement:** All hypothesis verification must cite tool output. "Seems fixed" is not verification. Run tests and show the output.

## Phase 4: Implementation

1. Write a failing test that reproduces the bug (`hw0k-workflow:write-test`)
2. Fix the root cause. One change.
3. Verify the fix — **cite test runner output**
4. If the fix fails 3 or more times: stop. Suspect the architecture. Discuss with the user.

## Red Flags — Stop and return to Phase 1

Stop immediately if you think:
- "Quick fix now, investigate later"
- "Let me change X and see what happens"
- "It's probably X, let me try fixing it"
- "I don't fully understand this but it might work"
- "One more fix attempt" (after 2+ failed attempts)
