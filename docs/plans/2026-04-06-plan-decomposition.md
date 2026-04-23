---
status: DONE
linked_spec: docs/specs/2026-04-06-plan-decomposition-design.md
---

# Plan Decomposition and Spec–Issue Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce 1 Spec = 1 Issue invariant across all skills, add `linked_spec` frontmatter to all Plan files, and add decomposition flows to `plan` and `specify`.

**Architecture:** Pure Markdown edits to four skill files plus retroactive frontmatter addition to seven existing plan files. No code, no test runner — verification is grep-based. Tasks ordered so `plan/SKILL.md` (foundational) is done first.

**Tech Stack:** Markdown only, `gh` CLI for issue operations in decomposition flows.

Issue: #6

---

## Files

| Action | Path |
|--------|------|
| Modify | `skills/plan/SKILL.md` |
| Modify | `skills/specify/SKILL.md` |
| Modify | `skills/sync-working-status/SKILL.md` |
| Modify | `docs/plans/2026-03-27-hw0k-workflow-plugin.md` |
| Modify | `docs/plans/2026-03-27-hw0k-workflow-enhancement-infra.md` |
| Modify | `docs/plans/2026-03-27-hw0k-workflow-enhancement-content.md` |
| Modify | `docs/plans/2026-03-27-skill-philosophy-rewrite.md` |
| Modify | `docs/plans/2026-04-01-specify-artifact-enforcement.md` |
| Modify | `docs/plans/2026-04-01-issues-2-3-4-plan-mode-sync-pre-commit.md` |
| Modify | `docs/plans/2026-04-06-dispatch-skill.md` |

> **No automated test framework for skill markdown.** Verification uses grep to confirm each new string is present after editing.

---

### Task 1: Update `skills/plan/SKILL.md` — `linked_spec` header + decomposition flow

**Files:**
- Modify: `skills/plan/SKILL.md`

- [ ] **Step 1: Confirm current Plan Header template string**

```bash
grep -n "linked_spec\|## Scope Check\|## Plan Header" skills/plan/SKILL.md
```

Expected: no `linked_spec` line, Scope Check section is brief (1 sentence).

- [ ] **Step 2: Add `linked_spec` to Plan Header template**

In `skills/plan/SKILL.md`, replace the Plan Header template block:

Old:
```markdown
Every plan must start with this header:

```markdown
# [Feature Name] Implementation Plan
```

New — prepend frontmatter to the template:
```markdown
Every plan must start with this header:

```markdown
---
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
status: DONE
---

# [Feature Name] Implementation Plan
```

- [ ] **Step 3: Replace Scope Check section with full decomposition flow**

Old `## Scope Check` section content:
```
If the spec covers multiple independent subsystems, split into separate plans. Each plan must produce independently working, testable software.
```

New:
```markdown
## Scope Check

After loading the spec, check whether the work can be split:
- Can each unit be developed with no shared in-progress state (no cross-unit file conflicts)?
- Can each unit be reviewed and merged independently?

If **both** conditions hold for N ≥ 2 units: propose decomposition to the user via `AskUserQuestion`. Do not proceed until confirmed.

**On confirmed decomposition:**
1. Split the original Spec into N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
2. Write N Plan files, each with `linked_spec` pointing to its new Spec
3. Create N GitHub Issues: `gh issue create --title "<unit name>" --body "<scope>\n\nDecomposed from: #<original>"`
4. Close original issue: `gh issue close <number> --comment "Decomposed into: #X, #Y, ..."`
5. Add superseded notice to original Spec: prepend `> **Superseded.** Decomposed into: [unit-a](path), [unit-b](path)`

If no decomposition: single plan (continue below), with `linked_spec` pointing to the parent Spec.
```

- [ ] **Step 4: Verify**

```bash
grep -n "linked_spec\|Superseded\|Decomposed from\|both.*conditions" skills/plan/SKILL.md
```

Expected: all four strings present.

- [ ] **Step 5: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "feat(plan): add linked_spec frontmatter and plan-time decomposition flow (#6)"
```

---

### Task 2: Update `skills/specify/SKILL.md` — specify-time decomposition

**Files:**
- Modify: `skills/specify/SKILL.md`

- [ ] **Step 1: Confirm current decomposition mention**

```bash
grep -n "decompose\|independent subsystem" skills/specify/SKILL.md
```

Expected: one-liner "If the input covers multiple independent subsystems: decompose first. Each subsystem gets its own specify cycle."

- [ ] **Step 2: Expand the decomposition mention into full action steps**

Old (in Step 1: Identify Ambiguities):
```
If the input covers multiple independent subsystems: decompose first. Each subsystem gets its own specify cycle.
```

New:
```markdown
If the input covers multiple independent subsystems, or the spec grows too large to be independently implementable as a single unit: decompose.

**On decomposition:**
1. Propose the N units to the user via `AskUserQuestion`. Do not proceed until confirmed.
2. Write N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
3. Create N GitHub Issues: `gh issue create --title "<unit name>" --body "<scope>\n\nDecomposed from: #<original>"`
4. If an original issue exists, close it: `gh issue close <number> --comment "Decomposed into: #X, #Y, ..."`
5. Each unit then enters its own Plan cycle independently.
```

- [ ] **Step 3: Verify**

```bash
grep -n "grows too large\|enters its own Plan cycle" skills/specify/SKILL.md
```

Expected: both strings present.

- [ ] **Step 4: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "feat(specify): add specify-time decomposition flow (#6)"
```

---

### Task 3: Update `skills/sync-working-status/SKILL.md` — Spec–Issue mismatch check

**Files:**
- Modify: `skills/sync-working-status/SKILL.md`

- [ ] **Step 1: Confirm current Step 2 content**

```bash
grep -n "Spec\|Issue\|mismatch\|linked" skills/sync-working-status/SKILL.md
```

Expected: no mismatch detection logic.

- [ ] **Step 2: Add Spec–Issue alignment check to Step 2**

In `skills/sync-working-status/SKILL.md`, append to the Step 2 section (after "Specs and plans are the single source of truth..."):

```markdown

Also verify the **1 Spec = 1 Issue** invariant:

```bash
# List open issues
gh issue list --state open --json number,title

# List spec files
ls docs/specs/
```

- For each open issue: is there a corresponding Spec file (matching issue number in frontmatter)?
- For each Spec file: is there a corresponding open or closed issue?

Surface any mismatches — do **not** auto-create missing artifacts. Note them in the sync report for human decision.
```

- [ ] **Step 3: Add resolution row to the discrepancy table**

In the `### 4. Resolve Discrepancies` table, add:

```markdown
| Spec exists, no linked Issue | Issue exists, no linked Spec | Surface for human decision — do not auto-create |
```

- [ ] **Step 4: Verify**

```bash
grep -n "1 Spec = 1 Issue\|auto-create\|human decision" skills/sync-working-status/SKILL.md
```

Expected: all three strings present.

- [ ] **Step 5: Commit**

```bash
git add skills/sync-working-status/SKILL.md
git commit -m "feat(sync-working-status): add spec-issue alignment check (#6)"
```

---

### Task 4: Add `linked_spec` frontmatter to existing plan files

**Files:**
- Modify: `docs/plans/2026-03-27-hw0k-workflow-plugin.md`
- Modify: `docs/plans/2026-03-27-hw0k-workflow-enhancement-infra.md`
- Modify: `docs/plans/2026-03-27-hw0k-workflow-enhancement-content.md`
- Modify: `docs/plans/2026-03-27-skill-philosophy-rewrite.md`
- Modify: `docs/plans/2026-04-01-specify-artifact-enforcement.md`
- Modify: `docs/plans/2026-04-01-issues-2-3-4-plan-mode-sync-pre-commit.md`
- Modify: `docs/plans/2026-04-06-dispatch-skill.md`

**Spec mapping:**

| Plan file | `linked_spec` value |
|-----------|---------------------|
| `2026-03-27-hw0k-workflow-plugin.md` | `docs/specs/2026-03-27-hw0k-workflow-plugin-design.md` |
| `2026-03-27-hw0k-workflow-enhancement-infra.md` | `docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md` |
| `2026-03-27-hw0k-workflow-enhancement-content.md` | `docs/specs/2026-03-27-hw0k-workflow-enhancement-design.md` |
| `2026-03-27-skill-philosophy-rewrite.md` | `docs/specs/2026-03-27-skill-philosophy-rewrite-design.md` |
| `2026-04-01-specify-artifact-enforcement.md` | `docs/specs/2026-04-01-specify-artifact-enforcement-design.md` |
| `2026-04-01-issues-2-3-4-plan-mode-sync-pre-commit.md` | `docs/specs/2026-04-01-plan-mode-to-executing-skills-design.md` (primary; this plan predates the 1 Spec = 1 Issue convention and covers 3 specs) |
| `2026-04-06-dispatch-skill.md` | `docs/specs/2026-04-06-dispatch-skill-design.md` |

- [ ] **Step 1: Confirm no plan files have existing frontmatter**

```bash
for f in docs/plans/*.md; do echo "=== $f ==="; head -3 "$f"; done
```

Expected: all files start with `#` (no `---` frontmatter block).

- [ ] **Step 2: Add frontmatter to each file**

For each file in the mapping table, prepend the YAML frontmatter block. Example for `hw0k-workflow-plugin.md`:

Current first line:
```
# hw0k-workflow Plugin Implementation Plan
```

New first two blocks:
```markdown
---
linked_spec: docs/specs/2026-03-27-hw0k-workflow-plugin-design.md
status: DONE
---

# hw0k-workflow Plugin Implementation Plan
```

Repeat for all 7 files using the mapping table above.

- [ ] **Step 3: Verify**

```bash
grep -rn "linked_spec" docs/plans/
```

Expected: 8 matches (7 existing + the plan file for this task itself).

- [ ] **Step 4: Commit**

```bash
git add docs/plans/
git commit -m "docs(plans): add linked_spec frontmatter to all existing plan files (#6)"
```
