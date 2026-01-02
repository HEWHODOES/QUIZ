import webbrowser
from threading import Timer
from flask import Flask, render_template
from routes.quiz import quiz_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = "easy_learn"

app.register_blueprint(quiz_bp)
app.register_blueprint(auth_bp)

@app.route('/login')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    def open_browser():
        webbrowser.open_new('http://localhost:5000')
    Timer(1, open_browser).start()
    app.run(debug=False)