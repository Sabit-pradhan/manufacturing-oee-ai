
from sqlalchemy import text
from app.database.connection import engine

machine_id = "M001"
shift_id = "20260101_A"

with engine.connect() as connection:

    print("\n1. PRODUCTION BY PRODUCT")

    rows = connection.execute(
        text("""
            SELECT
                pc.product_id,
                p.standard_cycle_time_sec,
                COUNT(*) AS records,
                SUM(pc.total_count) AS total_count,
                SUM(pc.good_count) AS good_count
            FROM production_counts pc
            JOIN products p ON p.product_id = pc.product_id
            WHERE pc.machine_id = :machine_id
              AND pc.shift_id = :shift_id
              AND pc.record_type = 'PRODUCTION_COUNT'
            GROUP BY pc.product_id, p.standard_cycle_time_sec
            ORDER BY pc.product_id
        """),
        {"machine_id": machine_id, "shift_id": shift_id}
    ).mappings().all()

    for row in rows:
        print(dict(row))

    print("\n2. DOWNTIME EVENTS")

    events = connection.execute(
        text("""
            SELECT event_type, COUNT(*) AS event_count,
                   SUM(duration_seconds) AS total_seconds
            FROM state_events
            WHERE machine_id = :machine_id
              AND event_timestamp >= (
                  SELECT start_time FROM shifts WHERE shift_id = :shift_id
              )
              AND event_timestamp < (
                  SELECT end_time FROM shifts WHERE shift_id = :shift_id
              )
            GROUP BY event_type
            ORDER BY event_type
        """),
        {"machine_id": machine_id, "shift_id": shift_id}
    ).mappings().all()

    for event in events:
        print(dict(event))

    print("\n3. SHIFT TIME")

    shift = connection.execute(
        text("""
            SELECT start_time, end_time
            FROM shifts
            WHERE shift_id = :shift_id
        """),
        {"shift_id": shift_id}
    ).mappings().first()

    print(dict(shift) if shift else "Shift not found")
