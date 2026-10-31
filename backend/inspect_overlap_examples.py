
from sqlalchemy import text
from app.database.connection import engine

query = text("""
    SELECT
        a.event_id AS event_a,
        b.event_id AS event_b,
        a.machine_id,

        a.event_type AS type_a,
        b.event_type AS type_b,

        a.event_timestamp AS start_a,
        b.event_timestamp AS start_b,

        a.duration_seconds AS duration_a,
        b.duration_seconds AS duration_b,

        a.product_id AS product_a,
        b.product_id AS product_b,

        a.recorded_by AS recorded_by_a,
        b.recorded_by AS recorded_by_b,

        a.severity AS severity_a,
        b.severity AS severity_b,

        a.source_event_id AS source_id_a,
        b.source_event_id AS source_id_b,

        a.canonical_event_id AS canonical_id_a,
        b.canonical_event_id AS canonical_id_b,

        EXTRACT(
            EPOCH FROM (
                LEAST(
                    a.event_timestamp
                        + (a.duration_seconds * INTERVAL '1 second'),
                    b.event_timestamp
                        + (b.duration_seconds * INTERVAL '1 second')
                )
                -
                GREATEST(a.event_timestamp, b.event_timestamp)
            )
        ) AS overlap_seconds

    FROM state_events a
    JOIN state_events b
      ON a.machine_id = b.machine_id
     AND a.event_id < b.event_id

     AND a.event_timestamp <
         b.event_timestamp
         + (COALESCE(b.duration_seconds, 0) * INTERVAL '1 second')

     AND b.event_timestamp <
         a.event_timestamp
         + (COALESCE(a.duration_seconds, 0) * INTERVAL '1 second')

    WHERE COALESCE(a.duration_seconds, 0) > 0
      AND COALESCE(b.duration_seconds, 0) > 0

      AND (
          (a.event_type = 'RUN' AND b.event_type = 'RUN')
          OR
          (a.event_type = 'RUN' AND b.event_type = 'FAULT')
          OR
          (a.event_type = 'RUN' AND b.event_type = 'PLANNED_BREAK')
          OR
          (a.event_type = 'CHANGEOVER' AND b.event_type = 'RUN')
      )

    ORDER BY a.event_timestamp
    LIMIT 20
""")

with engine.connect() as connection:
    rows = connection.execute(query).mappings().all()

    print("\nOVERLAPPING EVENT SOURCE DETAILS")

    for row in rows:
        print(dict(row))

print("\nInspection completed.")
