import pandas as pd
from pathlib import Path

p = Path("../data/processed")

production = pd.read_csv(p / "production_counts.csv")
quality = pd.read_csv(p / "quality_inspections.csv")

merged = production.merge(
    quality,
    left_on="record_id",
    right_on="source_record_id",
    suffixes=("_production", "_quality"),
    validate="one_to_one"
)

comparisons = [
    ("total_count", None),
    ("good_count", "good_count"),
    ("reject_count", "reject_count"),
    ("inspected_count", "inspected_count"),
    ("inspection_fail_count", "inspection_fail_count"),
]

print("PRODUCTION VS QUALITY FIELD COMPARISON")

for production_col, quality_col in comparisons:
    if quality_col is None:
        continue

    left = f"{production_col}_production"
    right = f"{quality_col}_quality"

    matches = (merged[left] == merged[right]).sum()

    print(f"{production_col}: {matches}/{len(merged)} matching")

print("\nINSPECTED COUNT COMPARISON")
print(
    "Production inspected count total:",
    merged["inspected_count_production"].sum()
)
print(
    "Quality inspected count total:",
    merged["inspected_count_quality"].sum()
)

print(
    "Inspected count mismatches:",
    (
        merged["inspected_count_production"]
        != merged["inspected_count_quality"]
    ).sum()
)

print("\nSAMPLE DIFFERENCES")

different = merged[
    merged["inspected_count_production"]
    != merged["inspected_count_quality"]
]

print(
    different[
        [
            "record_id",
            "inspected_count_production",
            "inspected_count_quality",
            "good_count_production",
            "reject_count_production",
        ]
    ].head(10).to_string(index=False)
)