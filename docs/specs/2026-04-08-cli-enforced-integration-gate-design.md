# CLI-Enforced Integration Gate

Issue: #21

## Problem

hw0k-workflow skills rely on LLM judgment to determine workflow state: whether a spec exists, whether a plan is complete, whether verify has passed. This creates inconsistency — different sessions, models, or context windows may reach different conclusions about the current workflow stage.

## What

A custom CLI tool that reads spec and plan files as the authoritative Source of Truth for workflow state. Each hw0k-workflow skill adds a **CLI Integration Gate** — a step that runs CLI commands and acts based on their output. The LLM does not judge state independently; it reads CLI output and acts on it.

## Custom CLI

A new command-line tool (language TBD — Python/uv is the leading candidate) with the following command surface:

| Command | Purpose |
|---|---|
| `hw0k status init <issue>` | Initialize tracking for issue N — locate spec/plan files, register AC items |
| `hw0k status check <issue>` | Parse spec/plan files, report current state and blockers |
| `hw0k status merge <issue>` | Mark issue as complete (post-merge state update) |

The CLI is **stateless** — it recomputes state by parsing files on each invocation. No persistent state file.

### Output Format

Structured output (exact schema TBD — JSON or human+machine-readable plaintext). Each command outputs:

- **Current state label** — one of: `NEEDS_SPEC`, `NEEDS_PLAN`, `IN_PROGRESS`, `NEEDS_VERIFY`, `READY_TO_MERGE`, `DONE`
- **Blocking items** — list of what is missing or incomplete
- **Satisfied items** — list of what is already fulfilled

Exit code: `0` = state is valid and unblocked, non-zero = blocked or error.

### State Determination Logic

The CLI derives state from two file types, both scanned in `docs/specs/` and `docs/plans/`:

**Spec file** — any `docs/specs/*.md` containing `Issue: #N` in the first 10 lines:
- Presence: spec exists for this issue
- `## Done When` section: AC checklist items (`- [ ]` = open, `- [x]` = satisfied)

**Plan file** — any `docs/plans/*.md` containing `Issue: #N` in the first 10 lines or in `linked_spec` frontmatter (resolved to match spec's issue):
- Presence: plan exists for this issue
- Task checklists (`- [ ]` / `- [x]`) anywhere in the file body

State transition table:

| Condition | State |
|---|---|
| No spec file found | `NEEDS_SPEC` |
| Spec found, no plan file found | `NEEDS_PLAN` |
| Plan found, any plan task unchecked | `IN_PROGRESS` |
| All plan tasks checked, `## Done When` AC not all satisfied | `NEEDS_VERIFY` |
| All plan tasks checked, all AC satisfied | `READY_TO_MERGE` |
| `status merge` has been called | `DONE` |

Note: "all AC satisfied" means all `- [ ]` items under `## Done When` in the spec have been converted to `- [x]`. This is the human/LLM responsibility to update; the CLI only reads it.

## CLI Integration Gates

Each skill adds a **`## CLI Integration Gate`** section specifying which command(s) to run and what state is required to proceed:

| Skill | Gate Command | Required State to Proceed |
|---|---|---|
| `dispatch` | `status check <issue>` | Any — output determines which skill to invoke |
| `plan` | `status check <issue>` | `NEEDS_PLAN` (spec with Done When must exist) |
| `write-test` / `implement` | `status check <issue>` | `IN_PROGRESS` or `NEEDS_VERIFY` (plan must exist) |
| `verify` | `status check <issue>` | `NEEDS_VERIFY` (all plan tasks complete) |
| `finish` | `status check <issue>` | `READY_TO_MERGE` |
| `specify` | `status init <issue>` | N/A — creates the spec, then outputs `NEEDS_PLAN` |

**LLM behavior at each gate:**
1. Run the CLI command with the target issue number
2. Read stdout
3. If required state matches: proceed with the skill
4. If required state does not match: surface CLI output verbatim to the user; do not proceed

## Out of Scope

- GitHub API calls from the CLI (local file parsing only — no `gh` calls)
- LLM interpretation of workflow state (CLI is authoritative)
- Test execution, code compilation, or any process execution
- Network calls of any kind from the CLI
- Persistent state files (CLI recomputes on every call)

## Done When

- [ ] Custom CLI tool is designed with final command surface and output schema
- [ ] State determination logic is fully specified for all stages
- [ ] `status init`, `status check`, and `status merge` are implemented and tested
- [ ] CLI is installable without global system dependencies (e.g., via `uv tool install`)
- [ ] CLI Integration Gate instructions are added to all affected skills
- [ ] `dispatch` uses `status check` output as the primary routing signal
