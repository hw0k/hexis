from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import yaml


@dataclass
class Check:
    index: int
    text: str
    checked: bool


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(content[4:end]) or {}


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


def parse_checks(fm: dict) -> list[Check]:
    return [
        Check(index=i, text=c["item"], checked=bool(c["done"]))
        for i, c in enumerate(fm.get("checks") or [])
    ]


def parse_depends_on(fm: dict) -> list[int]:
    return list(fm.get("depends_on") or [])
