# Scenario 002: Spec Exists, No Plan — Routes to `plan`

## Setup

The agent is on branch `feat/10-add-dispatch`. `docs/specs/2026-04-06-dispatch-skill-design.md` contains `#10`. No file in `docs/plans/` contains `#10`. Git is clean.

## Pressure

> I'm on feat/10-add-dispatch. I've already written the spec. What's next?

## Expected RED Behavior (skill NOT loaded)

Agent says "let's start implementing" or asks about requirements. Does not check `docs/plans/` for a plan file.

## Expected GREEN Behavior (skill loaded)

1. Outputs enforcement header.
2. Runs state detection: `git status --short` returns empty (clean). Searches `docs/specs/` for `#10` — finds the file. Searches `docs/plans/` for `#10` — finds nothing.
3. Outputs: "State: spec exists for #10, no plan found. Dispatching → hw0k-workflow:plan"
4. Immediately invokes `hw0k-workflow:plan`.

## PASS Criteria

RED PASS if: agent does not check `docs/plans/` for `#10` and does not invoke `hw0k-workflow:plan`.

GREEN PASS if:
- [ ] Enforcement header appears
- [ ] Agent confirms git is clean before checking docs
- [ ] Agent searches `docs/plans/` for `#10`
- [ ] Agent outputs "Dispatching → hw0k-workflow:plan"
- [ ] Agent invokes `hw0k-workflow:plan` immediately
