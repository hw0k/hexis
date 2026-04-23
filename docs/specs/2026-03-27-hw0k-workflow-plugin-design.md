---
---

# hw0k-workflow Plugin Design

> **Historical document.** This spec reflects the initial design state. Some skill names have since been renamed (e.g., `conventional-commit` → `commit-principles`, `new-project-setup` → `setup-new-project`).

**Date:** 2026-03-27
**Status:** Approved

## Summary

`hw0k-workflow` is a heavily opinionated Claude Code plugin covering the full development workflow — from spec to merge. It defines *what standards to apply* (content/principles) across the entire development lifecycle.

---

## Problem

Without a dedicated plugin, the following are left unenforced:
- Commit message format at commit time
- Status synchronization across multiple providers (Local, GitHub, etc.)
- Opinionated HTTP API design standards
- Opinionated exception handling standards
- Opinionated naming conventions

These gaps cause inconsistency across projects and require repeated manual correction.

---

## Scope

| Component | hw0k-workflow |
|-----------|---------------|
| Brainstorm → Plan → Implement | ✅ |
| How to integrate work (merge, PR, cleanup) | ✅ |
| **Commit message format enforcement** | ✅ |
| **Multi-provider status sync** | ✅ |
| **HTTP API design principles** | ✅ |
| **Exception handling principles** | ✅ |
| **Naming conventions** | ✅ |
| Code review against plan | ✅ |
| **Code review against principles** | ✅ |

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
│   └── sync.md                  # /hw0k-workflow:sync-working-status
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
| `sync.md` | `/hw0k-workflow:sync-working-status` | `sync-working-status` skill |

Workflow skills (`conventional-commit`, `sync-working-status`) are exposed as commands because they are user-initiated actions tied to specific development cycle events, not passive reference guides.

Principle skills (`http-api-principles`, `exception-principles`, `general-naming-principles`) are skills only — they are referenced automatically by Claude when developing, not user-triggered.

### Agent (1)

| Agent | Invocation | Purpose |
|-------|-----------|---------|
| `principles-reviewer` | Via `Agent` tool | Consolidates review against all three principles |

The `principles-reviewer` agent reviews code against the three principle skills simultaneously, providing the specific opinionated standards.

---

## Plugin Metadata

```json
{
  "name": "hw0k-workflow",
  "description": "Heavily opinionated common workflow plugin for Claude — covering the full development workflow — from spec to merge.",
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
