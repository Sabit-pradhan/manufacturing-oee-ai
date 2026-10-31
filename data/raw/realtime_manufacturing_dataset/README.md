# Synthetic Real-Time Manufacturing Dataset

## Scope
- 5 production lines; 30 machines (6 per line); 20 products
- 90 days: 2026-01-01 through 2026-03-31
- 3 shifts per day (A: 06:00-14:00, B: 14:00-22:00, C: 22:00-06:00)
- 100,000 timestamped machine state events
- 500,000 production count / inspection records

## Files
- lines.csv: line master
- machines.csv: machine master and nominal rate
- products.csv: product master and standard cycle time
- shifts.csv: shift calendar
- state_events_100k.csv: state event stream
- count_inspection_500k.csv: count and quality inspection fact records

## State event types
RUN, PLANNED_BREAK, MICRO_STOP, CHANGEOVER, MAINTENANCE, FAULT.
Each event has a timestamp and duration_seconds. Events are synthetic event samples,
not a guaranteed gap-free state timeline. For accurate OEE, derive machine state
intervals by sorting events per machine and resolving overlaps.

## Count/inspection fields
total_count, good_count, reject_count, inspected_count, inspection_fail_count.
COUNT_CORRECTION rows include signed count_adjustment values. These are adjustment
transactions and should be applied to the relevant production totals; do not blindly
sum correction rows as new production.

## Important
This is synthetic demo data, not actual factory telemetry. Timestamps are spread
across the 90-day window to simulate an event stream. For streaming tests, replay
the CSV rows ordered by timestamp and publish them at a chosen rate.
