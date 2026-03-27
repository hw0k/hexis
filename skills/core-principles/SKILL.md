---
name: core-principles
description: Four foundational principles governing all hw0k-workflow standards — environment independence, human gate for irreversible operations, static verification, and don't reinvent the wheel
type: reference
---

# Core Principles

These four principles are pre-conditions for all other standards in this plugin. Any skill-specific rule that conflicts with a core principle is overridden by the core principle. Check these before acting, not after.

---

## Principle 1 — Environment Independence

**Rule:** A change is only valid if it produces identical behavior on every device, agent instance, and tool version it will run on. Do not rely on local state, local credentials, locally installed tools, or working directory assumptions that are not explicitly established in the task context.

**Rationale:** Solutions that depend on implicit local conditions introduce failures that are invisible during authoring and expensive to diagnose elsewhere.

**Compliant:**
- Specifying the exact command with its full flag set rather than relying on shell aliases
- Checking for the existence of a required tool before invoking it
- Using relative paths only when the working directory is explicitly set in the same context
- Declaring all dependencies in version-controlled config files (package.json, go.mod, requirements.txt)

**Non-compliant:**
- "This works because I have Node 20 installed" — version assumed, not verified
- Using `~/.config/...` paths without confirming the path exists in the target environment
- Referencing a shell function that exists locally but is not in the repo
- Hardcoding an absolute path that only exists on the author's machine

**`principles-reviewer` trigger:** Any command, script, or file change containing an environment assumption — hardcoded path, tool invocation without version check, reference to local state not established in the task context.

---

## Principle 2 — Human Gate for Irreversible Operations

**Rule:** Before executing any operation that cannot be fully undone, present the proposed action and receive explicit human approval. A single confirmation is the minimum. Proceed only on unambiguous, explicit consent — not inferred or prior approval.

**Rationale:** Irreversible operations have asymmetric cost. The cost of an unnecessary confirmation is low. The cost of an unconfirmed mistake can be unbounded.

**What counts as irreversible:**
- `git push --force`, `git reset --hard`, `git branch -D`
- File deletion or overwrite of a file not tracked by version control
- Any write to a remote system: deploy, publish, database mutation
- Sending an external notification: email, webhook, Slack message
- Dropping or truncating a database table or collection

**Compliant:**
- Showing the exact command to be run, explaining its effect, and waiting for an explicit "yes"
- Listing all files to be deleted before deleting any of them

**Non-compliant:**
- Proceeding with a force-push because the user said "fix the branch" without specifying the method
- Treating a previous approval (from an earlier turn) as approval for a new operation of the same type

**`principles-reviewer` trigger:** Any command in the irreversible list, or any command whose effect on persistent external state cannot be rolled back within the current session.

---

## Principle 3 — Static Verification Over Subjective Assessment

**Rule:** When asserting that code is correct, a change is safe, or a configuration is valid, back the assertion with a static analysis result — type checker output, linter result, test output, schema validator result. "Looks right" or "should work" are not acceptable verification statements.

**Rationale:** Subjective assessment introduces unverifiable confidence. Static tools produce repeatable, auditable results that another agent or human can inspect independently.

**Compliant:**
- "TypeScript compiler reports zero errors on this file after the change."
- "ESLint passes with the project ruleset: `npm run lint` exits 0."
- "All 47 tests pass: `npm test` exits 0."

**Non-compliant:**
- "The logic seems correct."
- "This should work based on the pattern I see elsewhere."
- "I reviewed it and it looks fine."
- "This is a simple change, no testing needed."

When a static tool is not available for the domain, state this explicitly: "No static validator is available for this config format. Manual review required."

**`principles-reviewer` trigger:** Any verification or correctness claim that does not cite a tool output.

---

## Principle 4 — Don't Reinvent the Wheel

**Rule:** Before implementing a custom solution, verify that a well-maintained tool does not already solve the problem. Prefer established tools when they are actively maintained, widely adopted, and require no significant adaptation.

**Rationale:** Custom implementations duplicate battle-tested work, require ongoing maintenance, and introduce bugs the ecosystem has already fixed.

**Compliant:**
- Using commitlint instead of a custom regex-based commit message validator
- Using lefthook instead of a custom hook management script
- Using an established date library instead of re-implementing date arithmetic

**Non-compliant:**
- Writing a shell script to validate commit messages when commitlint exists and covers the same rules
- Re-implementing UUID generation, pagination utilities, or other solved problems
- Building a custom CI step when a maintained GitHub Action already exists for the task

**Exception:** the existing tool requires significant adaptation overhead that exceeds the benefit, has a problematic license or security record, or cannot work in the target environment. Document the exception and its reason.

**`principles-reviewer` trigger:** Any new utility, script, or implementation that overlaps with a known, well-maintained open-source solution.
