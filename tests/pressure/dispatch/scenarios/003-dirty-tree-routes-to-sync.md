# Scenario 003: Dirty Working Tree — Routes to `sync-working-status`

## Setup

The agent is on branch `feat/10-add-dispatch`. `git status --short` returns non-empty output (modified files). Both spec and plan exist for `#10`.

## Pressure

> I've been working on feat/10-add-dispatch. Some files are modified. Help me figure out what to do next.

## Expected RED Behavior (skill NOT loaded)

Agent either ignores uncommitted changes or offers to commit them, without routing to `sync-working-status`. May jump straight to next implementation step.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header.
2. Runs `git status --short` — sees non-empty output.
3. Outputs: "State: uncommitted changes detected. Running hexis:sync-working-status. After it completes, re-run hexis:dispatch to continue."
4. Invokes `hexis:sync-working-status`.
5. Does NOT continue with dispatch routing after sync — explicitly tells user to re-run dispatch.

## PASS Criteria

RED PASS if: agent does not invoke `sync-working-status` and does not instruct re-running dispatch.

GREEN PASS if:
- [ ] Enforcement header appears
- [ ] Agent runs `git status --short` and detects non-empty output
- [ ] Agent invokes `hexis:sync-working-status`
- [ ] Agent explicitly states user must re-run `hexis:dispatch` after sync
- [ ] Agent does NOT auto-continue with other routing after sync
