
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_users_db

conn = get_users_db()
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password_hash TEXT NOT NULL,
               created_at TEXT DEFAULT (datetime('now'))
    ) 
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS streaks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               current_streak INTEGER DEFAULT 0,
               max_streak INTEGER DEFAULT 0,
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               module_id INTEGER NOT NULL,
               completed_at TEXT DEFAULT (datetime('now')),
               perfect INTEGER DEFAULT 0,
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
               UNIQUE(user_id, module_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_progress(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               question_id INTEGER NOT NULL,
               correct BOOLEAN NOT NULL,
               answered_at TEXT DEFAULT (datetime('now')),
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
               UNIQUE(user_id, question_id)
    )
""")

conn.commit()
conn.close()
print("users.db erstellt!")