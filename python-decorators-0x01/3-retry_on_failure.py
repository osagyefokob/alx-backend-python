#!/usr/bin/env python3
"""
3-retry_on_failure.py

Task 3 — Retry Decorator for Database Operations.

Implements:
  - with_db_connection: opens/closes a SQLite connection.
  - retry_on_failure: retries the wrapped function if an exception occurs.
"""

import sqlite3
import functools
import time
from datetime import datetime


def with_db_connection(func=None):
    """Decorator that opens a SQLite connection, passes it to the wrapped function, and closes it afterward."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Opening database connection...")
            conn = sqlite3.connect("users.db")
            try:
                return f(conn, *args, **kwargs)
            finally:
                conn.close()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Connection closed.")
        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


def retry_on_failure(retries=3, delay=2):
    """
    Decorator factory to retry a function call on failure.
    - retries: number of attempts before giving up
    - delay: seconds to wait between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"[{timestamp}] Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print(f"[{timestamp}] All {retries} attempts failed.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch users, retrying automatically if an exception occurs."""
    cursor = conn.cursor()
    # simulate transient error randomly (optional for testing)
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    # Bootstrap local DB if needed
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

    print("Fetching users with retry logic...")
    users = fetch_users_with_retry()
    print("Fetched users:", users)
