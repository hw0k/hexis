---
name: implement
description: Use when you have a written implementation plan — defaults to subagent-driven execution, falls back to inline only when justified
type: workflow
---

# Implement

## Overview

Execute an implementation plan. Default: dispatch subagents per task. Inline execution only when there is a clear reason not to.

## $ARGUMENTS

If `$ARGUMENTS` is a plan file path, load that file. Otherwise use the **ask-user** capability to ask for the path (see `hexis:platform-capabilities`).

## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Plan spans multiple files with cross-task dependencies
- Execution approach is unclear (inline vs. subagent decision is non-obvious)
- Architectural or structural decisions required

**Complex task** → use the **plan-mode** capability. Review the plan, clarify execution strategy, get approval before writing any code (see `hexis:platform-capabilities`).
**Simple task** → proceed directly.

## Task Tracking

### On Start

1. Use the **track-tasks** capability filtered by prefix `implement:`. If open tasks exist from a prior session:
   - Use the **ask-user** capability: **Resume** (verify state of last open task) or **Start fresh** (stop all open tasks)
2. **track-tasks**: create "implement: execute plan <plan-filename>" → mark in_progress (parent task — created regardless of subagent or inline path)

> **Fallbacks:** If **track-tasks** is unavailable, maintain a markdown checklist in the current response. If **ask-user** is unavailable, output the question inline and wait for the next message.

### Subagent Path

Before dispatching each subagent:
- Use **track-tasks** filtered by prefix `implement/task-`. Confirm the prior task (if any) shows completed before dispatching the next.
- Instruct each dispatched subagent to use **track-tasks**: create "implement/task-N: <task-name>" → mark in_progress at start; mark completed on success; stop on failure. Use `N` and task name from the plan.
- After reviewing each subagent's output: update the parent task with a progress note.

### Inline Path

**track-tasks**: create task before the existing update in Step 4 (see below).

### On All Tasks Complete

Use **track-tasks** to mark the parent task completed.

### On Failure or Abort

Use **track-tasks** to stop the current open task and the parent task.

## Process

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

Use the **spawn-subagent** capability for each task (see `hexis:platform-capabilities`). If **spawn-subagent** is unavailable, use the Inline Path instead.

**Parallel dispatch rule:** Tasks with no dependencies on each other MUST be dispatched in a single message — all spawn-subagent calls in one response. Dispatching task A, waiting for the result, then dispatching task B is sequential regardless of what the surrounding text says. To dispatch N tasks in parallel: compose all N prompts first, then emit all N spawn-subagent calls in one message. Only dispatch the next task after a prior task completes when a data dependency exists (e.g., task B needs output from task A).

### Step 4: Inline Path (exception only)

For each task:
1. TaskCreate("implement/task-N: <task-name>") → TaskUpdate(in_progress)
2. Follow each step exactly as written
3. Run verifications as specified
4. TaskUpdate(completed)
5. Stop if blocked — report and wait

After all tasks done, invoke `hexis:sync-working-status`. Then invoke `hexis:finish`.

## When to Stop

Stop immediately and ask:
- Blocker (missing dependency, test fails repeatedly, unclear instruction)
- Plan has critical gaps preventing start
- Verification fails repeatedly

Don't guess. Stop and ask.

## Notes

- Never start implementation on main/master without explicit user consent
