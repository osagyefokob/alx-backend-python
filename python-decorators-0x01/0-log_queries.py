#!/usr/bin/env python3
"""
0-log_queries.py

Decorator that logs SQL queries before executing the decorated function.

This file implements a decorator usable as:
    @log_queries
    def f(query): ...
or
    @log_queries()
    def f(query): ...
"""

import functools
import inspect
import sqlite3
from typing import Callable, Any, Optional


def _extract_query_from_call(func: Callable, args: tuple, kwargs: dict) -> Optional[str]:
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

    # Fallback heuristic: if first positional arg is a string, treat as query
    if args and isinstance(args[0], str):
        return args[0]

    return None


def log_queries(func: Callable = None):
    """
    Decorator that prints the SQL query before calling the function.

    Supports both @log_queries and @log_queries().
    """
    def decorator(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            query = _extract_query_from_call(f, args, kwargs)
            if query is not None:
                print(f"Executing query: {query}")
            else:
                print("Executing query: <no query found>")
            return f(*args, **kwargs)
        return wrapper

    if callable(func):
        # Used as @log_queries
        return decorator(func)
    # Used as @log_queries()
    return decorator


# Task sample function (keep exact shape as task)
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Minimal local bootstrap for quick manual testing
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

    users = fetch_all_users(query="SELECT * FROM users")
    print("Result rows:", users)
