
def calculate_performance(
    ideal_cycle_time_sec: float,
    total_count: int,
    operating_time_sec: float
) -> float:
    """
    Performance =
    (Ideal Cycle Time x Total Production) / Operating Time

    Returns a decimal ratio.
    """

    if operating_time_sec <= 0:
        return 0.0

    if ideal_cycle_time_sec <= 0 or total_count < 0:
        raise ValueError("Invalid performance calculation inputs")

    ideal_production_time = ideal_cycle_time_sec * total_count

    return ideal_production_time / operating_time_sec
