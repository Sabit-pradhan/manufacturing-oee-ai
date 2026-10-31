from sqlalchemy import text
from app.database.connection import engine

try:
    with engine.connect() as connection:
        database = connection.execute(
            text("SELECT current_database()")
        ).scalar()

        schema = connection.execute(
            text("SELECT current_schema()")
        ).scalar()

        tables = connection.execute(
            text("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_name = 'document_chunks'
            """)
        ).fetchall()

        print("DATABASE:", database)
        print("SCHEMA:", schema)
        print("DOCUMENT TABLES:", tables)

except Exception as error:
    print("DATABASE ERROR:", error)