import logging
import pandas as pd
from sqlalchemy import text
from db.connection import engine

# ---------------------------------------------------
# 🪵 Logging Configuration
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# 📦 Table Schemas
# ---------------------------------------------------
TABLES = {
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            department_id INTEGER,
            salary INTEGER,
            joining_date TEXT
        )
    """,

    "departments": """
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL
        )
    """,

    "projects": """
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            department_id INTEGER,
            budget INTEGER
        )
    """,

    "sales": """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            sale_amount INTEGER,
            sale_date TEXT
        )
    """
}

# ---------------------------------------------------
# 🌱 Sample Seed Data
# ---------------------------------------------------
SEED_QUERIES = [

    """
    INSERT INTO departments (department_name)
    VALUES
    ('IT'),
    ('HR'),
    ('Finance')
    """,

    """
    INSERT INTO employees (
        employee_name,
        department_id,
        salary,
        joining_date
    )
    VALUES
    ('Abhiram', 1, 50000, '2024-01-15'),
    ('Ravi', 1, 65000, '2023-05-10'),
    ('Sita', 2, 70000, '2022-08-20')
    """,

    """
    INSERT INTO projects (
        project_name,
        department_id,
        budget
    )
    VALUES
    ('AI Agent', 1, 100000),
    ('HR Portal', 2, 50000)
    """,

    """
    INSERT INTO sales (
        employee_id,
        sale_amount,
        sale_date
    )
    VALUES
    (1, 10000, '2025-01-01'),
    (2, 20000, '2025-01-02'),
    (1, 15000, '2025-01-03')
    """
]

# ---------------------------------------------------
# 🚀 Execute SELECT Queries
# ---------------------------------------------------
def execute_select(query: str) -> pd.DataFrame:

    try:
        with engine.connect() as conn:

            result = conn.execute(text(query))

            df = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )

            logger.info(f"✅ SELECT query executed")

            return df

    except Exception as e:
        logger.error(f"❌ SELECT query failed: {e}")
        raise


# ---------------------------------------------------
# 🚀 Execute DML / DDL Queries
# ---------------------------------------------------
def execute_query(query: str) -> int:

    try:
        with engine.begin() as conn:

            result = conn.execute(text(query))

            affected_rows = result.rowcount

            logger.info(f"✅ Query executed successfully")

            return affected_rows

    except Exception as e:
        logger.error(f"❌ Query execution failed: {e}")
        raise


# ---------------------------------------------------
# 🔒 SQL Safety Validation
# ---------------------------------------------------
def is_safe_query(query: str) -> bool:

    forbidden_keywords = [
        "DROP",
        "TRUNCATE",
        "ALTER"
    ]

    query_upper = query.upper()

    return not any(
        keyword in query_upper
        for keyword in forbidden_keywords
    )


# ---------------------------------------------------
# 🎯 Unified Query Runner
# ---------------------------------------------------
def run_query(query: str):

    if not is_safe_query(query):
        raise ValueError("❌ Unsafe query detected")

    query_type = query.strip().lower()

    if query_type.startswith("select"):
        return execute_select(query)

    return execute_query(query)


# ---------------------------------------------------
# 🏗 Create All Tables
# ---------------------------------------------------
def create_all_tables():

    logger.info("🏗 Creating tables...")

    for table_name, query in TABLES.items():

        execute_query(query)

        logger.info(f"✅ Created table: {table_name}")


# ---------------------------------------------------
# 🌱 Insert Sample Data
# ---------------------------------------------------
def seed_sample_data():

    logger.info("🌱 Inserting sample data...")

    for query in SEED_QUERIES:

        execute_query(query)

    logger.info("✅ Sample data inserted")


# ---------------------------------------------------
# 📋 Show Existing Tables
# ---------------------------------------------------
def show_tables():

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """

    df = execute_select(query)

    print("\n📋 Existing Tables:\n")
    print(df)


# ---------------------------------------------------
# 🧪 Main Test Block
# ---------------------------------------------------
if __name__ == "__main__":

    try:

        # Step 1 → Create tables
        create_all_tables()

        # Step 2 → Seed data
        seed_sample_data()

        # Step 3 → Verify tables
        show_tables()

        # Step 4 → Sample analytics query
        sample_query = """
        SELECT
            employee_name,
            salary
        FROM employees
        WHERE salary > 55000
        """

        df = run_query(sample_query)

        print("\n📊 Query Result:\n")
        print(df)

    except Exception as e:

        logger.error(f"❌ Application failed: {e}")