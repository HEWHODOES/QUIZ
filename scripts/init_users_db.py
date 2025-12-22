
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_users_db

conn = get_users_db()
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               created_at TEXT DEFAULT (datetime('now'))
    ) 
""")

conn.commit()
conn.close()
print("users.db erstellt!")