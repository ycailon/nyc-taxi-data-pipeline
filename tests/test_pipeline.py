import json
import sqlite3

from taxi_pipeline.config import load_config
from taxi_pipeline.pipeline import run_demo


def test_demo_pipeline_builds_warehouse_and_marts(tmp_path):
    root = tmp_path
    (root / "config").mkdir()
    (root / "sql").mkdir()
    (root / "config" / "pipeline.yaml").write_text(open("config/pipeline.yaml", encoding="utf-8").read(), encoding="utf-8")
    for name in ["schema.sql", "marts.sql"]:
        (root / "sql" / name).write_text(open(f"sql/{name}", encoding="utf-8").read(), encoding="utf-8")

    config = load_config(root / "config" / "pipeline.yaml")
    summary = run_demo(root, config, rows=100)

    assert summary["source_rows"] == 100
    assert summary["valid_rows"] == 97
    assert summary["rejected_rows"] == 3
    assert (root / "data" / "warehouse" / "taxi.db").exists()
    assert (root / "output" / "marts" / "mart_daily_kpis.csv").exists()

    saved = json.loads((root / "output" / "summary_2025_01.json").read_text(encoding="utf-8"))
    assert saved["rows_loaded"] == 97

    connection = sqlite3.connect(root / "data" / "warehouse" / "taxi.db")
    try:
        count = connection.execute("SELECT COUNT(*) FROM fact_trip").fetchone()[0]
    finally:
        connection.close()
    assert count == 97
