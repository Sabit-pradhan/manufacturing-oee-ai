
from app.oee_engine.oee_calculator import calculate_oee

result = calculate_oee(
    planned_production_time_sec=28800,
    downtime_sec=3600,
    ideal_cycle_time_sec=5,
    total_count=4500,
    good_count=4400
)

print("\nOEE CALCULATION RESULT")
print("-" * 35)

for metric, value in result.items():
    print(f"{metric}: {value}")
