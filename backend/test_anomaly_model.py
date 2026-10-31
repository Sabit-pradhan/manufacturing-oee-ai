
from app.anomaly_detection.anomaly_detector import (
    train_anomaly_model
)

df, model = train_anomaly_model(contamination=0.03)

print("\nISOLATION FOREST MODEL RESULTS")
print("=" * 80)

print("Total records:", len(df))
print("Machines:", df["machine_id"].nunique())

print("\nAnomaly distribution:")
print(df["anomaly_status"].value_counts())

print("\nSample anomaly records:")

anomalies = df[df["anomaly_status"] == "Anomaly"]

print(
    anomalies[
        [
            "machine_id",
            "production_date",
            "total_count",
            "reject_rate",
            "production_deviation_pct",
            "anomaly_score",
            "anomaly_status"
        ]
    ]
    .sort_values("anomaly_score", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\nModel training completed.")
