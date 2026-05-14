import os
import time
import logging
from pathlib import Path

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv

# ---------------------------------------------------
# 📦 Load .env (ONLY for local)
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------
# 🪵 Logging setup
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# 🔐 Safe config loader (LOCAL + CLOUD)
# ---------------------------------------------------
def get_secret(key):
    """
    Priority:
    1. Streamlit Cloud Secrets
    2. Local .env
    """
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)


# ---------------------------------------------------
# 🔐 Read DB URL safely
# ---------------------------------------------------
DB_URL = get_secret("DB_URL")

if not DB_URL:
    raise ValueError("❌ DB_URL not found in environment or Streamlit secrets")


# ---------------------------------------------------
# 🧠 Detect DB type
# ---------------------------------------------------
db_type = make_url(DB_URL).get_backend_name()


# ---------------------------------------------------
# 🔌 Create Engine (conditional config)
# ---------------------------------------------------
if db_type == "sqlite":
    engine = create_engine(
        DB_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
    logger.info("📦 Using SQLite database")

else:
    engine = create_engine(
        DB_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        echo=False
    )
    logger.info("🐘 Using PostgreSQL database")


# ---------------------------------------------------
# 🧾 Session factory
# ---------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------------------------
# 🔁 Retry decorator
# ---------------------------------------------------
def retry_db_connection(func):
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 2

        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except OperationalError as e:
                logger.warning(
                    f"⚠️ DB connection failed (attempt {attempt+1}/{retries}): {e}"
                )
                time.sleep(delay)

        raise Exception("❌ Database connection failed after retries")

    return wrapper


# ---------------------------------------------------
# 📌 Get DB session
# ---------------------------------------------------
@retry_db_connection
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------
# 🧪 Test connection
# ---------------------------------------------------
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 2"))
            logger.info("✅ Database connection successful")
            return result.fetchone()
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        raise


# ---------------------------------------------------
# ▶ Run directly
# ---------------------------------------------------
if __name__ == "__main__":
    try:
        result = test_connection()
        print("✅ Database connected successfully")
        print("Test result:", result)
    except Exception as e:
        print("❌ Connection failed:", e)