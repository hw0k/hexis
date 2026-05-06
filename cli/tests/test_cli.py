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
        app,
        ["status", "update", "5", "--checked", "0", "--unchecked", "1", "--root", str(tmp_path)],
    )
    assert result.exit_code == 0
    fm = parse_frontmatter(spec_path.read_text())
    assert fm["checks"][0]["done"] is True
    assert fm["checks"][1]["done"] is False
    assert "STATE:" in result.output


def test_status_update_all_checked_yields_done(tmp_path):
    _setup_spec_with_plan(tmp_path, 5, [False])
    result = runner.invoke(
        app,
        ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)],
    )
    assert result.exit_code == 0
    assert "STATE: DONE" in result.output


def test_status_update_incomplete_coverage_exits_1(tmp_path):
    _setup_spec_with_plan(tmp_path, 5, [False, False])
    result = runner.invoke(
        app,
        ["status", "update", "5", "--checked", "0", "--unchecked", "", "--root", str(tmp_path)],
    )
    assert result.exit_code == 1


def test_status_update_overlapping_indices_exits_1(tmp_path):
    _setup_spec_with_plan(tmp_path, 5, [False, False])
    result = runner.invoke(
        app,
        ["status", "update", "5", "--checked", "0,1", "--unchecked", "0", "--root", str(tmp_path)],
    )
    assert result.exit_code == 1


def test_status_update_no_spec_exits_1(tmp_path):
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    result = runner.invoke(
        app,
        ["status", "update", "99", "--checked", "", "--unchecked", "", "--root", str(tmp_path)],
    )
    assert result.exit_code == 1
