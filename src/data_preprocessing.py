import pandas as pd
import os

# Paths
BASE_DIR = "D:/LocalFoodWastageManagement"
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "clean_data")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to clean contact number
def clean_contact(contact):
    if pd.isna(contact):
        return None
    return ''.join(filter(str.isdigit, str(contact)))

# Function to clean date
def clean_date(date_val):
    if pd.isna(date_val):
        return None
    try:
        return pd.to_datetime(date_val, errors='coerce').strftime('%Y-%m-%d')
    except:
        return None

# Cleaning function
def clean_csv(file_name, date_cols=None, contact_cols=None):
    path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(path)

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Clean contact columns
    if contact_cols:
        for col in contact_cols:
            if col in df.columns:
                df[col] = df[col].apply(clean_contact)

    # Clean date columns
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = df[col].apply(clean_date)

    # Remove completely empty rows
    df.dropna(how='all', inplace=True)

    # Save cleaned file
    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path, index=False)
    print(f"Cleaned file saved: {output_path}")

# Clean each CSV
clean_csv("receivers_data.csv", contact_cols=["contact"])
clean_csv("providers_data.csv", contact_cols=["contact"])
clean_csv("food_listings_data.csv", date_cols=["expiry_date"])
clean_csv("claims_data.csv", date_cols=["claim_date"])
