DROP VIEW IF EXISTS mart_daily_kpis;
CREATE VIEW mart_daily_kpis AS
SELECT
    pickup_date,
    COUNT(*) AS trip_count,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_minutes) AS avg_trip_minutes,
    SUM(fare_amount) AS fare_amount,
    SUM(tip_amount) AS tip_amount,
    SUM(total_amount) AS total_amount,
    SUM(cbd_congestion_fee) AS cbd_congestion_fee
FROM fact_trip
GROUP BY pickup_date;

DROP VIEW IF EXISTS mart_hourly_demand;
CREATE VIEW mart_hourly_demand AS
SELECT
    pickup_date,
    pickup_hour,
    COUNT(*) AS trip_count,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(total_amount) AS avg_total_amount
FROM fact_trip
GROUP BY pickup_date, pickup_hour;

DROP VIEW IF EXISTS mart_zone_performance;
CREATE VIEW mart_zone_performance AS
SELECT
    z.borough AS pickup_borough,
    z.zone AS pickup_zone,
    COUNT(*) AS trip_count,
    AVG(t.trip_distance) AS avg_trip_distance,
    AVG(t.fare_amount) AS avg_fare,
    AVG(t.total_amount) AS avg_total_amount
FROM fact_trip t
LEFT JOIN dim_zone z ON z.location_id = t.pickup_location_id
GROUP BY z.borough, z.zone;

DROP VIEW IF EXISTS mart_route_performance;
CREATE VIEW mart_route_performance AS
SELECT
    p.zone AS pickup_zone,
    d.zone AS dropoff_zone,
    COUNT(*) AS trip_count,
    AVG(t.trip_minutes) AS avg_trip_minutes,
    AVG(t.trip_distance) AS avg_trip_distance,
    AVG(t.total_amount) AS avg_total_amount
FROM fact_trip t
LEFT JOIN dim_zone p ON p.location_id = t.pickup_location_id
LEFT JOIN dim_zone d ON d.location_id = t.dropoff_location_id
GROUP BY p.zone, d.zone;
