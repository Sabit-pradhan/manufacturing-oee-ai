
from sqlalchemy import text
from app.database.connection import engine

query = text("""
    SELECT
        CASE
            WHEN a.product_id = b.product_id
                THEN 'SAME_PRODUCT'
            ELSE 'DIFFERENT_PRODUCT'
        END AS product_comparison,

        COUNT(*) AS overlapping_pairs,

        COUNT(DISTINCT a.machine_id) AS affected_machines,

        SUM(
            EXTRACT(
                EPOCH FROM (
                    LEAST(
                        a.event_timestamp
                            + a.duration_seconds * INTERVAL '1 second',
                        b.event_timestamp
                            + b.duration_seconds * INTERVAL '1 second'
                    )
                    -
                    GREATEST(
                        a.event_timestamp,
                        b.event_timestamp
                    )
                )
            )
        ) AS total_overlap_seconds

    FROM state_events a

    JOIN state_events b
      ON a.machine_id = b.machine_id
     AND a.event_id < b.event_id

     AND a.event_type = 'RUN'
     AND b.event_type = 'RUN'

     AND a.event_timestamp <
         b.event_timestamp
         + b.duration_seconds * INTERVAL '1 second'

     AND b.event_timestamp <
         a.event_timestamp
         + a.duration_seconds * INTERVAL '1 second'

    WHERE a.duration_seconds > 0
      AND b.duration_seconds > 0

    GROUP BY product_comparison
    ORDER BY overlapping_pairs DESC
""")

with engine.connect() as connection:
    rows = connection.execute(query).mappings().all()

    print("\nRUN EVENT PRODUCT OVERLAP ANALYSIS")

    for row in rows:
        print(dict(row))

print("\nDiagnostic completed.")
