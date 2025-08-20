import pandas as pd
from .db_connection import get_connection

def get_dataframe(sql: str, params: dict | None = None) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params or {})

def top_cities_by_listings():
    return get_dataframe("""
        SELECT location AS city, COUNT(*) AS listings_count
        FROM food_listings
        GROUP BY location
        ORDER BY listings_count DESC
        LIMIT 10
    """)

def claims_status_breakdown():
    return get_dataframe("""
        SELECT status, COUNT(*) AS total
        FROM claims
        GROUP BY status
    """)
