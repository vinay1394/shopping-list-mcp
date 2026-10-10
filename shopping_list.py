import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "shopping_list.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    return conn

def list_items() -> list[dict]:
    """Return all items on the shopping list as [{'id': 1, 'name': 'milk'}, ...]."""
    with _connect() as conn:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def add_item(name: str) -> dict:
    """Add an item to the shopping list and return it, including its new id."""
    name = name.strip()
    if not name:
        raise ValueError("Item name cannot be empty")
    with _connect() as conn:
        cur = conn.execute("INSERT INTO items (name) VALUES (?)", (name,))
        return {"id": cur.lastrowid, "name": name}

def delete_item(item_id: int) -> dict:
    """Delete the item with the given id. Raises if no such item exists."""
    with _connect() as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        if cur.rowcount == 0:
            raise ValueError(f"No item with id {item_id}")
    return {"deleted_id": item_id}

if __name__ == "__main__":
    print(add_item("milk"))
    print(add_item("eggs"))
    print(list_items())
    print(delete_item(1))
    print(list_items())