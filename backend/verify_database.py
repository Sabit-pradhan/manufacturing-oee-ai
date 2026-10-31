
from sqlalchemy import text
from app.database.connection import engine

tables = [
    "plants",
    "production_lines",
    "machines",
    "products",
    "shifts",
    "production_orders",
    "production_counts",
    "quality_inspections",
    "state_events",
]

print("\nDATABASE INGESTION VERIFICATION")
print("-" * 45)

with engine.connect() as connection:
    for table in tables:
        count = connection.execute(
            text(f'SELECT COUNT(*) FROM "{table}"')
        ).scalar_one()

        print(f"{table:<25} {count:>12,} rows")

print("\nVerification completed.")
