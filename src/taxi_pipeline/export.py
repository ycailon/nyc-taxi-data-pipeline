from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


MARTS = ["mart_daily_kpis", "mart_hourly_demand", "mart_zone_performance", "mart_route_performance"]


def export_marts(connection: sqlite3.Connection, output_dir: str | Path) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for mart in MARTS:
        pd.read_sql_query(f"SELECT * FROM {mart}", connection).to_csv(destination / f"{mart}.csv", index=False)
