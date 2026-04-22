# Universal Skill Support — Pressure Tests

Tests that hexis workflow skills fall back gracefully when running on platforms where Claude Code-specific tools (`AskUserQuestion`, `TaskCreate/Update`, `Agent`) are not available.

## Scenarios

- `001-specify-no-interactive-tools.md` — specify workflow completes using text-response fallbacks
- `002-implement-no-subagent.md` — implement falls back to inline execution when spawn-subagent is unavailable
