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


class FrontmatterFormatError(ValueError):
    pass


class _FlowSequence(list):
    pass


def _flow_sequence_representer(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


_IndentedYAMLDumper.add_representer(_FlowSequence, _flow_sequence_representer)


@dataclass
class Check:
    index: int
    text: str
    checked: bool


@dataclass
class PlanTasks:
    complete: int
    total: int


def _extract_frontmatter_parts(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content
    end = content.find("\n---\n", 4)
    if end == -1:
        return "", content
    return content[4:end], content[end + 5:]


def _validate_depends_on_syntax(frontmatter_text: str) -> None:
    match = re.search(r"(?m)^depends_on:(?P<value>[^\n]*)$", frontmatter_text)
    if match and not re.fullmatch(r"\s*\[[^\n]*\]\s*", match.group("value")):
        raise FrontmatterFormatError(
            "depends_on must use flow-sequence syntax like depends_on: [22, 23]"
        )


def parse_frontmatter(content: str) -> dict:
    frontmatter_text, _ = _extract_frontmatter_parts(content)
    if not frontmatter_text:
        return {}
    _validate_depends_on_syntax(frontmatter_text)
    return yaml.safe_load(frontmatter_text) or {}


class MultipleMatchError(Exception):
    pass


def read_frontmatter_file(path: Path) -> tuple[dict, str]:
    content = path.read_text()
    frontmatter_text, body = _extract_frontmatter_parts(content)
    if not frontmatter_text:
        return {}, content
    try:
        _validate_depends_on_syntax(frontmatter_text)
    except FrontmatterFormatError as exc:
        raise FrontmatterFormatError(f"{path}: {exc}") from exc
    return yaml.safe_load(frontmatter_text) or {}, body


def find_spec_file(root: Path, issue: int) -> Path | None:
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return None
    matches = [
        p for p in specs_dir.glob("*.md")
        if read_frontmatter_file(p)[0].get("issue") == issue
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
        if read_frontmatter_file(p)[0].get("issue") == issue
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


def write_frontmatter(path: Path, fm: dict, body: str) -> None:
    fm_to_dump = dict(fm)
    if "depends_on" in fm_to_dump and fm_to_dump["depends_on"] is not None:
        fm_to_dump["depends_on"] = _FlowSequence(fm_to_dump["depends_on"])
    new_fm = yaml.dump(
        fm_to_dump,
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


def write_checks(path: Path, new_checks: list[dict]) -> None:
    fm, body = read_frontmatter_file(path)
    fm["checks"] = new_checks
    write_frontmatter(path, fm, body)
