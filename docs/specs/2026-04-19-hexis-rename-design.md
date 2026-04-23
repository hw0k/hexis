---
issue: 25
status: DONE
---

# Rename hw0k-workflow to hexis

## Overview

Rename all occurrences of `hw0k-workflow` to `hexis` across the repository, GitHub infrastructure, and personal config. Historical assets in `docs/` are left untouched.

## Behavior

Every string `hw0k-workflow` that appears outside `docs/` is replaced with `hexis`. This covers:

- skill invocation syntax (`hw0k-workflow:<skill>` → `hexis:<skill>`)
- the plugin name field in `.claude-plugin/plugin.json`
- the plugin log prefix in `.githooks/run-if-exists.sh`
- the escape-hatch path `.hw0k-workflow/hooks/` → `.hexis/hooks/` in `.githooks/run-if-exists.sh`
- prose references in `CLAUDE.md`, `README.md`, agent files, and test files
- the GitHub repository name
- GitHub issue bodies for #22 and #23
- personal config files (not covered by repo grep — see Out of Scope note)

## Files Changed (Repository)

### Skill frontmatter and body — 18 files

All `skills/<name>/SKILL.md` files. In each:

- Frontmatter `name: hw0k-workflow:<name>` → `name: hexis:<name>`
- Body references to `hw0k-workflow:<skill>` invocation syntax → `hexis:<skill>`

Skills: `commit-principles`, `core-principles`, `debug`, `dispatch`, `exception-and-logging-principles`, `finish`, `general-naming-principles`, `http-api-principles`, `implement`, `plan`, `receive-review`, `review`, `setup-new-project`, `specify`, `sync-working-status`, `use-worktree`, `verify`, `write-test`

### Agent files

- `agents/principles-reviewer.md` — all `hw0k-workflow:` skill references

### Config / infrastructure

- `.claude-plugin/plugin.json` — `"name": "hw0k-workflow"` → `"name": "hexis"`
- `.pre-commit-config.yaml` — comment line referencing `hw0k-workflow`
- `.githooks/run-if-exists.sh`:
  - `PLUGIN_PREFIX="[hw0k-workflow]"` → `PLUGIN_PREFIX="[hexis]"`
  - `.hw0k-workflow/hooks/` path → `.hexis/hooks/`

### Repo root

- `CLAUDE.md` — all occurrences
- `README.md` — all occurrences

### Tests

- All files under `tests/pressure/` — all occurrences

## GitHub Operations

1. **Rename repo**: `gh repo rename hexis` — renames `claude-hw0k-workflow` → `hexis`
2. **Edit issue #22**: replace all `hw0k-workflow` occurrences in issue body
3. **Edit issue #23**: replace all `hw0k-workflow` occurrences in issue body

## Out of Scope

- `docs/` directory (historical assets — do not modify, do not verify)
- Personal config (`~/.claude/CLAUDE.md`, memory files) — updated as part of implementation but excluded from spec/plan documentation and repo grep check
