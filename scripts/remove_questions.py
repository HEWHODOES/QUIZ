import sqlite3
import os

def manage_db():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir,"..", "data", "quiz.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\nDieses Programm erlaubt dir ganze Module oder bestimmte Fragen aus einem Modul\naus der Quiz DB zu entfernen.\n")
    while True:

        action = input("Komplettes Modul löschen? [1]\n" \
        "Fragen aus einem Modul entfernen? [2]\n"
        "Programm beenden? [3]\n")

        if action not in ("1", "2", "3"):
            print("Du kannst nur 1, 2 oder 3 angeben!")
            continue

        if action == "1":
            cursor.execute("""SELECT DISTINCT module FROM questions""")
            all_modules = cursor.fetchall()
            
            show_modules = [m[0] for m in all_modules]
            print(f"\nVorhandene Module in der Datenbank:\n\n{show_modules}")

            module_to_delete = input("\nWelches Modul willst du löschen?:\n")

            if module_to_delete not in show_modules:
                print("\nDas eingegebene Modul ist nicht vorhanden! Bitte achte auf Groß- und Kleinschreibung.\n")
                
            if module_to_delete in show_modules:
                validate_choice = input(f"\nBist du Sicher, dass du {module_to_delete} und all seine Inhalte löschen willst? JA/NEIN:\n")
                if validate_choice.lower() == "ja":
                    cursor.execute("""DELETE FROM questions WHERE module = ?""", (module_to_delete,))
                    conn.commit()
                    print(f"\nDas Modul {module_to_delete} und sein gesamter Inhalt wurden gelöscht!\n")

        if action == "2":
                cursor.execute("""SELECT DISTINCT module FROM questions""")
                all_modules = cursor.fetchall()
            
                show_modules = [m[0] for m in all_modules]
                print(show_modules)

                selected_module = input("\nWelches Modul willst du bearbeiten?:\n")
                cursor.execute("""SELECT * FROM questions WHERE module = ?""", (selected_module,))
                questions_in_selected_module = cursor.fetchall()

                for question in questions_in_selected_module:
                     print(question)

                question_to_delete = input("\nGib die ID der Frage ein, welche du löschen willst:\n")

                cursor.execute("""SELECT * FROM questions WHERE module= ? AND id = ?""", 
                               (selected_module, question_to_delete,))     
                selected_question = cursor.fetchone()
                if selected_question:
                    print(f"\nDu möchtest diese Frage löschen:\n{selected_question}")
                    validate = input("\nBist du sicher? JA/NEIN:\n")

                    if validate.lower() == "ja":
                        cursor.execute("""DELETE FROM questions WHERE module= ? AND id = ?""",
                                        (selected_module, question_to_delete))
                        conn.commit()
                        print("\nDie Frage wurde gelöscht!\n")
                else:
                    print("\nFrage mit dieser ID nicht gefunden.\n")

        if action == "3":
            print("\nProgramm beendet...")
            break

    conn.close()
    print("Datenbankverbindung geschlossen...\n")               

manage_db()    