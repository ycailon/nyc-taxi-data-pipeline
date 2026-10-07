-- Busiest pickup hours.
SELECT pickup_hour, SUM(trip_count) AS trips
FROM mart_hourly_demand
GROUP BY pickup_hour
ORDER BY trips DESC;

-- Highest-volume pickup zones.
SELECT pickup_borough, pickup_zone, trip_count, avg_fare, avg_trip_distance
FROM mart_zone_performance
ORDER BY trip_count DESC
LIMIT 20;

-- Route performance.
SELECT pickup_zone, dropoff_zone, trip_count, avg_trip_minutes, avg_total_amount
FROM mart_route_performance
ORDER BY trip_count DESC
LIMIT 25;
