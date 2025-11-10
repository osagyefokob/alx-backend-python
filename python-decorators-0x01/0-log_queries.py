#!/usr/bin/env python3
"""
0-log_queries.py

Decorator that logs SQL queries before executing the decorated function.
"""

import functools
import inspect
import sqlite3
from datetime import datetime  # ✅ Added this import for timestamp


def _extract_query_from_call(func, args, kwargs):
    """Return the value passed for a parameter named 'query' if present."""
    if "query" in kwargs:
        return kwargs["query"]

    try:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        if "query" in bound.arguments:
            return bound.arguments["query"]
    except Exception:
        pass

    if args and isinstance(args[0], str):
        return args[0]
    return None


def log_queries(func=None):
    """Decorator that prints the SQL query with timestamp before calling the function."""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            query = _extract_query_from_call(f, args, kwargs)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if query:
                print(f"[{timestamp}] Executing query: {query}")
            else:
                print(f"[{timestamp}] Executing query: <no query found>")
            return f(*args, **kwargs)
        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print("Result rows:", users)
