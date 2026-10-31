
from collections import Counter

from app.anomaly_detection.anomaly_service import (
    run_anomaly_detection,
    get_machine_anomalies
)


if __name__ == "__main__":

    df = run_anomaly_detection()

    print("\nMACHINE ANOMALY ANALYSIS")
    print("=" * 90)

    print("Total observations:", len(df))
    print("Machines:", df["machine_id"].nunique())

    print("\nAnomaly distribution:")
    print(df["anomaly_status"].value_counts())

    print("\nSeverity distribution:")
    print(Counter(df.loc[
        df["anomaly_status"] == "Anomaly",
        "severity"
    ]))

    print("\nTOP 15 MACHINE ANOMALIES")
    print("-" * 90)

    anomalies = get_machine_anomalies()

    for row in anomalies[:15]:
        print(
            f"{row['machine_id']:<8}"
            f"{str(row['production_date'].date()):<15}"
            f"Score: {row['anomaly_score']:.5f}  "
            f"Severity: {row['severity']}"
        )

    print("\nMachine-specific anomaly example:")

    machine_results = get_machine_anomalies("M013")

    print("M013 anomaly records:", len(machine_results))

    print("\nAnomaly service test completed.")
