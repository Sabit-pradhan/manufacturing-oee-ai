
import pandas as pd

production = pd.read_csv(
    r"..\data\processed\production_counts.csv"
)

corrections = pd.read_csv(
    r"..\data\processed\count_corrections.csv"
)

production["record_timestamp"] = pd.to_datetime(
    production["record_timestamp"]
)

corrections["record_timestamp"] = pd.to_datetime(
    corrections["record_timestamp"]
)

production = production.rename(
    columns={"record_timestamp": "production_timestamp"}
)

corrections = corrections.rename(
    columns={"record_timestamp": "correction_timestamp"}
)

keys = ["machine_id", "line_id", "product_id"]

production = production.sort_values("production_timestamp")
corrections = corrections.sort_values("correction_timestamp")

before = pd.merge_asof(
    corrections,
    production,
    left_on="correction_timestamp",
    right_on="production_timestamp",
    by=keys,
    direction="backward",
    suffixes=("_correction", "_production")
)

after = pd.merge_asof(
    corrections,
    production,
    left_on="correction_timestamp",
    right_on="production_timestamp",
    by=keys,
    direction="forward",
    suffixes=("_correction", "_production")
)

before["gap_minutes"] = (
    before["correction_timestamp"]
    - before["production_timestamp"]
).dt.total_seconds() / 60

after["gap_minutes"] = (
    after["production_timestamp"]
    - after["correction_timestamp"]
).dt.total_seconds() / 60

print("\nCORRECTION MATCH STATISTICS")
print("=" * 65)

total = len(corrections)

for minutes in [1, 5, 15, 30, 60]:

    before_match = (
        before["gap_minutes"].le(minutes)
        & before["production_timestamp"].notna()
    )

    after_match = (
        after["gap_minutes"].le(minutes)
        & after["production_timestamp"].notna()
    )

    either_match = before_match | after_match
    both_match = before_match & after_match

    print(f"\nWithin {minutes} minutes:")
    print(
        f"Before: {before_match.sum()} "
        f"({before_match.mean() * 100:.2f}%)"
    )
    print(
        f"After: {after_match.sum()} "
        f"({after_match.mean() * 100:.2f}%)"
    )
    print(
        f"Either direction: {either_match.sum()} "
        f"({either_match.mean() * 100:.2f}%)"
    )
    print(
        f"Both directions: {both_match.sum()} "
        f"({both_match.mean() * 100:.2f}%)"
    )

print("\nUNMATCHED CORRECTIONS")
print(
    "No production candidate within 60 minutes:",
    (
        before["gap_minutes"].gt(60)
        & after["gap_minutes"].gt(60)
    ).sum()
)

print("\nAnalysis completed.")
