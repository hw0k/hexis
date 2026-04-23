---
issue: 25
status: DONE
linked_spec: docs/specs/2026-04-19-hexis-rename-design.md
---

# Hexis Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hw0k-workflow:implement` to execute task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace every occurrence of `hw0k-workflow` with `hexis` across skills, agents, config, tests, GitHub infrastructure, and personal config — leaving `docs/` untouched.

**Architecture:** Batch sed substitution across all in-scope files using two-pass pattern (`claude-hw0k-workflow` first, then `hw0k-workflow`) to correctly collapse the `claude-` prefix. GitHub operations follow after repo changes are pushed. Personal config is updated last.

**Tech Stack:** bash, sed, gh CLI

---

## Files Modified

| File | Change |
|---|---|
| `skills/*/SKILL.md` (×18) | frontmatter `name:` + all body invocation syntax |
| `agents/principles-reviewer.md` | all `hw0k-workflow:` skill references |
| `.claude-plugin/plugin.json` | `"name"` field |
| `.pre-commit-config.yaml` | comment line |
| `.githooks/run-if-exists.sh` | `PLUGIN_PREFIX`, `.hw0k-workflow/` path |
| `CLAUDE.md` | all occurrences |
| `README.md` | all occurrences |
| `tests/pressure/**/*.md` | all occurrences |
| `~/.claude/CLAUDE.md` | skill prefix table |
| `~/.claude/projects/*/memory/*.md` | project name references |

---

### Task 1: Rename skill SKILL.md files

**Files:**
- Modify: `skills/commit-principles/SKILL.md`, `skills/core-principles/SKILL.md`, `skills/debug/SKILL.md`, `skills/dispatch/SKILL.md`, `skills/exception-and-logging-principles/SKILL.md`, `skills/finish/SKILL.md`, `skills/general-naming-principles/SKILL.md`, `skills/http-api-principles/SKILL.md`, `skills/implement/SKILL.md`, `skills/plan/SKILL.md`, `skills/receive-review/SKILL.md`, `skills/review/SKILL.md`, `skills/setup-new-project/SKILL.md`, `skills/specify/SKILL.md`, `skills/sync-working-status/SKILL.md`, `skills/use-worktree/SKILL.md`, `skills/verify/SKILL.md`, `skills/write-test/SKILL.md`

- [ ] **Step 1: Confirm current state**

```bash
grep -r "hw0k-workflow" skills/ --include="*.md" -l | wc -l
```
Expected: `18`

- [ ] **Step 2: Apply substitution**

```bash
find skills/ -name "*.md" -exec sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' {} +
```

- [ ] **Step 3: Verify**

```bash
grep -r "hw0k-workflow" skills/ --include="*.md"
```
Expected: no output

---

### Task 2: Rename agent and infrastructure files

**Files:**
- Modify: `agents/principles-reviewer.md`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.pre-commit-config.yaml`
- Modify: `.githooks/run-if-exists.sh`

- [ ] **Step 1: Confirm current state**

```bash
grep -r "hw0k-workflow" agents/ .claude-plugin/ .pre-commit-config.yaml .githooks/
```
Expected: matches in all 4 files

- [ ] **Step 2: Apply substitution**

```bash
sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' \
  agents/principles-reviewer.md \
  .claude-plugin/plugin.json \
  .pre-commit-config.yaml \
  .githooks/run-if-exists.sh
```

- [ ] **Step 3: Verify**

```bash
grep -r "hw0k-workflow" agents/ .claude-plugin/ .pre-commit-config.yaml .githooks/
```
Expected: no output

- [ ] **Step 4: Spot-check plugin.json**

```bash
cat .claude-plugin/plugin.json
```
Expected: `"name": "hexis"`

---

### Task 3: Rename root files

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Confirm current state**

```bash
grep -c "hw0k-workflow" CLAUDE.md README.md
```
Expected: non-zero counts for both files

- [ ] **Step 2: Apply substitution**

```bash
sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' CLAUDE.md README.md
```

- [ ] **Step 3: Verify**

```bash
grep "hw0k-workflow" CLAUDE.md README.md
```
Expected: no output

---

### Task 4: Rename test files

**Files:**
- Modify: `tests/pressure/commit-principles/README.md`
- Modify: `tests/pressure/dispatch/README.md`
- Modify: `tests/pressure/dispatch/evaluation-log.md`
- Modify: `tests/pressure/dispatch/scenarios/001-no-spec-routes-to-specify.md`
- Modify: `tests/pressure/dispatch/scenarios/002-spec-no-plan-routes-to-plan.md`
- Modify: `tests/pressure/dispatch/scenarios/003-dirty-tree-routes-to-sync.md`
- Modify: `tests/pressure/dispatch/scenarios/004-enforcement-header.md`

- [ ] **Step 1: Confirm current state**

```bash
grep -r "hw0k-workflow" tests/ --include="*.md" -l | wc -l
```
Expected: `7`

- [ ] **Step 2: Apply substitution**

```bash
find tests/ -name "*.md" -exec sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' {} +
```

- [ ] **Step 3: Verify**

```bash
grep -r "hw0k-workflow" tests/
```
Expected: no output

---

### Task 5: Repo-wide verification and commit

- [ ] **Step 1: Full repo grep (excluding docs/ and .git/)**

```bash
grep -r "hw0k-workflow" . --exclude-dir=.git --exclude-dir=docs
```
Expected: no output. If any matches remain, fix them before continuing.

- [ ] **Step 2: Stage all changed files**

```bash
git add \
  skills/ \
  agents/principles-reviewer.md \
  .claude-plugin/plugin.json \
  .pre-commit-config.yaml \
  .githooks/run-if-exists.sh \
  CLAUDE.md \
  README.md \
  tests/
```

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: rename hw0k-workflow to hexis (#25)"
```

- [ ] **Step 4: Push**

```bash
git push
```

---

### Task 6: Rename GitHub repository

- [ ] **Step 1: Confirm current repo name**

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```
Expected: `hw0k/claude-hw0k-workflow`

- [ ] **Step 2: Rename repo**

```bash
gh repo rename hexis
```

- [ ] **Step 3: Update local remote URL**

```bash
git remote set-url origin https://github.com/hw0k/hexis.git
```

- [ ] **Step 4: Verify**

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
git remote get-url origin
```
Expected: `hw0k/hexis` and `https://github.com/hw0k/hexis.git`

---

### Task 7: Edit GitHub issues #22 and #23

- [ ] **Step 1: Check issue #22 for occurrences**

```bash
gh issue view 22 --json body -q .body | grep "hw0k-workflow"
```
Expected: any output indicates a match to replace (no output means no-op, still run Step 2 to be safe)

- [ ] **Step 2: Edit issue #22**

```bash
tmpfile=$(mktemp)
gh issue view 22 --json body -q .body \
  | sed 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' \
  > "$tmpfile"
gh issue edit 22 --body-file "$tmpfile"
rm "$tmpfile"
```

- [ ] **Step 3: Check issue #23 for occurrences**

```bash
gh issue view 23 --json body -q .body | grep "hw0k-workflow"
```
Expected: at least one match (`hw0k-workflow skill`)

- [ ] **Step 4: Edit issue #23**

```bash
tmpfile=$(mktemp)
gh issue view 23 --json body -q .body \
  | sed 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' \
  > "$tmpfile"
gh issue edit 23 --body-file "$tmpfile"
rm "$tmpfile"
```

- [ ] **Step 5: Verify both issues**

```bash
gh issue view 22 --json body -q .body | grep "hw0k-workflow" | wc -l
gh issue view 23 --json body -q .body | grep "hw0k-workflow" | wc -l
```
Expected: `0` for both

---

### Task 8: Update personal config

**Files:**
- Modify: `~/.claude/CLAUDE.md`
- Modify: `~/.claude/projects/-home-hw0k-win11-wsl-workspaces-hexis/memory/MEMORY.md`
- Modify: `~/.claude/projects/-home-hw0k-win11-wsl-workspaces-hexis/memory/*.md` (all memory files)

- [ ] **Step 1: Confirm occurrences in global CLAUDE.md**

```bash
grep -c "hw0k-workflow" ~/.claude/CLAUDE.md
```
Expected: non-zero

- [ ] **Step 2: Apply substitution to global CLAUDE.md**

```bash
sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' ~/.claude/CLAUDE.md
```

- [ ] **Step 3: Apply substitution to memory files**

```bash
find ~/.claude/projects/-home-hw0k-win11-wsl-workspaces-hexis/memory/ -name "*.md" \
  -exec sed -i 's/claude-hw0k-workflow/hexis/g; s/hw0k-workflow/hexis/g' {} +
```

- [ ] **Step 4: Verify**

```bash
grep "hw0k-workflow" ~/.claude/CLAUDE.md
grep -r "hw0k-workflow" ~/.claude/projects/-home-hw0k-win11-wsl-workspaces-hexis/memory/
```
Expected: no output for both

---

### Task 9: Final verification

- [ ] **Step 1: Repo grep**

```bash
grep -r "hw0k-workflow" . --exclude-dir=.git --exclude-dir=docs
```
Expected: no output

- [ ] **Step 2: GitHub repo name**

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```
Expected: `hw0k/hexis`

- [ ] **Step 3: Issue bodies**

```bash
gh issue view 22 --json body -q .body | grep "hw0k-workflow" | wc -l
gh issue view 23 --json body -q .body | grep "hw0k-workflow" | wc -l
```
Expected: `0` for both

- [ ] **Step 4: Close issue #25**

```bash
gh issue close 25 --comment "All done — zero \`hw0k-workflow\` occurrences confirmed. Repo renamed to hw0k/hexis."
```
