---
title: Plan Decomposition and Spec–Issue Alignment
issue: "#6"
---

# Plan Decomposition and Spec–Issue Alignment

## Problem

`plan` produces one monolithic plan file regardless of whether the work contains independent subsystems. All tasks execute serially. There is no mechanism to identify parts that could be developed and merged in parallel. Additionally, the relationship between GitHub Issues, Spec files, and Plan files is implicit and inconsistent.

## Core Rule: 1 Spec = 1 Issue

Every GitHub Issue corresponds to exactly one Spec file, and vice versa. This is the invariant that all skills must maintain.

- Issues and Specs may be created in either order (user-first or spec-first). `sync-working-status` is responsible for reconciling their bidirectional state.
- A Plan always has exactly one parent Spec.

## Spec–Plan Link

Every Plan file must declare its parent Spec via a `linked_spec` frontmatter field:

```yaml
---
linked_spec: docs/specs/YYYY-MM-DD-<topic>-design.md
---
```

- Applies to **all** Plan files — single-unit and decomposed alike.
- Spec files do **not** reference Plans (one-directional link: Plan → Spec).

## Decomposition

Decomposition is the act of splitting one unit of work into N independent units, each with its own Spec, Plan, and Issue. Because the invariant is 1 Spec = 1 Issue, any decomposition always produces N Specs + N Issues + N Plans, and closes the original.

Decomposition can be triggered at two points in the workflow:

### A. Specify-time Decomposition

Triggered when either:
- The user explicitly requests two or more distinct topics in a single input
- The spec being written grows too large to be independently implementable as a single unit

**Action:**
1. Propose the N units to the user via `AskUserQuestion`. Do not proceed until confirmed.
2. Write N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
3. Create N GitHub Issues: one per Spec (if original issue exists, close it with a comment listing the N new issue numbers)
4. Do not write Plan files — each unit enters its own Plan cycle.

### B. Plan-time Decomposition

Triggered when, after loading a spec, the plan skill determines the work can be split:
- Can each unit be developed with no shared in-progress state (no cross-unit file conflicts)?
- Can each unit be reviewed and merged independently?

**Action:**
1. Propose the N units to the user via `AskUserQuestion`. Do not proceed until confirmed.
2. Split the original Spec into N Spec files: `docs/specs/YYYY-MM-DD-<unit-name>-design.md`
3. Write N Plan files: `docs/plans/YYYY-MM-DD-<unit-name>.md`, each with `linked_spec` pointing to its new Spec
4. Create N GitHub Issues
5. Close the original issue with a comment listing the N new issue numbers
6. Archive the original Spec by adding a superseded notice at the top

### New Issue Format (for both cases)

```
Title: <unit name>
Body:
  <one-paragraph scope description>

  Decomposed from: #<original-issue-number>
```

Issues are standalone — no sub-issue relationship to the original.

## Sync (Bidirectional)

`sync-working-status` ensures the 1 Spec = 1 Issue invariant is maintained over time:
- If an Issue exists with no linked Spec: surface for resolution
- If a Spec exists with no Issue: surface for resolution
- Does not auto-create missing artifacts — surfaces discrepancies for human decision

## Out of Scope

- Decomposition does not cascade: Plan files are never further decomposed.
- `sync-working-status` changes are limited to surfacing discrepancies, not auto-resolving them.

## Done When

- All Plan files include `linked_spec` frontmatter
- `specify` can split into N Specs + N Issues when scope is too large or multi-topic
- `plan` can split into N Specs + N Plans + N Issues when independent parallelism is detected
- Single-unit path unchanged except for `linked_spec` addition
- `sync-working-status` surfaces Spec–Issue mismatches
