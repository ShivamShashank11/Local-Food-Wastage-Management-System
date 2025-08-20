-- Providers
INSERT INTO providers (provider_id, name, type, address, city, contact)
VALUES (
        1,
        'Fresh Bites',
        'Restaurant',
        '12 Lake Rd',
        'Bengaluru',
        '+91-900000001'
    ),
    (
        2,
        'City Mart',
        'Grocery Store',
        '88 MG Rd',
        'Mumbai',
        '+91-900000002'
    );
-- Receivers
INSERT INTO receivers (receiver_id, name, type, city, contact)
VALUES (
        1,
        'Helping Hands',
        'NGO',
        'Bengaluru',
        '+91-800000001'
    ),
    (
        2,
        'Shelter One',
        'Shelter',
        'Mumbai',
        '+91-800000002'
    );
-- Food Listings
INSERT INTO food_listings (
        food_id,
        food_name,
        quantity,
        expiry_date,
        provider_id,
        provider_type,
        location,
        food_type,
        meal_type
    )
VALUES (
        1,
        'Veg Thali',
        30,
        '2025-08-20',
        1,
        'Restaurant',
        'Bengaluru',
        'Vegetarian',
        'Lunch'
    ),
    (
        2,
        'Bread Loaves',
        40,
        '2025-08-18',
        2,
        'Grocery Store',
        'Mumbai',
        'Vegetarian',
        'Breakfast'
    );
-- Claims
INSERT INTO claims (
        claim_id,
        food_id,
        receiver_id,
        status,
        timestamp
    )
VALUES (1, 1, 1, 'Completed', '2025-08-14 10:00:00'),
    (2, 2, 2, 'Pending', '2025-08-14 11:00:00');