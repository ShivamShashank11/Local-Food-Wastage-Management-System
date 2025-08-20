# src/test_db_connection.py

from db_connection import run_query

if __name__ == "__main__":
    try:
        # Current DB ka naam check karo
        result = run_query("SELECT DATABASE() as db_name;")
        print("✅ Connected to MySQL!")
        print("Current Database:", result[0]['db_name'])

        # Tables list karo
        tables = run_query("SHOW TABLES;")
        print("\n📂 Tables in DB:")
        for t in tables:
            print("-", list(t.values())[0])

    except Exception as e:
        print("❌ Connection failed!")
        print("Error:", e)
