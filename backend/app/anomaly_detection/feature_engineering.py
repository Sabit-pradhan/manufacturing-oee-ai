
import pandas as pd

from sqlalchemy import text

from app.database.connection import SessionLocal


def fetch_machine_production_data():
    """
    Fetch machine-level production and downtime features
    from PostgreSQL.
    """

    query = text("""
        SELECT
            pc.machine_id,
            DATE(pc.record_timestamp) AS production_date,

            SUM(pc.total_count) AS total_count,
            SUM(pc.good_count) AS good_count,
            SUM(pc.reject_count) AS reject_count,

            COUNT(pc.production_count_id) AS production_records,

            COUNT(DISTINCT pc.product_id) AS product_count

        FROM production_counts pc

        WHERE pc.record_type = 'PRODUCTION_COUNT'

        GROUP BY
            pc.machine_id,
            DATE(pc.record_timestamp)

        ORDER BY
            production_date,
            pc.machine_id
    """)

    db = SessionLocal()

    try:
        rows = db.execute(query).mappings().all()
        return pd.DataFrame(rows)

    finally:
        db.close()


def create_machine_features():
    """
    Generate machine-level anomaly detection features.
    """

    df = fetch_machine_production_data()

    if df.empty:
        raise ValueError("No production data found in database")

    df["production_date"] = pd.to_datetime(df["production_date"])

    df["reject_rate"] = (
        df["reject_count"] /
        df["total_count"].replace(0, pd.NA)
    ).fillna(0)

    df["good_rate"] = (
        df["good_count"] /
        df["total_count"].replace(0, pd.NA)
    ).fillna(0)

    # Calculate rolling production averages per machine.
    df = df.sort_values(["machine_id", "production_date"])

    df["rolling_avg_production"] = (
        df.groupby("machine_id")["total_count"]
        .transform(
            lambda series: series.shift(1).rolling(
                window=7,
                min_periods=1
            ).mean()
        )
    )

    df["production_deviation"] = (
        df["total_count"] - df["rolling_avg_production"]
    )

    df["production_deviation_pct"] = (
        df["production_deviation"] /
        df["rolling_avg_production"].replace(0, pd.NA)
    ).fillna(0)

    return df
