
import pandas as pd

from app.anomaly_detection.feature_engineering import (
    create_machine_features
)

from app.anomaly_detection.anomaly_detector import (
    load_anomaly_model
)


def run_anomaly_detection():
    """
    Load the trained Isolation Forest model,
    generate current machine features and detect anomalies.
    """

    # Load trained model and feature configuration.
    model_bundle = load_anomaly_model()

    model = model_bundle["model"]
    feature_columns = model_bundle["feature_columns"]

    # Fetch latest available production data from PostgreSQL.
    df = create_machine_features()

    # Prepare model input.
    X = (
        df[feature_columns]
        .replace([float("inf"), float("-inf")], pd.NA)
        .fillna(0)
    )

    # Run anomaly predictions.
    df["anomaly_prediction"] = model.predict(X)

    # Higher score means more unusual.
    df["anomaly_score"] = -model.decision_function(X)

    df["anomaly_status"] = df["anomaly_prediction"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # Assign relative severity among detected anomalies.
    anomaly_mask = df["anomaly_prediction"] == -1

    df["severity"] = "None"

    if anomaly_mask.any():

        anomaly_scores = df.loc[
            anomaly_mask, "anomaly_score"
        ]

        low_threshold = anomaly_scores.quantile(0.33)
        high_threshold = anomaly_scores.quantile(0.66)

        df.loc[anomaly_mask, "severity"] = (
            df.loc[anomaly_mask, "anomaly_score"]
            .apply(
                lambda score:
                    "High" if score >= high_threshold
                    else "Medium" if score >= low_threshold
                    else "Low"
            )
        )

    return df


def get_machine_anomalies(machine_id=None):
    """
    Return anomaly records, optionally filtered by machine.
    """

    df = run_anomaly_detection()

    anomalies = df[
        df["anomaly_status"] == "Anomaly"
    ].copy()

    if machine_id:
        anomalies = anomalies[
            anomalies["machine_id"] == machine_id
        ]

    anomalies = anomalies.sort_values(
        "anomaly_score",
        ascending=False
    )

    return anomalies.to_dict(orient="records")
