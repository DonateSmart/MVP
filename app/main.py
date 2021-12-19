import base64

from flask import Flask, render_template, request, session, redirect
from sqlalchemy import select, update

from flask_sqlalchemy import SQLAlchemy
from app import db, app
from models import User

app = Flask(__name__)
app.secret_key = "daskdlaslddsa"

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
        password = request.form['password'].encode("utf-8")
        encoded_password = base64.b64encode(password)

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        url = request.form['url']
        mobile_phone = request.form['mobile_phone']

        print(username, password, firstname, lastname, url, mobile_phone)

        user = User(username=username, password=encoded_password, firstname=firstname,
                    lastname=lastname, url=url, mobile_phone=mobile_phone)

        s = db.session()
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
        pwd = request.form['password'].encode("utf-8")
        encoded_password = base64.b64encode(pwd)

        print(uname, pwd)

        s = db.session()
        result = s.execute(select(User).filter_by(username=uname))

        row = result.fetchone()

        if row != None:
            if encoded_password == row[0].password:
                conn_success = True

        if conn_success:
            message = 'connection is successful'
            session['username'] = uname
            return user_info()
        else:
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')

def get_user_info(username):
    s = db.session()
    result = s.execute(select(User).filter_by(username=username))

    row = result.fetchone()

    # username = row[0].username
    # firstname = row[0].firstname
    # lastname = row[0].lastname
    # url = row[0].url
    # mobile_phone = row[0].mobile_phone
    return row[0]


@app.route('/userInfo', methods=['GET', 'POST'])
def user_info():
    if 'username' in session:
        username = session['username']
        user = get_user_info(username)
        return render_template('userInfo.html', **userToDict(user))

def userToDict(user):
    d = {}
    d['username'] = user.username
    d['firstname'] = user.firstname
    d['lastname'] = user.lastname
    d['url'] = user.url
    d['mobile_phone'] = user.mobile_phone
    return d

@app.route('/editUserInfo', methods=['GET', 'POST'])
def edit_user_info():
    if request.method == 'POST':
        if 'username' in session:

            username = session['username']

            if request.form.get('username') != None and request.form.get('firstname') != None and \
                    request.form.get('lastname') != None and request.form.get('url') != None \
                    and request.form.get('mobile_phone') != None :

                message = 'User info is saved!'

                firstname = request.form['firstname']
                lastname = request.form['lastname']
                url = request.form['url']
                mobile_phone = request.form['mobile_phone']

                # update data in db

                s = db.session()
                stmt = update(User).where(User.username == username).values(firstname=firstname,lastname=lastname,
                                                                                 url=url, mobile_phone=mobile_phone)
                s.execute(stmt)


                return render_template('userInfo.html', username=username, firstname=firstname, lastname=lastname,
                                       url=url, mobile_phone=mobile_phone, message=message)

    else:
        if 'username' in session:
            username = session['username']
            user = get_user_info(username)
            return render_template('editUserInfo.html', **userToDict(user))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route('/listUsers')
def listUsers():
    s = db.session()
    results = s.execute(select(User).order_by(User.username))
    users = []
    for item in results.scalars():
        users.append(item.username + ' ' + item.password)
        print(item.username + ' ' + item.password)

    return render_template('list.html', members=users)

if __name__ == "__main__":
    app.run(debug=True)