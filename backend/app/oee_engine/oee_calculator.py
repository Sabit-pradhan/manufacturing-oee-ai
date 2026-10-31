
from app.oee_engine.quality_calculator import calculate_quality
from app.oee_engine.performance_calculator import calculate_performance


def calculate_availability(
    planned_production_time_sec: float,
    downtime_sec: float
) -> float:

    if planned_production_time_sec <= 0:
        return 0.0

    if downtime_sec < 0 or downtime_sec > planned_production_time_sec:
        raise ValueError("Invalid downtime duration")

    operating_time = planned_production_time_sec - downtime_sec

    return operating_time / planned_production_time_sec


def calculate_oee(
    planned_production_time_sec: float,
    downtime_sec: float,
    ideal_cycle_time_sec: float,
    total_count: int,
    good_count: int
) -> dict:

    availability = calculate_availability(
        planned_production_time_sec,
        downtime_sec
    )

    operating_time = planned_production_time_sec - downtime_sec

    performance = calculate_performance(
        ideal_cycle_time_sec,
        total_count,
        operating_time
    )

    quality = calculate_quality(
        good_count,
        total_count
    )

    oee = availability * performance * quality

    return {
        "availability": round(availability * 100, 2),
        "performance": round(performance * 100, 2),
        "quality": round(quality * 100, 2),
        "oee": round(oee * 100, 2),
        "operating_time_sec": operating_time,
        "downtime_sec": downtime_sec
    }
