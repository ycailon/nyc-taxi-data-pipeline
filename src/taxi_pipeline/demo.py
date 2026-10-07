from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd


def make_demo_trips(rows: int = 500, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    base = datetime(2025, 1, 1, 0, 0)
    records = []
    for index in range(rows):
        pickup = base + timedelta(minutes=index * 13)
        duration = random.randint(5, 55)
        dropoff = pickup + timedelta(minutes=duration)
        distance = round(random.uniform(0.5, 18.0), 2)
        fare = round(3.0 + distance * random.uniform(2.1, 3.2), 2)
        tip = round(fare * random.choice([0, 0.1, 0.15, 0.2]), 2)
        cbd_fee = 0.75 if pickup.hour in range(6, 21) else 0.0
        records.append(
            {
                "VendorID": random.choice([1, 2]),
                "tpep_pickup_datetime": pickup,
                "tpep_dropoff_datetime": dropoff,
                "passenger_count": random.randint(1, 4),
                "trip_distance": distance,
                "RatecodeID": 1,
                "store_and_fwd_flag": "N",
                "PULocationID": random.randint(1, 265),
                "DOLocationID": random.randint(1, 265),
                "payment_type": random.choice([1, 2]),
                "fare_amount": fare,
                "tip_amount": tip,
                "tolls_amount": 0.0,
                "improvement_surcharge": 1.0,
                "total_amount": fare + tip + 1.0 + cbd_fee,
                "congestion_surcharge": 2.5,
                "Airport_fee": 0.0,
                "cbd_congestion_fee": cbd_fee,
            }
        )
    frame = pd.DataFrame(records)
    if rows >= 10:
        frame.loc[2, "trip_distance"] = -2
        frame.loc[5, "tpep_dropoff_datetime"] = frame.loc[5, "tpep_pickup_datetime"] - timedelta(minutes=5)
        frame.loc[8, "total_amount"] = 10000
    return frame


def make_demo_zones() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "LocationID": range(1, 266),
            "Borough": ["Demo Borough"] * 265,
            "Zone": [f"Zone {value}" for value in range(1, 266)],
            "service_zone": ["Yellow Zone"] * 265,
        }
    )
