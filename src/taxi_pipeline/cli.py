from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from taxi_pipeline.config import load_config
from taxi_pipeline.pipeline import run_demo, run_live_month

app = typer.Typer(help="Incremental NYC TLC Yellow Taxi pipeline.")
console = Console()


@app.command()
def demo(
    root: Annotated[Path, typer.Option("--root")] = Path("."),
    rows: Annotated[int, typer.Option("--rows")] = 500,
) -> None:
    """Generate synthetic taxi data and run the complete pipeline."""
    config = load_config(root / "config" / "pipeline.yaml")
    summary = run_demo(root, config, rows=rows)
    console.print(summary)


@app.command()
def load(
    year: Annotated[int, typer.Option("--year")],
    month: Annotated[int, typer.Option("--month", min=1, max=12)],
    root: Annotated[Path, typer.Option("--root")] = Path("."),
    force: Annotated[bool, typer.Option("--force")] = False,
) -> None:
    """Download and load one official Yellow Taxi month."""
    config = load_config(root / "config" / "pipeline.yaml")
    summary = run_live_month(root, config, year=year, month=month, force=force)
    console.print(summary)


if __name__ == "__main__":
    app()
