---
issue: 20
status: IN_PROGRESS
linked_spec: docs/specs/2026-04-23-document-formats-design.md
---

# Document Formats Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize spec and plan document formats by moving all machine-readable fields to YAML frontmatter and updating every skill and file that produces or consumes them.

**Architecture:** Pure markdown edits across two layers — (1) skill definitions in `skills/` that govern future output, (2) backfill of all existing files in `docs/specs/` and `docs/plans/`. Two commit groups: skills first, backfill second.

**Tech Stack:** Markdown, YAML frontmatter, Python 3 (backfill scripts), bash

---

## File Structure

- Modify: `skills/specify/SKILL.md` — Step 4 output format
- Modify: `skills/plan/SKILL.md` — Plan Header frontmatter + Save section
- Modify: `skills/dispatch/SKILL.md` — grep commands + Notes
- Modify: `skills/sync-working-status/SKILL.md` — 1 Spec = 1 Issue bash block
- Modify: `skills/review/SKILL.md` — Red Flags section
- Modify: all 17 files in `docs/specs/` — add frontmatter, remove `Issue: #N` body line
- Modify: all 12 files in `docs/plans/` — add `issue: N` to frontmatter where applicable

---

### Task 1: Update skills/specify/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/specify/SKILL.md:94-110`

- [x] **Step 1: Implement**

Replace in `skills/specify/SKILL.md`:

```
Write to `docs/specs/YYYY-MM-DD-<topic>-design.md`. The file must begin with:

```markdown
# <Title>

Issue: #N
```

Where `N` is the GitHub issue number this spec addresses. If there is no associated issue, omit the `Issue:` line. This line is required for `hexis:dispatch` to locate the spec by issue number.
```

With:

```
Write to `docs/specs/YYYY-MM-DD-<topic>-design.md`. The file must match `docs/templates/spec.md`. The file must begin with:

```markdown
---
issue: N
---

# <Title>
```

Where `N` is the GitHub issue number this spec addresses (bare integer, no `#`). If there is no associated issue, omit the frontmatter. The `issue: N` frontmatter field is required for `hexis:dispatch` to locate the spec by issue number.
```

- [x] **Step 2: Verify**

```bash
grep -A 12 "Step 4: Write and Commit" skills/specify/SKILL.md | grep "issue: N"
```

Expected: `issue: N`

- [x] **Step 3: Commit** *(skip — commit at end of Task 5 with all skills together)*

---

### Task 2: Update skills/plan/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/plan/SKILL.md:60-63` (Plan Header frontmatter)
- Modify: `skills/plan/SKILL.md:187-189` (Save section)

- [x] **Step 1: Implement Edit A — Plan Header frontmatter**

Replace in `skills/plan/SKILL.md`:

```
---
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
---
```

With:

```
---
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
issue: N
---
```

- [x] **Step 2: Implement Edit B — Save section**

Replace in `skills/plan/SKILL.md`:

```
## Save

`docs/plans/YYYY-MM-DD-<feature>.md`. Commit: `docs: add <feature> plan`.
```

With:

```
## Save

1. Write `docs/plans/YYYY-MM-DD-<feature>.md`. Commit: `docs: add <feature> plan`.
2. Update the linked spec's YAML frontmatter: add `plan: docs/plans/<filename>.md`. Commit: `docs: add plan back-link to <topic> spec (#N)`.
```

- [x] **Step 3: Verify**

```bash
grep "issue: N" skills/plan/SKILL.md && grep "plan back-link" skills/plan/SKILL.md
```

Expected: both lines found

---

### Task 3: Update skills/dispatch/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/dispatch/SKILL.md:56-58` (grep commands)
- Modify: `skills/dispatch/SKILL.md:63-64` (spec_found/plan_found description)
- Modify: `skills/dispatch/SKILL.md:114` (Notes)

- [x] **Step 1: Implement Edit A — grep commands**

Replace in `skills/dispatch/SKILL.md`:

```bash
grep -rl "#N" docs/specs/ 2>/dev/null
grep -rl "#N" docs/plans/ 2>/dev/null
```

With:

```bash
grep -rl "^issue: N$" docs/specs/ 2>/dev/null
grep -rl "^issue: N$" docs/plans/ 2>/dev/null
```

Where `N` is the literal issue number (e.g., for issue 20: `grep -rl "^issue: 20$" docs/specs/ 2>/dev/null`).

- [x] **Step 2: Implement Edit B — Collect description**

Replace in `skills/dispatch/SKILL.md`:

```
- `spec_found`: true if any file in `docs/specs/` contains `#N`
- `plan_found`: true if any file in `docs/plans/` contains `#N`
```

With:

```
- `spec_found`: true if any file in `docs/specs/` has frontmatter line `issue: N`
- `plan_found`: true if any file in `docs/plans/` has frontmatter line `issue: N`
```

- [x] **Step 3: Implement Edit C — Notes**

Replace in `skills/dispatch/SKILL.md`:

```
- If spec/plan files do not embed `Issue: #N` in their content, dispatch cannot locate them — they are treated as non-existent, and dispatch routes to `specify` or `plan` accordingly.
```

With:

```
- If spec/plan files do not have `issue: N` in their YAML frontmatter, dispatch cannot locate them — they are treated as non-existent, and dispatch routes to `specify` or `plan` accordingly.
```

- [x] **Step 4: Verify**

```bash
grep "^issue: N" skills/dispatch/SKILL.md
```

Expected: two lines (one for specs, one for plans)

---

### Task 4: Update skills/sync-working-status/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/sync-working-status/SKILL.md:47-52`

- [x] **Step 1: Implement**

Replace in `skills/sync-working-status/SKILL.md`:

```bash
# List open issues
gh issue list --state open --json number,title

# List spec files
ls docs/specs/
```

With:

```bash
# List open issues
gh issue list --state open --json number,title

# List spec files with their issue numbers
grep -rn "^issue: " docs/specs/
```

- [x] **Step 2: Verify**

```bash
grep "^issue: " skills/sync-working-status/SKILL.md
```

Expected: `grep -rn "^issue: " docs/specs/`

---

### Task 5: Update skills/review/SKILL.md [No TDD — modifying skill documentation]

**Files:**
- Modify: `skills/review/SKILL.md` (Red Flags section)

- [x] **Step 1: Implement**

Replace in `skills/review/SKILL.md`:

```
- Skip review because "it's simple"
```

With:

```
- Skip review because "it's simple"
- Spec or plan files in the diff that don't follow `docs/templates/spec.md` / `docs/templates/plan.md`
```

- [x] **Step 2: Verify**

```bash
grep "docs/templates" skills/review/SKILL.md
```

Expected: `docs/templates/spec.md` / `docs/templates/plan.md`

- [x] **Step 3: Commit all skills changes together**

```bash
git add skills/specify/SKILL.md skills/plan/SKILL.md skills/dispatch/SKILL.md skills/sync-working-status/SKILL.md skills/review/SKILL.md
git commit -m "feat(skills): update specify/plan/dispatch/sync/review to use frontmatter issue field (#20)"
```

---

### Task 6: Backfill docs/specs/ [No TDD — bulk markdown backfill]

**Files:**
- Modify: all 17 existing files in `docs/specs/`

- [x] **Step 1: Implement**

Create and run the following Python script from the repo root:

```python
#!/usr/bin/env python3
import os, re

SPEC_TO_PLANS = {
    "2026-04-06-dispatch-skill-design": ["2026-04-06-dispatch-skill.md"],
    "2026-04-08-universal-task-tool-integration-design": ["2026-04-08-universal-task-tool-integration.md"],
    "2026-04-19-universal-skill-support-design": ["2026-04-19-universal-skill-support.md"],
    "2026-04-19-hexis-rename-design": ["2026-04-19-hexis-rename.md"],
    "2026-04-22-tdd-workflow-restructure-design": ["2026-04-22-tdd-workflow-restructure.md"],
    "2026-03-27-hw0k-workflow-enhancement-design": [
        "2026-03-27-hw0k-workflow-enhancement-content.md",
        "2026-03-27-hw0k-workflow-enhancement-infra.md",
    ],
    "2026-03-27-hw0k-workflow-plugin-design": ["2026-03-27-hw0k-workflow-plugin.md"],
    "2026-03-27-skill-philosophy-rewrite-design": ["2026-03-27-skill-philosophy-rewrite.md"],
    "2026-04-01-plan-mode-to-executing-skills-design": ["2026-04-01-issues-2-3-4-plan-mode-sync-pre-commit.md"],
    "2026-04-01-specify-artifact-enforcement-design": ["2026-04-01-specify-artifact-enforcement.md"],
    "2026-04-06-plan-decomposition-design": ["2026-04-06-plan-decomposition.md"],
}

SKIP = {"2026-04-23-document-formats-design"}

specs_dir = "docs/specs"

for fname in sorted(os.listdir(specs_dir)):
    if not fname.endswith(".md"):
        continue
    stem = fname[:-3]
    if stem in SKIP:
        print(f"SKIP (already correct): {fname}")
        continue

    path = os.path.join(specs_dir, fname)
    with open(path) as f:
        content = f.read()

    if content.startswith("---\n"):
        print(f"SKIP (already has frontmatter): {fname}")
        continue

    issue_match = re.search(r"^Issue: #(\d+)\s*$", content, re.MULTILINE)
    issue_num = int(issue_match.group(1)) if issue_match else None

    plans = SPEC_TO_PLANS.get(stem, [])

    fm_lines = ["---"]
    if issue_num:
        fm_lines.append(f"issue: {issue_num}")
    if len(plans) == 1:
        fm_lines.append(f"plan: docs/plans/{plans[0]}")
    elif len(plans) > 1:
        fm_lines.append("plan:")
        for p in plans:
            fm_lines.append(f"  - docs/plans/{p}")
    fm_lines.append("---")

    if len(fm_lines) == 2:  # only --- delimiters, nothing inside
        print(f"SKIP (no issue, no plan): {fname}")
        continue

    frontmatter = "\n".join(fm_lines) + "\n\n"
    new_body = re.sub(r"^Issue: #\d+\n\n?", "", content, flags=re.MULTILINE)
    new_content = frontmatter + new_body

    with open(path, "w") as f:
        f.write(new_content)
    print(f"Updated: {fname} (issue={issue_num}, plans={plans})")
```

- [x] **Step 2: Verify**

```bash
grep -l "^---" docs/specs/*.md | wc -l
```

Expected: `15` (8 specs with issue + 6 specs with plan-only frontmatter + 1 already-correct new spec)

```bash
grep -rl "^Issue: #" docs/specs/
```

Expected: no output (all `Issue: #N` body lines removed)

- [x] **Step 3: Commit**

```bash
git add docs/specs/
git commit -m "docs(specs): backfill frontmatter — move issue number from body to YAML (#20)"
```

---

### Task 7: Backfill docs/plans/ [No TDD — bulk markdown backfill]

**Files:**
- Modify: up to 12 files in `docs/plans/` (those whose linked spec has an issue number)

**Note:** Task 6 must be complete before Task 7 — the plan backfill reads issue numbers from spec frontmatter.

- [x] **Step 1: Implement**

Create and run the following Python script from the repo root:

```python
#!/usr/bin/env python3
import os, re

plans_dir = "docs/plans"

for fname in sorted(os.listdir(plans_dir)):
    if not fname.endswith(".md"):
        continue

    path = os.path.join(plans_dir, fname)
    with open(path) as f:
        content = f.read()

    if not content.startswith("---\n"):
        print(f"SKIP (no frontmatter): {fname}")
        continue

    if re.search(r"^issue: \d+", content, re.MULTILINE):
        print(f"SKIP (already has issue): {fname}")
        continue

    spec_match = re.search(r"^linked_spec: (.+)$", content, re.MULTILINE)
    if not spec_match:
        print(f"SKIP (no linked_spec): {fname}")
        continue

    spec_path = spec_match.group(1).strip()
    if not os.path.exists(spec_path):
        print(f"SKIP (spec not found: {spec_path}): {fname}")
        continue

    with open(spec_path) as f:
        spec_content = f.read()

    issue_match = re.search(r"^issue: (\d+)$", spec_content, re.MULTILINE)
    if not issue_match:
        print(f"SKIP (spec has no issue number): {fname}")
        continue

    issue_num = issue_match.group(1)
    new_content = re.sub(
        r"(^linked_spec: .+$)",
        rf"\1\nissue: {issue_num}",
        content,
        flags=re.MULTILINE,
    )

    with open(path, "w") as f:
        f.write(new_content)
    print(f"Updated: {fname} (issue={issue_num})")
```

- [x] **Step 2: Verify**

```bash
grep -l "^issue:" docs/plans/*.md | wc -l
```

Expected: `5`
(dispatch #10, universal-task-tool #15, universal-skill-support #16, hexis-rename #25, tdd-restructure #27)

- [x] **Step 3: Commit**

```bash
git add docs/plans/
git commit -m "docs(plans): backfill issue frontmatter field from linked spec (#20)"
```
