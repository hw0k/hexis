---
issue: 22
status: READY_TO_PLAN
checks:
  - item: '`hexis status read <issue>` outputs correct STATE label for all 5 states'
    done: true
  - item: '`hexis status read <issue> --json` outputs valid JSON with correct `state`
      key and `checks` array with indices'
    done: true
  - item: '`hexis status update <issue> --checked <indices> --unchecked <indices>`
      rewrites all Checks items atomically'
    done: true
  - item: Incomplete or overlapping index coverage exits 1 with an error message
    done: true
  - item: All state transitions are covered by pytest unit tests
    done: true
  - item: '`uv tool install ./cli` succeeds in a clean environment'
    done: true
  - item: CLI handles missing `docs/` directory gracefully (outputs `NEEDS_SPEC`,
      exit 0)
    done: true
---

# hexis CLI Tool

Decomposed from: #21

## What

A stateless Python CLI tool (`hexis`) that reads `docs/specs/` and `docs/plans/` files to determine and report workflow state for a given issue number. State is always derived from current file content — no caching, no marker files, no persistent state. All judgment about workflow state is made by the CLI — not the LLM.

## Commands

| Command | Behavior |
|---|---|
| `hexis status read <issue>` | Parse spec/plan files; report state label, plan task progress, and indexed AC items |
| `hexis status update <issue> --checked <indices> --unchecked <indices>` | Bulk-set all Checks items in one write — last-write-wins, all indices must be covered |

All commands accept `--json` for machine-readable output and `--root <path>` to specify the project root (defaults to current working directory).

## Output Format

### Plain text (default)

First line is always:

```
STATE: <LABEL>
```

Where `<LABEL>` is exactly one of: `NEEDS_SPEC`, `NEEDS_PLAN`, `IN_PROGRESS`, `NEEDS_VERIFY`, `DONE`

Full `status read` example:

```
STATE: NEEDS_VERIFY
ISSUE: 21
DEPENDS ON: (none)

PLAN TASKS: 4/4 complete

CHECKS:
  [x] #0  Custom CLI tool designed with final command surface
  [ ] #1  All state transitions covered by pytest unit tests
  [ ] #2  uv tool install succeeds in a clean environment
  [x] #3  CLI handles missing docs/ directory gracefully
```

When state is `NEEDS_SPEC` or `NEEDS_PLAN`, only the STATE/ISSUE/DEPENDS ON lines and a BLOCKING reason are shown:

```
STATE: NEEDS_PLAN
ISSUE: 23
DEPENDS ON: #22

BLOCKING:
  No plan file found in docs/plans/ for issue #23
```

### JSON output (`--json`)

```json
{
  "state": "NEEDS_VERIFY",
  "issue": 21,
  "depends_on": [],
  "plan_tasks": { "complete": 4, "total": 4 },
  "checks": [
    { "index": 0, "text": "Custom CLI tool designed with final command surface", "checked": true },
    { "index": 1, "text": "All state transitions covered by pytest unit tests", "checked": false },
    { "index": 2, "text": "uv tool install succeeds in a clean environment", "checked": false },
    { "index": 3, "text": "CLI handles missing docs/ directory gracefully", "checked": true }
  ],
  "blocking": []
}
```

The `STATE:` first-line convention applies to plain text only. In JSON mode the `state` key is authoritative.

Exit codes: `0` = success, `1` = usage/argument error, `2` = parse error (malformed file)

## State Determination Logic

The CLI scans `docs/specs/` and `docs/plans/` relative to the project root. State is computed fresh on every invocation.

**Finding a spec file:** Any `docs/specs/*.md` file whose YAML frontmatter `issue:` field equals `N`. If more than one file matches, exit code 2 with an error message to stderr.

**Finding a plan file:** Any `docs/plans/*.md` file whose YAML frontmatter `issue:` field equals `N`. If more than one file matches, exit code 2 with an error message to stderr.

**Parsing spec depends_on:** Read the `depends_on:` YAML frontmatter field if present. Value is a list of bare issue numbers (integers). Absent or empty means no dependencies. Surfaced in output as-is; not used in state determination.

**Parsing spec Checks:** Read the `checks:` YAML frontmatter array. Each entry is an object with `item` (string) and `done` (boolean). Items are zero-indexed in the order they appear.

**Parsing plan tasks:** Extract all checklist items (`- [ ]` or `- [x]`) anywhere in the plan file body (excluding YAML frontmatter).

**State transition table:**

| Condition | State |
|---|---|
| No spec file found | `NEEDS_SPEC` |
| Spec found, no plan file found | `NEEDS_PLAN` |
| Plan found, any plan task item is `[ ]` | `IN_PROGRESS` |
| All plan tasks `[x]`, any Checks item has `done: false` | `NEEDS_VERIFY` |
| All plan tasks `[x]`, all Checks items have `done: true` | `DONE` |

Conditions are evaluated in order. The first match determines the state.

## `status update` Behavior

A bulk, last-write-wins command. Accepts `--checked <indices>` and `--unchecked <indices>`, where each is a comma-separated list of 0-based indices (as shown in `status read` output). Together, the two lists must cover every AC item index exactly once — no gaps, no duplicates. If coverage is incomplete or overlapping: exit code 1, error message to stderr.

```bash
# 4 AC items: set #0 and #3 as done, #1 and #2 as not done
hexis status update 21 --checked 0,3 --unchecked 1,2
```

The entire `checks:` frontmatter array is rewritten atomically from this single call. One call replaces all Checks item states — no sequential per-index calls required.

Outputs the new state after writing (same format as `status read`).

`status update` modifies **only** the `checks:` frontmatter field in the spec file. Plan task items are read-only from the CLI's perspective.

## Package Layout

```
cli/
  pyproject.toml
  src/
    hexis/
      __init__.py
      cli.py          # Typer app, command definitions
      parser.py       # MultipleMatchError, Check, PlanTasks; find_spec_file, find_plan_file, parse_frontmatter, parse_checks, parse_depends_on, parse_plan_tasks, write_checks
      state.py        # State, StateResult, determine_state
  tests/
    test_parser.py
    test_state.py
    test_cli.py
```

Lives in the `cli/` subdirectory of the hexis repository.

## Technology

- Python ≥ 3.11
- `typer` (CLI framework, includes `rich`)
- `pyyaml` (YAML frontmatter parsing)
- `pytest` (test runner)
- Managed with `uv`; installable via `uv tool install ./cli`

## Out of Scope

- GitHub API calls (no `gh` invocations)
- Test execution or code analysis
- Network calls of any kind
- Persistent state of any kind (no marker files, no database)
- Modifying plan task checklist items (plan tasks are read-only from the CLI)
