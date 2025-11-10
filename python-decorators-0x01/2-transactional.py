#!/usr/bin/env python3
"""
2-transactional.py

Task 2 — Transaction Management Decorator.

Implements:
- with_db_connection: opens and closes a SQLite connection (copied from Task 1)
- transactional: wraps DB operations to commit on success or rollback on error

Usage:
    @with_db_connection
    @transactional
    def update_user_email(conn, user_id, new_email):
        ...
"""
import sqlite3
import functools
from datetime import datetime


def with_db_connection(func=None):
    """
    Decorator that opens a SQLite connection, passes it as the first argument
    to the wrapped function, and closes it afterward.
    """
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


def transactional(func):
    """
    Decorator that ensures a database operation is executed within a transaction.
    Commits if the wrapped function completes successfully, rolls back on exception.
    The wrapped function MUST accept the sqlite3.Connection as its first argument.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"[{timestamp}] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[{timestamp}] Transaction rolled back due to error: {e}")
            # Re-raise so callers and checkers see the original exception
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email. The connection and transactional behavior are
    handled by decorators.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# A small helper to fetch a user (used in __main__ to show before/after)
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Quick bootstrap for manual testing
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

    # Show before
    print("Before:", get_user_by_id(user_id=1))

    # Attempt update
    try:
        update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
    except Exception as exc:
        print("Update failed:", exc)

    # Show after
    print("After:", get_user_by_id(user_id=1))
