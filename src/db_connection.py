import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

def get_engine():
    # MySQL credentials
    user = os.getenv("MYSQL_USER", "root")  # MySQL username
    password = os.getenv("MYSQL_PASSWORD", "Nicky@123")  # Tumhara password
    host = os.getenv("MYSQL_HOST", "localhost")  # Usually localhost
    port = int(os.getenv("MYSQL_PORT", "3306"))  # MySQL default port
    db = os.getenv("MYSQL_DB", "local_food_waste")  # Tumhara database name

    # Create SQLAlchemy engine for MySQL
    url = f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{db}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True, pool_recycle=1800)

def run_query(sql: str, params: dict | None = None):
    """SELECT queries ke liye"""
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(text(sql), params or {})
        rows = res.fetchall()
        cols = res.keys()
        return [dict(zip(cols, row)) for row in rows]

def run_action(sql: str, params: dict | None = None):
    """INSERT / UPDATE / DELETE ke liye"""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text(sql), params or {})
        conn.commit()
