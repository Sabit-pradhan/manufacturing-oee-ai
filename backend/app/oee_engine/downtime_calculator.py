
def calculate_downtime(events: list[dict]) -> float:
    """
    Calculate total downtime in seconds.

    Only FAULT, MICRO_STOP and MAINTENANCE
    events are treated as downtime here.

    PLANNED_BREAK and CHANGEOVER are excluded
    from this initial calculation.
    """

    downtime_types = {
        "FAULT",
        "MICRO_STOP",
        "MAINTENANCE"
    }

    total_downtime = 0.0

    for event in events:
        event_type = event.get("event_type", "").upper()

        if event_type in downtime_types:
            duration = event.get("duration_seconds") or 0
            total_downtime += max(float(duration), 0)

    return total_downtime
