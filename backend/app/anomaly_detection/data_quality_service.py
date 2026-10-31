import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

COUNT_COLUMNS = [
    "total_count",
    "good_count",
    "reject_count",
    "inspected_count",
    "inspection_fail_count"
]


def detect_data_quality_issues():

    file_path = DATA_DIR / "production_counts.csv"
    df = pd.read_csv(file_path)

    # Rule 1: Good count + reject count must equal total count
    df["count_mismatch"] = (
        df["good_count"] + df["reject_count"] != df["total_count"]
    )

    # Rule 2: Inspected quantity cannot exceed total quantity
    df["inspection_exceeds_total"] = (
        df["inspected_count"] > df["total_count"]
    )

    # Rule 3: Inspection failures cannot exceed inspected quantity
    df["failures_exceed_inspected"] = (
        df["inspection_fail_count"] > df["inspected_count"]
    )

    # Rule 4: Production quantities cannot be negative
    df["negative_counts"] = (df[COUNT_COLUMNS] < 0).any(axis=1)

    issue_columns = [
        "count_mismatch",
        "inspection_exceeds_total",
        "failures_exceed_inspected",
        "negative_counts"
    ]

    anomalies = df[df[issue_columns].any(axis=1)].copy()

    anomalies["detection_type"] = "DATA_QUALITY"
    anomalies["correction_status"] = "NOT_APPLICABLE"

    return anomalies


def get_data_quality_summary():

    anomalies = detect_data_quality_issues()

    return {
        "detection_type": "DATA_QUALITY",
        "total_records_checked": 491156,
        "total_issues": int(len(anomalies)),
        "count_mismatch": int(anomalies["count_mismatch"].sum()),
        "inspection_exceeds_total": int(
            anomalies["inspection_exceeds_total"].sum()
        ),
        "failures_exceed_inspected": int(
            anomalies["failures_exceed_inspected"].sum()
        ),
        "negative_counts": int(anomalies["negative_counts"].sum()),
        "sample_records": anomalies.head(20).to_dict(orient="records")
    }