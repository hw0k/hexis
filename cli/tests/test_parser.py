from hexis.parser import (
    FrontmatterFormatError,
    parse_frontmatter,
    write_checks,
    write_frontmatter,
)

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
from hexis.parser import (
    MultipleMatchError,
    find_plan_file,
    find_spec_file,
    read_frontmatter_file,
)

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

def test_parse_plan_tasks_uses_frontmatter_checks_not_body_checkboxes():
    content = (
        "---\n"
        "checks:\n"
        "  - item: First criterion\n"
        "    done: true\n"
        "  - item: Second criterion\n"
        "    done: false\n"
        "---\n\n"
        "- [ ] Body checkbox that should be ignored\n"
        "- [x] Another ignored body checkbox\n"
    )
    assert parse_plan_tasks(content) == PlanTasks(complete=1, total=2)


def test_parse_plan_tasks_without_frontmatter_checks_returns_zero():
    content = "---\nissue: 5\n---\n\n- [x] Task one\n- [ ] Task two\n"
    assert parse_plan_tasks(content) == PlanTasks(complete=0, total=0)


def test_write_checks_indents_items_under_checks(tmp_path):
    spec_path = tmp_path / "spec.md"
    spec_path.write_text(
        "---\nissue: 5\nchecks:\n  - item: Old\n    done: false\n---\n\n# Spec\n"
    )

    write_checks(
        spec_path,
        [
            {"item": "First criterion", "done": True},
            {"item": "Second criterion", "done": False},
        ],
    )

    content = spec_path.read_text()
    assert "checks:\n  - item: First criterion\n    done: true\n  - item: Second criterion\n    done: false\n" in content
    assert "checks:\n- item:" not in content


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
