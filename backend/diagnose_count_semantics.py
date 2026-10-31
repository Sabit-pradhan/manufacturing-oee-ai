
from sqlalchemy import text
from app.database.connection import engine

with engine.connect() as connection:

    print("\n1. RECORD TYPE DISTRIBUTION")

    rows = connection.execute(text("""
        SELECT
            record_type,
            COUNT(*) AS records,
            SUM(total_count) AS total_count,
            SUM(good_count) AS good_count,
            SUM(count_adjustment) AS adjustments
        FROM production_counts
        GROUP BY record_type
        ORDER BY record_type
    """)).mappings().all()

    for row in rows:
        print(dict(row))

    print("\n2. CORRECTION RECORD SAMPLES")

    rows = connection.execute(text("""
        SELECT
            record_id,
            record_timestamp,
            machine_id,
            total_count,
            good_count,
            reject_count,
            count_adjustment,
            source_record_id,
            production_count_id
        FROM production_counts
        WHERE record_type = 'COUNT_CORRECTION'
        LIMIT 10
    """)).mappings().all()

    for row in rows:
        print(dict(row))

    print("\n3. COUNT ADJUSTMENT DISTRIBUTION")

    rows = connection.execute(text("""
        SELECT
            COUNT(*) AS records,
            COUNT(*) FILTER (
                WHERE count_adjustment <> 0
            ) AS nonzero_adjustments,
            MIN(count_adjustment) AS minimum_adjustment,
            MAX(count_adjustment) AS maximum_adjustment
        FROM production_counts
    """)).mappings().all()

    for row in rows:
        print(dict(row))

print("\nDiagnostic completed.")
