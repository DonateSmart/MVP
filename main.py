from flask import Flask, render_template, request
from sqlalchemy import select

import databaseManager
from databaseManager import User

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('signup.html')


# source venv/bin/activate
# run Flask application from terminal
# export FLASK_APP=main.py
# flask run
@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        print(uname, pwd)
        user = User(name=uname, password=pwd)
        s = databaseManager.session()
        s.add(user)
        s.commit()
        message= "success"

    return render_template('signup.html', error=error, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        conn_success = False
        uname = request.form['username']
        pwd = request.form['password']
        print(uname, pwd)

        s = databaseManager.session()
        result = s.execute(select(User).filter_by(name=uname))

        row = result.fetchone()
        print('password:' + row[0].password)
        if pwd == row[0].password:
            conn_success = True

        print('conn_success:' + str(conn_success))

        if conn_success:
            return render_template('list.html', error=error)
        else:
            return render_template('signup.html', error=error)
    else:
        return render_template('login.html')



@app.route('/listUsers')
def listUsers():
    s = databaseManager.session()
    results = s.execute(select(User).order_by(User.name))
    users = []
    for item in results.scalars():
        users.append(item.name + ' ' + item.password)
        print(item.name + ' ' + item.password)

    return render_template('list.html', members=users)


def save_new_user(username, password):
    db = databaseManager.engine
    conn = db.connect()

    users = databaseManager.users
    ins = users.insert().values(username=username, password=password)
    conn.execute(ins)


app.run(debug=True)