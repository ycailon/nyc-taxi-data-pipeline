from __future__ import annotations

import hashlib

import pandas as pd

from taxi_pipeline.config import PipelineConfig

CANONICAL_COLUMNS = [
    "trip_id",
    "pickup_datetime",
    "dropoff_datetime",
    "pickup_date",
    "pickup_hour",
    "trip_minutes",
    "trip_distance",
    "pickup_location_id",
    "dropoff_location_id",
    "passenger_count",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
    "cbd_congestion_fee",
    "source_year",
    "source_month",
]


def _series(frame: pd.DataFrame, column: str, default=None) -> pd.Series:
    if column in frame.columns:
        return frame[column]
    return pd.Series([default] * len(frame), index=frame.index)


def normalize_schema(frame: pd.DataFrame, config: PipelineConfig, year: int, month: int) -> pd.DataFrame:
    missing = [column for column in config.required_columns if column not in frame.columns]
    if missing:
        raise ValueError("Required TLC columns are missing: " + ", ".join(missing))

    pickup = pd.to_datetime(frame["tpep_pickup_datetime"], errors="coerce")
    dropoff = pd.to_datetime(frame["tpep_dropoff_datetime"], errors="coerce")

    output = pd.DataFrame(index=frame.index)
    output["pickup_datetime"] = pickup
    output["dropoff_datetime"] = dropoff
    output["pickup_date"] = pickup.dt.date.astype("string")
    output["pickup_hour"] = pickup.dt.hour
    output["trip_minutes"] = (dropoff - pickup).dt.total_seconds() / 60
    output["trip_distance"] = pd.to_numeric(frame["trip_distance"], errors="coerce")
    output["pickup_location_id"] = pd.to_numeric(frame["PULocationID"], errors="coerce")
    output["dropoff_location_id"] = pd.to_numeric(frame["DOLocationID"], errors="coerce")
    output["passenger_count"] = pd.to_numeric(_series(frame, "passenger_count"), errors="coerce")
    output["payment_type"] = pd.to_numeric(_series(frame, "payment_type"), errors="coerce")
    output["fare_amount"] = pd.to_numeric(frame["fare_amount"], errors="coerce")
    output["tip_amount"] = pd.to_numeric(_series(frame, "tip_amount", 0), errors="coerce").fillna(0)
    output["tolls_amount"] = pd.to_numeric(_series(frame, "tolls_amount", 0), errors="coerce").fillna(0)
    output["total_amount"] = pd.to_numeric(frame["total_amount"], errors="coerce")
    output["congestion_surcharge"] = pd.to_numeric(_series(frame, "congestion_surcharge", 0), errors="coerce").fillna(0)
    output["airport_fee"] = pd.to_numeric(_series(frame, "Airport_fee", 0), errors="coerce").fillna(0)
    output["cbd_congestion_fee"] = pd.to_numeric(_series(frame, "cbd_congestion_fee", 0), errors="coerce").fillna(0)
    output["source_year"] = year
    output["source_month"] = month

    ids = []
    for row_number, row in output.iterrows():
        raw = f"{year}|{month}|{row_number}|{row['pickup_datetime']}|{row['dropoff_datetime']}|{row['pickup_location_id']}|{row['dropoff_location_id']}"
        ids.append(hashlib.sha1(raw.encode("utf-8")).hexdigest())
    output.insert(0, "trip_id", ids)
    return output[CANONICAL_COLUMNS]
