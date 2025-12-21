
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db_connection import get_questions_db

def remove_data():

    conn = get_questions_db()
    cursor = conn.cursor()

    print("\nDieses Programm erlaubt dir ganze Kategorien, ganze Module\noder bestimmte Fragen aus einem Modul\naus der Quiz DB zu entfernen.\n")
    
    while True:

        action = input(
            "Komplette Kategorie löschen? [1]\n" \
            "Ein Modul entfernen? [2]\n"
            "Fragen aus einem Modul entfernen? [3]\n"
            "Programm beenden? [4]\n"
            "Wähle: "
            )

        if action not in ("1", "2", "3", "4"):
            print("Du kannst nur 1, 2, 3 oder 4 angeben!")
            continue

        if action == "1":
            cursor.execute("""SELECT id, name FROM categories""")
            categories = cursor.fetchall()
            
            if not categories:
                print("Keine Kategorien gespeichert!\n")
                continue

            print("=== Vorhandene Kategorien ===\n")
            for cat in categories:
                print(f"[{cat[0]}] {cat[1]}")
            category_id = input("\nGib die ID der Kategorie ein, die gelöscht werden soll:\n")
            
            confirm = input("Die Kategorie und ihr gesamter Inhalt wird gelöscht! Wirklich sicher? [JA/NEIN]: ")

            if confirm.lower() == "ja":
                cursor.execute("DELETE FROM categories WHERE id = ?," (category_id,))
                conn.commit()
                print("\nKategorie entfernt!")
            else:
                print("\nVorgang abgebrochen!")

        if action == "2":
            cursor.execute("""SELECT id, name FROM modules""")
            modules = cursor.fetchall()
            
            if not modules:
                print("Keine Module gespeichert!\n")
                continue

            print("=== Vorhandene Module ===\n")
            for module in modules:
                print(f"[{module[0]}] {module[1]}")
            module_id = input("\nGib die ID des Moduls ein, das gelöscht werden soll:\n")
            
            confirm = input("Das Modul und sein gesamter Inhalt wird gelöscht! Wirklich sicher? [JA/NEIN]: ")

            if confirm.lower() == "ja":
                cursor.execute("DELETE FROM modules WHERE id = ?," (module_id,))
                conn.commit()
                print("\nModul entfernt!")
            else:
                print("\nVorgang abgebrochen!")

        if action == "3":
            cursor.execute("""SELECT id, name FROM modules""")
            modules = cursor.fetchall()
            
            if not modules:
                print("Keine Module mit Fragen gespeichert!\n")
                continue

            print("=== Vorhandene Module ===\n")
            for module in modules:
                print(f"[{module[0]}] {module[1]}")
            module_id = input("\nGib die ID des Moduls ein, aus dem du Fragen löschen möchtest:\n")

            cursor.execute("SELECT id, text FROM questions WHERE module_id = ?," (module_id,))
            questions = cursor.fetchall()

            if not questions:
                print("\nIn diesem Modul sind keine Fragen enthalten!")

            print("\n=== Vorhandene Fragen ===\n")
            for q in questions:
                print(f"[{q[0]}] {q[1][:100]}") 

            question_id = input("\nGib die ID der zu löschenden Frage ein: ")
            confirm = input("\nBist du sicher, dass du diese Frage löschen willst? [JA/NEIN]: ")

            if confirm.lower() == "ja":
                cursor.execute("DELETE FROM questions WHERE id = ?," (question_id,))
                conn.commit()
                print("\nFrage gelöscht!")
            else: 
                print("Vorgang abgebrochen!") 
        if action == "4":
            print("\nProgramm beendet....")
            print("Verbindung zur Datenbank geschlossen...")
            break                  
            
            

remove_data()