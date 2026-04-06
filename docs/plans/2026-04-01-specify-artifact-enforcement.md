---
linked_spec: docs/specs/2026-04-01-specify-artifact-enforcement-design.md
---

# Specify Artifact Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen `skills/specify/SKILL.md` so agents cannot complete the skill flow without having written and committed a spec file to `docs/specs/`.

**Architecture:** Five targeted edits to one markdown file. No new files. Verification is grep-based (markdown has no compilation step).

**Tech Stack:** Markdown only.

---

## Files

- Modify: `skills/specify/SKILL.md`

> **No automated test framework for skill markdown.** Verification uses grep to confirm each new string is present post-edit.

---

### Task 1: Add five enforcement changes to `skills/specify/SKILL.md`

**Files:**
- Modify: `skills/specify/SKILL.md`

- [ ] **Step 1: Baseline read**

Read the file and confirm current strings:

```bash
grep -n "After approval, write to" skills/specify/SKILL.md
grep -n "Invoke \`hw0k-workflow:plan\`" skills/specify/SKILL.md
grep -n "Call \`ExitPlanMode\`" skills/specify/SKILL.md
```

Expected: each line found, no enforcement language present yet.

- [ ] **Step 2: Apply Change 1 — label plan file as temporary draft in Step 3**

In `skills/specify/SKILL.md`, locate the end of Step 3 (just before `Call \`ExitPlanMode\`. User approves the draft.`) and insert:

```markdown
> The plan file (`~/.claude/plans/`) is a **temporary approval draft only** — it is NOT the spec artifact. The real output is `docs/specs/YYYY-MM-DD-<topic>-design.md`, written in Step 4.
```

- [ ] **Step 3: Apply Change 2 — strengthen Step 4 with MANDATORY label**

Replace the current Step 4 body:

```markdown
After approval, write to `docs/specs/YYYY-MM-DD-<topic>-design.md`.

Commit: `docs: add <topic> spec`
```

With:

```markdown
**MANDATORY — do this immediately after approval, before anything else.**

Write to `docs/specs/YYYY-MM-DD-<topic>-design.md`. Commit: `docs: add <topic> spec`

Do NOT proceed to Step 5 until the spec file exists and is committed.
```

- [ ] **Step 4: Apply Change 3 — add HARD-GATE to Step 5**

Replace the current Step 5 body:

```markdown
Invoke `hw0k-workflow:plan`.
```

With:

```markdown
**HARD-GATE:** Before invoking `hw0k-workflow:plan`, verify the spec file exists. Run `ls docs/specs/` and confirm the file is present and committed. If it is not, return to Step 4.

Invoke `hw0k-workflow:plan`.
```

- [ ] **Step 5: Apply Changes 4 & 5 — add two rules**

In the `## Rules` section, append after the last existing rule:

```markdown
- If ExitPlanMode is rejected: return to Step 3 and re-draft. Do NOT skip to implementation.
- If the user requests to skip writing the spec file: use `AskUserQuestion` to confirm. Only proceed without a spec file with explicit user confirmation, and note the skip explicitly.
```

- [ ] **Step 6: Verify all changes present**

```bash
grep -n "temporary approval draft only" skills/specify/SKILL.md
grep -n "MANDATORY" skills/specify/SKILL.md
grep -n "HARD-GATE" skills/specify/SKILL.md
grep -n "ExitPlanMode is rejected" skills/specify/SKILL.md
grep -n "requests to skip writing the spec file" skills/specify/SKILL.md
```

Expected: each grep returns exactly one match. If any is missing, re-apply that change.

- [ ] **Step 7: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "fix: enforce spec file output in specify skill (#1)"
```
