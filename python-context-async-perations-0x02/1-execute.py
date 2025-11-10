#!/usr/bin/env python3
"""
1-execute.py

Reusable class-based context manager ExecuteQuery.
Executes a provided SQL query with parameters and returns the results.
"""

import sqlite3


class ExecuteQuery:
    """
    Context manager that:
      - Opens a SQLite connection on entry.
      - Executes a provided query with optional parameters.
      - Returns fetched results from __enter__.
      - Closes the connection automatically on exit.
    """

    def __init__(self, query: str, params: tuple = (), db_path: str = "users.db"):
        self.query = query
        self.params = params
        self.db_path = db_path
        self.connection = None
        self._results = None

    def __enter__(self):
        """Open connection, execute query
