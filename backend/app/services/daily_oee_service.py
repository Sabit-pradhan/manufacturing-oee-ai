
from datetime import date
from collections import defaultdict

from sqlalchemy import text

from app.services.oee_reporting_service import get_shift_oee_report
from app.database.connection import SessionLocal


def get_daily_oee_report(report_date: str):
    """
    Calculate daily OEE for each machine by combining
    its OEE results across all shifts on the selected date.
    """

    report_day = date.fromisoformat(report_date)

    db = SessionLocal()

    try:
        shifts = db.execute(
            text("""
                SELECT shift_id
                FROM shifts
                WHERE shift_date = :report_date
                ORDER BY shift_id
            """),
            {"report_date": report_day}
        ).fetchall()

        if not shifts:
            return []

        machine_totals = defaultdict(lambda: {
            "total_count": 0,
            "good_count": 0,
            "ideal_production_time_sec": 0.0,
            "planned_production_time_sec": 0.0,
            "downtime_sec": 0.0
        })

        for shift in shifts:
            shift_report = get_shift_oee_report(shift.shift_id)

            for machine in shift_report:
                machine_id = machine["machine_id"]
                totals = machine_totals[machine_id]

                totals["total_count"] += machine["total_count"]
                totals["good_count"] += machine["good_count"]

                totals["ideal_production_time_sec"] += (
                    machine["ideal_production_time_sec"]
                )

                totals["planned_production_time_sec"] += (
                    machine["planned_production_time_sec"]
                )

                totals["downtime_sec"] += machine["downtime_sec"]

        daily_report = []

        for machine_id, values in machine_totals.items():

            planned_time = values["planned_production_time_sec"]
            downtime = values["downtime_sec"]
            total_count = values["total_count"]
            good_count = values["good_count"]
            ideal_time = values["ideal_production_time_sec"]

            operating_time = planned_time - downtime

            availability = (
                operating_time / planned_time
                if planned_time > 0 else 0
            )

            performance = (
                ideal_time / operating_time
                if operating_time > 0 else 0
            )

            quality = (
                good_count / total_count
                if total_count > 0 else 0
            )

            oee = availability * performance * quality

            daily_report.append({
                "machine_id": machine_id,
                "total_count": total_count,
                "good_count": good_count,
                "availability": round(availability * 100, 2),
                "performance": round(performance * 100, 2),
                "quality": round(quality * 100, 2),
                "oee": round(oee * 100, 2)
            })

        return sorted(
            daily_report,
            key=lambda item: item["machine_id"]
        )

    finally:
        db.close()
