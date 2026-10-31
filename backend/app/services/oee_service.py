
from datetime import datetime, timedelta

from sqlalchemy import text

from app.database.connection import engine
from app.oee_engine.oee_calculator import calculate_oee


DOWNTIME_TYPES = {
    "FAULT",
    "MICRO_STOP",
    "MAINTENANCE",
}


def _as_datetime(value):
    """Convert a database timestamp to datetime if necessary."""
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _merge_intervals(intervals):
    """Merge overlapping intervals to avoid double-counting time."""
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda item: item[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        previous_start, previous_end = merged[-1]

        if start <= previous_end:
            merged[-1] = (
                previous_start,
                max(previous_end, end),
            )
        else:
            merged.append((start, end))

    return merged


def _subtract_intervals(intervals, exclusions):
    """Remove excluded intervals from a collection of intervals."""
    result = []

    for start, end in intervals:
        remaining = [(start, end)]

        for exclude_start, exclude_end in exclusions:
            updated = []

            for current_start, current_end in remaining:
                if (
                    exclude_end <= current_start
                    or exclude_start >= current_end
                ):
                    updated.append((current_start, current_end))
                    continue

                if current_start < exclude_start:
                    updated.append((current_start, exclude_start))

                if exclude_end < current_end:
                    updated.append((exclude_end, current_end))

            remaining = updated

        result.extend(remaining)

    return result


def _duration(intervals):
    """Calculate total seconds represented by intervals."""
    return sum(
        (end - start).total_seconds()
        for start, end in intervals
    )


def calculate_machine_oee(machine_id: str, shift_id: str):
    """
    Calculate provisional machine-level OEE for a shift.

    Uses canonical event intervals for machine-state calculations.
    Production counts remain sourced from production_counts.

    Source events are sampled, not a guaranteed continuous
    machine timeline. Results remain provisional.
    """

    with engine.connect() as connection:

        # 1. Retrieve shift
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

        shift_start = _as_datetime(shift["start_time"])
        shift_end = _as_datetime(shift["end_time"])

        shift_duration = (
            shift_end - shift_start
        ).total_seconds()

        if shift_duration <= 0:
            raise ValueError("Invalid shift duration")

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
                "shift_id": shift_id,
            }
        ).mappings().all()

        if not products:
            raise ValueError(
                f"No production records found for "
                f"machine {machine_id}, shift {shift_id}"
            )

        total_count = 0
        good_count = 0
        ideal_production_time = 0.0

        for product in products:
            product_total = int(product["total_count"] or 0)
            product_good = int(product["good_count"] or 0)
            cycle_time = float(
                product["standard_cycle_time_sec"]
            )

            if product_total < 0 or product_good < 0:
                raise ValueError(
                    f"Negative production count for product "
                    f"{product['product_id']}"
                )

            if product_good > product_total:
                raise ValueError(
                    f"Good count exceeds total count for product "
                    f"{product['product_id']}"
                )

            if cycle_time <= 0:
                raise ValueError(
                    f"Invalid cycle time for product "
                    f"{product['product_id']}"
                )

            total_count += product_total
            good_count += product_good

            ideal_production_time += (
                cycle_time * product_total
            )

        if total_count <= 0:
            raise ValueError("Total production count must be positive")

        # 3. Retrieve only events that intersect this shift.
        events = connection.execute(
            text("""
                SELECT
                    event_id,
                    source_event_id,
                    event_timestamp,
                    event_type,
                    COALESCE(duration_seconds, 0)
                        AS duration_seconds
                FROM state_events
                WHERE machine_id = :machine_id
                  AND event_timestamp < :end_time
                  AND event_timestamp
                      + (
                          COALESCE(duration_seconds, 0)
                          * INTERVAL '1 second'
                      ) > :start_time
                ORDER BY event_timestamp
            """),
            {
                "machine_id": machine_id,
                "start_time": shift_start,
                "end_time": shift_end,
            }
        ).mappings().all()

    # 4. Build event intervals clipped to the shift
    planned_break_intervals = []
    downtime_intervals = []

    for event in events:
        event_type = str(event["event_type"]).upper()
        duration = float(event["duration_seconds"] or 0)

        if duration < 0:
            raise ValueError(
                f"Negative duration found for event "
                f"{event['event_id']}"
            )

        if duration == 0:
            continue

        event_start = _as_datetime(event["event_timestamp"])
        event_end = event_start + timedelta(seconds=duration)

        clipped_start = max(event_start, shift_start)
        clipped_end = min(event_end, shift_end)

        if clipped_start >= clipped_end:
            continue

        interval = (clipped_start, clipped_end)

        if event_type == "PLANNED_BREAK":
            planned_break_intervals.append(interval)

        elif event_type in DOWNTIME_TYPES:
            downtime_intervals.append(interval)

        # CHANGEOVER remains excluded pending classification.

    # 5. Merge overlapping intervals
    planned_break_intervals = _merge_intervals(
        planned_break_intervals
    )

    downtime_intervals = _merge_intervals(
        downtime_intervals
    )

    planned_break_sec = _duration(
        planned_break_intervals
    )

    # Exclude downtime occurring during planned breaks.
    effective_downtime_intervals = _subtract_intervals(
        downtime_intervals,
        planned_break_intervals
    )

    downtime_sec = _duration(
        effective_downtime_intervals
    )

    # 6. Calculate planned production time
    planned_production_time = (
        shift_duration - planned_break_sec
    )

    if planned_production_time <= 0:
        raise ValueError(
            "Invalid planned production time"
        )

    if downtime_sec > planned_production_time:
        raise ValueError(
            "Downtime exceeds planned production time"
        )

    # 7. Calculate OEE
    result = calculate_oee(
        planned_production_time_sec=planned_production_time,
        downtime_sec=downtime_sec,
        ideal_cycle_time_sec=(
            ideal_production_time / total_count
        ),
        total_count=total_count,
        good_count=good_count,
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
        "planned_break_sec": round(
            planned_break_sec, 2
        ),
        "planned_production_time_sec": round(
            planned_production_time, 2
        ),
        "event_count_considered": len(events),
        "changeover_included": False,
        "oee_status": "PROVISIONAL",
        "calculation_limitations": [
            "Source events are sampled, not a continuous timeline.",
            "Ideal cycle times are not machine-calibrated.",
            "Count corrections are excluded pending linkage.",
            "Changeover is excluded from downtime.",
            "Overlapping RUN intervals were resolved in the canonical event dataset.",
        ],
        **result,
    }
