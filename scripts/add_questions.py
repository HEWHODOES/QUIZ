
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_questions_db

conn = get_questions_db()
cursor = conn.cursor()

def new_question():

    add_more = ""
    while add_more.lower() != "nein":
        
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()

        if not categories:
            print("\nDie Datenbank ist leer!\n")
            category_choice = input("Kategorie angeben: ")

        if categories:
            print("\nVorhandene Kategorien:")
            for cat in categories:
                print(f"[{cat[0]}] {cat[1]}")

            category_choice = input("Kategorie-ID oder neue Kategorie eingeben: ")        

        if category_choice.isdigit():
            category_id = int(category_choice)
        else:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_choice,))
            conn.commit()
            category_id = cursor.lastrowid
            print(f"Neue Kategorie '{category_choice}' erstellt!")

        cursor.execute("SELECT id, name FROM modules WHERE category_id = ?", (category_id,))    
        modules = cursor.fetchall()

        if modules:
            print("\nVorhandene Module:")
            for mod in modules:
                print(f"[{mod[0]}] {mod[1]}")

        module_choice = input("\nModul_ID oder Namen für neues Modul eingeben:") 
        
        if module_choice.isdigit():
            module_id = int(module_choice)
        else:
            cursor.execute("INSERT INTO modules (category_id, name) VALUES (?, ?)", (category_id, module_choice))
            conn.commit()
            module_id = cursor.lastrowid
            print(f"Neues Modul '{module_choice}' erstellt!")

        print("\n=== Frage erstellen ===")
        text = input("Frage: ")
        answer_a = input("Antwort A: ")            
        answer_b = input("Antwort B: ")
        answer_c = input("Antwort C: ")

        correct = "Z"
        while correct.lower() not in "abc":
            correct = input("Jetzt noch den Buchstaben der korrekten Antwort: ")

            if correct.lower() not in ("abc"):
                print("Du kannst nur A, B oder C als korrekte Antwort angeben!")

        cursor.execute("""INSERT INTO questions (module_id, text, answer_a, answer_b, answer_c, correct) 
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (module_id, text, answer_a, answer_b, answer_c, correct.lower()))

        conn.commit()
        print("Frage gespeichert!")

        add_more = ""
        while add_more.lower() not in ("ja", "nein"):            
            add_more = input("Willst du noch mehr eingeben? (Ja/Nein): ")

        
    
    conn.close()
    print("\nFertig!")

new_question()            


                