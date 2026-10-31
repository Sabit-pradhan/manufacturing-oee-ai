
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

from app.anomaly_detection.feature_engineering import (
    create_machine_features
)


# Features used by the anomaly detection model.
FEATURE_COLUMNS = [
    "total_count",
    "reject_rate",
    "production_deviation_pct",
    "product_count",
    "production_records"
]

MODEL_DIR = Path(__file__).resolve().parent / "saved_models"
MODEL_PATH = MODEL_DIR / "isolation_forest.joblib"


def train_anomaly_model(contamination=0.03):
    """
    Train an Isolation Forest model to identify
    unusual machine production patterns.

    contamination represents the assumed proportion
    of anomalies for this initial baseline.
    """

    df = create_machine_features()

    # Replace missing and infinite values before training.
    X = (
        df[FEATURE_COLUMNS]
        .replace([float("inf"), float("-inf")], pd.NA)
        .fillna(0)
    )

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    # Predict: 1 = normal, -1 = anomaly.
    df["anomaly_prediction"] = model.predict(X)

    # Higher score means more unusual.
    df["anomaly_score"] = -model.decision_function(X)

    df["anomaly_status"] = df["anomaly_prediction"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # Save model and its feature configuration.
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
            "contamination": contamination
        },
        MODEL_PATH
    )

    return df, model


def load_anomaly_model():
    """Load the previously trained model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Train the model first."
        )

    return joblib.load(MODEL_PATH)
