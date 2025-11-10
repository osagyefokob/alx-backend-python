#!/usr/bin/env python3
"""
0-databaseconnection.py

Custom class-based context manager for database connection handling.
Opens and closes a SQLite connection automatically.
"""

import sqlite3


class DatabaseConnection:
    """
    Custom context manager for SQLite database connection.

    Usage:
        with DatabaseConnection("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            print(cursor.fetchall())
    """

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        """Open the SQLite connection and return it."""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection automatically when leaving the context."""
        if self.connection:
            self.connection.close()


# ✅ Test when run directly
if __name__ == "__main__":
    # Create table and seed data if needed
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);"
    )
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [("Alice", "alice@example.com"), ("Bob", "bob@example.com")],
        )
        conn.commit()
    conn.close()

    # Use context manager to fetch and print users
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users:", users)
