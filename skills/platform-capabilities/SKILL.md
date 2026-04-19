---
name: platform-capabilities
description: Platform capability map — resolves abstract capability names to concrete tools for Claude Code, Codex, and Opencode
type: reference
---

# Platform Capabilities

Hexis skills reference capabilities by name rather than by platform-specific tool names. Use this reference to resolve each capability name to the concrete tool or method available on your platform.

## Capability Map

| Capability | Claude Code | Codex | Opencode | Generic fallback |
|---|---|---|---|---|
| **ask-user** — pose a question and wait for input | TBD | TBD | TBD | Output question inline in response text; wait for next message |
| **track-tasks** — record and update step progress | TBD | TBD | TBD | Inline markdown checklist in current response |
| **spawn-subagent** — delegate work to a parallel agent | TBD | TBD | TBD | Execute sequentially in current context |
| **plan-mode** — present a plan and get approval before executing | TBD | TBD | TBD | Write plan inline as numbered list; use **ask-user** for approval |
| **worktree** — isolate work in a git worktree | TBD | TBD | TBD | `git worktree add .worktrees/<branch> -b <branch>` |
| **read-file** — read a file from the filesystem | TBD | TBD | TBD | Shell `cat` |
| **edit-file** — make targeted edits to a file | TBD | TBD | TBD | Shell-based file write |
| **run-shell** — execute shell commands | TBD | TBD | TBD | Platform shell equivalent |

TBD entries in named platform columns are filled as concrete equivalents are confirmed. The generic fallback is always available.

## How to Use

When a hexis skill references a capability name in bold (e.g., **ask-user**), find that row and use the tool or method for your current platform. If your platform is not listed or the capability is TBD, use the generic fallback.
