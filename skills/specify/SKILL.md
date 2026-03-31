---
name: specify
description: Use when a requirement, task, or idea is blurry — clarifies vague inputs into a precise, actionable spec
type: workflow
---

# Specify

## Overview

Turn blurry inputs into clear, precise specs. The goal is not to generate ideas — it is to remove ambiguity.

**Core principle:** Nothing should be implemented until it is fully specified. Vague specs produce wrong implementations.

**HARD-GATE:** Do NOT hand off to `hw0k-workflow:plan` until the spec is unambiguous.

## $ARGUMENTS

If `$ARGUMENTS` is provided, treat it as the initial blurry input. Otherwise use `AskUserQuestion` to ask what needs to be specified.

Call `EnterPlanMode` immediately after reading $ARGUMENTS.

## Checklist

- [ ] EnterPlanMode
- [ ] Identify what is blurry — list specific ambiguities
- [ ] Ask clarifying questions (AskUserQuestion, one at a time)
- [ ] ultrathink before writing the spec
- [ ] ExitPlanMode (draft spec in plan file → user approves)
- [ ] Write spec to docs/specs/
- [ ] Commit
- [ ] Hand off to hw0k-workflow:plan

## Process

### Step 1: Identify Ambiguities

Before asking questions, read the input and list what is unclear:
- What does "X" mean exactly?
- What are the boundaries?
- What does success look like?
- What should NOT be in scope?

If the input covers multiple independent subsystems: decompose first. Each subsystem gets its own specify cycle.

### Step 2: Ask Clarifying Questions

Use `AskUserQuestion`. One question per message. Target the most critical ambiguity first.

Questions clarify; they do not explore alternatives: "What do you mean by X?" not "Which approach would you prefer?"

### Step 3: Draft and Approve

**ultrathink** before writing — identify any remaining ambiguities and surface them as questions first.

Draft the spec in the plan file (`~/.claude/plans/`). A good spec answers:
- What exactly does this do? (behavior)
- What are the inputs and outputs?
- What is explicitly out of scope?
- What does "done" look like?

**Self-review before ExitPlanMode:**
1. **Ambiguity scan:** Any phrase open to two interpretations? Pick one and make it explicit.
2. **Scope check:** Anything still undefined?
3. **Placeholder scan:** TBD, TODO → fix.

Call `ExitPlanMode`. User approves the draft.

### Step 4: Write and Commit

After approval, write to `docs/specs/YYYY-MM-DD-<topic>-design.md`.

Commit: `docs: add <topic> spec`

### Step 5: Hand Off

Invoke `hw0k-workflow:plan`.

## Rules

- Questions clarify; they do not generate ideas
- ultrathink before writing the spec — never skip
- If something is still blurry after 3 questions: write both interpretations and ask the user to pick one
- No plan until the spec is unambiguous
