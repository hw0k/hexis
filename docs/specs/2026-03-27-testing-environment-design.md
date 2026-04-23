---
status: DONE
---

# Testing Environment Design

> **Historical document.** This spec compares testing approaches from a prior tooling setup with hw0k-workflow. References to the previous tooling are preserved as research context.

**Date:** 2026-03-27
**Status:** In progress — implementation deferred pending skill content changes

---

## Context

The prior tooling has two distinct testing mechanisms. This document records what was learned and what was decided for hw0k-workflow.

---

## Prior Tooling Testing Mechanisms

### 1. Shell-Based Integration Tests (`tests/claude-code/`)

Runs real `claude` headless sessions and verifies behavior by parsing JSONL session transcripts.

- Verifies: skill invocation, subagent dispatch, file creation, test pass/fail, git commits
- Execution time: 10–30 minutes per test
- Requires: `claude` CLI installed, plugin loaded via `settings.json`, `--permission-mode bypassPermissions`
- Used for: complex workflow skills (e.g., `subagent-driven-development`)

### 2. Skill Pressure Testing (`skills/writing-skills/testing-skills-with-subagents.md`)

TDD applied to skill documentation. Run scenarios without the skill (RED), add skill (GREEN), close loopholes (REFACTOR).

- Verifies: that discipline-enforcing skills resist rationalization under pressure
- Execution time: minutes (conversation-only, no headless sessions)
- Used for: skills with rules agents have incentive to bypass

---

## hw0k-workflow Skill Inventory

| Skill | Type | Testable? |
|-------|------|-----------|
| `conventional-commit` | Workflow / rule-enforcing | Yes — pressure testing |
| `sync-working-status` | Workflow | Low priority |
| `http-api-principles` | Reference / principle | No — pure reference |
| `exception-principles` | Reference / principle | No — pure reference |
| `general-naming-principles` | Reference / principle | No — pure reference |
| `principles-reviewer` (agent) | Agent | Yes — integration test |

---

## Prior Tooling Commit Convention Coverage

The prior tooling has **no dedicated commit skill or command**. Commit message format examples appear only in its reference docs — they happen to match Conventional Commits format but are not enforced. hw0k-workflow's `conventional-commit` skill and `/commit` command fill this gap intentionally.

---

## Decisions

### What to test and when

| Target | Method | Timing | Rationale |
|--------|--------|--------|-----------|
| `conventional-commit` | Skill pressure testing | **Now** | Rules are fixed (CC 1.0.0 spec), cost is low, enforcement compliance is unknown |
| `principles-reviewer` | Shell integration test | **After principle skills stabilize** | Skill content still evolving; integration test would need frequent revision |
| Full shell test infrastructure | Shell integration tests | **After skill count grows** | Current scale doesn't justify the setup overhead |

### Trigger for integration test infrastructure

Add shell-based integration tests when principle skills (`http-api-principles`, `exception-principles`, `general-naming-principles`) are no longer actively being revised — i.e., when real usage has validated their content.

---

## Notes

- Integration tests must run from the plugin directory (not temp dirs) so skills load correctly
- Token cost per integration test run: ~$4–5 based on prior tooling benchmarks
- Pressure testing for `conventional-commit` can begin immediately with no infrastructure changes