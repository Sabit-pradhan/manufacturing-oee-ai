
from sqlalchemy import text

from app.database.connection import engine
from app.oee_engine.oee_calculator import calculate_oee


def calculate_machine_oee(machine_id: str, shift_id: str):
    """
    Calculate provisional machine-level OEE for a shift.

    Supports multiple products using product-specific
    ideal cycle times.

    Assumption: PRODUCTION_COUNT rows are additive records.
    COUNT_CORRECTION rows are excluded pending validation
    of their correction semantics.
    """

    with engine.connect() as connection:

        # 1. Retrieve shift duration
        shift = connection.execute(
            text("""
                SELECT start_time, end_time
                FROM shifts
                WHERE shift_id = :shift_id
            """),
            {"shift_id": shift_id}
        ).mappings().first()

        if not shift:
            raise ValueError(f"Shift not found: {shift_id}")

        shift_duration = (
            shift["end_time"] - shift["start_time"]
        ).total_seconds()

        # 2. Aggregate production by product
        products = connection.execute(
            text("""
                SELECT
                    pc.product_id,
                    p.standard_cycle_time_sec,
                    SUM(pc.total_count) AS total_count,
                    SUM(pc.good_count) AS good_count
                FROM production_counts pc
                JOIN products p
                    ON p.product_id = pc.product_id
                WHERE pc.machine_id = :machine_id
                  AND pc.shift_id = :shift_id
                  AND pc.record_type = 'PRODUCTION_COUNT'
                GROUP BY
                    pc.product_id,
                    p.standard_cycle_time_sec
            """),
            {
                "machine_id": machine_id,
                "shift_id": shift_id
            }
        ).mappings().all()

        if not products:
            raise ValueError("No production records found")

        # Calculate total production and ideal production time
        total_count = 0
        good_count = 0
        ideal_production_time = 0.0

        for product in products:
            product_total = int(product["total_count"] or 0)
            product_good = int(product["good_count"] or 0)
            cycle_time = float(product["standard_cycle_time_sec"])

            total_count += product_total
            good_count += product_good

            ideal_production_time += (
                cycle_time * product_total
            )

        # 3. Retrieve event durations for this shift
        events = connection.execute(
            text("""
                SELECT
                    event_type,
                    COALESCE(duration_seconds, 0) AS duration_seconds
                FROM state_events
                WHERE machine_id = :machine_id
                  AND event_timestamp >= :start_time
                  AND event_timestamp < :end_time
            """),
            {
                "machine_id": machine_id,
                "start_time": shift["start_time"],
                "end_time": shift["end_time"]
            }
        ).mappings().all()

    # 4. Separate planned breaks and downtime
    planned_break_sec = 0.0
    downtime_sec = 0.0

    for event in events:
        event_type = event["event_type"].upper()
        duration = max(float(event["duration_seconds"]), 0)

        if event_type == "PLANNED_BREAK":
            planned_break_sec += duration

        elif event_type in {
            "FAULT",
            "MICRO_STOP",
            "MAINTENANCE"
        }:
            downtime_sec += duration

    # 5. Calculate planned production time
    planned_production_time = (
        shift_duration - planned_break_sec
    )

    if planned_production_time <= 0:
        raise ValueError("Invalid planned production time")

    if planned_break_sec > shift_duration:
        raise ValueError("Planned breaks exceed shift duration")

    # 6. Calculate OEE
    result = calculate_oee(
        planned_production_time_sec=planned_production_time,
        downtime_sec=downtime_sec,
        ideal_cycle_time_sec=(
            ideal_production_time / total_count
            if total_count > 0 else 0
        ),
        total_count=total_count,
        good_count=good_count
    )

    return {
        "machine_id": machine_id,
        "shift_id": shift_id,
        "product_count": len(products),
        "total_count": total_count,
        "good_count": good_count,
        "ideal_production_time_sec": round(
            ideal_production_time, 2
        ),
        "shift_duration_sec": shift_duration,
        "planned_break_sec": planned_break_sec,
        "planned_production_time_sec": planned_production_time,
        **result
    }
