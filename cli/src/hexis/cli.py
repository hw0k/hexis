from __future__ import annotations
import json as json_lib
from pathlib import Path

import typer

from hexis.parser import MultipleMatchError
from hexis.state import State, StateResult, determine_state

app = typer.Typer()
status_app = typer.Typer()
app.add_typer(status_app, name="status")


def _render_plain(result: StateResult) -> None:
    typer.echo(f"STATE: {result.state.value}")
    typer.echo(f"ISSUE: {result.issue}")
    depends_str = ", ".join(f"#{n}" for n in result.depends_on) if result.depends_on else "(none)"
    typer.echo(f"DEPENDS ON: {depends_str}")

    if result.state in (State.NEEDS_SPEC, State.NEEDS_PLAN):
        typer.echo("")
        typer.echo("BLOCKING:")
        for b in result.blocking:
            typer.echo(f"  {b}")
        return

    if result.plan_tasks is not None:
        typer.echo("")
        typer.echo(f"PLAN TASKS: {result.plan_tasks.complete}/{result.plan_tasks.total} complete")

    typer.echo("")
    typer.echo("CHECKS:")
    for c in result.checks:
        mark = "x" if c.checked else " "
        typer.echo(f"  [{mark}] #{c.index}  {c.text}")


@status_app.command("read")
def status_read(
    issue: int,
    json: bool = typer.Option(False, "--json"),
    root: Path = typer.Option(Path("."), "--root"),
) -> None:
    root = root.resolve()
    try:
        result = determine_state(root, issue)
    except MultipleMatchError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(2)

    if json:
        output = {
            "state": result.state.value,
            "issue": result.issue,
            "depends_on": result.depends_on,
            "plan_tasks": (
                {"complete": result.plan_tasks.complete, "total": result.plan_tasks.total}
                if result.plan_tasks is not None
                else None
            ),
            "checks": [
                {"index": c.index, "text": c.text, "checked": c.checked}
                for c in result.checks
            ],
            "blocking": result.blocking,
        }
        typer.echo(json_lib.dumps(output, indent=2))
    else:
        _render_plain(result)
