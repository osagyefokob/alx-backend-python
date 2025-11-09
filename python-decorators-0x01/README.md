# Python Decorators — 0x01

This project explores how **Python decorators** can make database operations cleaner, safer, and more reusable.  
Each task focuses on automating a common database concern — logging, connection handling, transactions, retries, and caching.

---

## 🧠 Learning Objectives
By the end of this project you will:
- Understand how decorators intercept and extend function behavior.
- Automate repetitive database operations (connections, commits, rollbacks).
- Build resilient, maintainable, and efficient backend code.
- Write PEP8-compliant, production-grade Python.

---

## ⚙️ Project Setup
- **Python version:** 3.8 or higher  
- **Database:** SQLite3 (`users.db` used for testing)
- **Repository:** `alx-backend-python`  
- **Directory:** `python-decorators-0x01/`

---

## 🧩 Task 0 — Logging Database Queries
**Objective:** Create a decorator that logs every SQL query executed by a function.

**File:** `0-log_queries.py`

### Example
```python
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")
