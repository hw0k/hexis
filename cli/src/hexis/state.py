from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from hexis.parser import (
    Check,
    PlanTasks,
    MultipleMatchError,
    find_spec_file,
    find_plan_file,
    parse_frontmatter,
    parse_checks,
    parse_depends_on,
    parse_plan_tasks,
)


class State(str, Enum):
    NEEDS_SPEC = "NEEDS_SPEC"
    NEEDS_PLAN = "NEEDS_PLAN"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_VERIFY = "NEEDS_VERIFY"
    DONE = "DONE"


@dataclass
class StateResult:
    state: State
    issue: int
    depends_on: list[int] = field(default_factory=list)
    plan_tasks: PlanTasks | None = None
    checks: list[Check] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)


def determine_state(root: Path, issue: int) -> StateResult:
    spec_path = find_spec_file(root, issue)
    if spec_path is None:
        return StateResult(
            state=State.NEEDS_SPEC,
            issue=issue,
            blocking=[f"No spec file found in docs/specs/ for issue #{issue}"],
        )

    spec_fm = parse_frontmatter(spec_path.read_text())
    checks = parse_checks(spec_fm)
    depends_on = parse_depends_on(spec_fm)

    plan_path = find_plan_file(root, issue)
    if plan_path is None:
        return StateResult(
            state=State.NEEDS_PLAN,
            issue=issue,
            depends_on=depends_on,
            checks=checks,
            blocking=[f"No plan file found in docs/plans/ for issue #{issue}"],
        )

    plan_tasks = parse_plan_tasks(plan_path.read_text())

    if plan_tasks.total > 0 and plan_tasks.complete < plan_tasks.total:
        return StateResult(
            state=State.IN_PROGRESS,
            issue=issue,
            depends_on=depends_on,
            plan_tasks=plan_tasks,
            checks=checks,
        )

    if any(not c.checked for c in checks):
        return StateResult(
            state=State.NEEDS_VERIFY,
            issue=issue,
            depends_on=depends_on,
            plan_tasks=plan_tasks,
            checks=checks,
        )

    return StateResult(
        state=State.DONE,
        issue=issue,
        depends_on=depends_on,
        plan_tasks=plan_tasks,
        checks=checks,
    )
