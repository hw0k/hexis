---
issue: 23
status: READY_TO_IMPLEMENT
linked_spec: docs/specs/2026-04-08-skill-integration-gate-design.md
---

# Skill Integration Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add CLI integration gates to all 6 hexis workflow skills, replacing LLM-driven state judgment with `hexis status read/update` output.

**Architecture:** Each skill gets a `## CLI Integration Gate` section that runs `hexis status read <issue>` at entry and blocks if the state does not match the required label. `dispatch` replaces its grep-based routing with `hexis status read --json` output. `verify` additionally gets an exit gate that calls `hexis status update` inside the existing Gate Function, inserted before SYNC so the spec change is captured in the same commit.

**Tech Stack:** Markdown skill files (no code changes), `hexis` CLI (implemented in #22)

> Decomposition considered: all 6 tasks touch separate files with no cross-task conflicts and are individually mergeable, but partial deployment leaves the system inconsistent — only some skills gated while others use old grep logic. Single plan retained.

---

## Spec Check → Task Mapping

| Spec check index | Spec check item | Task |
|---|---|---|
| 0 | `dispatch` routes via `hexis status read` for all 5 state labels | Task 1 |
| 1 | `specify` gate blocks overwrite of existing spec without confirmation | Task 2 |
| 2 | `plan` gate blocks on non-`NEEDS_PLAN` state | Task 3 |
| 3 | `implement` gate blocks on non-`IN_PROGRESS` state | Task 4 |
| 4 | `verify` entry gate blocks on non-`NEEDS_VERIFY` state | Task 5 |
| 5 | `verify` exit gate runs `hexis status update` with complete AC state | Task 5 |
| 6 | `finish` gate blocks on non-`DONE` state | Task 6 |

---

## Files

| File | Change |
|---|---|
| `skills/dispatch/SKILL.md` | Replace Step 1b grep commands with `hexis status read --json`; replace routing Rules 2–4 with 5 CLI-state rules; renumber downstream rules |
| `skills/specify/SKILL.md` | Add `## CLI Integration Gate` section after `## $ARGUMENTS` |
| `skills/plan/SKILL.md` | Add `## CLI Integration Gate` section after `## $ARGUMENTS` |
| `skills/implement/SKILL.md` | Add `## CLI Integration Gate` section after `## $ARGUMENTS` |
| `skills/verify/SKILL.md` | Add `## CLI Integration Gate` section (entry gate) after `## $ARGUMENTS`; insert exit gate step in existing `## Gate Function` |
| `skills/finish/SKILL.md` | Add `## CLI Integration Gate` section after `## $ARGUMENTS` |

---

## Task 1: Update `dispatch` routing to use `hexis status read` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/dispatch/SKILL.md`

- [ ] **Step 1: Implement**

Replace the Step 1b bash block and variable descriptions (lines 56–67 of current file):

**Old — Step 1b bash block:**
```
Run in parallel:

```bash
grep -rl "^issue: N$" docs/specs/ 2>/dev/null
grep -rl "^issue: N$" docs/plans/ 2>/dev/null
gh pr list --head $(git branch --show-current) --json number,state,isDraft,reviewDecision,statusCheckRollup --limit 1
```

Where `N` is the literal issue number (e.g., for issue 20: `grep -rl "^issue: 20$" docs/specs/ 2>/dev/null`).

Collect:
- `spec_found`: true if any file in `docs/specs/` has frontmatter line `issue: N`
- `plan_found`: true if any file in `docs/plans/` has frontmatter line `issue: N`
- `pr`: the PR object from `gh`, or empty if none
```

**New — Step 1b bash block:**
```
Run in parallel:

```bash
hexis status read N --json
gh pr list --head $(git branch --show-current) --json number,state,isDraft,reviewDecision,statusCheckRollup --limit 1
```

Where `N` is the literal issue number (e.g., for issue 20: `hexis status read 20 --json`).

Collect:
- `status`: the full JSON object from `hexis status read --json` (contains `state`, `issue`, `plan_tasks`, `checks`, `blocking`)
- `pr`: the PR object from `gh`, or empty if none
```

Replace the routing table (Rules 1–8):

**Old routing table:**
```
| Rule | Condition | Next Skill |
|------|-----------|-----------|
| 1 | `git status --short` output is non-empty | `sync-working-status` |
| 2 | `spec_found` is false | `specify` |
| 3 | `spec_found` is true AND `plan_found` is false | `plan` |
| 4 | `plan_found` is true AND (no PR exists OR PR is draft) | `implement` |
| 5 | PR open AND any check is failing | `verify` |
| 6 | PR open AND all checks passing AND review not approved | `review` |
| 7 | PR open AND approved | `finish` |
| 8 | PR merged | — (stop, see below) |
```

**New routing table:**
```
| Rule | Condition | Next Skill |
|------|-----------|-----------|
| 1 | `git status --short` output is non-empty | `sync-working-status` |
| 2 | `status.state` is `NEEDS_SPEC` | `specify` |
| 3 | `status.state` is `NEEDS_PLAN` | `plan` |
| 4 | `status.state` is `IN_PROGRESS` | `implement` |
| 5 | `status.state` is `NEEDS_VERIFY` | `verify` |
| 6 | `status.state` is `DONE` AND no open PR | — (stop: output "Issue #N is complete. Nothing to dispatch.") |
| 7 | PR open AND any check is failing | `verify` |
| 8 | PR open AND all checks passing AND review not approved | `review` |
| 9 | PR open AND approved | `finish` |
| 10 | PR merged | — (stop, see below) |
```

Change "**Rule 8 — PR merged:**" heading to "**Rule 10 — PR merged:**".

Replace the first bullet in `## Notes`:

**Old:**
```
- If spec/plan files do not have `issue: N` in their YAML frontmatter, dispatch cannot locate them — they are treated as non-existent, and dispatch routes to `specify` or `plan` accordingly.
```

**New:**
```
- `hexis status read` is the authoritative source for issue state. The LLM does not infer state from file presence independently — CLI output determines routing.
```

- [ ] **Step 2: Verify**

Run: `grep -n "hexis status read\|status\.state\|Rule 10" skills/dispatch/SKILL.md`

Expected: Lines showing `hexis status read N --json` in Step 1b, five `status.state` routing conditions in Step 2, and `Rule 10 — PR merged` in the rule description section.

- [ ] **Step 3: Commit**

```bash
git add skills/dispatch/SKILL.md
git commit -m "feat(dispatch): route via hexis status read instead of grep (#23)"
```

---

## Task 2: Add CLI integration gate to `specify` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/specify/SKILL.md`

- [ ] **Step 1: Implement**

Insert the following section after `## $ARGUMENTS` and before `## Checklist` in `skills/specify/SKILL.md`:

```markdown
## CLI Integration Gate

If an issue number is known from `$ARGUMENTS` or session context (e.g., the current branch is `feat/23-something`):

1. Run: `hexis status read <issue>`
2. If output shows `STATE: NEEDS_SPEC`: proceed.
3. If output shows any other state: a spec already exists for this issue. Surface the full CLI output verbatim to the user and ask for explicit confirmation before overwriting. Do not proceed without confirmation.

If no issue number is known (genuinely new work with no GitHub issue yet): skip this gate and proceed.
```

- [ ] **Step 2: Verify**

Run: `grep -A 12 "## CLI Integration Gate" skills/specify/SKILL.md`

Expected: Shows the 4-line gate section ending with "skip this gate and proceed."

- [ ] **Step 3: Commit**

```bash
git add skills/specify/SKILL.md
git commit -m "feat(specify): add CLI integration gate (#23)"
```

---

## Task 3: Add CLI integration gate to `plan` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/plan/SKILL.md`

- [ ] **Step 1: Implement**

Insert the following section after `## $ARGUMENTS` and before `## Scope Check` in `skills/plan/SKILL.md`:

```markdown
## CLI Integration Gate

After loading the spec and reading the `issue:` value from its frontmatter, before writing any plan content:

1. Run: `hexis status read <issue>`
2. If output shows `STATE: NEEDS_PLAN`: proceed.
3. If output shows any other state: surface the full CLI output verbatim to the user; stop. Do not write any plan content.
```

- [ ] **Step 2: Verify**

Run: `grep -A 7 "## CLI Integration Gate" skills/plan/SKILL.md`

Expected: Shows the 3-step gate section ending with "Do not write any plan content."

- [ ] **Step 3: Commit**

```bash
git add skills/plan/SKILL.md
git commit -m "feat(plan): add CLI integration gate (#23)"
```

---

## Task 4: Add CLI integration gate to `implement` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/implement/SKILL.md`

- [ ] **Step 1: Implement**

Insert the following section after `## $ARGUMENTS` and before `## Complexity Check` in `skills/implement/SKILL.md`:

```markdown
## CLI Integration Gate

After loading the plan and reading the `issue:` value from its frontmatter, before writing any code:

1. Run: `hexis status read <issue>`
2. If output shows `STATE: IN_PROGRESS`: proceed.
3. If output shows any other state: surface the full CLI output verbatim to the user; stop. Do not begin implementation.
```

- [ ] **Step 2: Verify**

Run: `grep -A 7 "## CLI Integration Gate" skills/implement/SKILL.md`

Expected: Shows the 3-step gate section ending with "Do not begin implementation."

- [ ] **Step 3: Commit**

```bash
git add skills/implement/SKILL.md
git commit -m "feat(implement): add CLI integration gate (#23)"
```

---

## Task 5: Add CLI integration gate (entry + exit) to `verify` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/verify/SKILL.md`

- [ ] **Step 1: Implement — entry gate section**

Insert the following section after `## $ARGUMENTS` and before `## Complexity Check` in `skills/verify/SKILL.md`:

```markdown
## CLI Integration Gate

### Entry Gate

At skill start, before running any verification commands:

1. Obtain the issue number: use the number in `$ARGUMENTS` if provided; otherwise infer from the current branch name (first integer after the last `/`) or ask the user.
2. Run: `hexis status read <issue> --json`
3. If `state` is `NEEDS_VERIFY`: proceed. Surface the `checks` array to the user so they know which items need verification.
4. If `state` is `IN_PROGRESS`: surface the full CLI output verbatim to the user (blocking plan tasks are shown); stop — implementation must complete first.
5. If `state` is any other value: surface the full CLI output verbatim to the user; stop.
```

- [ ] **Step 2: Implement — exit gate inside existing `## Gate Function`**

In `## Gate Function`, the current step sequence is:

```
5. SYNC: invoke hexis:sync-working-status
6. ONLY THEN: claim
```

Replace it with:

```
5. UPDATE: run `hexis status update <issue> --checked <satisfied-indices> --unchecked <unsatisfied-indices>` using the checks from the entry gate read output (exit gate — updates spec before sync so the change is included in the commit)
6. SYNC: invoke hexis:sync-working-status
7. ONLY THEN: claim
```

- [ ] **Step 3: Verify**

Run: `grep -A 15 "## CLI Integration Gate" skills/verify/SKILL.md`

Expected: Shows the entry gate section with 5 steps. Then run:

```bash
grep -A 10 "## Gate Function" skills/verify/SKILL.md
```

Expected: Steps 5 UPDATE, 6 SYNC, 7 ONLY THEN visible in sequence.

- [ ] **Step 4: Commit**

```bash
git add skills/verify/SKILL.md
git commit -m "feat(verify): add CLI integration gate with exit update (#23)"
```

---

## Task 6: Add CLI integration gate to `finish` [No TDD — skill file (markdown)]

**Files:**
- Modify: `skills/finish/SKILL.md`

- [ ] **Step 1: Implement**

Insert the following section after `## $ARGUMENTS` and before `## Process` in `skills/finish/SKILL.md`:

```markdown
## CLI Integration Gate

Before any commit, push, or PR creation:

1. Obtain the issue number: use the number in `$ARGUMENTS` if provided; otherwise infer from the current branch name (first integer after the last `/`) or ask the user.
2. Run: `hexis status read <issue>`
3. If output shows `STATE: DONE`: proceed.
4. If output shows any other state: surface the full CLI output verbatim to the user; stop. Do not proceed with commit, push, or PR creation.
```

- [ ] **Step 2: Verify**

Run: `grep -A 8 "## CLI Integration Gate" skills/finish/SKILL.md`

Expected: Shows the 4-step gate section ending with "Do not proceed with commit, push, or PR creation."

- [ ] **Step 3: Commit**

```bash
git add skills/finish/SKILL.md
git commit -m "feat(finish): add CLI integration gate (#23)"
```
