
from sqlalchemy import text
from app.database.connection import engine

query = text("""
    SELECT
        COUNT(*) AS total_run_overlap_pairs,

        COUNT(*) FILTER (
            WHERE a.product_id = b.product_id
        ) AS same_product_pairs,

        COUNT(*) FILTER (
            WHERE a.product_id IS DISTINCT FROM b.product_id
        ) AS different_product_pairs,

        COUNT(DISTINCT a.machine_id) AS affected_machines

    FROM state_events a
    JOIN state_events b
      ON a.machine_id = b.machine_id
     AND a.event_id < b.event_id

     AND a.event_type = 'RUN'
     AND b.event_type = 'RUN'

     AND a.event_timestamp <
         b.event_timestamp
         + (COALESCE(b.duration_seconds, 0) * INTERVAL '1 second')

     AND b.event_timestamp <
         a.event_timestamp
         + (COALESCE(a.duration_seconds, 0) * INTERVAL '1 second')

    WHERE COALESCE(a.duration_seconds, 0) > 0
      AND COALESCE(b.duration_seconds, 0) > 0
""")

with engine.connect() as connection:
    result = connection.execute(query).mappings().first()
    print("\nRUN OVERLAP COUNT VERIFICATION")
    print(dict(result))
    print("\nVerification completed.")
