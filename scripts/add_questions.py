import sqlite3
import os

def new_question():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir,"..", "data", "quiz.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module TEXT NOT NULL,
        text TEXT NOT NULL,
        answer_a TEXT NOT NULL,
        answer_b TEXT NOT NULL,
        answer_c TEXT NOT NULL,
        correct TEXT NOT NULL                                                                                 
    )""")


    add_more = ""
    while add_more.lower() != "nein":
        

        module = input("Gib hier ein, zu welchem Themenbereich du ein Quiz erstellen möchtest: ")
        text = input("Gib hier die Frage ein: ")
        answer_a = input("Gib hier Antwort A ein: ")
        answer_b = input("Gib jetzt Antwort B ein: ")
        answer_c = input("Und nun noch Antwort C: ")

        correct = "Z"
        while correct.lower() not in "abc":
            correct = input("Jetzt noch den Buchstaben der korrekten Antwort: ")

            if correct.lower() not in ("abc"):
                print("Du kannst nur A, B oder C als korrekte Antwort angeben!")

        add_more = ""
        while add_more.lower() != "ja" and add_more.lower() != "nein":            
            add_more = input("Willst du noch mehr eingeben? (Ja/Nein): ")

            if add_more.lower() != "ja" and add_more.lower() != "nein":
                print("Du musst entweder ja oder nein eingeben!")

            if add_more.lower() == "nein":
                break

        cursor.execute("""INSERT INTO questions (module, text, answer_a, answer_b, answer_c, correct) 
                       VALUES (?, ?, ?, ?, ?, ?)""", (module, text, answer_a, answer_b, answer_c, correct))
    conn.commit()
    conn.close()

new_question()            


                