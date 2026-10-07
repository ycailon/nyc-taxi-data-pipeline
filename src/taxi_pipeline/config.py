from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class QualityConfig:
    max_trip_hours: float
    max_trip_distance_miles: float
    max_total_amount: float
    valid_location_min: int
    valid_location_max: int


@dataclass(frozen=True)
class PipelineConfig:
    dataset: str
    base_url: str
    taxi_zone_lookup_url: str
    required_columns: tuple[str, ...]
    optional_columns: tuple[str, ...]
    quality: QualityConfig


def load_config(path: str | Path) -> PipelineConfig:
    with Path(path).open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    return PipelineConfig(
        dataset=str(raw["dataset"]),
        base_url=str(raw["base_url"]),
        taxi_zone_lookup_url=str(raw["taxi_zone_lookup_url"]),
        required_columns=tuple(raw["required_columns"]),
        optional_columns=tuple(raw.get("optional_columns", [])),
        quality=QualityConfig(**raw["quality"]),
    )
