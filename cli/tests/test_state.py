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
        f"- [{'x' if done else ' '}] Task {i + 1}" for i, done in enumerate(tasks)
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
