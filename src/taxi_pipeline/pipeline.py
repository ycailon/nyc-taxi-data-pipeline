from __future__ import annotations

import json
from pathlib import Path

from taxi_pipeline.config import PipelineConfig
from taxi_pipeline.demo import make_demo_trips, make_demo_zones
from taxi_pipeline.export import export_marts
from taxi_pipeline.manifest import Manifest, ManifestEntry
from taxi_pipeline.quality import classify_rows
from taxi_pipeline.source import download_file, read_trip_file, trip_url
from taxi_pipeline.transform import normalize_schema
from taxi_pipeline.warehouse import connect, execute_sql_file, load_zones, replace_month


def process_month(root: Path, config: PipelineConfig, source_path: Path, zone_path: Path, year: int, month: int) -> dict:
    source = read_trip_file(source_path)
    normalized = normalize_schema(source, config, year, month)
    valid, rejected = classify_rows(normalized, config.quality)

    output_dir = root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    rejected.to_csv(output_dir / f"rejected_{year}_{month:02d}.csv", index=False)

    connection = connect(root / "data" / "warehouse" / "taxi.db")
    try:
        execute_sql_file(connection, root / "sql" / "schema.sql")
        load_zones(connection, zone_path)
        loaded = replace_month(connection, year, month, valid)
        execute_sql_file(connection, root / "sql" / "marts.sql")
        export_marts(connection, output_dir / "marts")
    finally:
        connection.close()

    summary = {
        "dataset": config.dataset,
        "year": year,
        "month": month,
        "source_rows": len(source),
        "valid_rows": len(valid),
        "rejected_rows": len(rejected),
        "rows_loaded": loaded,
    }
    (output_dir / f"summary_{year}_{month:02d}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def run_demo(root: Path, config: PipelineConfig, rows: int = 500) -> dict:
    generated = root / "data" / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    trip_path = generated / "yellow_demo.csv"
    zone_path = generated / "taxi_zone_lookup.csv"
    make_demo_trips(rows).to_csv(trip_path, index=False)
    make_demo_zones().to_csv(zone_path, index=False)
    return process_month(root, config, trip_path, zone_path, 2025, 1)


def run_live_month(root: Path, config: PipelineConfig, year: int, month: int, force: bool = False) -> dict:
    manifest = Manifest(root / "data" / "manifest.json")
    if manifest.is_complete(config.dataset, year, month) and not force:
        return {"dataset": config.dataset, "year": year, "month": month, "status": "skipped", "reason": "already complete"}

    raw = root / "data" / "raw" / config.dataset
    trip_path = raw / f"year={year}" / f"month={month:02d}" / f"yellow_tripdata_{year}-{month:02d}.parquet"
    zone_path = root / "data" / "raw" / "taxi_zone_lookup.csv"
    download_file(trip_url(config, year, month), trip_path)
    download_file(config.taxi_zone_lookup_url, zone_path)
    summary = process_month(root, config, trip_path, zone_path, year, month)
    manifest.upsert(ManifestEntry(config.dataset, year, month, str(trip_path), "complete", summary["rows_loaded"]))
    return summary
