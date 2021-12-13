from flask import Flask, render_template, request

import databaseManager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

# run databaseManager.py for first time to create database
# source venv/bin/activate
# run Flask application from terminal
# export FLASK_APP=main.py
# flask run
@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        save_new_user(username, password)

    return render_template('login.html', error=error)


def save_new_user(username, password):
    db = databaseManager.engine
    conn = db.connect()

    users = databaseManager.users
    ins = users.insert().values(username=username, password=password)
    conn.execute(ins)
