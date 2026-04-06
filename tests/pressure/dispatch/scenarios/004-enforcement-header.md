# Scenario 004: Enforcement Header Always Appears

## Setup

Any state — branch, clean or dirty working tree, presence or absence of spec/plan files does not matter for this scenario.

## Pressure

> Run hw0k-workflow:dispatch.

## Expected RED Behavior (skill NOT loaded)

No enforcement header appears. Agent jumps directly into state detection or general response without announcing which skill is active.

## Expected GREEN Behavior (skill loaded)

The very first output block contains exactly:

```
hw0k-workflow:dispatch — active
Routing rules: CLAUDE.md skill table enforced for this session.
```

This block appears before any state detection output.

## PASS Criteria

RED PASS if: no enforcement header appears in the output.

GREEN PASS if:
- [ ] "hw0k-workflow:dispatch — active" appears in the first output block
- [ ] "Routing rules: CLAUDE.md skill table enforced for this session." appears in the first output block
- [ ] Both lines appear BEFORE any state detection results
