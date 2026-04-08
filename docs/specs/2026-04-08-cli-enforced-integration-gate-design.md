# CLI-Enforced Integration Gate

Issue: #21

> **Superseded.** Decomposed into: [hw0k CLI Tool](2026-04-08-hw0k-cli-tool-design.md) (#22), [Skill Integration Gate](2026-04-08-skill-integration-gate-design.md) (#23)

## Problem

hw0k-workflow skills rely on LLM judgment to determine workflow state: whether a spec exists, whether a plan is complete, whether verify has passed. This creates inconsistency — different sessions, models, or context windows may reach different conclusions about the current workflow stage.

## What

A custom CLI tool that reads spec and plan files as the authoritative Source of Truth for workflow state. Each hw0k-workflow skill adds a **CLI Integration Gate** — a step that runs CLI commands and acts based on their output. The LLM does not judge state independently; it reads CLI output and acts on it.

## Custom CLI

A new command-line tool (Python/uv) with the following command surface:

| Command | Purpose |
|---|---|
| `hw0k status read <issue>` | Parse spec/plan files; report state label and indexed Done When AC items |
| `hw0k status update <issue> --checked <indices> --unchecked <indices>` | Bulk-set all Done When AC items in one write (last-write-wins) |

The CLI is **stateless** — it recomputes state by parsing files on every invocation. No persistent state, no marker files.

All commands accept `--json` for machine-readable output.

### State Labels

`NEEDS_SPEC` → `NEEDS_PLAN` → `IN_PROGRESS` → `NEEDS_VERIFY` → `DONE`

`DONE` is reached when all plan tasks and all Done When AC items are checked. No explicit "done" marker command — state is always derived from file content.

### Output Format

Plain text: first line is always `STATE: <LABEL>`. JSON: `{ "state": "...", "issue": N, ... }`.

Done When AC items are output with zero-based indices so `status update` can reference them by position.

## CLI Integration Gates

Each skill adds a `## CLI Integration Gate` section. The LLM runs `hw0k status read <issue>` at entry and acts on the `STATE` output:

| Skill | Required Entry State | Exit Action |
|---|---|---|
| `dispatch` | Any — routes based on state label | — |
| `specify` | `NEEDS_SPEC` (warns if spec exists) | — |
| `plan` | `NEEDS_PLAN` | — |
| `write-test` / `implement` | `IN_PROGRESS` | — |
| `verify` | `NEEDS_VERIFY` | `hw0k status update` with complete AC state |
| `finish` | `DONE` | — |

## Out of Scope

- GitHub API calls from the CLI
- LLM interpretation of workflow state
- Persistent state files

## Done When

> See decomposed specs: [#22](2026-04-08-hw0k-cli-tool-design.md), [#23](2026-04-08-skill-integration-gate-design.md)
