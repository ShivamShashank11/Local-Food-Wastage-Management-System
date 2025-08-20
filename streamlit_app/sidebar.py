import streamlit as st
from utils import get_distinct

def render_filters():
    st.sidebar.header("Filters")

    # Fetch distinct values from DB
    cities = get_distinct("location", "food_listings")
    providers = get_distinct("name", "providers")
    food_types = get_distinct("food_type", "food_listings")
    meal_types = get_distinct("meal_type", "food_listings")

    # Sidebar dropdowns with default "All"
    city = st.sidebar.selectbox("City", ["All"] + cities, index=0)
    provider = st.sidebar.selectbox("Provider", ["All"] + providers, index=0)
    food_type = st.sidebar.selectbox("Food Type", ["All"] + food_types, index=0)
    meal_type = st.sidebar.selectbox("Meal Type", ["All"] + meal_types, index=0)

    # Slider for expiry filter
    days = st.sidebar.slider("Listings expiring within (days)", min_value=0, max_value=30, value=7, step=1)

    # Return a params dictionary with None for "All" selections
    return {
        "city": None if city == "All" else city,
        "provider": None if provider == "All" else provider,
        "food_type": None if food_type == "All" else food_type,
        "meal_type": None if meal_type == "All" else meal_type,
        "days": days
    }
