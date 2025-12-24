
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_streaks_db

def get_user_streaks(user_id):

    conn = get_streaks_db()
    cursor = conn.cursor()

    cursor.execute("SELECT current_streak, max_streak FROM streaks WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"current_streak": result[0], "max_streak": result[1]}
    else:
        create_streak_entry(user_id)
        return {"current_streak": 0, "max_streak": 0}
    
def create_streak_entry(user_id):

    conn = get_streaks_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO streaks (user_id, current_streak, max_streak) VALUES (?, 0, 0)", (user_id,))
    conn.commit()
    conn.close()

def update_streak(user_id, is_correct):
    
    conn = get_streaks_db()
    cursor = conn.cursor()

    cursor.execute("SELECT current_streak, max_streak FROM streaks WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        create_streak_entry(user_id)
        current = 0
        max_streak = 0
    else:
        current = result[0]
        max_streak = result[1]

    if is_correct:
        current += 1
        if current > max_streak:
            max_streak = current
    else: 
        current = 0

    cursor.execute("UPDATE streaks SET current_streak = ?, max_streak = ? WHERE user_id = ?",
                   (current, max_streak, user_id))

    conn.commit()
    conn.close() 

    return {"current_streak": current, "max_streak": max_streak}                   