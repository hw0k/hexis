# Universal Skill Support

Issue: #16

## What

Evolve all hexis skills so a single `SKILL.md` serves Claude Code, Codex, OpenClaw, and future AI coding platforms. No per-platform file splits — the single-file constraint is hard (Claude Code's skill loader is file-based). Platform-specific behavior is expressed inline via two patterns.

Skills describe what they need using capability names — not platform-specific tool names. The `platform-capabilities` reference skill is the single place where capability names map to concrete tools per platform.

## Platform Inference

No explicit detection step in any skill. Each agent infers its platform from available tools and system context. Skill content documents all variants; the agent self-selects what applies to its environment.

## New Artifact: `platform-capabilities` Reference Skill

Create `skills/platform-capabilities/SKILL.md` (`type: reference`) — the canonical capability map across known platforms.

### Capability Map

| Capability | Claude Code | Codex | OpenClaw | Generic fallback |
|---|---|---|---|---|
| **ask-user** — pose a question and wait for input | TBD | TBD | TBD | Inline question in response text; wait for next message |
| **track-tasks** — record and update step progress | TBD | TBD | TBD | Inline markdown checklist in current response |
| **spawn-subagent** — delegate work to a parallel agent | TBD | TBD | TBD | Execute sequentially in current context |
| **worktree** — isolate work in a git worktree | TBD | TBD | TBD | `git worktree add .worktrees/<branch> -b <branch>` |
| **read-file** — read a file from the filesystem | TBD | TBD | TBD | Shell `cat` |
| **edit-file** — make targeted edits to a file | TBD | TBD | TBD | Shell-based file write |
| **run-shell** — execute shell commands | TBD | TBD | TBD | Platform shell equivalent |

TBD entries in non-generic columns are acceptable at initial merge. They are filled as concrete equivalents are confirmed per platform.

## Skill Update Patterns

### Pattern 1: Graceful Degradation

Use when a capability exists on all platforms but requires different mechanisms. Reference the capability name; the agent resolves the concrete method from `platform-capabilities`:

```markdown
## Spawning a subagent

Use the **spawn-subagent** capability (see `hexis:platform-capabilities`).
If unavailable, execute sequentially in the current context.
```

### Pattern 2: Platform-Specific Branching

Use when behavior must differ structurally. Describe what each platform should do without naming tools:

```markdown
## Worktree Setup

Use the **worktree** capability (see `hexis:platform-capabilities`).
```

For steps where no generic fallback exists and platform behavior is genuinely incompatible, use explicit conditional prose:

```markdown
If **worktree** capability is available: isolate work in a dedicated worktree before proceeding.
If not: proceed in the current working directory, noting the lack of isolation.
```

## Skills in Scope

### Group 1: Principles (audit only)

`core-principles`, `http-api-principles`, `exception-and-logging-principles`, `general-naming-principles`, `commit-principles`

These are `type: reference` with no procedural steps. Verify each file contains no platform-specific references. Mark as confirmed if clean; update only if a reference is found.

### Group 2: Planning

`specify`, `plan`

Replace any platform-specific tool references with capability names. Add a fallback note for **ask-user** (inline question pattern) and **track-tasks** (inline checklist pattern) where these capabilities are used.

### Group 3: Verification and Review

`verify`, `review`, `receive-review`

Audit for platform-specific tool references. Replace with capability names and add fallback notes where found.

### Group 4: Execution

`implement`, `use-worktree`, `finish`

Replace platform-specific tool references with capability names. Add explicit conditional prose (Pattern 2) for **spawn-subagent** and **worktree** where behavior must structurally differ.

## Out of Scope

- `dispatch`, `sync-working-status`, `debug`, `setup-new-project`, `write-test` — deferred to a follow-up
- Resolving all TBD entries in the capability map before shipping
- Per-platform SKILL.md file splits

## Done When

- [ ] `skills/platform-capabilities/SKILL.md` created with capability map (generic fallback column complete; platform-specific columns TBD-allowed)
- [ ] All 5 principle skills confirmed platform-agnostic (no changes, or documented changes if a reference is found)
- [ ] `specify` and `plan` updated: platform-specific tool references replaced with capability names and fallback notes
- [ ] `verify`, `review`, `receive-review` updated: platform-specific tool references replaced with capability names and fallback notes
- [ ] `implement`, `use-worktree`, `finish` updated: platform-specific tool references replaced with capability names; Pattern 2 applied for spawn-subagent and worktree
- [ ] Pressure test scenario added at `tests/pressure/universal-skill-support/`
