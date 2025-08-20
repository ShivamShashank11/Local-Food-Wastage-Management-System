PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;
CREATE TABLE providers (
    provider_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT CHECK (
        type IN (
            'Restaurant',
            'Grocery Store',
            'Supermarket',
            'Bakery',
            'Caterer',
            'Other'
        )
    ) NOT NULL,
    address TEXT,
    city TEXT NOT NULL,
    contact TEXT
);
CREATE TABLE receivers (
    receiver_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT CHECK (
        type IN (
            'NGO',
            'Community Center',
            'Individual',
            'Shelter',
            'Other'
        )
    ) NOT NULL,
    city TEXT NOT NULL,
    contact TEXT
);
CREATE TABLE food_listings (
    food_id INTEGER PRIMARY KEY,
    food_name TEXT NOT NULL,
    quantity INTEGER CHECK (quantity >= 0) NOT NULL,
    expiry_date DATE NOT NULL,
    provider_id INTEGER NOT NULL,
    provider_type TEXT,
    location TEXT NOT NULL,
    food_type TEXT CHECK (
        food_type IN ('Vegetarian', 'Non-Vegetarian', 'Vegan', 'Other')
    ) NOT NULL,
    meal_type TEXT CHECK (
        meal_type IN (
            'Breakfast',
            'Lunch',
            'Dinner',
            'Snacks',
            'Other'
        )
    ) NOT NULL,
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id) ON DELETE CASCADE
);
CREATE TABLE claims (
    claim_id INTEGER PRIMARY KEY,
    food_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    status TEXT CHECK (status IN ('Pending', 'Completed', 'Cancelled')) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_listings(food_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id) ON DELETE CASCADE
);
-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_food_location ON food_listings(location);
CREATE INDEX IF NOT EXISTS idx_food_provider ON food_listings(provider_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);