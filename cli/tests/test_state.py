from hexis.state import (
    State,
    determine_state,
    plan_status_for_state,
    spec_status_for_state,
)


def _write_spec(path, issue, checks, depends_on=None):
    checks_yaml = "\n".join(
        f"  - item: {c['item']}\n    done: {'true' if c['done'] else 'false'}"
        for c in checks
    )
    dep_yaml = f"depends_on: {depends_on}\n" if depends_on else ""
    path.write_text(
        f"---\nissue: {issue}\n{dep_yaml}checks:\n{checks_yaml}\n---\n\n# Spec\n"
    )


def _write_plan(path, issue, status="READY_TO_IMPLEMENT", body="# Plan\n"):
    path.write_text(f"---\nissue: {issue}\nstatus: {status}\n---\n\n{body}")


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
    _write_plan(plans_dir / "plan.md", 5, status="READY_TO_IMPLEMENT")
    result = determine_state(tmp_path, 5)
    assert result.state == State.IN_PROGRESS
    assert result.plan_tasks is None


def test_needs_verify(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}])
    _write_plan(plans_dir / "plan.md", 5, status="DONE")
    result = determine_state(tmp_path, 5)
    assert result.state == State.NEEDS_VERIFY


def test_done(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": True}])
    _write_plan(plans_dir / "plan.md", 5, status="DONE")
    result = determine_state(tmp_path, 5)
    assert result.state == State.DONE


def test_depends_on_surfaced(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}], depends_on=[22])
    result = determine_state(tmp_path, 5)
    assert result.depends_on == [22]


def test_body_checkboxes_do_not_affect_state(tmp_path):
    specs_dir = tmp_path / "docs" / "specs"
    plans_dir = tmp_path / "docs" / "plans"
    specs_dir.mkdir(parents=True)
    plans_dir.mkdir(parents=True)
    _write_spec(specs_dir / "spec.md", 5, [{"item": "A", "done": False}])
    _write_plan(
        plans_dir / "plan.md",
        5,
        status="DONE",
        body="```md\n- [ ] Example checkbox\n```\n\n- [x] Actual note\n",
    )

    result = determine_state(tmp_path, 5)
    assert result.state == State.NEEDS_VERIFY


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
