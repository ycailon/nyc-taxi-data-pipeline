CREATE TABLE IF NOT EXISTS fact_trip (
    trip_id TEXT PRIMARY KEY,
    pickup_datetime TEXT NOT NULL,
    dropoff_datetime TEXT NOT NULL,
    pickup_date TEXT NOT NULL,
    pickup_hour INTEGER,
    trip_minutes REAL,
    trip_distance REAL,
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    passenger_count REAL,
    payment_type REAL,
    fare_amount REAL,
    tip_amount REAL,
    tolls_amount REAL,
    total_amount REAL,
    congestion_surcharge REAL,
    airport_fee REAL,
    cbd_congestion_fee REAL,
    source_year INTEGER NOT NULL,
    source_month INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fact_trip_month ON fact_trip(source_year, source_month);
CREATE INDEX IF NOT EXISTS idx_fact_trip_pickup_date ON fact_trip(pickup_date);
CREATE INDEX IF NOT EXISTS idx_fact_trip_pickup_zone ON fact_trip(pickup_location_id);
CREATE INDEX IF NOT EXISTS idx_fact_trip_dropoff_zone ON fact_trip(dropoff_location_id);
