
from app.services.daily_oee_service import get_daily_oee_report

report_date = "2026-01-01"

results = get_daily_oee_report(report_date)

print("\nDAILY MACHINE OEE REPORT")
print("=" * 90)

print(
    f"{'Machine':<12}"
    f"{'Availability':>15}"
    f"{'Performance':>15}"
    f"{'Quality':>12}"
    f"{'OEE':>12}"
    f"{'Production':>15}"
)

print("-" * 90)

for row in results:
    print(
        f"{row['machine_id']:<12}"
        f"{row['availability']:>14.2f}%"
        f"{row['performance']:>14.2f}%"
        f"{row['quality']:>11.2f}%"
        f"{row['oee']:>11.2f}%"
        f"{row['total_count']:>15,}"
    )

print("-" * 90)
print("Machines:", len(results))
print("Date:", report_date)
