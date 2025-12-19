import webbrowser
from threading import Timer
from flask import Flask
from routes.quiz import quiz_bp

app = Flask(__name__)
app.secret_key = "easy_learn"

app.register_blueprint(quiz_bp)

if __name__ == '__main__':
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')

    Timer(1, open_browser).start()    
    app.run(debug=False)