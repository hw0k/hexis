---
name: implement
description: Use when you have a written implementation plan — defaults to subagent-driven execution, falls back to inline only when justified
type: workflow
---

# Implement

## Overview

Execute an implementation plan. Default: dispatch subagents per task. Inline execution only when there is a clear reason not to.

## $ARGUMENTS

If `$ARGUMENTS` is a plan file path, load that file. Otherwise ask the user for the plan file path.

## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Plan spans multiple files with cross-task dependencies
- Execution approach is unclear (inline vs. subagent decision is non-obvious)
- Architectural or structural decisions required

**Complex task** → present a plan and get user approval before writing any code.
**Simple task** → proceed directly.

## Process

### Step 0: Branch Check

Check the current branch. If it is `main` or `master`, ask the user whether to proceed on this branch or switch to a feature branch. Do not proceed until the user explicitly confirms. This check is mandatory even if the user invoked the skill directly.

### Step 1: Load and Review

1. Read the plan file
2. Review critically — raise questions or concerns before starting
3. Assess execution mode (Step 2)

### Step 2: Choose Execution Mode

**Default: dispatch a subagent per task.**

Inline execution is only justified when ALL of the following apply:
- The plan has 3 or fewer tasks
- Each task is a single, self-contained change with no cross-task dependencies
- No intermediate review between tasks is needed

If any condition is unmet, use subagents. State the reason if choosing inline.

### Step 3: Subagent Path

Dispatch a subagent for each task.

**Parallel dispatch rule:** Tasks with no dependencies on each other MUST be dispatched in a single message — all subagent dispatches in one response. Dispatching task A, waiting for the result, then dispatching task B is sequential regardless of what the surrounding text says. To dispatch N tasks in parallel: compose all N prompts first, then emit all N subagent dispatches in one message. Only dispatch the next task after a prior task completes when a data dependency exists (e.g., task B needs output from task A).

### Step 4: Inline Path (exception only)

For each task:
1. Follow each step exactly as written
2. Run verifications as specified
3. Stop if blocked — report and wait

After all tasks done, invoke `hexis:sync-working-status`. Then invoke `hexis:finish`.

## When to Stop

Stop immediately and ask:
- Blocker (missing dependency, test fails repeatedly, unclear instruction)
- Plan has critical gaps preventing start
- Verification fails repeatedly

Don't guess. Stop and ask.

## Notes

- Never start implementation on main/master without explicit user confirmation — enforced by Step 0
- For tasks marked `[TDD]`, follow the Red-Green-Refactor cycle from `hexis:testing-principles`. The failing test must be seen to fail before writing implementation code.
