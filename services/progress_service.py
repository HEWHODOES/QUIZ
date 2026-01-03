
import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_users_db

def mark_module_completed(user_id, module_id, perfect=False):

    conn = get_users_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, perfect FROM progress
            WHERE user_id = ? AND module_id = ?
        """, (user_id, module_id))
        existing = cursor.fetchone()
        if existing:
            existing_id, existing_perfect = existing

            if perfect and not existing_perfect:
                cursor.execute("""
                    UPDATE progress
                    SET perfect = 1, completed_at = datetime('now')
                    WHERE user_id = ? AND module_id = ?
                """, (user_id, module_id))

        else:
            cursor.execute("""
                INSERT INTO progress (user_id, module_id, perfect)
                VALUES (?, ?, ?)
            """, (user_id, module_id, 1 if perfect else 0))

        conn.commit()
        conn.close()
        return True        
    
    except sqlite3.IntegrityError as e:
        conn.close()
        print(f"Integrity error: {e}")
        return False
    
    except sqlite3.Error as e:
        conn.close()
        print(f"Database error: {e}")
        return False


def get_completed_modules(user_id):

    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT module_id FROM progress WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return [r[0] for r in results]

def get_perfect_modules(user_id):

    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT module_id FROM progress WHERE user_id = ? AND perfect = 1", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return [r[0] for r in results]
   