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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        url = request.form['url']
        mobile_phone = request.form['mobile_phone']

        print(username, password, firstname, lastname, url, mobile_phone)

        user = User(username=username, password=password, firstname=firstname,
                    lastname=lastname, url=url, mobile_phone=mobile_phone)

        s = databaseManager.session()
        s.add(user)
        s.commit()
        message = "New user is created!"
        return render_template('signup.html', message=message)

    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        message = 'username or password is wrong'
        conn_success = False
        uname = request.form['username']
        pwd = request.form['password']
        print(uname, pwd)

        s = databaseManager.session()
        result = s.execute(select(User).filter_by(username=uname))

        row = result.fetchone()

        if row != None:
            if pwd == row[0].password:
                conn_success = True

        if conn_success:
            message = 'connection is successful'

        return render_template('login.html', message=message)
    else:
        return render_template('login.html')



@app.route('/listUsers')
def listUsers():
    s = databaseManager.session()
    results = s.execute(select(User).order_by(User.username))
    users = []
    for item in results.scalars():
        users.append(item.username + ' ' + item.password)
        print(item.username + ' ' + item.password)

    return render_template('list.html', members=users)



app.run(debug=True)