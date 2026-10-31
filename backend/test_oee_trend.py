
from app.services.oee_trend_service import get_oee_trend


if __name__ == "__main__":

    trend = get_oee_trend(
        start_date="2026-01-01",
        end_date="2026-03-31"
    )

    print("\n90-DAY MANUFACTURING OEE TREND")
    print("=" * 115)

    print(
        f"{'Date':<14}"
        f"{'Machines':>10}"
        f"{'Availability':>15}"
        f"{'Performance':>15}"
        f"{'Quality':>12}"
        f"{'Average OEE':>14}"
        f"{'Production':>15}"
    )

    print("-" * 115)

    for row in trend:
        print(
            f"{row['date']:<14}"
            f"{row['machine_count']:>10}"
            f"{row['average_availability']:>14.2f}%"
            f"{row['average_performance']:>14.2f}%"
            f"{row['average_quality']:>11.2f}%"
            f"{row['average_oee']:>13.2f}%"
            f"{row['total_production']:>15,}"
        )

    print("-" * 115)

    if trend:
        best_day = max(trend, key=lambda row: row["average_oee"])
        worst_day = min(trend, key=lambda row: row["average_oee"])

        print(f"Days with production data: {len(trend)}")
        print(
            f"Best OEE day: {best_day['date']} "
            f"({best_day['average_oee']}%)"
        )
        print(
            f"Worst OEE day: {worst_day['date']} "
            f"({worst_day['average_oee']}%)"
        )
    else:
        print("No OEE data found for the selected date range.")
