# Pressure Tests — `conventional-commit`

Skill pressure testing applies TDD to skill documentation. The goal is to verify that the `conventional-commit` skill actually constrains agent behavior — not just that it exists.

## What RED/GREEN means

- **RED:** Run the scenario in a fresh Claude Code session with NO `hw0k-workflow` skills loaded. The scenario **passes RED** if the agent violates the rule (confirming the test catches a real failure mode).
- **GREEN:** Run the same scenario in a session with `hw0k-workflow:conventional-commit` loaded. The scenario **passes GREEN** if the agent complies with the rule.

A scenario that **fails RED** (agent follows the rule without the skill) means the pressure is too weak. Strengthen the setup.

A scenario that **fails GREEN** (agent breaks the rule even with the skill) means the skill has a loophole. Enter **REFACTOR**: document the failure in a `## Loopholes Found` section in the scenario file, patch the skill wording, and re-run until GREEN passes.

## How to run a scenario

1. Open the scenario file. Read **Setup** and **Pressure**.
2. Start a **fresh Claude Code session** (clear context, no prior conversation).
3. **RED phase:** Do not load any `hw0k-workflow` skills. Paste the **Pressure** prompt verbatim.
4. **GREEN phase:** In a new fresh session, load `hw0k-workflow:conventional-commit`. Paste the same prompt.
5. Evaluate against **PASS Criteria** in the scenario file.
6. Record results in `evaluation-log.md`.

## Enforced rules (what these tests cover)

- Type must be from the allowed list: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Scope must be lowercase, no spaces
- Description must be imperative mood (not past tense)
- Korean (or author's primary language) is allowed in description and body
- Issue prefix `#{number}` belongs in the subject line, not the footer
- Breaking change must use `!` or `BREAKING CHANGE:` footer

## How to add a new scenario

1. Increment the scenario number. Copy the template below.
2. The **Pressure** section must be a verbatim prompt that creates genuine temptation.
3. **PASS Criteria** must be binary and checkable without judgment.

```markdown
# Scenario NNN: <Short Title>

## Setup
<Realistic context that makes rule-following uncomfortable>

## Pressure
<Verbatim prompt to paste into the test session>

## Expected RED Behavior (skill NOT loaded)
<Specific failure mode>

## Expected GREEN Behavior (skill loaded)
<Minimum acceptable output>

## PASS Criteria
RED PASS if: <agent violates the rule>
GREEN PASS if: <specific, checkable conditions>
```
