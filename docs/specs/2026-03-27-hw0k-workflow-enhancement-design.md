# hw0k-workflow Enhancement Design

> **Historical document.** This spec reflects the initial design state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

**Date:** 2026-03-27
**Status:** Approved

---

## Summary

This document describes the planned enhancements to the `hw0k-workflow` Claude Code plugin. The goal is to complete the ruleset so that any person, device, agent, or tool that follows this plugin enforces the same standards — with git-level enforcement that is tool-agnostic.

---

## Problem

The initial plugin (v0.1.0) covered commit format, status sync, and three principle skills. It left open:

- No Core Principle definition (the foundational rules for all other standards)
- No Logging Principle (exception handling and logging are one decision — separating them creates gaps)
- No git-level enforcement (skills guide Claude but cannot block a bad commit from VS Code or a CLI)
- No project onboarding guide (each contributor must infer setup from scratch)
- No tests (skill wording is unverified against agent rationalization)
- Skill files are not structured for selective loading (full content loads even when only core rules are needed)
- Status sync covers only git/GitHub — local Specs/Plans progress is not reconciled with remote state

---

## Completed Workflow (Post-Enhancement)

### 1. New Project Onboarding

Any contributor runs `hw0k-workflow:new-project-setup`. The skill guides:

```bash
git config core.hooksPath .githooks
lefthook install
```

After this, **every git commit on any tool** passes through lefthook hooks.

### 2. Pre-Work — Spec Review

`hw0k-workflow:core-principles` loads. Agent checks:
- Environment Independence: does this change rely on local state?
- Human Gate: are irreversible operations flagged for approval?
- Static Verification: is the done-criteria measurable by a tool?

`principles-reviewer` agent scans specs for principle violations.

### 3. Pre-Work — Status Sync

`/hw0k-workflow:sync-working-status` (manual) or `Stop` hook (auto). Three sync targets are reconciled before work begins:

1. **Local git state** — uncommitted changes, branch tracking, ahead/behind remote
2. **Specs/Plans** — plan checkboxes and spec files in `docs/` are the single source of truth for task progress; sync ensures they reflect actual state, not stale intent
3. **Remote issue state** — GitHub PR status, CI, review threads, linked issues

### 4. Development

Principle skills (`http-api-principles`, `exception-and-logging-principles`, `general-naming-principles`) load automatically. `principles-reviewer` agent runs after file changes.

### 5. Commit

`/hw0k-workflow:commit` → Claude writes the message → lefthook fires:

- `pre-commit`: lint + format + test (project-aware, skip if not configured)
- `commit-msg`: Conventional Commits validation — blocks on violation

Tool-agnostic: VS Code, JetBrains, terminal, any agent.

### 6. Post-Work — Status Sync

`/hw0k-workflow:sync-working-status` (manual) or auto via `Stop` hook. Same four targets as pre-work sync:
local git → Specs/Plans → remote issue state.

---

## Repository Structure

```
hw0k-workflow/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── conventional-commit/
│   │   ├── SKILL.md              (existing — content unchanged)
│   │   └── reference.md          (new — edge cases, scope examples)
│   ├── sync-working-status/
│   │   └── SKILL.md              (existing — unchanged)
│   ├── http-api-principles/
│   │   ├── SKILL.md              (existing — trim to 500 lines)
│   │   └── examples.md           (new — detailed JSON examples)
│   ├── exception-and-logging-principles/   ← replaces exception-principles
│   │   ├── SKILL.md              (new — exception + logging combined)
│   │   └── examples.md           (new)
│   ├── general-naming-principles/
│   │   ├── SKILL.md              (existing — trim to 500 lines)
│   │   └── examples.md           (new — name comparison lists)
│   ├── core-principles/          (new)
│   │   └── SKILL.md
│   └── new-project-setup/        (new)
│       ├── SKILL.md
│       └── lefthook.yml          (template for user projects)
├── commands/
│   ├── commit.md                 (existing — unchanged)
│   └── sync.md                   (existing — unchanged)
├── agents/
│   └── principles-reviewer.md   (existing — add core-principles scope)
├── tests/
│   └── pressure/
│       └── conventional-commit/
│           ├── README.md
│           ├── scenarios/
│           │   ├── 001-past-tense-temptation.md
│           │   ├── 002-non-standard-type.md
│           │   ├── 003-scope-with-spaces.md
│           │   ├── 004-body-before-blank-line.md
│           │   └── 005-uppercase-description.md
│           └── evaluation-log.md
└── .githooks/
    ├── lefthook.yml
    ├── check-commit-msg.sh
    └── run-if-exists.sh
```

---

## Component Change Map

| Component | Status | Reason |
|-----------|--------|--------|
| `skills/conventional-commit/` | modify — add `reference.md` | Separate edge cases and scope examples |
| `skills/sync-working-status/` | **modify** | Expand to cover 3 sync targets: local git state, Specs/Plans (`docs/`), remote issue state |
| `skills/http-api-principles/` | modify — add `examples.md` | Separate detailed JSON examples |
| `skills/exception-principles/` | **delete** | Replaced by `exception-and-logging-principles` |
| `skills/exception-and-logging-principles/` | **new** | Combined exception + logging skill |
| `skills/general-naming-principles/` | modify — add `examples.md` | Separate name comparison lists |
| `skills/core-principles/` | **new** | Define the three foundational principles |
| `skills/new-project-setup/` | **new** | Onboarding guide + lefthook template |
| `commands/commit.md` | unchanged | |
| `commands/sync.md` | **modify** | Update steps to reflect all 4 sync targets |
| `agents/principles-reviewer.md` | modify | Add core-principles scope, update exception reference |
| `tests/pressure/conventional-commit/` | **new** | RED/GREEN/REFACTOR scenarios |
| `.githooks/` | **new** | lefthook.yml + shell scripts |

---

## Skill Refactoring Criteria

**Rule: SKILL.md holds the rule set. examples.md holds the evidence.**

| Content type | SKILL.md | examples.md |
|---|---|---|
| Rule statement (imperative) | ✅ | |
| Rationale (1–2 sentences) | ✅ | |
| Inline example (≤ 5 lines) | ✅ | |
| Full code block (> 5 lines) | | ✅ |
| Before/after comparison | | ✅ |
| Edge case walkthrough | | ✅ |
| Reference table (≤ 10 rows) | ✅ | |
| Reference table (> 10 rows) | | ✅ |

**Test:** if removing a block makes a rule ambiguous → keep in SKILL.md. If it only reduces illustration depth → move to examples.md.

SKILL.md target: under 500 lines (per official Claude Code documentation).

---

## Pressure Test Framework

### Location

`tests/pressure/conventional-commit/`

### Structure

```
tests/pressure/conventional-commit/
├── README.md
├── scenarios/
│   └── NNN-<short-title>.md      (one file per scenario, numbered)
└── evaluation-log.md
```

### Scenario File Format

```markdown
# Scenario NNN: <Short Title>

## Setup
<Realistic context that creates temptation to skip the rule>

## Pressure
<Verbatim prompt to paste into the test session>

## Expected RED Behavior (skill NOT loaded)
<Specific failure mode — not just "it fails">

## Expected GREEN Behavior (skill loaded)
<Minimum acceptable output — precise enough to eliminate judgment>

## PASS Criteria
RED PASS if: <agent violates the rule>
GREEN PASS if: <agent complies — specific conditions>
```

### Evaluation Phases

| Phase | Input | PASS means | Action on FAIL |
|-------|-------|-----------|----------------|
| RED | No skill loaded | Agent violates rule (test is valid) | Strengthen scenario pressure |
| GREEN | Skill loaded | Agent complies with rule | Enter REFACTOR — patch skill wording, re-run |

Evaluation is binary: PASS or FAIL. No partial credit.

### Conventional Commit Violation Checklist (GREEN phase)

The following are checkable without judgment:

- Type not from allowed list
- No blank line between subject and body (when body present)
- Breaking change not flagged with `!` or `BREAKING CHANGE:` footer
- Scope contains spaces or is not lowercase

**Removed rules (English-specific, no longer enforced):**
- Description starts with lowercase letter
- Description uses imperative mood
- Description ends with period

---

## lefthook + `.githooks/` Design

### `.githooks/lefthook.yml`

```yaml
commit_msg:
  commands:
    validate-conventional-commit:
      run: bunx commitlint --edit {1}

pre_commit:
  parallel: true
  commands:
    lint:
      run: .githooks/run-if-exists.sh lint
      skip: [merge, rebase]
    format:
      run: .githooks/run-if-exists.sh format
      skip: [merge, rebase]
    test:
      run: .githooks/run-if-exists.sh test
      skip: [merge, rebase]
```

### Commit Message Validation — commitlint

**Rationale (Don't Reinvent the Wheel):** commitlint is a widely-adopted, actively-maintained tool that enforces Conventional Commits out of the box. A custom shell script would duplicate this work and require ongoing maintenance. Use commitlint.

commitlint is configured via `.commitlintrc.yml` in the project root. The base config (`@commitlint/config-conventional`) enforces type/scope structure. English-specific rules are disabled:

```yaml
# .commitlintrc.yml (template — committed to the project)
extends:
  - '@commitlint/config-conventional'
rules:
  subject-case: [0]        # disabled — non-English subjects are valid
  subject-full-stop: [0]   # disabled — trailing period is optional
  # type-enum enforced (allowed types)
  # type-case enforced (lowercase type)
  # scope-case enforced (lowercase scope)
```

**Enforced rules:**
- Type from allowed list (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert)
- Type is lowercase
- Scope is lowercase, no spaces
- Breaking change: `!` or `BREAKING CHANGE:` footer
- Blank line between subject and body (when body present)

**Not enforced (removed as English-specific):**
- Subject starts with lowercase
- Imperative mood
- No trailing period

### `run-if-exists.sh` — Project-Aware Hook Delegation

Receives a task name (`lint`, `format`, `test`). Detects and runs the first match in priority order:

1. `package.json` has matching script → `npm run <task>` (or `yarn`/`pnpm` based on lockfile)
2. `Makefile` has matching target → `make <task>`
3. `.hw0k-workflow/hooks/pre-commit-<task>.sh` exists → execute directly
4. Nothing found → print skip message, exit 0

**Purpose:** any language project (JS, Python, Go, Rust, etc.) gets hook enforcement without configuring the plugin — it discovers the project's existing toolchain.

**For test hooks specifically:** the `.hw0k-workflow/hooks/pre-commit-test.sh` escape hatch is the recommended path for running only change-related tests (not the full suite) on commit. `new-project-setup` guides users to create this script if they want scoped test runs.

**Project-specific escape hatch:**

```
.hw0k-workflow/
  hooks/
    pre-commit-lint.sh
    pre-commit-format.sh
    pre-commit-test.sh     ← run only affected tests, not full suite
```

These files are committed to the project repo (not the plugin repo).

**Global bypass:** `LEFTHOOK=0 git commit` skips all hooks — standard lefthook behavior, no `--no-verify` needed.

---

## `core-principles/SKILL.md` Design

### Section Structure

```
1. Purpose
2. Principle 1 — Environment Independence
3. Principle 2 — Human Gate for Irreversible Operations
4. Principle 3 — Static Verification Over Subjective Assessment
5. Principle 4 — Don't Reinvent the Wheel
6. Integration with principles-reviewer
```

### Per-Principle Format

Each principle section contains:
- **Rule** (imperative sentence)
- **Rationale** (1–2 sentences)
- **Compliant** examples
- **Non-compliant** examples
- **Trigger point** for `principles-reviewer`

### Principle Definitions

**Principle 1 — Environment Independence**

Rule: A change is only valid if it produces identical behavior on every device, agent instance, and tool version it will run on.

Trigger: any command or file change containing an environment assumption (hardcoded path, tool invocation without version check, reference to local state).

**Principle 2 — Human Gate for Irreversible Operations**

Rule: Before executing any irreversible operation, the agent must present the proposed action and receive explicit human approval.

Irreversible: `git push --force`, `git reset --hard`, file deletion outside version control, remote system writes (deploy, publish, database mutation, external notifications).

Trigger: any command that appears in the irreversible list, or any command whose effect on persistent external state cannot be rolled back.

**Principle 3 — Static Verification Over Subjective Assessment**

Rule: Correctness claims must be backed by static analysis results (type checker, linter, test output, schema validator). "Looks right" or "should work" are not acceptable.

Compliant: "TypeScript compiler reports zero errors." "ESLint passes with the project ruleset."
Non-compliant: "The logic seems correct." "This should work based on the pattern I see elsewhere."

Trigger: any verification or correctness claim that does not cite a tool output.

**Principle 4 — Don't Reinvent the Wheel**

Rule: Before implementing a custom solution, verify that a well-maintained tool does not already solve the problem. Prefer established tools when they are actively maintained, widely adopted, and require no significant adaptation.

Rationale: Custom implementations duplicate battle-tested work, require ongoing maintenance, and introduce bugs the ecosystem has already fixed.

Compliant: using commitlint instead of a custom regex commit validator; using lefthook instead of a custom hook manager.
Non-compliant: writing a shell script to validate commit messages when commitlint exists; re-implementing date parsing, UUID generation, or other solved problems.

Exception: the existing tool requires significant adaptation overhead that exceeds the benefit, has a problematic license or security record, or cannot work in the target environment.

Trigger: any new utility, script, or implementation that overlaps with a known, well-maintained open-source solution.

---

## `exception-and-logging-principles/SKILL.md` Design

### Design Rationale

Exception handling and logging are one decision point: when you catch, you also decide what to log and at what level. Organizing them sequentially — classify → catch → log → re-throw/recover — eliminates the need to hold two separate skills open simultaneously.

### Section Structure

```
1. Purpose and Scope
2. Failure Classification
3. Catch Rules
4. Logging Rules
   4.1 Log Levels
   4.2 Structured Log Format
   4.3 Correlation ID Propagation
   4.4 What to Log / What NOT to Log
5. Re-throw and Context Propagation
6. Recovery Strategies
7. Boundary Definition
```

### Key Design Decisions

**Failure Classification (stays in SKILL.md — 3 rows, within limit):**

| Category | Definition | Example |
|----------|-----------|---------|
| Expected | Known, recoverable domain condition | Validation error, not found |
| Unexpected | Outside normal operating envelope | Null dereference, disk full |
| External | Originates in a dependency | Downstream API 500 |

**Log Levels (stays in SKILL.md):**

| Level | When to use |
|-------|------------|
| ERROR | Operation failed, human or automated intervention required |
| WARN | Operation succeeded despite anomaly, or recoverable failure handled |
| INFO | Significant business event completed normally |
| DEBUG | Internal state for problem diagnosis; off by default in production |

**Structured Log Format (required fields):**
```json
{
  "timestamp": "<ISO 8601>",
  "level": "<ERROR|WARN|INFO|DEBUG>",
  "message": "<human-readable summary>",
  "correlationId": "<propagated from entry point>",
  "service": "<service name>",
  "context": {}
}
```

**Boundary Definition:** HTTP handler, message queue consumer, scheduled job entry point, public library API. Internal helpers are not boundaries — they throw, not catch-and-log.

Extended examples (annotated code blocks, multi-layer re-throw chains, retry/circuit-breaker patterns) move to `examples.md`.

---

## `principles-reviewer` Update Design

### Updated Scope

```
1. Core principles    (hw0k-workflow:core-principles)               ← new, first
2. HTTP API design    (hw0k-workflow:http-api-principles)
3. Exception & Logging (hw0k-workflow:exception-and-logging-principles)
4. Naming conventions (hw0k-workflow:general-naming-principles)
```

Core principles leads — process-level violations can invalidate how the other three areas are applied.

### Two Violation Formats

**Code violation** (areas 2–4):
```
`file:line [rule] — what found → what it should be`
```

**Process violation** (area 1 — no file/line, pattern-level):
```
[rule] — observation → expected behavior
```

### Output Structure

```
## Core Principles
### Violations
[rule] — observation → expected behavior
### Passed
- ...

## HTTP API Design
### Violations
`file:line [rule] — what found → what it should be`
### Passed
- ...

## Exception & Logging
...

## Naming Conventions
...
```

---

## `new-project-setup/SKILL.md` Design

### Section Structure

```
1. Purpose
2. Prerequisites
3. Steps
   3.1 Install lefthook
   3.2 Set git hooks path
   3.3 Copy and install lefthook template
   3.4 (Optional) Configure auto-sync
4. run-if-exists.sh Pattern
5. Customizing pre-commit hooks
6. Auto-sync: When to Enable vs Disable
7. Troubleshooting
```

### Onboarding Steps

**Step 1 — Install lefthook (once per machine)**
```bash
brew install lefthook        # macOS/Linux
npm install --save-dev lefthook  # Node projects
go install github.com/evilmartians/lefthook@latest  # Go toolchain
```

**Step 2 — Set git hooks path**
```bash
git config core.hooksPath .githooks
```
This points git to the version-controlled hooks directory, making enforcement consistent across all contributors.

**Step 3 — Copy template and install**
```bash
# Copy the lefthook.yml template from the plugin
cp <hw0k-workflow-plugin-dir>/new-project-setup/lefthook.yml ./lefthook.yml
lefthook install
```
If the project already has a `lefthook.yml`, merge only the sections marked `# hw0k-workflow`.

**Step 4 — (Optional) Configure auto-sync**

Add to `.claude/settings.json` (team-wide) or `.claude/settings.local.json` (personal opt-in):
```json
{
  "hooks": {
    "Stop": [
      { "type": "command", "command": "/hw0k-workflow:sync-working-status" }
    ]
  }
}
```

### `run-if-exists.sh` Pattern

The `run-if-exists.sh` script is how `hw0k-workflow` achieves project-aware enforcement without knowing the project's language or toolchain.

**How it works:**

When lefthook runs `run-if-exists.sh lint`, the script searches in this priority order:

1. `package.json` has a `"lint"` script → `npm run lint`
2. `Makefile` has a `lint` target → `make lint`
3. `.hw0k-workflow/hooks/pre-commit-lint.sh` exists → execute directly
4. None found → print `[hw0k-workflow] No lint script found, skipping.` and exit 0

The same logic applies for `format` and `test`.

**This means:**
- A Node.js project with `"lint": "eslint ."` in `package.json` gets ESLint on commit automatically.
- A Python project with `lint:` in a `Makefile` gets `make lint` automatically.
- Any project can override by dropping a script into `.hw0k-workflow/hooks/`.
- A project with none of the above is unaffected — no errors, no broken commits.

### Customizing Pre-Commit Hooks

For test hooks, running the full test suite on every commit is usually too slow. Create a scoped runner:

```bash
# .hw0k-workflow/hooks/pre-commit-test.sh
#!/bin/bash
# Run only tests related to changed files
changed=$(git diff --cached --name-only --diff-filter=ACM)
# <project-specific logic to run targeted tests>
```

Commit this file to the project repo. `run-if-exists.sh` will detect and use it instead of the generic `npm test` / `make test`.

### Auto-sync: When to Enable vs Disable

**Enable** (team-wide via `settings.json`):
- Active development with hw0k-workflow standards applied continuously
- All contributors use Claude Code with the plugin

**Keep personal** (via `settings.local.json`, gitignored):
- Some contributors prefer manual sync
- Mixed adoption across the team

**Disable** (comment out, do not delete):
```json
{ "type": "command", "command": "# /hw0k-workflow:sync-working-status" }
```
Keeping the commented entry makes re-enabling straightforward.

---

## Implementation Priority

| Priority | Components |
|----------|-----------|
| 1 (highest) | `tests/pressure/conventional-commit/` |
| 2 | Skill refactoring (SKILL.md → main + examples.md split) |
| 3 | `core-principles`, `exception-and-logging-principles`, `principles-reviewer` update |
| 4 | `.githooks/` lefthook config, `new-project-setup` skill |

---

## Out of Scope

- MCP servers, LSP integration
- Shell integration tests (deferred — see `2026-03-27-testing-environment-design.md`)
- Logging aggregation / OpenTelemetry integration (Scope B — not included)
- `marketplace.json`
