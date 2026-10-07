from __future__ import annotations

import pandas as pd

from taxi_pipeline.config import QualityConfig


def classify_rows(frame: pd.DataFrame, quality: QualityConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    reasons = pd.Series("", index=frame.index, dtype="string")

    def add(mask: pd.Series, reason: str) -> None:
        nonlocal reasons
        reasons.loc[mask] = reasons.loc[mask].where(reasons.loc[mask] == "", reasons.loc[mask] + "; ") + reason

    add(frame["pickup_datetime"].isna() | frame["dropoff_datetime"].isna(), "invalid timestamp")
    add(frame["trip_minutes"].le(0), "dropoff must be after pickup")
    add(frame["trip_minutes"].gt(quality.max_trip_hours * 60), "trip duration exceeds limit")
    add(frame["trip_distance"].lt(0) | frame["trip_distance"].gt(quality.max_trip_distance_miles), "invalid trip distance")
    add(frame["fare_amount"].lt(0), "negative fare")
    add(frame["total_amount"].lt(0) | frame["total_amount"].gt(quality.max_total_amount), "invalid total amount")
    add(~frame["pickup_location_id"].between(quality.valid_location_min, quality.valid_location_max), "invalid pickup zone")
    add(~frame["dropoff_location_id"].between(quality.valid_location_min, quality.valid_location_max), "invalid dropoff zone")

    rejected = frame.loc[reasons != ""].copy()
    rejected["rejection_reason"] = reasons.loc[reasons != ""]
    valid = frame.loc[reasons == ""].copy()
    return valid, rejected
