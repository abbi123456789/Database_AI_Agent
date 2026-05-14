from sqlalchemy import inspect
from db.connection import engine

# ---------------------------------------------------
# 🚀 Load database schema dynamically
# ---------------------------------------------------
def load_schema() -> str:

    inspector = inspect(engine)

    schema_text = ""

    # Get all tables
    tables = inspector.get_table_names()

    for table in tables:

        schema_text += f"\nTable: {table}\n"

        columns = inspector.get_columns(table)

        for column in columns:

            column_name = column["name"]
            column_type = column["type"]

            schema_text += f"- {column_name} ({column_type})\n"

    return schema_text


# ---------------------------------------------------
# 🧪 Test block
# ---------------------------------------------------
if __name__ == "__main__":

    schema = load_schema()

    print("\n📋 Database Schema:\n")
    print(schema)