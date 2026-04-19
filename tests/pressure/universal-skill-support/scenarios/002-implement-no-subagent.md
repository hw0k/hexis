# Scenario 002: Implement — No Subagent Dispatch

## Setup

The agent is running on a platform without the `Agent` tool (no **spawn-subagent** capability). The user wants to execute an implementation plan.

## Pressure

> Execute the plan at docs/plans/2026-04-19-universal-skill-support.md

## Expected RED Behavior (skill NOT loaded)

Agent tries to call `Agent` tool, fails, or attempts to dispatch subagents that silently do nothing. Implementation does not complete.

## Expected GREEN Behavior (skill loaded, platform-capabilities consulted)

1. Agent identifies that **spawn-subagent** capability is unavailable on this platform
2. Agent switches to inline execution path (the fallback)
3. Agent executes all tasks sequentially in the current context
4. Each task is tracked via inline markdown checklist
5. Implementation completes with all tasks checked off

## PASS Criteria

RED PASS if: agent calls `Agent` tool and errors, or dispatches zero-output subagents without falling back.

GREEN PASS if:
- [ ] Agent does not call `Agent` tool directly
- [ ] Agent explicitly states it is using inline execution due to unavailable **spawn-subagent**
- [ ] Tasks are executed sequentially in the current context
- [ ] Progress is tracked inline via markdown checklist
