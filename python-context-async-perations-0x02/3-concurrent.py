#!/usr/bin/env python3
"""
3-concurrent.py

Run concurrent async SQLite queries using aiosqlite and asyncio.gather.
"""

import asyncio
import aiosqlite  # required for async SQLite
import sqlite3


async def asyncfetchusers():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def asyncfetcholder_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    all_users, older_users = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users(),
    )
    print("All users:", all_users)
    print("Users older than 40:", older_users)


# Bootstrap DB (sync) to ensure there's data before async run
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER);"
)
cur.execute("SELECT COUNT(*) FROM users;")
if cur.fetchone()[0] == 0:
    cur.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)
