import pandas as pd
from sqlalchemy import text

from app.database.connection import engine

CSV_PATH = "../data/processed/state_events_canonical.csv"

df = pd.read_csv(CSV_PATH)

# Add database columns not present in the canonical CSV.
df["canonical_event_id"] = df["event_id"]
df["duration_minutes"] = df["duration_seconds"] / 60.0

# Ensure database column order and names.
columns = [
    "event_id",
    "event_timestamp",
    "machine_id",
    "line_id",
    "event_type",
    "product_id",
    "duration_seconds",
    "recorded_by",
    "severity",
    "source_event_id",
    "canonical_event_id",
    "duration_minutes",
]

df = df[columns]
df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
df = df.astype(object).where(pd.notna(df), None)

records = df.to_dict(orient="records")

insert_sql = text("""
    INSERT INTO state_events (
        event_id, event_timestamp, machine_id, line_id,
        event_type, product_id, duration_seconds,
        recorded_by, severity, source_event_id,
        canonical_event_id, duration_minutes
    )
    VALUES (
        :event_id, :event_timestamp, :machine_id, :line_id,
        :event_type, :product_id, :duration_seconds,
        :recorded_by, :severity, :source_event_id,
        :canonical_event_id, :duration_minutes
    )
""")

with engine.begin() as connection:
    # Replace only the state_events table contents.
    connection.execute(text("DELETE FROM state_events"))

    batch_size = 5000

    for start in range(0, len(records), batch_size):
        connection.execute(
            insert_sql,
            records[start:start + batch_size]
        )

    final_count = connection.execute(
        text("SELECT COUNT(*) FROM state_events")
    ).scalar_one()

print("STATE EVENTS RELOADED SUCCESSFULLY")
print("Expected rows:", len(records))
print("Database rows:", final_count)
