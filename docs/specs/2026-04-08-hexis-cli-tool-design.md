---
issue: 22
status: READY_TO_PLAN
checks:
  - item: "`hexis status read <issue>` outputs correct STATE label for all 5 states"
    done: false
  - item: "`hexis status read <issue> --json` outputs valid JSON with correct `state` key and `done_when` array with indices"
    done: false
  - item: "`hexis status update <issue> --checked <indices> --unchecked <indices>` rewrites all Done When items atomically"
    done: false
  - item: "Incomplete or overlapping index coverage exits 1 with an error message"
    done: false
  - item: "All state transitions are covered by pytest unit tests"
    done: false
  - item: "`uv tool install ./cli` succeeds in a clean environment"
    done: false
  - item: "CLI handles missing `docs/` directory gracefully (outputs `NEEDS_SPEC`, exit 0)"
    done: false
---

# hexis CLI Tool

Decomposed from: #21

## What

A stateless Python CLI tool (`hexis`) that reads `docs/specs/` and `docs/plans/` files to determine and report workflow state for a given issue number. State is always derived from current file content — no caching, no marker files, no persistent state. All judgment about workflow state is made by the CLI — not the LLM.

## Commands

| Command | Behavior |
|---|---|
| `hexis status read <issue>` | Parse spec/plan files; report state label, plan task progress, and indexed AC items |
| `hexis status update <issue> --checked <indices> --unchecked <indices>` | Bulk-set all Done When AC items in one write — last-write-wins, all indices must be covered |

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

PLAN TASKS: 4/4 complete

DONE WHEN (AC):
  [x] #0  Custom CLI tool designed with final command surface
  [ ] #1  All state transitions covered by pytest unit tests
  [ ] #2  uv tool install succeeds in a clean environment
  [x] #3  CLI handles missing docs/ directory gracefully
```

When state is `NEEDS_SPEC` or `NEEDS_PLAN`, only the STATE/ISSUE lines and a BLOCKING reason are shown:

```
STATE: NEEDS_PLAN
ISSUE: 21

BLOCKING:
  No plan file found in docs/plans/ for issue #21
```

### JSON output (`--json`)

```json
{
  "state": "NEEDS_VERIFY",
  "issue": 21,
  "plan_tasks": { "complete": 4, "total": 4 },
  "done_when": [
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

**Finding a spec file:** Any `docs/specs/*.md` file containing `Issue: #<N>` anywhere in the file body.

**Finding a plan file:** Any `docs/plans/*.md` file containing `Issue: #<N>` anywhere in the file body, OR whose YAML frontmatter contains a `linked_spec` key that points to a spec containing `Issue: #<N>`.

**Parsing spec Done When:** Extract all checklist items (`- [ ]` or `- [x]`) under the `## Done When` heading, up to the next `##` heading or end of file. Items are zero-indexed in the order they appear.

**Parsing plan tasks:** Extract all checklist items (`- [ ]` or `- [x]`) anywhere in the plan file body (excluding YAML frontmatter).

**State transition table:**

| Condition | State |
|---|---|
| No spec file found | `NEEDS_SPEC` |
| Spec found, no plan file found | `NEEDS_PLAN` |
| Plan found, any plan task item is `[ ]` | `IN_PROGRESS` |
| All plan tasks `[x]`, any Done When item is `[ ]` | `NEEDS_VERIFY` |
| All plan tasks `[x]`, all Done When items `[x]` | `DONE` |

Conditions are evaluated in order. The first match determines the state.

## `status update` Behavior

A bulk, last-write-wins command. Accepts `--checked <indices>` and `--unchecked <indices>`, where each is a comma-separated list of 0-based indices (as shown in `status read` output). Together, the two lists must cover every AC item index exactly once — no gaps, no duplicates. If coverage is incomplete or overlapping: exit code 1, error message to stderr.

```bash
# 4 AC items: set #0 and #3 as done, #1 and #2 as not done
hexis status update 21 --checked 0,3 --unchecked 1,2
```

The entire Done When section is rewritten atomically from this single call. One call replaces all AC item states — no sequential per-index calls required.

Outputs the new state after writing (same format as `status read`).

`status update` modifies **only** Done When (AC) items in the spec file. Plan task items are read-only from the CLI's perspective.

## Package Layout

```
cli/
  pyproject.toml
  src/
    hexis/
      __init__.py
      cli.py          # Typer app, command definitions
      parser.py       # find_spec_file, find_plan_file, parse_done_when, parse_plan_tasks
      state.py        # determine_state, StateResult
  tests/
    test_parser.py
    test_state.py
    test_cli.py
```

Lives in the `cli/` subdirectory of the hexis repository.

## Technology

- Python ≥ 3.11
- `typer` (CLI framework, includes `rich`)
- `pytest` (test runner)
- No other runtime dependencies
- Managed with `uv`; installable via `uv tool install ./cli`

## Out of Scope

- GitHub API calls (no `gh` invocations)
- Test execution or code analysis
- Network calls of any kind
- Persistent state of any kind (no marker files, no database)
- Modifying plan task checklist items (plan tasks are read-only from the CLI)
