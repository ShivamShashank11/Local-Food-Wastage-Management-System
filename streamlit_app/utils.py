import os
import sqlite3
import pandas as pd
from pathlib import Path

# ---- Database Path ----
DB_PATH = os.getenv(
    "FOOD_DB_PATH",
    str(Path(__file__).resolve().parents[1] / "local_food.db")
)

# ---- Querying Functions ----
def query_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    """
    Execute a SELECT query and return a Pandas DataFrame.
    
    Args:
        sql (str): SQL query string.
        params (dict, optional): Parameters for SQL query. Defaults to None.
    
    Returns:
        pd.DataFrame: Query result as DataFrame. Empty if no rows.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        if cur.description is None:  # No result set
            return pd.DataFrame()
        return pd.read_sql_query(sql, conn, params=params or {})


def execute_sql(sql: str, params: dict | None = None) -> int:
    """
    Execute INSERT, UPDATE, or DELETE statements.
    
    Args:
        sql (str): SQL query string.
        params (dict, optional): Parameters for SQL query. Defaults to None.
    
    Returns:
        int: Number of rows affected.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        conn.commit()
        return cur.rowcount


def get_distinct(column: str, table: str) -> list[str]:
    """
    Get distinct non-null values of a column from a table.
    
    Args:
        column (str): Column name.
        table (str): Table name.
    
    Returns:
        list[str]: Sorted list of distinct values as strings.
    """
    df = query_df(
        f"SELECT DISTINCT {column} AS v FROM {table} WHERE {column} IS NOT NULL ORDER BY {column}"
    )
    return df["v"].dropna().astype(str).tolist()


def execute_script(path: Path):
    """
    Execute a SQL script file (.sql) on the database.
    
    Args:
        path (Path): Path to SQL script file.
    """
    if not path.exists():
        raise FileNotFoundError(f"SQL script not found: {path}")
    
    with sqlite3.connect(DB_PATH) as conn, open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
