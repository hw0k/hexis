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
