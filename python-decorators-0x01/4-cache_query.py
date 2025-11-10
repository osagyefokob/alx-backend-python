#!/usr/bin/env python3
"""
4-cache_query.py

Task 4 — Using Decorators to Cache Database Queries.

Implements:
  - with_db_connection: handles opening/closing DB connections
  - cache_query: caches query results to avoid redundant database calls
"""

import sqlite3
import functools
import time
from datetime import datetime

# Global cache for query results
query_cache = {}


def with_db_connection(func=None):
    """Decorator that opens and closes a SQLite connection automatically."""
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


def cache_query(func):
    """
    Decorator that caches database query results based on the SQL query string.
    Uses a global dictionary `query_cache` where:
      - Key: query string
      - Value: result from database
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query (must be passed as keyword or positional arg)
        query = kwargs.get("query")
        if query is None and len(args) > 0:
            query = args[0]

        if query in query_cache:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Cache hit for query: {query}")
            return query_cache[query]

        # Otherwise, execute function and cache the result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Cache miss. Query executed and stored.")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from DB and cache results."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # Bootstrap minimal database if needed
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

    # First call — cache miss
    print("\nFirst call: executing query and caching result...")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users:", users)

    # Second call — cache hit
    print("\nSecond call: should use cached result...")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Users (from cache):", users_again)
