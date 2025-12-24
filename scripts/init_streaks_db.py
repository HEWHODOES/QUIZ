
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_streaks_db

conn = get_streaks_db()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS streaks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               current_streak INTEGER DEFAULT 0,
               max_streak INTEGER DEFAULT 0,
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

conn.commit()
conn.close()

print("Streaks-DB erstellt!")