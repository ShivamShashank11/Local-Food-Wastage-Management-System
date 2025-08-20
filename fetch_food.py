import sqlite3
import pandas as pd
import os

# Database path (root folder me DB hai)
DB_PATH = r"D:\LocalFoodWastageManagement\local_food.db"

# Current script ka folder (yani data folder)
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV → Table mapping
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
                print(f"✅ Inserted: {csv_file} → Table: {table_name}")

                # Show first 5 rows for verification
                sample_df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)
                print(sample_df, "\n")
            else:
                print(f"❌ File not found: {file_path}")

        print("🎯 All CSV data inserted successfully!")
    except Exception as e:
        print(f"⚠ Error inserting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_csv_to_sqlite()
