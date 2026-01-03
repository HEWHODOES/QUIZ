
import sqlite3
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_users_db
from services.streak_service import reset_current_streak

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username und Passwort benötigt!!"}), 400
    
    password_hash = generate_password_hash(password)
    
    conn = get_users_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (username, password_hash)
                       )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        session['user_id'] = user_id
        session['username'] = username

        return jsonify({"success": True, "username": username})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username bereits vergeben!"}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username und Passwort benötigt!"}), 400
    
    conn = get_users_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", 
                   (username,)
                   )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Falscher Username oder Passwort!"}), 401
    
    user_id, user_name, password_hash = user
    if not check_password_hash(password_hash, password):
        return jsonify({"error": "Falscher Username oder Passwort!"}), 401
    
    session['user_id'] = user_id
    session['username'] = user_name
    reset_current_streak(user_id)

    return jsonify({"success": True, "username": user_name})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "username": session["username"]})
    return jsonify({"logged_in": False})