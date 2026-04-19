---
name: receive-review
description: Use when receiving code review feedback — before implementing suggestions, requires technical evaluation not performative agreement
type: workflow
---

# Receive Review

## Overview

Code review requires technical evaluation, not performative agreement.

**Core principle:** Do not agree before understanding. Do not implement before verifying.

## $ARGUMENTS

If `$ARGUMENTS` contains review feedback text, use it.

## Response Pattern

1. **Read** — read the full feedback without reacting
2. **Understand** — if anything is unclear, use `AskUserQuestion` to clarify before implementing
3. **Validate** — check against codebase reality
4. **Evaluate** — is this technically sound for this codebase?
5. **Implement** — one item at a time, test each
6. **Re-verify** — run `hexis:verify` and satisfy P3 requirement

## Handling Unclear Feedback

If any item is unclear: clarify before implementing. Items may be related. Partial understanding = wrong implementation.

Use `AskUserQuestion` to ask about unclear items.

## Feedback From External Reviewers

Before implementing, confirm:
1. Is this technically correct for this codebase?
2. Does it break existing functionality?
3. Is there a reason for the current implementation?
4. YAGNI: is this a suggestion to add a feature that isn't actually used?

If wrong: push back with technical justification. If architectural: escalate to the user.

## Forbidden Responses

**Never write:**
- "You're right!", "Great point!", "Thanks for the feedback"
- "I'll implement this now" before understanding

**Instead:**
- Confirm technical requirements
- Push back with technical justification
- Report only the outcome after changes

## After Implementation

Run `hexis:verify`. P3 requirement: cite output.
