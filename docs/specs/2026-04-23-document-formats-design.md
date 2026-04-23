---
issue: 20
---

# Standardize Spec and Plan Document Formats

## Problem

`docs/specs/` and `docs/plans/` exist as conventions, but their internal structure is undocumented. Skills that produce or consume these files (`specify`, `plan`, `dispatch`, `sync-working-status`) each hold implicit assumptions about the structure — assumptions that can diverge silently.

Two specific gaps:

1. **Inconsistent machine-readable markers.** Spec files embed `Issue: #N` as a plain body line; plan files use `linked_spec` YAML frontmatter. There is no consistent contract for where machine-readable fields live.
2. **No shared source of truth for format.** Skills describe their output format inline and independently, so structural drift goes undetected.

## Goal

Define a canonical format for spec files and plan files, with all machine-readable fields in YAML frontmatter. Encode these formats in `docs/templates/` as the single source of truth. Update all skills that produce or consume these files to reference the templates. Apply the new format to all existing files.

Issue body format and PR description format are **out of scope** — those follow each team's or project's own conventions.

## Changes

### 1. `docs/templates/spec.md` — canonical spec format

```markdown
---
issue: N
---

# <Title>

## Problem

## Goal

## Changes

## Out of Scope

## Done Criteria
```

**Frontmatter fields:**
- `issue: N` — required when linked to a GitHub issue (bare integer, no `#`)
- `plan: docs/plans/...` — optional; added by the `plan` skill once the plan file is created

**Body sections:**
- `## Problem` — required
- `## Goal` — required
- `## Changes` — required
- `## Out of Scope` — optional
- `## Done Criteria` — required

**Removed:** `Issue: #N` as a body line (replaced by frontmatter `issue: N`).

---

### 2. `docs/templates/plan.md` — canonical plan format

```markdown
---
linked_spec: docs/specs/<filename>.md
issue: N
---

# <Title> Implementation Plan

> **For agentic workers:** ...

**Goal:** ...
**Architecture:** ...
**Tech Stack:** ...

---

## File Structure

---

### Task N: <Name> [TDD] or [No TDD — <reason>]
...
```

**Frontmatter fields:**
- `linked_spec: docs/specs/...` — required
- `issue: N` — required when linked to a GitHub issue (new field; bare integer)

**Body structure** follows the existing `plan` skill conventions (Goal, Architecture, Tech Stack, File Structure, tasks with TDD labels).

---

### 3. `skills/specify/SKILL.md`

- Step 4 (Write and Commit): output file must match `docs/templates/spec.md`
- Frontmatter must include `issue: N` — replaces `Issue: #N` body line
- Remove instruction to write `Issue: #N` in the body

---

### 4. `skills/plan/SKILL.md`

- Plan output must match `docs/templates/plan.md`
- Frontmatter must include `issue: N` (in addition to existing `linked_spec`)
- After creating the plan file, update the spec's frontmatter to add `plan: docs/plans/<filename>.md`

---

### 5. `skills/dispatch/SKILL.md`

Current grep:
```bash
grep -rl "#N" docs/specs/ 2>/dev/null
grep -rl "#N" docs/plans/ 2>/dev/null
```

Replace with:
```bash
grep -rl "^issue: N$" docs/specs/ 2>/dev/null
grep -rl "^issue: N$" docs/plans/ 2>/dev/null
```

Where `N` is the literal issue number (e.g., `^issue: 20$`).

---

### 6. `skills/sync-working-status/SKILL.md`

- When verifying the "1 Spec = 1 Issue" invariant, locate spec/plan files by matching frontmatter `issue: N` rather than scanning filenames.

---

### 7. `skills/review/SKILL.md`

- Add a note: spec and plan files consumed during review follow the formats in `docs/templates/spec.md` and `docs/templates/plan.md`.

---

### 8. Backfill all existing spec and plan files

Apply the new format to all files in `docs/specs/` (17 files) and `docs/plans/` (12 files):

- **Spec files**: add YAML frontmatter with `issue: N` (extract N from existing `Issue: #N` body line), then remove the `Issue: #N` body line. Add `plan:` field if a corresponding plan file exists.
- **Plan files**: add `issue: N` to existing frontmatter. Add `issue:` based on the issue number referenced in the linked spec.
- Files with no linked issue: add frontmatter block without `issue:` field (just `linked_spec:` for plans, empty frontmatter `---\n---` for standalone specs).

---

### 9. Delete `docs/templates/issue.md` and `docs/templates/pr.md`

These were created during spec drafting but are out of scope. Remove them.

## Out of Scope

- Issue body format
- PR description format
- GitHub-native templates (`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`)
- Backfilling is full-scope (all existing files, not just open issues)

## Done Criteria

- `docs/templates/spec.md` defines canonical spec format with frontmatter
- `docs/templates/plan.md` defines canonical plan format with frontmatter including `issue: N`
- `docs/templates/issue.md` and `docs/templates/pr.md` deleted
- `skills/specify/SKILL.md` outputs spec with frontmatter `issue: N`; no longer writes `Issue: #N` in body
- `skills/plan/SKILL.md` outputs plan with frontmatter `issue: N`; adds `plan:` back-link to spec frontmatter
- `skills/dispatch/SKILL.md` greps `^issue: N$` in frontmatter instead of `#N` in body
- `skills/sync-working-status/SKILL.md` locates spec/plan by frontmatter `issue: N`
- `skills/review/SKILL.md` references `docs/templates/` for expected format
- All 17 spec files and 12 plan files updated to match new format
