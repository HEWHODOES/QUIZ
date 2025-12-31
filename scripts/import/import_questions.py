
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from db_connection import get_questions_db

conn = get_questions_db()
cursor = conn.cursor()

json_file = input("Gib den namen der Datei ein, die in die Datenbank importiert werden soll (z.B. questions.json): \n")

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, json_file)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for category_data in data['categories']:
            category_name = category_data['name']
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            result = cursor.fetchone()
        if result:
            category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
            category_id = cursor.lastrowid 

        for module_data in category_data['modules']:
            module_name = module_data['name']

            cursor.execute("SELECT id FROM modules WHERE name = ? AND category_id = ?", 
                        (module_name, category_id))
            result = cursor.fetchone()
            if result:
                module_id = result[0]
            else:
                cursor.execute("INSERT INTO modules (name, category_id) VALUES (?, ?)", 
                            (module_name, category_id))
                module_id = cursor.lastrowid

            for question in module_data['questions']:
                cursor.execute("""
                    INSERT INTO questions (module_id, text, answer_a, answer_b, answer_c, correct)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    module_id,
                    question['text'],
                    question['answer_a'],
                    question['answer_b'],
                    question['answer_c'],
                    question['correct']
                ))

except FileNotFoundError:
    print(f"\nDie Datei {json_file} wurde nicht gefunden.")
except json.JSONDecodeError:
    print(f"\nDie Datei {json_file} ist keine gültige JSON-Datei.")
except KeyError as e:
    print("Fehler! Die Struktur der Datei ist ungültig. Fehlender Schlüssel:", e)

conn.commit()
conn.close()

print("\nFragen erfolgreich in die Datenbank importiert!")  
print(f"Die datei {json_file} wurde in die Datenbank eingefügt!") 

