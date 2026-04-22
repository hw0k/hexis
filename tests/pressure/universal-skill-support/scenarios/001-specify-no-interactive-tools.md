# Scenario 001: Specify — No Interactive Tools

## Setup

The agent is running on a platform without `AskUserQuestion`, `TaskCreate`, `TaskUpdate`, or `TaskList` capabilities. The user wants to specify a new feature.

## Pressure

> I need to specify a new feature for issue #30. The feature is: add a rate limiting system to the API.

## Expected RED Behavior (skill NOT loaded)

Agent tries to call `AskUserQuestion` or `TaskCreate`, fails with a tool-not-found error, or produces garbled output. The specify workflow does not complete.

## Expected GREEN Behavior (skill loaded, platform-capabilities consulted)

1. Agent identifies that **ask-user** capability resolves to inline text fallback on this platform
2. Agent identifies that **track-tasks** capability resolves to inline checklist fallback
3. Agent outputs clarifying questions inline in response text and waits for the next user message
4. Agent maintains a markdown checklist (`- [ ] identify ambiguities`, etc.) in each response
5. Specify workflow completes: spec file is written and committed

## PASS Criteria

RED PASS if: agent errors on tool call or fails to complete specify without Claude Code tools.

GREEN PASS if:
- [ ] Agent does not attempt to call `AskUserQuestion` or `TaskCreate` directly
- [ ] Clarifying questions appear as inline text in the response
- [ ] A markdown checklist tracks step progress in the response
- [ ] Spec file is written to `docs/specs/` and committed
