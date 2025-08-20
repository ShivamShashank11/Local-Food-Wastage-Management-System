import streamlit as st
from utils import query_df

def show_all_queries(params: dict):
    st.subheader("SQL Insights (15)")
    queries = []

    city_filter = params.get("city")
    provider_filter = params.get("provider")
    food_type_filter = params.get("food_type")
    meal_type_filter = params.get("meal_type")
    days_filter = params.get("days", 7)

    # 1. Providers count by city
    queries.append((
        "Providers count by city",
        "SELECT city, COUNT(*) AS providers_count FROM providers "
        "WHERE (:city IS NULL OR city = :city) "
        "GROUP BY city",
        {"city": city_filter}
    ))

    # 2. Receivers count by city
    queries.append((
        "Receivers count by city",
        "SELECT city, COUNT(*) AS receivers_count FROM receivers "
        "WHERE (:city IS NULL OR city = :city) "
        "GROUP BY city",
        {"city": city_filter}
    ))

    # 3. Provider type contributing most food
    queries.append((
        "Provider type by total quantity",
        "SELECT provider_type, SUM(quantity) AS total_quantity "
        "FROM food_listings "
        "WHERE (:provider IS NULL OR provider_id IN (SELECT provider_id FROM providers WHERE name=:provider)) "
        "GROUP BY provider_type ORDER BY total_quantity DESC",
        {"provider": provider_filter}
    ))

    # 4. Providers in selected city
    queries.append((
        f"Providers in city: {city_filter or 'All'}",
        "SELECT name, type, contact, address FROM providers "
        "WHERE (:city IS NULL OR city=:city) ORDER BY name",
        {"city": city_filter}
    ))

    # 5. Top receivers by completed claims
    queries.append((
        "Top receivers by completed claims",
        "SELECT r.receiver_id, r.name, COUNT(*) AS completed_claims "
        "FROM claims c JOIN receivers r ON r.receiver_id = c.receiver_id "
        "WHERE c.status='Completed' "
        "GROUP BY r.receiver_id, r.name ORDER BY completed_claims DESC",
        {}
    ))

    # 6. Total quantity available
    queries.append((
        "Total quantity available",
        "SELECT SUM(quantity) AS total_quantity_available FROM food_listings "
        "WHERE (:food_type IS NULL OR food_type=:food_type) "
        "AND (:meal_type IS NULL OR meal_type=:meal_type)",
        {"food_type": food_type_filter, "meal_type": meal_type_filter}
    ))

    # 7. City with most listings
    queries.append((
        "Listings by city",
        "SELECT location AS city, COUNT(*) AS listings_count "
        "FROM food_listings "
        "WHERE (:city IS NULL OR location=:city) "
        "GROUP BY location ORDER BY listings_count DESC",
        {"city": city_filter}
    ))

    # 8. Most common food types
    queries.append((
        "Most common food types",
        "SELECT food_type, COUNT(*) AS occurrences "
        "FROM food_listings "
        "GROUP BY food_type ORDER BY occurrences DESC",
        {}
    ))

    # 9. Claims per food item
    queries.append((
        "Claims per food item",
        "SELECT f.food_id, f.food_name, COUNT(c.claim_id) AS total_claims "
        "FROM food_listings f LEFT JOIN claims c ON c.food_id = f.food_id "
        "GROUP BY f.food_id, f.food_name ORDER BY total_claims DESC",
        {}
    ))

    # 10. Top providers by successful claims
    queries.append((
        "Top providers by successful (Completed) claims",
        "SELECT p.provider_id, p.name, COUNT(*) AS successful_claims "
        "FROM claims c JOIN food_listings f ON f.food_id=c.food_id "
        "JOIN providers p ON p.provider_id=f.provider_id "
        "WHERE c.status='Completed' "
        "GROUP BY p.provider_id, p.name ORDER BY successful_claims DESC",
        {}
    ))

    # 11. Claims by status (%)
    queries.append((
        "Claims by status (%)",
        "SELECT status, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims),2) AS pct "
        "FROM claims GROUP BY status",
        {}
    ))

    # 12. Avg quantity per receiver
    queries.append((
        "Avg quantity per receiver",
        "SELECT r.receiver_id, r.name, ROUND(AVG(f.quantity),2) AS avg_claimed_quantity "
        "FROM claims c JOIN receivers r ON r.receiver_id=c.receiver_id "
        "JOIN food_listings f ON f.food_id=c.food_id "
        "WHERE c.status IN ('Pending','Completed') "
        "GROUP BY r.receiver_id, r.name ORDER BY avg_claimed_quantity DESC",
        {}
    ))

    # 13. Most claimed meal type
    queries.append((
        "Most claimed meal type",
        "SELECT f.meal_type, COUNT(*) AS claims_count "
        "FROM claims c JOIN food_listings f ON f.food_id=c.food_id "
        "GROUP BY f.meal_type ORDER BY claims_count DESC",
        {}
    ))

    # 14. Total donated by provider
    queries.append((
        "Total donated by provider",
        "SELECT p.provider_id, p.name, SUM(f.quantity) AS total_donated "
        "FROM food_listings f JOIN providers p ON p.provider_id=f.provider_id "
        "GROUP BY p.provider_id, p.name ORDER BY total_donated DESC",
        {}
    ))

    # 15. Listings expiring within N days
    queries.append((
        f"Listings expiring within {days_filter} days",
        "SELECT * FROM food_listings "
        "WHERE DATE(expiry_date) <= DATE('now','+{} days') "
        "ORDER BY expiry_date".format(days_filter),
        {}
    ))

    # Execute and display
    for title, sql, p in queries:
        st.markdown(f"**{title}**")
        df = query_df(sql, p)
        st.dataframe(df, use_container_width=True)
        st.caption(f"`{sql.strip()[:120]}...`")
