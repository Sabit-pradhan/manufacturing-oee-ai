from app.database.base import Base
import app.models

print("Registered database tables:")

for table_name in Base.metadata.tables:
    print("-", table_name)

print("\nSQLAlchemy model registration successful!")