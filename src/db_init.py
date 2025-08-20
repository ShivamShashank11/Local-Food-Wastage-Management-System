import os
import sqlite3
import pandas as pd
from pathlib import Path

# Use same DB path as in db_connection.py
DB_PATH = os.getenv("FOOD_DB_PATH", str(Path(__file__).resolve().parents[1] / "local_food.db"))

# Paths for SQL & CSV files
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"

def create_and_populate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create tables
    create_sql_file = SQL_DIR / "create_tables.sql"
    if create_sql_file.exists():
        with open(create_sql_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        print("✅ Tables created successfully.")
    else:
        print("❌ Missing create_tables.sql")

    # 2. Insert data from CSVs
    csv_files = {
        "providers": "providers_data.csv",
        "receivers": "receivers_data.csv",
        "food_listings": "food_listings_data.csv",
        "claims": "claims_data.csv"
    }

    for table, filename in csv_files.items():
        file_path = DATA_DIR / filename
        if file_path.exists():
            df = pd.read_csv(file_path)
            df.to_sql(table, conn, if_exists="append", index=False)
            print(f"✅ Inserted data into {table}")
        else:
            print(f"❌ Missing file: {filename}")

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    create_and_populate_db()
