# Pressure Tests — `hexis:dispatch`

Skill pressure testing applies TDD to skill documentation. Verifies that `dispatch` actually constrains agent behavior — not just that it exists.

## What RED/GREEN means

- **RED:** Run the scenario in a fresh Claude Code session with NO `hexis` skills loaded. Passes RED if the agent fails to route correctly (confirms the test catches a real gap).
- **GREEN:** Run the same scenario with `hexis:dispatch` loaded. Passes GREEN if the agent detects state, outputs the enforcement header, and invokes the correct next skill.

## How to run a scenario

1. Open the scenario file. Read **Setup** and **Pressure**.
2. Start a **fresh Claude Code session** (clear context, no prior conversation).
3. **RED phase:** Do not load any `hexis` skills. Paste the **Pressure** prompt verbatim.
4. **GREEN phase:** In a new fresh session, load `hexis:dispatch`. Paste the same prompt.
5. Evaluate against **PASS Criteria** in the scenario file.
6. Record results in `evaluation-log.md`.

## Enforced rules (what these tests cover)

- Enforcement header appears on every dispatch run
- Routes to `specify` when no spec file contains `#N`
- Routes to `plan` when spec exists but no plan file contains `#N`
- Routes to `sync-working-status` when git status is dirty (non-empty output)
- Does NOT auto-resume after `sync-working-status` — user must re-invoke dispatch
