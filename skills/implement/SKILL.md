---
name: implement
description: Use when you have a written implementation plan — defaults to subagent-driven execution, falls back to inline only when justified
type: workflow
---

# Implement

## Overview

Execute an implementation plan. Default: dispatch subagents per task. Inline execution only when there is a clear reason not to.

**Announce at start:** "I'm using the hw0k-workflow:implement skill to execute this plan."

## $ARGUMENTS

If `$ARGUMENTS` is a plan file path, load that file. Otherwise use `AskUserQuestion` to ask for the path.

## Complexity Check

Before starting, assess task complexity against these criteria (any one is sufficient):
- Plan spans multiple files with cross-task dependencies
- Execution approach is unclear (inline vs. subagent decision is non-obvious)
- Architectural or structural decisions required

**Complex task** → call `EnterPlanMode`. Review the plan, clarify execution strategy, get user approval via `ExitPlanMode` before writing any code.
**Simple task** → proceed directly.

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

Dispatch a subagent for each task. Review between tasks before dispatching the next.

### Step 4: Inline Path (exception only)

For each task:
1. TaskUpdate: mark in_progress
2. Follow each step exactly as written
3. Run verifications as specified
4. TaskUpdate: mark completed
5. Stop if blocked — report and wait

After all tasks done, invoke `hw0k-workflow:sync-working-status`. Then invoke `hw0k-workflow:finish`.

## When to Stop

Stop immediately and ask:
- Blocker (missing dependency, test fails repeatedly, unclear instruction)
- Plan has critical gaps preventing start
- Verification fails repeatedly

Don't guess. Stop and ask.

## Notes

- Never start implementation on main/master without explicit user consent
