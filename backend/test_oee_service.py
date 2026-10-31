
from sqlalchemy import text

from app.database.connection import engine
from app.services.oee_service import calculate_machine_oee


# Fetch a real machine and shift combination
with engine.connect() as connection:
    record = connection.execute(
        text("""
            SELECT DISTINCT machine_id, shift_id
            FROM production_counts
            WHERE record_type = 'PRODUCTION_COUNT'
            ORDER BY machine_id, shift_id
            LIMIT 1
        """)
    ).mappings().first()

if not record:
    raise ValueError("No production records found in database")

machine_id = record["machine_id"]
shift_id = record["shift_id"]

print("Testing database-connected OEE calculation")
print("-" * 45)
print("Machine:", machine_id)
print("Shift:", shift_id)

result = calculate_machine_oee(machine_id, shift_id)

print("\nOEE RESULT")
print("-" * 45)

for metric, value in result.items():
    print(f"{metric}: {value}")
