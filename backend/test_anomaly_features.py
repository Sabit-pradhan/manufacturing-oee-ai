
from app.anomaly_detection.feature_engineering import (
    create_machine_features
)

df = create_machine_features()

print("\nMACHINE ANOMALY DETECTION FEATURES")
print("=" * 80)

print("Total records:", len(df))
print("Machines:", df["machine_id"].nunique())

print("\nFeature columns:")
print(df.columns.tolist())

print("\nSample records:")
print(
    df[
        [
            "machine_id",
            "production_date",
            "total_count",
            "reject_rate",
            "good_rate",
            "rolling_avg_production",
            "production_deviation_pct"
        ]
    ].head(10).to_string(index=False)
)
