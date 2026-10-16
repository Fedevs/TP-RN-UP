import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "products.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
