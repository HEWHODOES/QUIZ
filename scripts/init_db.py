
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_questions_db

conn = get_questions_db()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               category_id INTEGER NOT NULL,
               name TEXT NOT NULL,
               FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               module_id INTEGER NOT NULL,
               text TEXT NOT NULL,
               answer_a TEXT NOT NULL,
               answer_b TEXT NOT NULL,
               answer_c TEXT NOT NULL,
               correct TEXT NOT NULL,
               FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            )    
        """)

conn.commit()
conn.close()
print("Datenbank erstellt!")