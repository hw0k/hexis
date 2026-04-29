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
