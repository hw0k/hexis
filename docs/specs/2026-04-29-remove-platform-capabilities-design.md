---
issue: 32
status: READY_TO_PLAN
checks:
  - item: "`skills/platform-capabilities/` directory does not exist"
    done: false
  - item: "No skill file contains bold capability names: **ask-user**, **track-tasks**, **spawn-subagent**, **plan-mode**"
    done: false
  - item: "No skill file contains `hexis:platform-capabilities` references"
    done: false
  - item: "No skill file contains explicit fallback notes for capability unavailability"
    done: false
  - item: "Task Tracking sections are removed from all skill files that had them"
    done: false
---

# Remove Platform-Capabilities Abstraction

## Problem

The `platform-capabilities` skill defines an abstraction layer where bold capability names
(`**ask-user**`, `**track-tasks**`, `**spawn-subagent**`, `**plan-mode**`, `**worktree**`)
in skill files map to platform-specific tool implementations via a lookup table.

The table is entirely TBD — no platform column has ever been filled. The underlying
assumption is that frontier models cannot determine appropriate tools on their own. This
assumption is incorrect. The abstraction layer adds maintenance overhead (manual table
updates per platform) without providing value.

## Goal

Remove the capability abstraction layer. Skill files describe what needs to happen in
natural language, trusting the model to select appropriate tools. The `platform-capabilities`
skill is deleted entirely.

## Changes

### 1. Delete `skills/platform-capabilities/`

Remove the directory and all its contents. Remove `hexis:platform-capabilities` from
`agents/principles-reviewer.md` scope if listed.

### 2. Replace capability references in all affected skills

For each skill file, apply the following conversion rules:

| Capability | Replacement |
|---|---|
| `**ask-user**` | Ask the question directly in natural language. E.g., "Ask the user: '...?'" |
| `**track-tasks**` | Remove. Session state tracking is deferred to #23. |
| `**spawn-subagent**` | Describe the intent inline. E.g., "Delegate each task to a subagent" or "Run the `hexis:principles-reviewer` agent" |
| `**plan-mode**` | "Present a plan and get user approval before proceeding" |
| `**worktree**` capability references | Remove. The `hexis:use-worktree` skill handles worktree setup. |

Remove all `(see hexis:platform-capabilities)` references alongside the capability names.

### 3. Remove all explicit fallback notes

Delete lines of the form "If **X** is unavailable, …". The model handles unavailable
tools at its own discretion.

### 4. Remove Task Tracking sections

The "Task Tracking" section present in `specify`, `plan`, `implement`, `verify`,
`review`, and `finish` is driven by `**track-tasks**`. Remove these sections entirely.

**Session state tracking note:** The "Resume vs Start fresh" behavior (checking prior
open tasks at session start) is owned by #23 (CLI Integration Gate). Until #23 lands,
models handle cross-session state recovery at their discretion.

## Affected Files

- `skills/platform-capabilities/` — delete
- `skills/specify/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/review/SKILL.md`
- `skills/finish/SKILL.md`
- `skills/dispatch/SKILL.md`
- `skills/use-worktree/SKILL.md`
- `skills/receive-review/SKILL.md`

## Out of Scope

- Defining canonical natural language per capability type (determined per-skill during implementation)
- Session state tracking and "Resume vs Start fresh" logic — owned by #23
- `setup-new-project/SKILL.md` changes (on hold)
- Changes to `agents/`, `tests/`, or `docs/` structure beyond the capability skill deletion
