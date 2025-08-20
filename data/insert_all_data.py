import sqlite3
import pandas as pd
import os

# Database ka path (root folder me)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "local_food.db")

# Current folder (yani data folder)
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV file → Table name mapping
csv_to_table = {
    "claims_data.csv": "claims",
    "food_listings_data.csv": "food_listings",
    "providers_data.csv": "providers",
    "receivers_data.csv": "receivers"
}

def insert_csv_to_sqlite():
    conn = sqlite3.connect(DB_PATH)
    try:
        for csv_file, table_name in csv_to_table.items():
            file_path = os.path.join(DATA_DIR, csv_file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"✅ {csv_file} → {table_name}")
            else:
                print(f"❌ Missing file: {file_path}")
        print("🎯 All CSV data inserted successfully!")
    except Exception as e:
        print(f"⚠ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_csv_to_sqlite()
