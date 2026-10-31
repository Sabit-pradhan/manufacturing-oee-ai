
from app.services.line_oee_service import get_line_oee_report

results = get_line_oee_report("20260101_A")

print("\nPRODUCTION LINE OEE REPORT")
print("=" * 75)

for row in results:
    print(
        f"{row['line_id']} | "
        f"Machines: {row['machine_count']} | "
        f"Availability: {row['availability']}% | "
        f"Performance: {row['performance']}% | "
        f"Quality: {row['quality']}% | "
        f"OEE: {row['oee']}%"
    )
