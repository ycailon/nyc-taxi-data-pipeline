from taxi_pipeline.config import load_config
from taxi_pipeline.demo import make_demo_trips
from taxi_pipeline.quality import classify_rows
from taxi_pipeline.transform import normalize_schema


def test_quality_rejects_intentionally_bad_rows():
    config = load_config("config/pipeline.yaml")
    source = make_demo_trips(rows=30)
    normalized = normalize_schema(source, config, 2025, 1)
    valid, rejected = classify_rows(normalized, config.quality)

    assert len(valid) == 27
    assert len(rejected) == 3
    assert rejected["rejection_reason"].str.len().gt(0).all()
