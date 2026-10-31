from sqlalchemy.orm import configure_mappers

from app.database.base import Base
from app.database.connection import engine
import app.models  # Registers all nine models


def create_tables():
    try:
        # Validate SQLAlchemy relationships and foreign-key mappings
        configure_mappers()

        # Create tables that do not already exist
        Base.metadata.create_all(bind=engine)

        print("Database tables created successfully!")

        print("\nCreated/registered tables:")
        for table_name in Base.metadata.tables:
            print(f"- {table_name}")

    except Exception as error:
        print(f"Error creating database tables: {error}")
        raise


if __name__ == "__main__":
    create_tables()
    