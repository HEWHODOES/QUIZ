from flask import Blueprint, jsonify, request, render_template, session
from db_connection import get_questions_db
import random

quiz_bp = Blueprint("quiz", __name__)

asked_questions = []

def get_module():
    conn = get_questions_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT module FROM questions", ())
    modules_found = cursor.fetchall()
    conn.close()

    modules_to_pick_from = [m[0] for m in modules_found]
    return modules_to_pick_from

def get_random_question(module):

    conn = get_questions_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE module = ?", (module,))
    all_questions = cursor.fetchall()
    conn.close()

    remaining = [q for q in all_questions if q[0] not in asked_questions]
    if not remaining:
        return None
    
    result = random.choice(remaining)
    asked_questions.append(result[0])   
    
    return {
    "id": result[0],
    "text": result[2],
    "answer_a": result[3],
    "answer_b": result[4],
    "answer_c": result[5],
    "correct": result[6]
    }

@quiz_bp.route('/')
def start():
    session["score"] = 0
    session["streak"] = 0
    modules = get_module()
    return render_template("quiz.html", modules=modules)

@quiz_bp.route("/reset_questions", methods=["POST"])
def reset_questions():
    asked_questions.clear()
    return jsonify({"success": True})

@quiz_bp.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data.get("question_id")
    selected_answer = data.get("selected_answer")

    conn = get_questions_db()
    cursor = conn.cursor()

    cursor.execute("SELECT correct FROM questions WHERE id= ?", (question_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "Question not found"}), 404
    
    correct_answer = result[0]
    is_correct = (selected_answer.lower() == correct_answer.lower())
    if "score" not in session:
        session["score"] = 0
    if "streak" not in session:
        session["streak"] = 0

    if is_correct:
        session["score"] += 1   
        session["streak"] += 1
    else:
        session["streak"] = 0

    show_celebration = (session["streak"] in [5, 10, 20])

    return jsonify({
        "correct": is_correct, 
        "score": session["score"], 
        "correct_answer": correct_answer.lower(),
        "streak": session["streak"],
        "celebrate": show_celebration
        })

@quiz_bp.route("/get_question/<module>")
def get_question(module):
    question = get_random_question(module)
    if question is None:
        return jsonify({"error": "No questions found"}), 404
    return jsonify(question)