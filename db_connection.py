import sqlite3
import os

def get_questions_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "data", "quiz.db")
    return sqlite3.connect(db_path)

def get_users_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "data", "users.db")
    return sqlite3.connect(db_path)

def get_progress_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "data", "progress.db")
    return sqlite3.connect(db_path)

def get_streaks_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "data", "streaks.db")
    return sqlite3.connect(db_path)

def get_analytics_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "data", "analytics.db")
    return sqlite3.connect(db_path)