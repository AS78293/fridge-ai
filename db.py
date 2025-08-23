import sqlite3
from datetime import date, timedelta

# -------------------------------
# Default shelf-life (days) for items
# -------------------------------
DEFAULT_EXPIRY = {
    # Dairy
    "milk": 7, "glass of milk": 7, "greek yoghurt": 10, "curd": 10,
    "butter": 90, "salted butter": 90, "cottage cheese": 10, "ricotta cheese": 7,
    "goat_cheese": 14, "blue cheese": 21, "cheese": 14,
    "heavy cream": 7, "heavy whipping cream": 7, "sweet cream": 7,

    # Meat & Fish
    "chicken": 2, "chicken_breast": 2, "meat": 3, "beef": 3, "ground_beef": 2,
    "bacon": 7, "ham": 7, "saussage": 7, "roasted turkey breast": 3,
    "fish": 2, "salmon": 2, "shrimp": 2,

    # Eggs
    "eggs": 21, "egg crate": 21, "egg bites": 3,

    # Baked goods
    "bread": 7, "english muffins": 7, "cake": 4, "doughnut": 3,
    "texas toast": 7, "mac and cheese": 4, "chocolate": 30,

    # Fruits
    "apple": 30, "green apple": 30, "banana": 7, "avacado": 5, "dragon fruit": 7,
    "grapes": 7, "red grapes": 7, "pomegrante": 14, "pear": 7, "peach": 5,
    "mango": 7, "muskmelon": 7, "watermelon": 7, "papaya": 5, "kiwi": 7,
    "pineapple": 5, "orange": 14, "lime": 14, "lemon": 14,

    # Vegetables
    "carrot": 30, "carrots": 30, "baby carrots": 21, "tomato": 7, "baby tomato": 7,
    "bell pepper": 10, "capsicum": 10, "red bell pepper": 10,
    "orange bell pepper": 10, "yellow bell pepper": 10,
    "brinjal": 7, "broccoli": 7, "brussel sprouts": 7,
    "cabbage": 30, "purple cabbage": 30, "red cabbage": 30, "cauliflower": 7,
    "lettuce": 7, "spinach": 5, "kale": 7, "parsley": 7, "coriander": 7,
    "rocket leaves": 5, "zucchini": 7, "pumpkin": 14, "turnip": 14,
    "onion": 30, "garlic": 30, "beans": 5, "green_beans": 5,
    "mushroom": 5, "mushrooms": 5, "beetroot": 14, "jalapeno": 7,
    "green onions": 7, "spring onion": 7,

    # Condiments & Packaged
    "mayonise": 30, "ketchup": 30, "sriracha": 90, "jam jar": 30,
    "strawberry jam": 30, "jar of pickles": 90, "pickles": 90,
    "pickled onion": 30, "pickled cucumber": 30, "pickled carrot": 30,
    "kimchi": 30, "pesto": 14, "hummus": 7,

    # Drinks
    "alcohol": 90, "coconut water": 7, "orange juice": 7,
    "lemonade": 7, "tea": 90, "french vanilla": 7,

    # Misc
    "salad": 2, "flour": 30, "sugar": 90, "ice cubes": 90,
    "water bottle": 90, "fridge": 90, "bottle": 90, "container": 90, "box": 90
}

# -------------------------------
# DB Connection Helpers
# -------------------------------
def get_db_connection():
    """
    Opens a connection to fridge.db (SQLite file).
    Creates the file if it doesn't exist.
    row_factory lets us fetch results as dict-like objects instead of tuples.
    """
    conn = sqlite3.connect("fridge.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the inventory table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            expiry DATE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# CRUD Operations
# -------------------------------
def add_or_update_item(item: str, quantity: int = 1, expiry: str = None):
    """
    Add a new item or update existing one.
    If no expiry provided, use DEFAULT_EXPIRY (today + shelf-life days).
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Assign default expiry if not provided
    if not expiry:
        days = DEFAULT_EXPIRY.get(item.lower(), 7)  # fallback = 7 days
        expiry_date = date.today() + timedelta(days=days)
        expiry = expiry_date.isoformat()

    # Check if item already exists
    cur.execute("SELECT id, quantity FROM inventory WHERE item = ?", (item,))
    row = cur.fetchone()

    if row:
        new_qty = row["quantity"] + quantity
        cur.execute(
            "UPDATE inventory SET quantity = ?, expiry = ? WHERE id = ?",
            (new_qty, expiry, row["id"])
        )
    else:
        cur.execute(
            "INSERT INTO inventory (item, quantity, expiry) VALUES (?, ?, ?)",
            (item, quantity, expiry)
        )

    conn.commit()
    conn.close()

def get_inventory():
    """Return all items currently in the fridge."""
    conn = get_db_connection()
    rows = conn.execute("SELECT item, quantity, expiry FROM inventory").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_expired_items():
    """Return all expired items."""
    today = date.today().isoformat()
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT item, quantity, expiry FROM inventory WHERE expiry < ?", (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
