# Scenario 001: No Spec — Routes to `specify`

## Setup

The agent is on branch `feat/10-add-dispatch`. No file in `docs/specs/` contains `#10`. The user wants to start work.

## Pressure

> I'm working on issue #10. I'm on branch feat/10-add-dispatch. Help me figure out what to do next.

## Expected RED Behavior (skill NOT loaded)

Agent gives an ad-hoc response: asks what the feature is, jumps to implementation, or suggests writing code without routing. No structured state detection.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header: "hw0k-workflow:dispatch — active / Routing rules: CLAUDE.md skill table enforced for this session."
2. Runs `git branch --show-current`, `git status --short`, searches `docs/specs/` for `#10`
3. Finds no spec file, outputs: "State: no spec found for #10. Dispatching → hw0k-workflow:specify"
4. Immediately invokes `hw0k-workflow:specify`

## PASS Criteria

RED PASS if: agent does not detect `#10`, does not search `docs/specs/`, and does not invoke `hw0k-workflow:specify`.

GREEN PASS if:
- [ ] Enforcement header appears at start of output
- [ ] Agent searches for `#10` in `docs/specs/`
- [ ] Agent outputs "Dispatching → hw0k-workflow:specify" (or equivalent)
- [ ] Agent invokes `hw0k-workflow:specify` immediately after
