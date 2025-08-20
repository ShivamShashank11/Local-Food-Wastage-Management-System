import streamlit as st
from sidebar import render_filters
from utils import query_df, execute_sql
from display_queries import show_all_queries

# ---- Page Config ----
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

st.title("Local Food Wastage Management System")
st.write("Connect surplus **providers** with **receivers**, reduce waste, and gain insights.")

# ---- Sidebar Filters ----
params = render_filters()

# ---- Filtered Listings ----
st.subheader("Browse Food Listings")
base_sql = """
SELECT f.food_id, f.food_name, f.quantity, f.expiry_date,
       p.name AS provider, p.contact, f.location, f.food_type, f.meal_type
FROM food_listings f
JOIN providers p ON p.provider_id = f.provider_id
WHERE (:city IS NULL OR f.location = :city)
  AND (:provider IS NULL OR p.name = :provider)
  AND (:food_type IS NULL OR f.food_type = :food_type)
  AND (:meal_type IS NULL OR f.meal_type = :meal_type)
ORDER BY f.expiry_date
"""
df_list = query_df(base_sql, params)
st.dataframe(df_list, use_container_width=True)
st.caption("Tip: Click column headers to sort. Use sidebar to filter.")

# ---- Contacts ----
st.subheader("Contact Details (Providers)")
contact_df = query_df("""
SELECT name, type, city, contact FROM providers
WHERE (:city IS NULL OR city = :city)
ORDER BY name
""", {"city": params.get("city")})
st.dataframe(contact_df, use_container_width=True)

# ---- CRUD quick forms ----
with st.expander("➕ Add Food Listing"):
    with st.form("add_food"):
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        expiry_date = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1, step=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location (City)")
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks", "Other"])
        submitted = st.form_submit_button("Create")
        if submitted:
            execute_sql("""
                INSERT INTO food_listings 
                (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (:food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type, :meal_type)
            """, {
                "food_name": food_name,
                "quantity": int(quantity),
                "expiry_date": str(expiry_date),
                "provider_id": int(provider_id),
                "provider_type": provider_type,
                "location": location,
                "food_type": food_type,
                "meal_type": meal_type
            })
            st.success("Food listing added. Refresh the page to see it.")

with st.expander("🗑️ Delete Food Listing"):
    food_id = st.number_input("Food ID to delete", min_value=1, step=1, key="del_food")
    if st.button("Delete"):
        execute_sql("DELETE FROM food_listings WHERE food_id=:fid", {"fid": int(food_id)})
        st.success("Deleted (if ID existed).")

# ---- Insights section (15 queries) ----
st.subheader("Insights")
show_all_queries(params)

st.markdown("---")

