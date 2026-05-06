---
issue: 37
status: READY_TO_IMPLEMENT
linked_spec: docs/specs/2026-05-02-frontmatter-authority-design.md
---

# Frontmatter Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `hexis status update` the authoritative writer for derived frontmatter state while enforcing flow-style `depends_on` syntax across CLI reads, writes, and repository documents.

**Architecture:** Extend the parser layer so frontmatter reads inspect raw YAML text before deserializing, reject non-canonical `depends_on` syntax, and rewrite frontmatter with deterministic style rules (`depends_on` flow, `checks` block). Keep workflow-state-to-document-status mapping in `state.py`, then let `cli.py` use that mapping after `status update` mutates checks so spec and plan files are rewritten in one synchronized pass.

**Tech Stack:** Python 3.11+, typer, PyYAML, pytest, uv

---

## File Structure

| File | Responsibility |
|---|---|
| `cli/src/hexis/parser.py` | Raw frontmatter extraction, `depends_on` syntax validation, canonical frontmatter writing |
| `cli/src/hexis/state.py` | Workflow state derivation plus spec/plan status label mapping |
| `cli/src/hexis/cli.py` | CLI error handling and synchronized `status update` rewrites for spec + plan |
| `cli/tests/test_parser.py` | Parser tests for invalid legacy syntax and canonical YAML emission |
| `cli/tests/test_state.py` | State-to-status mapping tests |
| `cli/tests/test_cli.py` | End-to-end CLI tests for status synchronization and deterministic rejection |
| `docs/specs/2026-04-08-skill-integration-gate-design.md` | Migrate legacy block-style `depends_on` frontmatter to canonical flow style |

---

### Task 1: Add parser coverage for canonical frontmatter rules [TDD]

**Files:**
- Modify: `cli/tests/test_parser.py`

- [x] **Step 1: Write failing test**

```python
import pytest
from hexis.parser import FrontmatterFormatError, parse_frontmatter, write_frontmatter


def test_parse_frontmatter_rejects_block_style_depends_on():
    content = "---\ndepends_on:\n  - 22\n---\n\n# Title\n"
    with pytest.raises(FrontmatterFormatError, match="depends_on must use flow-sequence syntax"):
        parse_frontmatter(content)


def test_write_frontmatter_keeps_depends_on_flow_and_checks_block(tmp_path):
    path = tmp_path / "spec.md"
    body = "\n# Spec\n"
    write_frontmatter(
        path,
        {
            "issue": 5,
            "status": "IN_PROGRESS",
            "depends_on": [22, 23],
            "checks": [
                {"item": "First criterion", "done": True},
                {"item": "Second criterion", "done": False},
            ],
        },
        body,
    )

    content = path.read_text()
    assert "depends_on: [22, 23]\n" in content
    assert "checks:\n  - item: First criterion\n    done: true\n  - item: Second criterion\n    done: false\n" in content
    assert "depends_on:\n  - 22\n" not in content
```

- [x] **Step 2: Confirm failure**

Run: `cd cli && pytest tests/test_parser.py -k "depends_on or write_frontmatter"`
Expected: FAIL — `cannot import name 'FrontmatterFormatError'` or `cannot import name 'write_frontmatter'`

- [x] **Step 3: Minimal implementation**

```python
class FrontmatterFormatError(ValueError):
    pass


class _FlowSequence(list):
    pass


def _flow_sequence_representer(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


_IndentedYAMLDumper.add_representer(_FlowSequence, _flow_sequence_representer)


def _extract_frontmatter_parts(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content
    end = content.find("\n---\n", 4)
    if end == -1:
        return "", content
    return content[4:end], content[end + 5:]


def _validate_depends_on_syntax(frontmatter_text: str) -> None:
    match = re.search(r"(?m)^depends_on:(?P<value>[^\n]*)$", frontmatter_text)
    if match and not re.fullmatch(r"\s*\[[^\n]*\]\s*", match.group("value")):
        raise FrontmatterFormatError(
            "depends_on must use flow-sequence syntax like depends_on: [22, 23]"
        )


def parse_frontmatter(content: str) -> dict:
    frontmatter_text, _ = _extract_frontmatter_parts(content)
    if not frontmatter_text:
        return {}
    _validate_depends_on_syntax(frontmatter_text)
    return yaml.safe_load(frontmatter_text) or {}


def write_frontmatter(path: Path, fm: dict, body: str) -> None:
    fm_to_dump = dict(fm)
    if "depends_on" in fm_to_dump and fm_to_dump["depends_on"] is not None:
        fm_to_dump["depends_on"] = _FlowSequence(fm_to_dump["depends_on"])
    new_fm = yaml.dump(
        fm_to_dump,
        Dumper=_IndentedYAMLDumper,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    new_content = f"---\n{new_fm}---\n{body}"
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, delete=False, suffix=".tmp", encoding="utf-8"
    ) as f:
        f.write(new_content)
        tmp = f.name
    os.replace(tmp, path)
```

- [x] **Step 4: Confirm pass**

Run: `cd cli && pytest tests/test_parser.py -k "depends_on or write_frontmatter"`
Expected: PASS

- **Step 5: Commit** — deferred to the final `hexis:finish` phase

```bash
git add cli/tests/test_parser.py cli/src/hexis/parser.py
git commit -m "test(cli): cover canonical frontmatter rules (#37)"
```

### Task 2: Apply parser changes to file discovery and spec rewrites [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py`
- Modify: `cli/tests/test_parser.py`

- [x] **Step 1: Write failing test**

```python
from hexis.parser import find_spec_file, read_frontmatter_file


def test_find_spec_file_surfaces_invalid_depends_on(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "bad.md").write_text(
        "---\nissue: 5\ndepends_on:\n  - 22\nchecks:\n  - item: A\n    done: false\n---\n\n# Bad\n"
    )

    with pytest.raises(FrontmatterFormatError, match="depends_on must use flow-sequence syntax"):
        find_spec_file(tmp_path, 5)


def test_read_frontmatter_file_preserves_body(tmp_path):
    path = tmp_path / "plan.md"
    path.write_text("---\nissue: 5\nstatus: READY_TO_IMPLEMENT\n---\n\n# Plan\n")

    fm, body = read_frontmatter_file(path)
    assert fm["issue"] == 5
    assert body == "\n# Plan\n"
```

- [x] **Step 2: Confirm failure**

Run: `cd cli && pytest tests/test_parser.py -k "find_spec_file_surfaces_invalid_depends_on or read_frontmatter_file_preserves_body"`
Expected: FAIL — `cannot import name 'read_frontmatter_file'`

- [x] **Step 3: Minimal implementation**

```python
def read_frontmatter_file(path: Path) -> tuple[dict, str]:
    content = path.read_text()
    frontmatter_text, body = _extract_frontmatter_parts(content)
    if not frontmatter_text:
        return {}, content
    try:
        _validate_depends_on_syntax(frontmatter_text)
    except FrontmatterFormatError as exc:
        raise FrontmatterFormatError(f"{path}: {exc}") from exc
    return yaml.safe_load(frontmatter_text) or {}, body


def find_spec_file(root: Path, issue: int) -> Path | None:
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return None
    matches = [
        p for p in specs_dir.glob("*.md")
        if read_frontmatter_file(p)[0].get("issue") == issue
    ]
    if len(matches) > 1:
        names = ", ".join(p.name for p in sorted(matches))
        raise MultipleMatchError(f"Multiple spec files match issue #{issue}: {names}")
    return matches[0] if matches else None


def find_plan_file(root: Path, issue: int) -> Path | None:
    plans_dir = root / "docs" / "plans"
    if not plans_dir.is_dir():
        return None
    matches = [
        p for p in plans_dir.glob("*.md")
        if read_frontmatter_file(p)[0].get("issue") == issue
    ]
    if len(matches) > 1:
        names = ", ".join(p.name for p in sorted(matches))
        raise MultipleMatchError(f"Multiple plan files match issue #{issue}: {names}")
    return matches[0] if matches else None


def write_checks(path: Path, new_checks: list[dict]) -> None:
    fm, body = read_frontmatter_file(path)
    fm["checks"] = new_checks
    write_frontmatter(path, fm, body)
```

- [x] **Step 4: Confirm pass**

Run: `cd cli && pytest tests/test_parser.py`
Expected: PASS

- **Step 5: Commit** — deferred to the final `hexis:finish` phase

```bash
git add cli/src/hexis/parser.py cli/tests/test_parser.py
git commit -m "feat(cli): enforce canonical parser reads and writes (#37)"
```

### Task 3: Add workflow-state to document-status mapping [TDD]

**Files:**
- Modify: `cli/src/hexis/state.py`
- Modify: `cli/tests/test_state.py`

- [x] **Step 1: Write failing test**

```python
from hexis.state import State, plan_status_for_state, spec_status_for_state


def test_spec_status_for_state_mapping():
    assert spec_status_for_state(State.NEEDS_PLAN) == "READY_TO_PLAN"
    assert spec_status_for_state(State.IN_PROGRESS) == "IN_PROGRESS"
    assert spec_status_for_state(State.NEEDS_VERIFY) == "NEEDS_VERIFY"
    assert spec_status_for_state(State.DONE) == "DONE"


def test_plan_status_for_state_mapping():
    assert plan_status_for_state(State.NEEDS_PLAN) is None
    assert plan_status_for_state(State.IN_PROGRESS) == "IN_PROGRESS"
    assert plan_status_for_state(State.NEEDS_VERIFY) == "DONE"
    assert plan_status_for_state(State.DONE) == "DONE"
```

- [x] **Step 2: Confirm failure**

Run: `cd cli && pytest tests/test_state.py -k "status_for_state_mapping"`
Expected: FAIL — `cannot import name 'plan_status_for_state'`

- [x] **Step 3: Minimal implementation**

```python
def spec_status_for_state(state: State) -> str:
    mapping = {
        State.NEEDS_PLAN: "READY_TO_PLAN",
        State.IN_PROGRESS: "IN_PROGRESS",
        State.NEEDS_VERIFY: "NEEDS_VERIFY",
        State.DONE: "DONE",
    }
    return mapping[state]


def plan_status_for_state(state: State) -> str | None:
    if state == State.NEEDS_PLAN:
        return None
    mapping = {
        State.IN_PROGRESS: "IN_PROGRESS",
        State.NEEDS_VERIFY: "DONE",
        State.DONE: "DONE",
    }
    return mapping[state]
```

- [x] **Step 4: Confirm pass**

Run: `cd cli && pytest tests/test_state.py -k "status_for_state_mapping"`
Expected: PASS

- **Step 5: Commit** — deferred to the final `hexis:finish` phase

```bash
git add cli/src/hexis/state.py cli/tests/test_state.py
git commit -m "test(cli): cover derived document status mapping (#37)"
```

### Task 4: Add CLI coverage for synchronized status rewrites and invalid syntax rejection [TDD]

**Files:**
- Modify: `cli/tests/test_cli.py`

- [x] **Step 1: Write failing test**

```python
def test_status_read_rejects_block_style_depends_on(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "spec.md").write_text(
        "---\nissue: 5\nstatus: READY_TO_PLAN\ndepends_on:\n  - 22\nchecks:\n  - item: A\n    done: false\n---\n\n# Spec\n"
    )

    result = runner.invoke(app, ["status", "read", "5", "--root", str(tmp_path)])
    assert result.exit_code == 1
    assert "depends_on must use flow-sequence syntax" in result.output


def test_status_update_rewrites_spec_and_plan_statuses(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    spec_path = specs_dir / "spec.md"
    plan_path = plans_dir / "plan.md"
    spec_path.write_text(
        "---\nissue: 5\nstatus: READY_TO_PLAN\ndepends_on: [22]\nchecks:\n  - item: A\n    done: false\n---\n\n# Spec\n"
    )
    plan_path.write_text(
        "---\nissue: 5\nstatus: READY_TO_IMPLEMENT\nlinked_spec: docs/specs/spec.md\n---\n\n- [x] Step 1\n"
    )

    result = runner.invoke(
        app,
        ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)],
    )

    assert result.exit_code == 0
    assert parse_frontmatter(spec_path.read_text())["status"] == "DONE"
    assert parse_frontmatter(plan_path.read_text())["status"] == "DONE"
    assert "STATE: DONE" in result.output
```

- [x] **Step 2: Confirm failure**

Run: `cd cli && pytest tests/test_cli.py -k "rejects_block_style_depends_on or rewrites_spec_and_plan_statuses"`
Expected: FAIL — status values remain `READY_TO_PLAN` / `READY_TO_IMPLEMENT`

- [x] **Step 3: Minimal implementation**

```python
from hexis.parser import (
    FrontmatterFormatError,
    MultipleMatchError,
    find_plan_file,
    find_spec_file,
    parse_frontmatter,
    read_frontmatter_file,
    write_checks,
    write_frontmatter,
)
from hexis.state import (
    State,
    StateResult,
    determine_state,
    plan_status_for_state,
    spec_status_for_state,
)
```

- [x] **Step 4: Confirm pass**

Run: `cd cli && pytest tests/test_cli.py -k "rejects_block_style_depends_on or rewrites_spec_and_plan_statuses"`
Expected: PASS

- **Step 5: Commit** — deferred to the final `hexis:finish` phase

```bash
git add cli/tests/test_cli.py cli/src/hexis/cli.py
git commit -m "test(cli): cover status synchronization and syntax rejection (#37)"
```

### Task 5: Implement synchronized `status update` rewrites in the CLI [TDD]

**Files:**
- Modify: `cli/src/hexis/cli.py`

- [x] **Step 1: Write failing test**

```python
def test_status_update_sets_in_progress_statuses_when_plan_has_open_tasks(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    spec_path = specs_dir / "spec.md"
    plan_path = plans_dir / "plan.md"
    spec_path.write_text(
        "---\nissue: 5\nstatus: READY_TO_PLAN\nchecks:\n  - item: A\n    done: false\n---\n\n# Spec\n"
    )
    plan_path.write_text(
        "---\nissue: 5\nstatus: READY_TO_IMPLEMENT\nlinked_spec: docs/specs/spec.md\n---\n\n- [x] Step 1\n- [ ] Step 2\n"
    )

    runner.invoke(
        app,
        ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)],
    )

    assert parse_frontmatter(spec_path.read_text())["status"] == "IN_PROGRESS"
    assert parse_frontmatter(plan_path.read_text())["status"] == "IN_PROGRESS"
```

- [x] **Step 2: Confirm failure**

Run: `cd cli && pytest tests/test_cli.py -k "in_progress_statuses_when_plan_has_open_tasks"`
Expected: FAIL — plan status remains `READY_TO_IMPLEMENT`

Note: this check passed immediately because the synchronized rewrite path was already implemented during Task 4.

- [x] **Step 3: Minimal implementation**

```python
def _rewrite_status_frontmatter(root: Path, issue: int, result: StateResult) -> None:
    spec_path = find_spec_file(root, issue)
    if spec_path is None:
        return

    spec_fm, spec_body = read_frontmatter_file(spec_path)
    spec_fm["status"] = spec_status_for_state(result.state)
    write_frontmatter(spec_path, spec_fm, spec_body)

    plan_status = plan_status_for_state(result.state)
    if plan_status is None:
        return

    plan_path = find_plan_file(root, issue)
    if plan_path is None:
        return

    plan_fm, plan_body = read_frontmatter_file(plan_path)
    plan_fm["status"] = plan_status
    write_frontmatter(plan_path, plan_fm, plan_body)


@status_app.command("update")
def status_update(
    issue: int,
    checked: str = typer.Option(..., "--checked"),
    unchecked: str = typer.Option(..., "--unchecked"),
    root: Path = typer.Option(Path("."), "--root"),
) -> None:
    root = root.resolve()

    try:
        checked_idx = [int(i.strip()) for i in checked.split(",") if i.strip()]
        unchecked_idx = [int(i.strip()) for i in unchecked.split(",") if i.strip()]
    except ValueError:
        typer.echo("Error: indices must be integers", err=True)
        raise typer.Exit(1)

    all_idx = sorted(checked_idx + unchecked_idx)

    try:
        spec_path = find_spec_file(root, issue)
    except (MultipleMatchError, FrontmatterFormatError) as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)

    if spec_path is None:
        typer.echo(f"No spec file found for issue #{issue}", err=True)
        raise typer.Exit(1)

    fm, body = read_frontmatter_file(spec_path)
    n = len(fm.get("checks") or [])
    expected = list(range(n))

    if all_idx != expected:
        typer.echo(
            f"Error: indices {all_idx} do not cover all {n} checks exactly once "
            f"(expected {expected})",
            err=True,
        )
        raise typer.Exit(1)

    checked_set = set(checked_idx)
    fm["checks"] = [
        {"item": c["item"], "done": i in checked_set}
        for i, c in enumerate(fm["checks"])
    ]
    write_frontmatter(spec_path, fm, body)

    result = determine_state(root, issue)
    _rewrite_status_frontmatter(root, issue, result)
    result = determine_state(root, issue)
    _render_plain(result)
```

- [x] **Step 4: Confirm pass**

Run: `cd cli && pytest tests/test_cli.py`
Expected: PASS

- **Step 5: Commit** — deferred to the final `hexis:finish` phase

```bash
git add cli/src/hexis/cli.py cli/tests/test_cli.py
git commit -m "feat(cli): synchronize frontmatter status rewrites (#37)"
```

### Task 6: Migrate repository frontmatter and run the full suite [No TDD — markdown frontmatter normalization]

**Files:**
- Modify: `docs/specs/2026-04-08-skill-integration-gate-design.md`

- [x] **Step 1: Implement**

Change the frontmatter from the legacy multi-line sequence form for `depends_on` to:


```yaml
depends_on: [22]
```

Then confirm no document frontmatter still uses block-style `depends_on`.

- [x] **Step 2: Verify**

Run: `find docs/specs docs/plans -type f -name '*.md' -print0 | xargs -0 rg -nU "^depends_on:\n\s*-" && cd cli && pytest`
Expected: `rg` returns no matches and `pytest` reports PASS

- **Step 3: Commit** — deferred to the final `hexis:finish` phase

```bash
git add docs/specs/2026-04-08-skill-integration-gate-design.md cli/src/hexis/parser.py cli/src/hexis/state.py cli/src/hexis/cli.py cli/tests/test_parser.py cli/tests/test_state.py cli/tests/test_cli.py
git commit -m "feat(cli): make frontmatter state CLI-authoritative (#37)"
```
