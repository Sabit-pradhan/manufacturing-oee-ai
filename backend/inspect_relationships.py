import pandas as pd
from pathlib import Path

p = Path("../data/processed")

corrections = pd.read_csv(p / "count_corrections.csv")
production = pd.read_csv(p / "production_counts.csv")
quality = pd.read_csv(p / "quality_inspections.csv")
cycle = pd.read_csv(p / "ideal_cycle_times.csv")

production_ids = set(production["record_id"].astype(str))
quality_ids = set(quality["source_record_id"].astype(str))
correction_targets = set(corrections["source_record_id"].astype(str))

print("\n1. COUNT CORRECTIONS")
print("Total corrections:", len(corrections))
print("Applied:", corrections["correction_applied"].sum())
print("Not applied:", (~corrections["correction_applied"]).sum())
print("Application statuses:")
print(corrections["application_status"].value_counts(dropna=False))
print("Correction source IDs matching production IDs:",
      len(correction_targets & production_ids))
print("Correction IDs equal source IDs:",
      (corrections["correction_id"].astype(str) ==
       corrections["source_record_id"].astype(str)).sum())

print("\n2. PRODUCTION AND QUALITY LINKAGE")
print("Production records:", len(production))
print("Quality records:", len(quality))
print("Matching production/quality source IDs:",
      len(production_ids & quality_ids))
print("Quality source IDs missing from production:",
      len(quality_ids - production_ids))

print("\n3. QUALITY RECONCILIATION")
print("Production good + reject mismatches:",
      (production["good_count"] + production["reject_count"] !=
       production["total_count"]).sum())
print("Quality good + reject mismatches:",
      (quality["good_count"] + quality["reject_count"] !=
       quality["inspected_count"]).sum())

print("\n4. IDEAL CYCLE TIME CALIBRATION")
print("Total mappings:", len(cycle))
print("Calibrated mappings:", cycle["is_calibrated"].sum())
print("Uncalibrated mappings:", (~cycle["is_calibrated"]).sum())
print("Mapping methods:")
print(cycle["mapping_method"].value_counts(dropna=False))

