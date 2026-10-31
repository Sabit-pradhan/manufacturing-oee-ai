
from sqlalchemy import text
from app.database.connection import engine
from app.services.oee_service import calculate_machine_oee


def get_shift_oee_report(shift_id: str):
    """
    Calculate OEE for every machine producing
    during the selected shift.
    """

    with engine.connect() as connection:
        machines = connection.execute(
            text("""
                SELECT DISTINCT machine_id
                FROM production_counts
                WHERE shift_id = :shift_id
                  AND record_type = 'PRODUCTION_COUNT'
                ORDER BY machine_id
            """),
            {"shift_id": shift_id}
        ).scalars().all()

    report = []

    for machine_id in machines:
        try:
            result = calculate_machine_oee(
                machine_id=machine_id,
                shift_id=shift_id
            )
            report.append(result)

        except ValueError as error:
            print(f"Skipping {machine_id}: {error}")

    return report


def print_shift_oee_report(shift_id: str):

    results = get_shift_oee_report(shift_id)

    print(f"\nOEE REPORT FOR SHIFT: {shift_id}")
    print("=" * 95)

    print(
        f"{'Machine':<12}"
        f"{'Availability':>15}"
        f"{'Performance':>15}"
        f"{'Quality':>12}"
        f"{'OEE':>12}"
        f"{'Total Count':>15}"
    )

    print("-" * 95)

    for row in results:
        print(
            f"{row['machine_id']:<12}"
            f"{row['availability']:>14.2f}%"
            f"{row['performance']:>14.2f}%"
            f"{row['quality']:>11.2f}%"
            f"{row['oee']:>11.2f}%"
            f"{row['total_count']:>15,}"
        )

    print("-" * 95)
    print(f"Machines processed: {len(results)}")

    return results
