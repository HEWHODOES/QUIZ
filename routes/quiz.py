from flask import Blueprint, jsonify, request, render_template, session
from db_connection import get_questions_db
import random
from services.streak_service import update_streak, get_user_streaks
from services.progress_service import mark_module_completed, get_completed_modules, get_perfect_modules

quiz_bp = Blueprint("quiz", __name__)

asked_questions = []

def get_random_question(module_id):

    conn = get_questions_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE module_id = ?", (module_id,))
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

@quiz_bp.route('/get_categories')
def get_categories():
    conn = get_questions_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return jsonify([{"id": cat[0], "name": cat[1]} for cat in categories])

@quiz_bp.route('/get_modules/<int:category_id>')
def get_modules(category_id):
    conn = get_questions_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM modules WHERE category_id = ?", (category_id,))
    modules = cursor.fetchall()
    conn.close()

    if 'user_id' in session:
        completed = get_completed_modules(session['user_id'])
        perfect = get_perfect_modules(session['user_id'])
    else:
        completed = []
        perfect = []

    result = []
    for mod in modules:
        result.append({
            "id": mod[0],
            "name": mod[1],
            "completed": mod[0] in completed,
            "perfect": mod[0] in perfect
        })
    return jsonify(result)        

@quiz_bp.route("/get_question/<int:module_id>")
def get_question(module_id):

    if "current_module" not in session or session["current_module"] != module_id:
        asked_questions.clear()
        conn = get_questions_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions WHERE module_id = ?", (module_id,))
        total = cursor.fetchone()[0]
        conn.close()

        session["current_module"] = module_id
        session["total_questions"] = total
        session["module_questions_correct"] = 0

    question = get_random_question(module_id)
    
    if question is None:
        # End of module — compute totals from session
        total = session.get("total_questions", 0)
        correct = session.get("module_questions_correct", 0)

        # If the user answered all questions correctly, mark as perfect (only for logged-in users)
        # NOTE: previously this compared against a non-existent key 'module_questions_total'
        if correct == total:
            if "user_id" in session:
                mark_module_completed(session["user_id"], module_id, perfect=True)
            # if anonymous, we don't persist perfect (per requirement)

        return jsonify({
            "completed": True,
            "total_questions": total,
            "correct_answers": correct
        }), 200

    return jsonify(question)    

@quiz_bp.route('/')
def start():
    session["score"] = 0
    session["streak"] = 0
    return render_template("quiz.html")

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

    if is_correct:
        session["score"] += 1
        if "module_questions_correct" in session:
            session["module_questions_correct"] += 1   
        else:
            session["module_questions_correct"] = 1     


    if "user_id" in session:
        streak_data = update_streak(session["user_id"], is_correct)
        current_streak = streak_data["current_streak"]

    else:
        if "streak" not in session:
            session["streak"] = 0

        if is_correct:
            session["streak"] += 1
        else:
            session["streak"] = 0

        current_streak = session["streak"]           


    show_celebration = (current_streak in [5, 10, 20])

    return jsonify({
        "correct": is_correct, 
        "score": session["score"], 
        "correct_answer": correct_answer.lower(),
        "streak": current_streak,
        "celebrate": show_celebration
        })