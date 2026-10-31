
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from app.database.connection import engine


# Project data directory
DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "processed"

# Load master tables before dependent tables
DATASETS = [
    ("plants.csv", "plants", {}),
    ("lines.csv", "production_lines", {"plant": "plant_id"}),
    ("machines.csv", "machines", {}),
    ("products.csv", "products", {}),
    ("shifts.csv", "shifts", {}),
    ("production_orders.csv", "production_orders", {}),
    ("production_counts.csv", "production_counts", {}),
    ("quality_inspections.csv", "quality_inspections", {}),
    ("state_events_canonical.csv", "state_events", {}),
]

BATCH_SIZE = 5000


def load_dataset(filename, table_name, column_mapping):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    print(f"\nLoading {filename} into {table_name}...")

    total_inserted = 0

    # Read the CSV in batches to control memory usage
    for chunk in pd.read_csv(file_path, chunksize=BATCH_SIZE):

        # Map source column names to database column names
        chunk = chunk.rename(columns=column_mapping)

        # Convert pandas missing values to Python None
        chunk = chunk.astype(object).where(pd.notna(chunk), None)

        records = chunk.to_dict(orient="records")

        if not records:
            continue

        # Insert this batch using SQLAlchemy
        columns = list(records[0].keys())
        column_sql = ", ".join(f'"{col}"' for col in columns)
        values_sql = ", ".join(f":{col}" for col in columns)

        query = text(
            f'INSERT INTO "{table_name}" ({column_sql}) '
            f"VALUES ({values_sql})"
        )

        with engine.begin() as connection:
            connection.execute(query, records)

        total_inserted += len(records)

    print(f"Inserted {total_inserted:,} rows into {table_name}")
    return total_inserted


def load_all_datasets():
    results = {}

    try:
        for filename, table_name, mapping in DATASETS:
            results[table_name] = load_dataset(
                filename,
                table_name,
                mapping
            )

        print("\nAll datasets loaded successfully!")

        print("\nFinal ingestion summary:")
        for table, count in results.items():
            print(f"{table}: {count:,} rows")

    except Exception as error:
        print(f"\nDatabase ingestion failed: {error}")
        raise


if __name__ == "__main__":
    load_all_datasets()
