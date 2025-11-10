#!/usr/bin/env python3
"""
0-databaseconnection.py

Class-based context manager that opens and closes a SQLite connection
using __enter__ and __exit__. Demonstrates a simple SELECT * FROM users.
"""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    A simple context manager for SQLite connections.

    Usage:
        with DatabaseConnection("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
    """

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Always close connection. Let exceptions propagate (return False implicitly).
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Minimal bootstrap: ensure table exists and has data
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER);"
    )
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?);",
            [
                ("Alice", "alice@example.com", 30),
                ("Bob", "bob@example.com", 45),
                ("Clara", "clara@example.com", 50),
            ],
        )
        conn.commit()
    conn.close()

    # Use the context manager to run the query and print results
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Users:", rows)
