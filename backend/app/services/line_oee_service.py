
from sqlalchemy import text

from app.database.connection import engine
from app.services.oee_reporting_service import get_shift_oee_report


def get_line_oee_report(shift_id: str):

    # Get machine-level OEE results
    machine_results = get_shift_oee_report(shift_id)

    if not machine_results:
        return []

    # Calculate the line-level metrics from machines
    machine_ids = [row["machine_id"] for row in machine_results]

    with engine.connect() as connection:
        line_mapping = connection.execute(
            text("""
                SELECT machine_id, line_id
                FROM machines
                WHERE machine_id = ANY(:machine_ids)
            """),
            {"machine_ids": machine_ids}
        ).mappings().all()

    machine_to_line = {
        row["machine_id"]: row["line_id"]
        for row in line_mapping
    }

    grouped = {}

    for row in machine_results:
        line_id = machine_to_line.get(row["machine_id"])

        if not line_id:
            continue

        grouped.setdefault(line_id, []).append(row)

    report = []

    for line_id, machines in grouped.items():

        total_count = sum(m["total_count"] for m in machines)
        good_count = sum(m["good_count"] for m in machines)

        ideal_time = sum(
            m["ideal_production_time_sec"]
            for m in machines
        )

        planned_time = sum(
            m["planned_production_time_sec"]
            for m in machines
        )

        downtime = sum(
            m["downtime_sec"]
            for m in machines
        )

        operating_time = planned_time - downtime

        availability = (
            operating_time / planned_time * 100
            if planned_time > 0 else 0
        )

        performance = (
            ideal_time / operating_time * 100
            if operating_time > 0 else 0
        )

        quality = (
            good_count / total_count * 100
            if total_count > 0 else 0
        )

        oee = availability * performance * quality / 10000

        report.append({
            "line_id": line_id,
            "machine_count": len(machines),
            "total_count": total_count,
            "good_count": good_count,
            "availability": round(availability, 2),
            "performance": round(performance, 2),
            "quality": round(quality, 2),
            "oee": round(oee, 2)
        })

    return sorted(report, key=lambda x: x["line_id"])
