# hw0k-workflow Plugin Design

**Date:** 2026-03-27
**Status:** Approved

## Summary

`hw0k-workflow` is a heavily opinionated Claude Code plugin that covers the full development workflow. hw0k-workflow defines both workflow process and coding standards.

---

## Problem

The existing workflow covers the full development lifecycle process but does not enforce:
- Commit message format at commit time
- Status synchronization across multiple providers (Local, GitHub, etc.)
- Opinionated HTTP API design standards
- Opinionated exception handling standards
- Opinionated naming conventions

These gaps cause inconsistency across projects and require repeated manual correction.

---

## Scope

| Component | existing workflow | hw0k-workflow |
|-----------|-------------|---------------|
| Brainstorm → Plan → Implement | ✅ | — |
| How to integrate work (merge, PR, cleanup) | ✅ `finishing-a-development-branch` | — |
| **Commit message format enforcement** | ❌ | ✅ |
| **Multi-provider status sync** | ❌ | ✅ |
| **HTTP API design principles** | ❌ | ✅ |
| **Exception handling principles** | ❌ | ✅ |
| **Naming conventions** | ❌ | ✅ |
| Code review against plan | ✅ `code-reviewer` agent | — |
| **Code review against principles** | ❌ | ✅ |

---

## Repository Structure

```
hw0k-workflow/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── skills/
│   ├── conventional-commit/
│   │   └── SKILL.md             # Commit message format guide
│   ├── sync-working-status/
│   │   └── SKILL.md             # Local/GitHub status sync
│   ├── http-api-principles/
│   │   └── SKILL.md             # HTTP API design principles
│   ├── exception-principles/
│   │   └── SKILL.md             # Exception handling principles
│   └── general-naming-principles/
│       └── SKILL.md             # Naming conventions
├── commands/
│   ├── commit.md                # /hw0k-workflow:commit
│   └── sync.md                  # /hw0k-workflow:sync
├── agents/
│   └── principles-reviewer.md  # Consolidates all principle checks
└── README.md
```

---

## Components

### Skills (5)

All skills use the flat namespace: `hw0k-workflow:{skill-name}`.

| Skill | Trigger point | Purpose |
|-------|--------------|---------|
| `conventional-commit` | Pre-commit | Enforce Conventional Commits format |
| `sync-working-status` | On demand | Sync work state across Local/GitHub |
| `http-api-principles` | During development | HTTP API design standards |
| `exception-principles` | During development | Exception handling standards |
| `general-naming-principles` | During development | Naming conventions |

Skills are reference guides Claude reads automatically or on demand. They do not execute code; they guide Claude's behavior.

### Commands (2)

Commands are slash commands that the user invokes explicitly at specific points in the development cycle.

| Command | Invocation | Delegates to |
|---------|-----------|-------------|
| `commit.md` | `/hw0k-workflow:commit` | `conventional-commit` skill |
| `sync.md` | `/hw0k-workflow:sync` | `sync-working-status` skill |

Workflow skills (`conventional-commit`, `sync-working-status`) are exposed as commands because they are user-initiated actions tied to specific development cycle events, not passive reference guides.

Principle skills (`http-api-principles`, `exception-principles`, `general-naming-principles`) are skills only — they are referenced automatically by Claude when developing, not user-triggered.

### Agent (1)

| Agent | Invocation | Purpose |
|-------|-----------|---------|
| `principles-reviewer` | Via `Agent` tool | Consolidates review against all three principles |

The `principles-reviewer` agent reviews code against the three principle skills simultaneously. This is complementary to `hw0k-workflow:review` (plan alignment + general quality) — it provides the specific opinionated standards.

---

## Plugin Metadata

```json
{
  "name": "hw0k-workflow",
  "description": "Heavily opinionated common workflow plugin for Claude — covers the full development workflow.",
  "version": "0.1.0",
  "keywords": [
    "workflow",
    "conventional-commit",
    "http-api",
    "principles",
    "opinionated"
  ]
}
```

No `marketplace.json` needed — this is a single-plugin GitHub public repository.

---

## Distribution

- GitHub public repository
- Install: `/plugin install hw0k-workflow --plugin-dir github:hw0k/hw0k-workflow`
- No marketplace catalog required

---

## Out of Scope

- MCP servers (`.mcp.json`)
- LSP integration (`.lsp.json`)
- Session hooks (`hooks/hooks.json`) — may be added in a later version when skills mature
- `marketplace.json` — single plugin, not a catalog
