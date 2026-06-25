# Vulnerable Flask API

**DO NOT USE IN PRODUCTION**

This version intentionally demonstrates OWASP Top 10 vulnerabilities.

## Vulnerabilities Present
- **A01: Broken Access Control** — No auth on `/order`, no authorization on `/admin/users`
- **A03: Injection** — SQL injection in authentication and order endpoints
- **A02: Cryptographic Failures** — Passwords stored in plaintext, weak session secret

## Run
```bash
pip install -r requirements.txt
python app.py

Exploit Examples:
# SQL Injection login bypass
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin' OR '1'='1", "password": "anything"}'

# Access admin without auth
curl http://localhost:5000/admin/users

5. Click **"Commit new file"**

---

## Step 3: Create the Secure App (5 files)

Now create the fixed version. Same process: **Add file** → **Create new file** → type path → paste content → commit.

### File 4: `secure/models.py`

**Filename:** `secure/models.py`

```python
import sqlite3
from werkzeug.security import generate_password_hash

def get_db():
 conn = sqlite3.connect("shop.db")
 conn.row_factory = sqlite3.Row
 return conn

def init_db():
 conn = get_db()
 cursor = conn.cursor()
 cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
         id INTEGER PRIMARY KEY,
         username TEXT UNIQUE NOT NULL,
         password_hash TEXT NOT NULL,
         role TEXT DEFAULT 'user'
     )
 """)
 cursor.execute("""
     CREATE TABLE IF NOT EXISTS products (
         id INTEGER PRIMARY KEY,
         name TEXT NOT NULL,
         price REAL NOT NULL
     )
 """)
 cursor.execute("""
     CREATE TABLE IF NOT EXISTS orders (
         id INTEGER PRIMARY KEY,
         user_id INTEGER NOT NULL,
         product_id INTEGER NOT NULL,
         quantity INTEGER NOT NULL,
         FOREIGN KEY (user_id) REFERENCES users(id)
     )
 """)
 conn.commit()
