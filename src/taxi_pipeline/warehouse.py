from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def connect(path: str | Path) -> sqlite3.Connection:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(destination)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def execute_sql_file(connection: sqlite3.Connection, path: str | Path) -> None:
    connection.executescript(Path(path).read_text(encoding="utf-8"))


def load_zones(connection: sqlite3.Connection, zone_path: str | Path) -> int:
    zones = pd.read_csv(zone_path)
    zones = zones.rename(columns={"LocationID": "location_id", "Borough": "borough", "Zone": "zone", "service_zone": "service_zone"})
    zones.to_sql("dim_zone", connection, if_exists="replace", index=False)
    connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_dim_zone_location ON dim_zone(location_id)")
    connection.commit()
    return len(zones)


def append_trips(connection: sqlite3.Connection, frame: pd.DataFrame) -> int:
    if frame.empty:
        return 0
    payload = frame.copy()
    for column in ["pickup_datetime", "dropoff_datetime"]:
        payload[column] = payload[column].astype(str)
    payload.to_sql("fact_trip", connection, if_exists="append", index=False)
    connection.commit()
    return len(payload)


def replace_month(connection: sqlite3.Connection, year: int, month: int, frame: pd.DataFrame) -> int:
    connection.execute("DELETE FROM fact_trip WHERE source_year = ? AND source_month = ?", (year, month))
    connection.commit()
    return append_trips(connection, frame)
