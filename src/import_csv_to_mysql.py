import csv
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",
    database="local_food_waste"
)
cursor = conn.cursor()

# 1️⃣ Providers
with open("D:/LocalFoodWastageManagement/data/providers_data.csv", "r") as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        cursor.execute(
            "INSERT INTO providers (name, contact, location) VALUES (%s, %s, %s)",
            row
        )

# 2️⃣ Receivers
with open("D:/LocalFoodWastageManagement/data/receivers_data.csv", "r") as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        cursor.execute(
            "INSERT INTO receivers (name, contact, location) VALUES (%s, %s, %s)",
            row
        )

# 3️⃣ Food Listings
with open("D:/LocalFoodWastageManagement/data/food_listings_data.csv", "r") as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        cursor.execute(
            "INSERT INTO food_listings (provider_id, food_name, quantity, expiry_date, status) VALUES (%s, %s, %s, %s, %s)",
            row
        )

# 4️⃣ Claims
with open("D:/LocalFoodWastageManagement/data/claims_data.csv", "r") as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        cursor.execute(
            "INSERT INTO claims (food_id, receiver_id, status, timestamp) VALUES (%s, %s, %s, %s)",
            row
        )

# Commit & close
conn.commit()
cursor.close()
conn.close()

print("✅ Saara data insert ho gaya!")
