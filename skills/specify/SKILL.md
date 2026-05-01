---
name: specify
description: Use when a requirement, task, or idea is blurry — clarifies vague inputs into a precise, actionable spec
type: workflow
---

# Specify

## Overview

Turn blurry inputs into clear, precise specs. The goal is not to generate ideas — it is to remove ambiguity.

**Core principle:** Nothing should be implemented until it is fully specified. Vague specs produce wrong implementations.

**HARD-GATE:** Do NOT hand off to `hexis:plan` until the spec is unambiguous.

## $ARGUMENTS

If `$ARGUMENTS` is provided, treat it as the initial blurry input. Otherwise ask the user what needs to be specified.

## CLI Integration Gate

If an issue number is known from `$ARGUMENTS` or session context (e.g., the current branch is `feat/23-something`):

1. Run: `hexis status read <issue>`
2. If output shows `STATE: NEEDS_SPEC`: proceed.
3. If output shows any other state: a spec already exists for this issue. Surface the full CLI output verbatim to the user and ask for explicit confirmation before overwriting. Do not proceed without confirmation.

If no issue number is known (genuinely new work with no GitHub issue yet): skip this gate and proceed.

## Checklist

- [ ] Identify what is blurry — list specific ambiguities
- [ ] Ask clarifying questions
- [ ] ultrathink before writing the spec
- [ ] Write spec to docs/specs/
- [ ] Commit
- [ ] Hand off to hexis:plan

## Process

### Step 1: Identify Ambiguities

Before asking questions, read the input and list what is unclear:
- What does "X" mean exactly?
- What are the boundaries?
- What does success look like?
- What should NOT be in scope?

If the input covers multiple independent subsystems, or the spec grows too large to be independently implementable as a single unit: decompose.

**On decomposition:**
1. Propose the N units to the user. Do not proceed until confirmed.
2. Write N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
3. Create N GitHub Issues: `gh issue create --title "<unit name>" --body $'<scope>\n\nDecomposed from: #<original>'`
4. If an original issue exists, close it: `gh issue close <number> --comment "Decomposed into: #X, #Y, ..."`
5. Each unit then enters its own Plan cycle independently.

### Step 2: Ask Clarifying Questions

Ask the user. Group related ambiguities into a single request when possible.

Questions clarify; they do not explore alternatives: "What do you mean by X?" not "Which approach would you prefer?"

### Step 3: Draft

**ultrathink** before writing — identify any remaining ambiguities and surface them as questions first.

A good spec answers:
- What exactly does this do? (behavior)
- What are the inputs and outputs?
- What is explicitly out of scope?
- What does "done" look like?

**Self-review before writing:**
1. **Ambiguity scan:** Any phrase open to two interpretations? Pick one and make it explicit.
2. **Scope check:** Anything still undefined?
3. **Placeholder scan:** TBD, TODO → fix.

### Step 4: Write and Commit

**MANDATORY — do this immediately after approval, before anything else.**

Write to `docs/specs/YYYY-MM-DD-<topic>-design.md`. The file must match `docs/templates/spec.md`. The file must begin with:

```markdown
---
issue: N
status: READY_TO_PLAN
depends_on: [M, ...]   # optional — omit if no dependencies
checks:
  - item: "criterion description"
    done: false
---

# <Title>
```

Where `N` is the GitHub issue number this spec addresses (bare integer, no `#`). If there is no associated issue, omit `issue:`. The `issue: N` frontmatter field is required for `hexis:dispatch` to locate the spec by issue number. `depends_on` lists issue numbers this spec depends on (bare integers); omit if none.

**HARD RULE:** The `## Done Criteria` body section is FORBIDDEN. All acceptance criteria MUST be defined in `checks:` frontmatter as a list of `{item, done}` objects. A spec file with a `## Done Criteria` body section is malformed.

Commit: `docs: add <topic> spec`

Do NOT proceed to Step 5 until the spec file exists and is committed.

### Step 5: Hand Off

**HARD-GATE:** Before invoking `hexis:plan`, verify the spec file exists. Run `ls docs/specs/` and confirm the file is present and committed. If it is not, return to Step 4.

Invoke `hexis:plan`.

## Rules

- Questions clarify; they do not generate ideas
- ultrathink before writing the spec — never skip
- If something is still blurry after 3 questions: write both interpretations and ask the user to pick one
- No plan until the spec is unambiguous
- If the user requests to skip writing the spec file: ask the user to confirm. Only proceed without a spec file with explicit user confirmation, and note the skip explicitly.
