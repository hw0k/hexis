---
status: DONE
checks:
  - item: "All three skills (`write-test`, `implement`, `verify`) include a `sync-working-status` invocation at their completion stage"
    done: true
---

# Sync Working Status in Executing Task Skills

## Problem

After `write-test`, `implement`, and `verify` complete, work state is not immediately reflected. Subsequent agents or humans may not have an accurate picture of current progress.

## What

Add an `hw0k-workflow:sync-working-status` invocation at the completion stage of each executing task skill.

**Files to update:**
- `skills/write-test/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/verify/SKILL.md`

## Timing

| Skill | Trigger Point |
|---|---|
| `write-test` | After pre-completion checklist passes |
| `implement` | After all tasks complete, before invoking `hw0k-workflow:finish` |
| `verify` | After verification evidence is cited, before claiming completion |

## Rationale

Executing skills produce real work (code, commits). Syncing state at the point of completion ensures future agents and humans have accurate context.

## Out of Scope

- No changes to the `sync-working-status` skill itself
- No additions to `specify`, `plan`, `debug`, or other non-executing skills
