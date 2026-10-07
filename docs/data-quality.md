# Data quality rules

The pipeline rejects rows when:

- pickup/dropoff timestamps cannot be parsed;
- dropoff is not after pickup;
- trip duration exceeds the configured limit;
- trip distance is negative or beyond the configured limit;
- fare or total amount is negative;
- total amount is implausibly high;
- pickup/dropoff taxi-zone IDs are outside the configured range.

Rejected records are exported separately with a reason. They are not silently deleted.
