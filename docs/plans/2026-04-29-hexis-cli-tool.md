---
issue: 22
status: READY_TO_IMPLEMENT
linked_spec: docs/specs/2026-04-08-hexis-cli-tool-design.md
---

# hexis CLI Tool — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `hexis:implement` to execute task by task. For TDD tasks, follow `hexis:testing-principles`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a stateless Python CLI (`hexis`) that reads `docs/specs/` and `docs/plans/` to report workflow state and update spec acceptance-criteria completion.

**Architecture:** Three modules with a clean dependency chain — `parser.py` (file I/O and content parsing) ← `state.py` (state machine) ← `cli.py` (Typer commands). All reads are fresh per invocation; writes are atomic via `os.replace`. YAML frontmatter is parsed with PyYAML.

**Tech Stack:** Python ≥ 3.11, typer[all], pyyaml, pytest, hatchling (build), uv (install/run)

---

## File Structure

| File | Responsibility |
|---|---|
| `cli/pyproject.toml` | Package metadata, entry point, dependencies |
| `cli/src/hexis/__init__.py` | Package marker (empty) |
| `cli/src/hexis/parser.py` | `MultipleMatchError`, `Check`, `PlanTasks`; frontmatter parsing, file discovery, `write_checks` |
| `cli/src/hexis/state.py` | `State`, `StateResult`, `determine_state` |
| `cli/src/hexis/cli.py` | Typer app, `status read`, `status update` commands |
| `cli/tests/test_parser.py` | Tests for all `parser.py` functions |
| `cli/tests/test_state.py` | Tests for `determine_state` covering all 5 states |
| `cli/tests/test_cli.py` | End-to-end CLI tests via `typer.testing.CliRunner` |

---

### Task 1: Project scaffolding [No TDD — pure configuration]

**Files:**
- Create: `cli/pyproject.toml`
- Create: `cli/src/hexis/__init__.py`
- Create: `cli/src/hexis/parser.py`
- Create: `cli/src/hexis/state.py`
- Create: `cli/src/hexis/cli.py`
- Create: `cli/tests/test_parser.py`
- Create: `cli/tests/test_state.py`
- Create: `cli/tests/test_cli.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p cli/src/hexis cli/tests
```

- [ ] **Step 2: Write `cli/pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hexis"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.9.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[project.scripts]
hexis = "hexis.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/hexis"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 3: Write skeleton source files**

`cli/src/hexis/__init__.py` — empty file.

`cli/src/hexis/parser.py`:
```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml
```

`cli/src/hexis/state.py`:
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
```

`cli/src/hexis/cli.py`:
```python
from __future__ import annotations
import typer

app = typer.Typer()
status_app = typer.Typer()
app.add_typer(status_app, name="status")
```

`cli/tests/test_parser.py`, `cli/tests/test_state.py`, `cli/tests/test_cli.py` — empty files.

- [ ] **Step 4: Verify install**

```bash
cd cli && uv pip install -e ".[dev]" --quiet && python -c "import hexis; print('OK')"
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add cli/
git commit -m "feat: scaffold hexis CLI package (#22)"
```

---

### Task 2: `parse_frontmatter` [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py`
- Modify: `cli/tests/test_parser.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_parser.py
from hexis.parser import parse_frontmatter

def test_parse_frontmatter_valid():
    content = "---\nissue: 5\nstatus: READY_TO_PLAN\n---\n\n# Title\n"
    fm = parse_frontmatter(content)
    assert fm == {"issue": 5, "status": "READY_TO_PLAN"}

def test_parse_frontmatter_with_checks():
    content = "---\nchecks:\n  - item: criterion\n    done: false\n---\n\n# Title\n"
    fm = parse_frontmatter(content)
    assert fm["checks"] == [{"item": "criterion", "done": False}]

def test_parse_frontmatter_no_frontmatter():
    assert parse_frontmatter("# Just a title\n") == {}

def test_parse_frontmatter_incomplete_delimiter():
    assert parse_frontmatter("---\nissue: 5\n") == {}
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_parser.py -x
```

Expected: FAIL — `ImportError` or `AttributeError`

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/parser.py — add after imports
def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(content[4:end]) or {}
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_parser.py -x
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/parser.py cli/tests/test_parser.py
git commit -m "feat(cli): implement parse_frontmatter (#22)"
```

---

### Task 3: File discovery — `find_spec_file`, `find_plan_file` [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py`
- Modify: `cli/tests/test_parser.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_parser.py — append
import pytest
from hexis.parser import find_spec_file, find_plan_file, MultipleMatchError

def test_find_spec_file_found(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "2026-01-01-foo-design.md").write_text(
        "---\nissue: 5\nstatus: READY_TO_PLAN\n---\n\n# Foo\n"
    )
    result = find_spec_file(tmp_path, 5)
    assert result is not None
    assert result.name == "2026-01-01-foo-design.md"

def test_find_spec_file_not_found(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    assert find_spec_file(tmp_path, 99) is None

def test_find_spec_file_missing_dir(tmp_path):
    assert find_spec_file(tmp_path, 5) is None

def test_find_spec_file_multiple_raises(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "a.md").write_text("---\nissue: 5\n---\n\n# A\n")
    (specs_dir / "b.md").write_text("---\nissue: 5\n---\n\n# B\n")
    with pytest.raises(MultipleMatchError):
        find_spec_file(tmp_path, 5)

def test_find_plan_file_found(tmp_path):
    plans_dir = tmp_path / "docs" / "plans"
    plans_dir.mkdir(parents=True)
    (plans_dir / "2026-01-01-foo.md").write_text(
        "---\nissue: 5\nstatus: READY_TO_IMPLEMENT\n---\n\n# Foo Plan\n"
    )
    result = find_plan_file(tmp_path, 5)
    assert result is not None

def test_find_plan_file_not_found(tmp_path):
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    assert find_plan_file(tmp_path, 99) is None

def test_find_plan_file_missing_dir(tmp_path):
    assert find_plan_file(tmp_path, 5) is None
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_parser.py::test_find_spec_file_found -x
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/parser.py — append

class MultipleMatchError(Exception):
    pass

def find_spec_file(root: Path, issue: int) -> Path | None:
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return None
    matches = [
        p for p in specs_dir.glob("*.md")
        if parse_frontmatter(p.read_text()).get("issue") == issue
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
        if parse_frontmatter(p.read_text()).get("issue") == issue
    ]
    if len(matches) > 1:
        names = ", ".join(p.name for p in sorted(matches))
        raise MultipleMatchError(f"Multiple plan files match issue #{issue}: {names}")
    return matches[0] if matches else None
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_parser.py -x
```

Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/parser.py cli/tests/test_parser.py
git commit -m "feat(cli): implement find_spec_file and find_plan_file (#22)"
```

---

### Task 4: Spec content parsing — `parse_checks`, `parse_depends_on` [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py`
- Modify: `cli/tests/test_parser.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_parser.py — append
from hexis.parser import parse_checks, parse_depends_on, Check

def test_parse_checks_mixed():
    fm = {
        "checks": [
            {"item": "First criterion", "done": True},
            {"item": "Second criterion", "done": False},
        ]
    }
    result = parse_checks(fm)
    assert result == [
        Check(index=0, text="First criterion", checked=True),
        Check(index=1, text="Second criterion", checked=False),
    ]

def test_parse_checks_empty_fm():
    assert parse_checks({}) == []

def test_parse_checks_preserves_order():
    fm = {"checks": [{"item": "Z", "done": False}, {"item": "A", "done": True}]}
    result = parse_checks(fm)
    assert result[0].text == "Z"
    assert result[1].text == "A"

def test_parse_depends_on_list():
    assert parse_depends_on({"depends_on": [22, 23]}) == [22, 23]

def test_parse_depends_on_absent():
    assert parse_depends_on({}) == []

def test_parse_depends_on_null():
    assert parse_depends_on({"depends_on": None}) == []
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_parser.py::test_parse_checks_mixed -x
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/parser.py — insert after imports, before parse_frontmatter

@dataclass
class Check:
    index: int
    text: str
    checked: bool

# ... existing functions ...

# append at end of parser.py

def parse_checks(fm: dict) -> list[Check]:
    return [
        Check(index=i, text=c["item"], checked=bool(c["done"]))
        for i, c in enumerate(fm.get("checks") or [])
    ]

def parse_depends_on(fm: dict) -> list[int]:
    return list(fm.get("depends_on") or [])
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_parser.py -x
```

Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/parser.py cli/tests/test_parser.py
git commit -m "feat(cli): implement parse_checks and parse_depends_on (#22)"
```

---

### Task 5: Plan task parsing — `parse_plan_tasks` [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py`
- Modify: `cli/tests/test_parser.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_parser.py — append
from hexis.parser import parse_plan_tasks, PlanTasks

def test_parse_plan_tasks_mixed():
    content = "---\nissue: 5\n---\n\n- [x] Task one\n- [ ] Task two\n- [x] Task three\n"
    assert parse_plan_tasks(content) == PlanTasks(complete=2, total=3)

def test_parse_plan_tasks_all_done():
    content = "---\nissue: 5\n---\n\n- [x] Task one\n- [x] Task two\n"
    assert parse_plan_tasks(content) == PlanTasks(complete=2, total=2)

def test_parse_plan_tasks_none():
    content = "---\nissue: 5\n---\n\n# No tasks\n"
    assert parse_plan_tasks(content) == PlanTasks(complete=0, total=0)

def test_parse_plan_tasks_excludes_frontmatter():
    content = "---\nchecks:\n  - item: x\n    done: false\n---\n\n- [x] Real task\n"
    assert parse_plan_tasks(content) == PlanTasks(complete=1, total=1)
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_parser.py::test_parse_plan_tasks_mixed -x
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/parser.py — insert dataclass before parse_frontmatter, add function at end

import re  # add to top-level imports

@dataclass
class PlanTasks:
    complete: int
    total: int

# ... at end of file:

def parse_plan_tasks(content: str) -> PlanTasks:
    body = content
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            body = content[end + 5:]
    checked = len(re.findall(r"^- \[x\]", body, re.MULTILINE))
    unchecked = len(re.findall(r"^- \[ \]", body, re.MULTILINE))
    return PlanTasks(complete=checked, total=checked + unchecked)
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_parser.py -x
```

Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/parser.py cli/tests/test_parser.py
git commit -m "feat(cli): implement parse_plan_tasks (#22)"
```

---

### Task 6: State determination — `determine_state` [TDD]

**Files:**
- Modify: `cli/src/hexis/state.py`
- Modify: `cli/tests/test_state.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_state.py
from hexis.state import State, determine_state

def _write_spec(path, issue, checks, depends_on=None):
    checks_yaml = "\n".join(
        f"  - item: {c['item']}\n    done: {'true' if c['done'] else 'false'}"
        for c in checks
    )
    dep_yaml = f"depends_on: {depends_on}\n" if depends_on else ""
    path.write_text(
        f"---\nissue: {issue}\n{dep_yaml}checks:\n{checks_yaml}\n---\n\n# Spec\n"
    )

def _write_plan(path, issue, tasks):
    task_lines = "\n".join(
        f"- [{'x' if done else ' '}] Task {i+1}" for i, done in enumerate(tasks)
    )
    path.write_text(f"---\nissue: {issue}\n---\n\n{task_lines}\n")

def test_needs_spec_missing_dir(tmp_path):
    result = determine_state(tmp_path, 99)
    assert result.state == State.NEEDS_SPEC

def test_needs_spec_no_file(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    result = determine_state(tmp_path, 99)
    assert result.state == State.NEEDS_SPEC
    assert result.issue == 99
    assert len(result.blocking) == 1

def test_needs_plan(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}])
    result = determine_state(tmp_path, 5)
    assert result.state == State.NEEDS_PLAN
    assert len(result.blocking) == 1

def test_in_progress(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}])
    _write_plan(plans_dir / "plan.md", 5, [True, False])
    result = determine_state(tmp_path, 5)
    assert result.state == State.IN_PROGRESS
    assert result.plan_tasks is not None
    assert result.plan_tasks.complete == 1
    assert result.plan_tasks.total == 2

def test_needs_verify(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}])
    _write_plan(plans_dir / "plan.md", 5, [True, True])
    result = determine_state(tmp_path, 5)
    assert result.state == State.NEEDS_VERIFY

def test_done(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": True}])
    _write_plan(plans_dir / "plan.md", 5, [True])
    result = determine_state(tmp_path, 5)
    assert result.state == State.DONE

def test_depends_on_surfaced(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}], depends_on=[22])
    result = determine_state(tmp_path, 5)
    assert result.depends_on == [22]
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_state.py -x
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/state.py — full content

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from hexis.parser import (
    Check, PlanTasks, MultipleMatchError,
    find_spec_file, find_plan_file,
    parse_frontmatter, parse_checks, parse_depends_on, parse_plan_tasks,
)


class State(str, Enum):
    NEEDS_SPEC = "NEEDS_SPEC"
    NEEDS_PLAN = "NEEDS_PLAN"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_VERIFY = "NEEDS_VERIFY"
    DONE = "DONE"


@dataclass
class StateResult:
    state: State
    issue: int
    depends_on: list[int] = field(default_factory=list)
    plan_tasks: PlanTasks | None = None
    checks: list[Check] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)


def determine_state(root: Path, issue: int) -> StateResult:
    spec_path = find_spec_file(root, issue)
    if spec_path is None:
        return StateResult(
            state=State.NEEDS_SPEC,
            issue=issue,
            blocking=[f"No spec file found in docs/specs/ for issue #{issue}"],
        )

    spec_fm = parse_frontmatter(spec_path.read_text())
    checks = parse_checks(spec_fm)
    depends_on = parse_depends_on(spec_fm)

    plan_path = find_plan_file(root, issue)
    if plan_path is None:
        return StateResult(
            state=State.NEEDS_PLAN,
            issue=issue,
            depends_on=depends_on,
            checks=checks,
            blocking=[f"No plan file found in docs/plans/ for issue #{issue}"],
        )

    plan_tasks = parse_plan_tasks(plan_path.read_text())

    if plan_tasks.total > 0 and plan_tasks.complete < plan_tasks.total:
        return StateResult(
            state=State.IN_PROGRESS,
            issue=issue,
            depends_on=depends_on,
            plan_tasks=plan_tasks,
            checks=checks,
        )

    if any(not c.checked for c in checks):
        return StateResult(
            state=State.NEEDS_VERIFY,
            issue=issue,
            depends_on=depends_on,
            plan_tasks=plan_tasks,
            checks=checks,
        )

    return StateResult(
        state=State.DONE,
        issue=issue,
        depends_on=depends_on,
        plan_tasks=plan_tasks,
        checks=checks,
    )
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_state.py -x
```

Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/state.py cli/tests/test_state.py
git commit -m "feat(cli): implement determine_state (#22)"
```

---

### Task 7: `status read` command [TDD]

**Files:**
- Modify: `cli/src/hexis/cli.py`
- Modify: `cli/tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_cli.py
import json
from typer.testing import CliRunner
from hexis.cli import app

runner = CliRunner()


def _setup_needs_verify(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    (specs_dir / "spec.md").write_text(
        "---\nissue: 5\nchecks:\n  - item: A\n    done: false\n  - item: B\n    done: true\n---\n\n# Spec\n"
    )
    (plans_dir / "plan.md").write_text(
        "---\nissue: 5\n---\n\n- [x] Step 1\n- [x] Step 2\n"
    )


def test_status_read_needs_spec_plain(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    result = runner.invoke(app, ["status", "read", "99", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "STATE: NEEDS_SPEC" in result.output
    assert "ISSUE: 99" in result.output
    assert "DEPENDS ON: (none)" in result.output
    assert "BLOCKING:" in result.output


def test_status_read_needs_verify_plain(tmp_path):
    _setup_needs_verify(tmp_path)
    result = runner.invoke(app, ["status", "read", "5", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "STATE: NEEDS_VERIFY" in result.output
    assert "PLAN TASKS: 2/2 complete" in result.output
    assert "CHECKS:" in result.output
    assert "[ ] #0  A" in result.output
    assert "[x] #1  B" in result.output


def test_status_read_json_needs_spec(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    result = runner.invoke(app, ["status", "read", "99", "--json", "--root", str(tmp_path)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["state"] == "NEEDS_SPEC"
    assert data["issue"] == 99
    assert data["depends_on"] == []
    assert data["plan_tasks"] is None
    assert data["checks"] == []
    assert len(data["blocking"]) == 1


def test_status_read_json_needs_verify(tmp_path):
    _setup_needs_verify(tmp_path)
    result = runner.invoke(app, ["status", "read", "5", "--json", "--root", str(tmp_path)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["state"] == "NEEDS_VERIFY"
    assert data["plan_tasks"] == {"complete": 2, "total": 2}
    assert data["checks"][0] == {"index": 0, "text": "A", "checked": False}
    assert data["checks"][1] == {"index": 1, "text": "B", "checked": True}


def test_status_read_missing_docs_graceful(tmp_path):
    result = runner.invoke(app, ["status", "read", "99", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "STATE: NEEDS_SPEC" in result.output
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_cli.py::test_status_read_needs_spec_plain -x
```

Expected: FAIL — command not found or no such command

- [ ] **Step 3: Implement**

```python
# cli/src/hexis/cli.py — full content

from __future__ import annotations
import json as json_lib
from pathlib import Path

import typer

from hexis.parser import MultipleMatchError
from hexis.state import State, StateResult, determine_state

app = typer.Typer()
status_app = typer.Typer()
app.add_typer(status_app, name="status")


def _render_plain(result: StateResult) -> None:
    typer.echo(f"STATE: {result.state.value}")
    typer.echo(f"ISSUE: {result.issue}")
    depends_str = ", ".join(f"#{n}" for n in result.depends_on) if result.depends_on else "(none)"
    typer.echo(f"DEPENDS ON: {depends_str}")

    if result.state in (State.NEEDS_SPEC, State.NEEDS_PLAN):
        typer.echo("")
        typer.echo("BLOCKING:")
        for b in result.blocking:
            typer.echo(f"  {b}")
        return

    if result.plan_tasks is not None:
        typer.echo("")
        typer.echo(f"PLAN TASKS: {result.plan_tasks.complete}/{result.plan_tasks.total} complete")

    typer.echo("")
    typer.echo("CHECKS:")
    for c in result.checks:
        mark = "x" if c.checked else " "
        typer.echo(f"  [{mark}] #{c.index}  {c.text}")


@status_app.command("read")
def status_read(
    issue: int,
    json: bool = typer.Option(False, "--json"),
    root: Path = typer.Option(Path("."), "--root"),
) -> None:
    root = root.resolve()
    try:
        result = determine_state(root, issue)
    except MultipleMatchError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)

    if json:
        output = {
            "state": result.state.value,
            "issue": result.issue,
            "depends_on": result.depends_on,
            "plan_tasks": (
                {"complete": result.plan_tasks.complete, "total": result.plan_tasks.total}
                if result.plan_tasks is not None else None
            ),
            "checks": [
                {"index": c.index, "text": c.text, "checked": c.checked}
                for c in result.checks
            ],
            "blocking": result.blocking,
        }
        typer.echo(json_lib.dumps(output, indent=2))
    else:
        _render_plain(result)
```

- [ ] **Step 4: Confirm pass**

```bash
cd cli && uv run pytest tests/test_cli.py -x -k "read"
```

Expected: all `read` tests passed

- [ ] **Step 5: Commit**

```bash
git add cli/src/hexis/cli.py cli/tests/test_cli.py
git commit -m "feat(cli): implement status read command (#22)"
```

---

### Task 8: `status update` command [TDD]

**Files:**
- Modify: `cli/src/hexis/parser.py` (add `write_checks`)
- Modify: `cli/src/hexis/cli.py` (add `status update` command)
- Modify: `cli/tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

```python
# cli/tests/test_cli.py — append
from hexis.parser import parse_frontmatter


def _setup_spec_with_plan(tmp_path, issue, checks_done):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True, exist_ok=True)
    plans_dir.mkdir(parents=True, exist_ok=True)
    checks_yaml = "\n".join(
        f"  - item: Item {i}\n    done: {'true' if d else 'false'}"
        for i, d in enumerate(checks_done)
    )
    spec_path = specs_dir / "spec.md"
    spec_path.write_text(
        f"---\nissue: {issue}\nchecks:\n{checks_yaml}\n---\n\n# Spec\n"
    )
    (plans_dir / "plan.md").write_text(
        f"---\nissue: {issue}\n---\n\n- [x] Step 1\n"
    )
    return spec_path


def test_status_update_sets_checked(tmp_path):
    spec_path = _setup_spec_with_plan(tmp_path, 5, [False, False])
    result = runner.invoke(
        app, ["status", "update", "5", "--checked", "0", "--unchecked", "1", "--root", str(tmp_path)]
    )
    assert result.exit_code == 0
    fm = parse_frontmatter(spec_path.read_text())
    assert fm["checks"][0]["done"] is True
    assert fm["checks"][1]["done"] is False
    assert "STATE:" in result.output


def test_status_update_all_checked_yields_done(tmp_path):
    spec_path = _setup_spec_with_plan(tmp_path, 5, [False])
    result = runner.invoke(
        app, ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)]
    )
    assert result.exit_code == 0
    assert "STATE: DONE" in result.output


def test_status_update_incomplete_coverage_exits_1(tmp_path):
    _setup_spec_with_plan(tmp_path, 5, [False, False])
    result = runner.invoke(
        app, ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)]
    )
    assert result.exit_code == 1


def test_status_update_overlapping_indices_exits_1(tmp_path):
    _setup_spec_with_plan(tmp_path, 5, [False, False])
    result = runner.invoke(
        app, ["status", "update", "5", "--checked", "0,1", "--unchecked", "0", "--root", str(tmp_path)]
    )
    assert result.exit_code == 1


def test_status_update_no_spec_exits_1(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    result = runner.invoke(
        app, ["status", "update", "99", "--checked", "", "--unchecked", "", "--root", str(tmp_path)]
    )
    assert result.exit_code == 1
```

- [ ] **Step 2: Confirm failure**

```bash
cd cli && uv run pytest tests/test_cli.py::test_status_update_sets_checked -x
```

Expected: FAIL — no such command `update`

- [ ] **Step 3: Implement `write_checks` in `parser.py`**

```python
# cli/src/hexis/parser.py — add imports at top and function at end

import os
import tempfile

def write_checks(path: Path, new_checks: list[dict]) -> None:
    content = path.read_text()
    end = content.find("\n---\n", 4)
    fm = yaml.safe_load(content[4:end]) or {}
    body = content[end + 5:]
    fm["checks"] = new_checks
    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_fm}---\n{body}"
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, delete=False, suffix=".tmp", encoding="utf-8"
    ) as f:
        f.write(new_content)
        tmp = f.name
    os.replace(tmp, path)
```

- [ ] **Step 4: Implement `status update` in `cli.py`**

```python
# cli/src/hexis/cli.py — add import and command

from hexis.parser import MultipleMatchError, find_spec_file, parse_frontmatter, write_checks

# ... existing code ...

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
    except MultipleMatchError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)

    if spec_path is None:
        typer.echo(f"No spec file found for issue #{issue}", err=True)
        raise typer.Exit(1)

    fm = parse_frontmatter(spec_path.read_text())
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
    new_checks = [
        {"item": c["item"], "done": i in checked_set}
        for i, c in enumerate(fm["checks"])
    ]
    write_checks(spec_path, new_checks)

    result = determine_state(root, issue)
    _render_plain(result)
```

- [ ] **Step 5: Confirm pass**

```bash
cd cli && uv run pytest tests/test_cli.py -x
```

Expected: all passed

- [ ] **Step 6: Commit**

```bash
git add cli/src/hexis/parser.py cli/src/hexis/cli.py cli/tests/test_cli.py
git commit -m "feat(cli): implement status update command (#22)"
```

---

### Task 9: Packaging verification [No TDD — install test]

**Files:**
- No code changes — install and smoke-test only

- [ ] **Step 1: Run full test suite**

```bash
cd cli && uv run pytest
```

Expected: all tests pass, 0 failures

- [ ] **Step 2: Install via `uv tool install`**

```bash
uv tool install ./cli
```

Expected: exits 0, no errors

- [ ] **Step 3: Smoke-test installed binary**

```bash
hexis --help
hexis status read --help
hexis status update --help
```

Expected: each shows command help without errors.

- [ ] **Step 4: Verify NEEDS_SPEC output with real repo**

```bash
hexis status read 999
```

Expected:
```
STATE: NEEDS_SPEC
ISSUE: 999
DEPENDS ON: (none)

BLOCKING:
  No spec file found in docs/specs/ for issue #999
```

- [ ] **Step 5: Verify real issue lookup**

```bash
hexis status read 22
```

Expected: first line is `STATE: NEEDS_VERIFY` or `STATE: IN_PROGRESS` (since spec and plan now exist for #22).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "docs: verify hexis CLI packaging and smoke tests (#22)"
```
