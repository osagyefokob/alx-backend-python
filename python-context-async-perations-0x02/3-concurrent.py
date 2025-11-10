#!/usr/bin/env python3
import asyncio
import aiosqlite
import sqlite3

async def asyncfetchusers():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def asyncfetcholder_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(asyncfetchusers(), asyncfetcholder_users())
    print("All users:", all_users)
    print("Users older than 40:", older_users)

# ensure table/data exists
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
            ("Daniel", "daniel@example.com", 22),
        ],
    )
    conn.commit()
conn.close()

asyncio.run(fetch_concurrently())
