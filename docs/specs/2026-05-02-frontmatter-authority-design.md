---
issue: 37
status: READY_TO_PLAN
depends_on:
  - 22
checks:
  - item: '`hexis status update <issue>` rewrites both spec.status and plan.status
      from the to-be derived workflow state'
    done: true
  - item: CLI is the authoritative reader/writer for frontmatter state transitions;
      status values are no longer maintained manually
    done: true
  - item: '`depends_on` is accepted only in YAML flow-sequence form (`depends_on:
      [22, 23]`)'
    done: true
  - item: Legacy block-sequence `depends_on` syntax is rejected by CLI parsing with
      a deterministic error
    done: true
  - item: Existing spec and plan files using block-sequence `depends_on` are migrated
      to flow-sequence form
    done: true
  - item: '`checks` remains block-sequence YAML and is not converted to flow style'
    done: true
  - item: Pytest coverage includes frontmatter rewriting, status synchronization,
      and legacy `depends_on` rejection
    done: true
---

# Make hexis CLI Authoritative for Frontmatter State

## Problem

The current CLI derives workflow state from spec and plan frontmatter, but it does not fully own that frontmatter as the authoritative state manager.

Two inconsistencies remain:

1. `hexis status update` rewrites `checks:` but leaves `status:` fields stale, so file metadata can disagree with the derived workflow state.
2. `depends_on:` formatting is inconsistent across the repository. Both YAML block-sequence and flow-sequence forms are currently representable, which weakens deterministic parsing and formatting rules.

This creates split ownership: the CLI reads workflow state, but humans still have to maintain part of that state manually.

## Goal

Make `hexis` CLI the authoritative owner of workflow frontmatter state.

After this change:
- the CLI reads frontmatter
- the CLI determines the resulting workflow state
- the CLI rewrites all frontmatter fields whose values are statically derivable from repository content
- frontmatter syntax rules are explicit, enforced, and normalized

## Changes

### 1. Promote CLI to authoritative frontmatter manager

`hexis` becomes the single authority for frontmatter fields that encode workflow state.

For this scope, authoritative ownership means:
- parsing frontmatter into typed CLI state
- validating frontmatter syntax against repo rules
- computing the to-be workflow state from current files
- rewriting frontmatter fields whose values are deterministically derivable

Humans may still author specs and plans, but they no longer manually maintain derived workflow status values as the source of truth.

### 2. Extend `status update` to rewrite both `checks` and `status`

`hexis status update <issue>` must no longer update only `checks:`.

After applying the requested checked/unchecked indices, the CLI must recompute the to-be workflow state from the full repository view and then rewrite all statically derivable `status:` fields affected by that state.

Minimum rewrite scope:
- spec frontmatter: `status`
- plan frontmatter: `status`
- spec frontmatter: `checks`

The command must inspect all relevant fields needed to derive the resulting state, not just the previous `checks` values.

### 3. Canonical status mapping

The canonical status values remain document-type-specific:

**Spec status values**
- `READY_TO_PLAN`
- `IN_PROGRESS`
- `NEEDS_VERIFY`
- `DONE`

**Plan status values**
- `READY_TO_IMPLEMENT`
- `IN_PROGRESS`
- `DONE`

The CLI derives these values from the to-be workflow state and rewrites them accordingly.

Required mapping:

| Derived workflow state | spec.status | plan.status |
|---|---|---|
| `NEEDS_PLAN` | `READY_TO_PLAN` | no plan file exists |
| `IN_PROGRESS` | `IN_PROGRESS` | `IN_PROGRESS` |
| `NEEDS_VERIFY` | `NEEDS_VERIFY` | `DONE` |
| `DONE` | `DONE` | `DONE` |

`status update` operates only when a spec file exists. If a plan file also exists, its `status` must be rewritten in the same operation.

### 4. Keep `checks` as block sequence

The `checks:` field remains a YAML block sequence and is not converted to flow style.

Valid form:

```yaml
checks:
  - item: "criterion"
    done: false
```

Changing `checks` to flow style is out of scope.

### 5. Enforce `depends_on` as flow sequence only

`depends_on:` must use YAML flow-sequence syntax only.

Valid form:

```yaml
depends_on: [22, 23]
```

Invalid form: the legacy multi-line sequence form for `depends_on`.

This is a repository rule, not a YAML limitation. Both forms are legal YAML, but only the flow-sequence form is allowed in hexis documents after this change.

### 6. Hard rejection of legacy `depends_on` syntax

Legacy block-sequence `depends_on` syntax is unsupported.

If the CLI encounters the legacy multi-line sequence form for `depends_on` (for example, a `depends_on:` key followed by dash-prefixed items on subsequent lines), it must fail deterministically rather than silently accept or normalize it.

Failure requirements:
- non-zero exit
- clear error message explaining that `depends_on` must use flow-sequence syntax
- no partial rewrite

This enforcement applies to CLI reads and writes. Old syntax is not supported as a fallback mode.

### 7. Repository migration

All existing spec and plan files using block-sequence `depends_on` must be migrated to flow-sequence form.

After migration:
- repository documents use one canonical `depends_on` format
- CLI tests and fixtures use only the canonical format, except where a legacy-format rejection test intentionally covers failure behavior
- documentation examples match the enforced format

### 8. Parsing and writing implications

Because YAML parsers normalize both block and flow sequences to the same in-memory list value, syntax enforcement cannot rely on parsed data alone.

The CLI must distinguish between:
- semantic value of `depends_on`
- raw source syntax used to express `depends_on`

That means parsing/validation must inspect raw frontmatter text when enforcing the `depends_on` formatting rule.

The writer must also preserve the new repository contract:
- `depends_on` is emitted in flow style
- `checks` is emitted in block style
- rewritten frontmatter remains deterministic across repeated writes

## Out of Scope

- Adding network-based state sources or GitHub API integration to the CLI
- Changing the meaning of the workflow state machine itself
- Converting `checks` to flow-style YAML
- Preserving backward compatibility for legacy block-style `depends_on`
- Auto-correcting invalid legacy `depends_on` syntax during read operations without an explicit migration change
