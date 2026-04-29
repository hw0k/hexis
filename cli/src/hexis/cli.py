from __future__ import annotations
import typer

app = typer.Typer()
status_app = typer.Typer()
app.add_typer(status_app, name="status")
