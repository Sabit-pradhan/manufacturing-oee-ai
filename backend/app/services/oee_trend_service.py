
from datetime import date, timedelta
from statistics import mean

from app.services.daily_oee_service import get_daily_oee_report


def get_oee_trend(start_date: str, end_date: str):
    """
    Generate daily OEE trends between two dates.

    Daily OEE is the arithmetic average of the
    machine-level OEE percentages for that date.
    """

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if start > end:
        raise ValueError("start_date must be before or equal to end_date")

    trend_data = []
    current_date = start

    while current_date <= end:
        date_string = current_date.isoformat()

        daily_report = get_daily_oee_report(date_string)

        if daily_report:
            trend_data.append({
                "date": date_string,
                "machine_count": len(daily_report),
                "average_availability": round(
                    mean(row["availability"] for row in daily_report), 2
                ),
                "average_performance": round(
                    mean(row["performance"] for row in daily_report), 2
                ),
                "average_quality": round(
                    mean(row["quality"] for row in daily_report), 2
                ),
                "average_oee": round(
                    mean(row["oee"] for row in daily_report), 2
                ),
                "total_production": sum(
                    row["total_count"] for row in daily_report
                ),
                "total_good_production": sum(
                    row["good_count"] for row in daily_report
                )
            })

        current_date += timedelta(days=1)

    return trend_data
