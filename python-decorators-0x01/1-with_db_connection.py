#!/usr/bin/env python3
"""
1-with_db_connection.py

Decorator that automatically handles opening and closing a SQLite database connection.
"""

import sqlite3
import functools
from datetime import datetime


def with_db_connection(func=None):
    """
    Decorator that:
      • Opens a SQLite database connection before calling the wrapped function,
      • Passes the connection object as the first argument,
      • Closes the connection after the function finishes,
      • Logs each connection open/close with a timestamp.
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Opening database connection...")
            conn = sqlite3.connect("users.db")
            try:
                result = f(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Connection closed.")
        return wrapper

    if callable(func):
        # used as @with_db_connection
        return decorator(func)
    return decorator


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a user row by ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Optional quick local bootstrap for testing
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);"
    )
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?);",
            [("Alice", "alice@example.com"), ("Bob", "bob@example.com")],
        )
        conn.commit()
    conn.close()

    user = get_user_by_id(user_id=1)
    print("Fetched user:", user)
