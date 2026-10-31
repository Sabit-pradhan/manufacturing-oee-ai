@'
# Manufacturing OEE Analytics - Data Dictionary

## 1. Dataset Overview

This project uses synthetic manufacturing data for OEE monitoring and AI analytics.

The dataset represents:
- 5 production lines
- 30 machines
- 20 products
- 90 days of manufacturing activity
- 100,000 machine state events
- 500,000 combined production count and inspection records

## 2. Original Source Data

Location: data/raw/realtime_manufacturing_dataset/

- lines.csv
- machines.csv
- products.csv
- shifts.csv
- state_events_100k.csv
- count_inspection_500k.csv

Original source records must remain unchanged.

## 3. Processed Datasets

Location: data/processed/

- plants.csv: Plant master derived from source line information.
- lines.csv: Production line information.
- machines.csv: Machine master.
- products.csv: Product master and standard cycle times.
- shifts.csv: Shift master.
- shift_dimension.csv: Shift data with canonical shift identifiers.
- production_orders.csv: Generated production order groupings.
- production_counts.csv: Production count records.
- count_corrections.csv: Separate count correction records.
- quality_inspections.csv: Quality inspection information.
- state_events.csv: Machine state event records.
- downtime_reasons.csv: Downtime event classifications.
- ideal_cycle_times.csv: Product-machine cycle time mapping.
- oee_aggregates_provisional.csv: Preliminary OEE calculations.

## 4. Ground Truth

Location: data/ground_truth/

ground_truth.csv contains synthetic anomaly candidates for testing validation and anomaly detection.

These labels are derived from deterministic rules and are not verified real-world incident labels.

## 5. OEE Formulas

Availability = Run Time / Planned Production Time

Performance = Ideal Cycle Time * Total Count / Run Time

Quality = Good Count / Total Count

OEE = Availability * Performance * Quality

## 6. Important Limitations

1. Source events are sampled and do not form a guaranteed continuous machine timeline.
2. Count corrections are kept separate because target-record linkage is not available.
3. The source does not clearly define cumulative versus incremental counts.
4. Machine-specific ideal cycle time calibration is not supplied.
5. OEE aggregates are provisional and must not be treated as production-grade results.
6. All source data and generated anomaly labels are synthetic.

## 7. Reproducibility

Random seed: 20261022
'@ | Set-Content .\data\docs\DATA_DICTIONARY.md -Encoding UTF8