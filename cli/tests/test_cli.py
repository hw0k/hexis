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
