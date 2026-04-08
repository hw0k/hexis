# Skill Integration Gate

Issue: #23

Decomposed from: #21

## What

Add a `## CLI Integration Gate` section to each hw0k-workflow skill. Each gate runs `hw0k status read` at skill entry and acts based on CLI output — replacing LLM-driven state judgment with deterministic, file-based state reporting.

## Prerequisite

Depends on #22 (hw0k CLI tool). The command surface and output format defined in that spec are the interface this spec consumes.

## Gate Behavior (Universal)

At the gate entry point in each skill:

1. Run `hw0k status read <issue>` (optionally `--json`)
2. Read the `STATE: <LABEL>` from stdout (plain text) or `state` key (JSON)
3. If the state matches the required label(s): proceed with the skill
4. If the state does not match: output the full CLI stdout verbatim, then stop — do not proceed, do not override

The LLM does not interpret state independently. CLI output is authoritative.

## Per-Skill Gate Definitions

### `dispatch`

**Gate position:** Replaces Step 1b's grep-based file detection.

**Command:** `hw0k status read <issue> --json`

**Routing table (replaces current Rule 2–4):**

| STATE label | Action |
|---|---|
| `NEEDS_SPEC` | Invoke `hw0k-workflow:specify` |
| `NEEDS_PLAN` | Invoke `hw0k-workflow:plan` |
| `IN_PROGRESS` | Invoke `hw0k-workflow:implement` |
| `NEEDS_VERIFY` | Invoke `hw0k-workflow:verify` |
| `DONE` | Output "Issue #N is complete." Stop. |

Rules 1 (uncommitted changes) and 5–8 (PR state) remain unchanged — they still use `git`/`gh`. After `DONE`, `dispatch` checks PR state to route to `review` or `finish` if the PR is still open.

### `specify`

**Gate position:** At skill start, before creating or editing any file.

**Command:** `hw0k status read <issue>`

**Logic:**
- If state is `NEEDS_SPEC`: proceed — this is the expected entry state
- If state is NOT `NEEDS_SPEC` (spec already exists): surface CLI output to user; ask for explicit confirmation before overwriting

### `plan`

**Gate position:** At skill start, before any planning work.

**Command:** `hw0k status read <issue>`

**Logic:**
- If state is `NEEDS_PLAN`: proceed
- Otherwise: surface CLI output verbatim; stop

### `write-test` and `implement`

**Gate position:** At skill start.

**Command:** `hw0k status read <issue>`

**Logic:**
- If state is `IN_PROGRESS`: proceed
- Otherwise: surface CLI output verbatim; stop

### `verify`

**Gate position — entry:** At skill start, before running any verification commands.

**Command:** `hw0k status read <issue> --json`

**Logic:**
- If state is `NEEDS_VERIFY`: proceed — also surface the `done_when` array to the user so they know which AC items need verification
- If state is `IN_PROGRESS`: surface blocking plan tasks from CLI output; stop — implement must complete first
- Otherwise: surface CLI output verbatim; stop

**Gate position — exit:** After all verification work is complete.

**Command:** `hw0k status update <issue> --checked <indices> --unchecked <indices>`

**Logic:** LLM reads the `done_when` indices from the entry `read` output, determines which items have been satisfied, and calls `update` once with the complete AC state. Outputs the new state.

### `finish`

**Gate position — entry:** At skill start, before any commit/PR/merge work.

**Command:** `hw0k status read <issue>`

**Logic:**
- If state is `DONE`: proceed
- Otherwise: surface CLI output verbatim; stop

## Affected Files

| File | Change |
|---|---|
| `skills/dispatch/SKILL.md` | Replace Step 1b grep logic with `hw0k status read` routing; remove `READY_TO_MERGE` from routing table |
| `skills/specify/SKILL.md` | Add `## CLI Integration Gate` section |
| `skills/plan/SKILL.md` | Add `## CLI Integration Gate` section |
| `skills/write-test/SKILL.md` | Add `## CLI Integration Gate` section |
| `skills/implement/SKILL.md` | Add `## CLI Integration Gate` section |
| `skills/verify/SKILL.md` | Add `## CLI Integration Gate` section (entry + exit gates) |
| `skills/finish/SKILL.md` | Add `## CLI Integration Gate` section |

## Out of Scope

- Modifying skill process logic beyond the gate sections
- Updating `sync-working-status`, `debug`, `review`, `receive-review` (no file-based state gates needed)
- Adding tests for skill files (they are instructions, not code)

## Done When

- [ ] `dispatch` routes via `hw0k status read` output for all 5 state labels
- [ ] `specify` gate runs `hw0k status read` and blocks overwrite of existing spec without confirmation
- [ ] `plan` gate runs `hw0k status read` and blocks on non-`NEEDS_PLAN` state
- [ ] `write-test` and `implement` gates run `hw0k status read` and block on non-`IN_PROGRESS` state
- [ ] `verify` entry gate runs `hw0k status read` and blocks on non-`NEEDS_VERIFY` state
- [ ] `verify` exit gate runs `hw0k status update` with complete AC state after verification
- [ ] `finish` gate runs `hw0k status read` at entry and blocks on non-`DONE` state
