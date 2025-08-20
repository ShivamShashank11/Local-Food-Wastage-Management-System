from typing import Dict, Any, List
from .db_connection import get_connection

# ---------- Providers ----------
def create_provider(data: Dict[str, Any]) -> int:
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO providers (name, type, address, city, contact)
            VALUES (:name, :type, :address, :city, :contact)
        """, data)
        return cur.lastrowid

def update_provider(provider_id: int, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
            UPDATE providers SET name=:name, type=:type, address=:address, city=:city, contact=:contact
            WHERE provider_id=:provider_id
        """, {**data, "provider_id": provider_id})

def delete_provider(provider_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM providers WHERE provider_id=?", (provider_id,))

def list_providers(city: str | None = None) -> List[dict]:
    with get_connection() as conn:
        if city:
            rows = conn.execute("SELECT * FROM providers WHERE city=? ORDER BY name", (city,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM providers ORDER BY city, name").fetchall()
        return [dict(r) for r in rows]

# ---------- Receivers ----------
def create_receiver(data: Dict[str, Any]) -> int:
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO receivers (name, type, city, contact)
            VALUES (:name, :type, :city, :contact)
        """, data)
        return cur.lastrowid

def update_receiver(receiver_id: int, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
            UPDATE receivers SET name=:name, type=:type, city=:city, contact=:contact
            WHERE receiver_id=:receiver_id
        """, {**data, "receiver_id": receiver_id})

def delete_receiver(receiver_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM receivers WHERE receiver_id=?", (receiver_id,))

# ---------- Food Listings ----------
def create_food_listing(data: Dict[str, Any]) -> int:
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO food_listings (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            VALUES (:food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type, :meal_type)
        """, data)
        return cur.lastrowid

def update_food_listing(food_id: int, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
            UPDATE food_listings
            SET food_name=:food_name, quantity=:quantity, expiry_date=:expiry_date,
                provider_id=:provider_id, provider_type=:provider_type,
                location=:location, food_type=:food_type, meal_type=:meal_type
            WHERE food_id=:food_id
        """, {**data, "food_id": food_id})

def delete_food_listing(food_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM food_listings WHERE food_id=?", (food_id,))

# ---------- Claims ----------
def create_claim(data: Dict[str, Any]) -> int:
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO claims (food_id, receiver_id, status, timestamp)
            VALUES (:food_id, :receiver_id, :status, COALESCE(:timestamp, CURRENT_TIMESTAMP))
        """, data)
        return cur.lastrowid

def update_claim_status(claim_id: int, status: str) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE claims SET status=? WHERE claim_id=?", (status, claim_id))

def delete_claim(claim_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM claims WHERE claim_id=?", (claim_id,))
