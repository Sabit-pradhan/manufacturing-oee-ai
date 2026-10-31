
from sqlalchemy import text
from app.database.connection import engine

with engine.connect() as connection:

    print("\n1. EVENT TYPE DISTRIBUTION")
    rows = connection.execute(text("""
        SELECT
            event_type,
            COUNT(*) AS event_count,
            SUM(COALESCE(duration_seconds, 0)) AS total_seconds,
            MIN(duration_seconds) AS min_seconds,
            MAX(duration_seconds) AS max_seconds
        FROM state_events
        GROUP BY event_type
        ORDER BY event_type
    """)).mappings().all()

    for row in rows:
        print(dict(row))

    print("\n2. EVENTS WITH INVALID DURATIONS")
    rows = connection.execute(text("""
        SELECT COUNT(*) AS invalid_duration_count
        FROM state_events
        WHERE duration_seconds < 0
    """)).mappings().first()
    print(dict(rows))

    print("\n3. EVENTS LONGER THAN ONE HOUR")
    rows = connection.execute(text("""
        SELECT
            event_id,
            machine_id,
            event_type,
            event_timestamp,
            duration_seconds
        FROM state_events
        WHERE duration_seconds > 3600
        ORDER BY duration_seconds DESC
        LIMIT 10
    """)).mappings().all()

    for row in rows:
        print(dict(row))

    print("\n4. EVENTS CROSSING SHIFT END")
    rows = connection.execute(text("""
        SELECT COUNT(*) AS crossing_shift_events
        FROM state_events e
        JOIN shifts s
          ON e.event_timestamp >= s.start_time
         AND e.event_timestamp < s.end_time
        WHERE e.duration_seconds > 0
          AND e.event_timestamp + (
              e.duration_seconds * INTERVAL '1 second'
          ) > s.end_time
    """)).mappings().first()
    print(dict(rows))

print("\nEvent diagnostic completed.")
