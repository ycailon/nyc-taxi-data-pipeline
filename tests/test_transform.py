from taxi_pipeline.config import load_config
from taxi_pipeline.demo import make_demo_trips
from taxi_pipeline.transform import normalize_schema


def _write_config(path):
    path.write_text("""dataset: yellow
base_url: x
taxi_zone_lookup_url: x
required_columns: [tpep_pickup_datetime, tpep_dropoff_datetime, trip_distance, PULocationID, DOLocationID, fare_amount, total_amount]
optional_columns: []
quality:
  max_trip_hours: 12
  max_trip_distance_miles: 300
  max_total_amount: 5000
  valid_location_min: 1
  valid_location_max: 265
""", encoding="utf-8")


def test_schema_adds_new_fee_when_missing(tmp_path):
    config_path = tmp_path / "config.yaml"
    _write_config(config_path)
    config = load_config(config_path)
    frame = make_demo_trips(20).drop(columns=["cbd_congestion_fee"])
    result = normalize_schema(frame, config, 2024, 12)

    assert "cbd_congestion_fee" in result.columns
    assert result["cbd_congestion_fee"].eq(0).all()


def test_schema_keeps_2025_cbd_fee(tmp_path):
    config_path = tmp_path / "config.yaml"
    _write_config(config_path)
    config = load_config(config_path)
    frame = make_demo_trips(20)
    result = normalize_schema(frame, config, 2025, 1)

    assert result["cbd_congestion_fee"].ge(0).all()
