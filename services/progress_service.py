
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_users_db

def mark_module_completed(user_id, module_id, perfect=False):

    conn = get_users_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO progress (user_id, module_id, perfect) VALUES (?, ?, ?)", 
                       (user_id, module_id, 1 if perfect else 0))

        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_perfect_modules(user_id):

    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT module_id FROM progress WHERE user_id = ? AND perfect = 1", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return [r[0] for r in results]

def get_completed_modules(user_id):

    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT module_id FROM progress WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return [r[0] for r in results]

def is_module_completed(user_id, module_id):

    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM progress WHERE user_id = ? AND module_id = ?", (user_id, module_id))
    result = cursor.fetchone()
    conn.close()

    return result is not None    