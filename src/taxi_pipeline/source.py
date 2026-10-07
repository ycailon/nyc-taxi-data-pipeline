from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

from taxi_pipeline.config import PipelineConfig


def trip_url(config: PipelineConfig, year: int, month: int) -> str:
    return f"{config.base_url}/yellow_tripdata_{year}-{month:02d}.parquet"


def download_file(url: str, destination: str | Path, timeout: int = 60) -> Path:
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with target.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)
    return target


def read_trip_file(path: str | Path) -> pd.DataFrame:
    source = Path(path)
    if source.suffix.lower() == ".csv":
        return pd.read_csv(source)
    if source.suffix.lower() == ".parquet":
        return pd.read_parquet(source)
    raise ValueError(f"Unsupported source file: {source.suffix}")
