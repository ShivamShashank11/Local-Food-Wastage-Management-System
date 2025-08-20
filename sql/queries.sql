-- 1. Providers & receivers count by city
SELECT city,
    COUNT(*) AS providers_count
FROM providers
GROUP BY city;
SELECT city,
    COUNT(*) AS receivers_count
FROM receivers
GROUP BY city;
-- 2. Provider type contributing the most food
SELECT provider_type,
    SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY provider_type
ORDER BY total_quantity DESC;
-- 3. Contact info of providers in a specific city (:city)
SELECT name,
    type,
    contact,
    address
FROM providers
WHERE city = :city
ORDER BY name;
-- 4. Receivers with most completed claims
SELECT r.receiver_id,
    r.name,
    COUNT(*) AS completed_claims
FROM claims c
    JOIN receivers r ON r.receiver_id = c.receiver_id
WHERE c.status = 'Completed'
GROUP BY r.receiver_id,
    r.name
ORDER BY completed_claims DESC;
-- 5. Total quantity available
SELECT SUM(quantity) AS total_quantity_available
FROM food_listings;
-- 6. City with most listings
SELECT location AS city,
    COUNT(*) AS listings_count
FROM food_listings
GROUP BY location
ORDER BY listings_count DESC;
-- 7. Most common food types
SELECT food_type,
    COUNT(*) AS occurrences
FROM food_listings
GROUP BY food_type
ORDER BY occurrences DESC;
-- 8. Claims per food item
SELECT f.food_id,
    f.food_name,
    COUNT(c.claim_id) AS total_claims
FROM food_listings f
    LEFT JOIN claims c ON c.food_id = f.food_id
GROUP BY f.food_id,
    f.food_name
ORDER BY total_claims DESC;
-- 9. Provider with most successful claims
SELECT p.provider_id,
    p.name,
    COUNT(*) AS successful_claims
FROM claims c
    JOIN food_listings f ON f.food_id = c.food_id
    JOIN providers p ON p.provider_id = f.provider_id
WHERE c.status = 'Completed'
GROUP BY p.provider_id,
    p.name
ORDER BY successful_claims DESC;
-- 10. Claims percentage by status
SELECT status,
    ROUND(
        100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM claims
        ),
        2
    ) AS pct
FROM claims
GROUP BY status;
-- 11. Average quantity claimed per receiver
SELECT r.receiver_id,
    r.name,
    ROUND(AVG(f.quantity), 2) AS avg_claimed_quantity
FROM claims c
    JOIN receivers r ON r.receiver_id = c.receiver_id
    JOIN food_listings f ON f.food_id = c.food_id
WHERE c.status IN ('Pending', 'Completed')
GROUP BY r.receiver_id,
    r.name
ORDER BY avg_claimed_quantity DESC;
-- 12. Most claimed meal type
SELECT f.meal_type,
    COUNT(*) AS claims_count
FROM claims c
    JOIN food_listings f ON f.food_id = c.food_id
GROUP BY f.meal_type
ORDER BY claims_count DESC;
-- 13. Total quantity donated per provider
SELECT p.provider_id,
    p.name,
    SUM(f.quantity) AS total_donated
FROM food_listings f
    JOIN providers p ON p.provider_id = f.provider_id
GROUP BY p.provider_id,
    p.name
ORDER BY total_donated DESC;
-- 14. Listings expiring in next N days (:days)
SELECT *
FROM food_listings
WHERE DATE(expiry_date) <= DATE('now', '+' || :days || ' days')
ORDER BY expiry_date;
-- 15. Top cities by completed claims
SELECT f.location AS city,
    COUNT(*) AS completed_claims
FROM claims c
    JOIN food_listings f ON f.food_id = c.food_id
WHERE c.status = 'Completed'
GROUP BY f.location
ORDER BY completed_claims DESC;