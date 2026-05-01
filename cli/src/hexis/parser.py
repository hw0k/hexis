from __future__ import annotations
from dataclasses import dataclass
import os
from pathlib import Path
import re
import tempfile
import yaml


class _IndentedYAMLDumper(yaml.SafeDumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


@dataclass
class Check:
    index: int
    text: str
    checked: bool


@dataclass
class PlanTasks:
    complete: int
    total: int


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


def parse_plan_tasks(content: str) -> PlanTasks:
    body = content
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            body = content[end + 5:]
    checked = len(re.findall(r"^- \[x\]", body, re.MULTILINE))
    unchecked = len(re.findall(r"^- \[ \]", body, re.MULTILINE))
    return PlanTasks(complete=checked, total=checked + unchecked)


def write_checks(path: Path, new_checks: list[dict]) -> None:
    content = path.read_text()
    end = content.find("\n---\n", 4)
    fm = yaml.safe_load(content[4:end]) or {}
    body = content[end + 5:]
    fm["checks"] = new_checks
    new_fm = yaml.dump(
        fm,
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
