import base64

from flask import render_template, request, session, redirect

from app import db, app, bcrypt
from models import User

@app.route('/')
def index():
    # return render_template('signup.html')
    return render_template('index.html')


# source venv/bin/activate
# run Flask application from terminal
# export FLASK_APP=main.py
# flask run
@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password, 10)

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        url = request.form['url']
        mobile_phone = request.form['mobile_phone']

        age = request.form['age']
        description = request.form['description']
        bank_field = request.form['bank_field']

        print(username, password, firstname, lastname, url, mobile_phone, age, description, bank_field)

        user = User(username=username, password=password_hash, firstname=firstname,
                    lastname=lastname, url=url, mobile_phone=mobile_phone, age=age, description=description,
                    bank_field=bank_field)

        s = db.session()
        s.add(user)
        s.commit()
        message = "New user is created!"
        return render_template('index.html', message=message)

    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        message = 'username or password is wrong'
        conn_success = False
        uname = request.form['username']
        password = request.form['password']

        print(uname, password)

        result = User.query.filter_by(username=uname).first()

        if result != None:
            if bcrypt.check_password_hash(result.password, password):
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
    result = User.query.filter_by(username=username).first()
    return result


@app.route('/userInfo', methods=['GET', 'POST'])
def user_info():
    if 'username' in session:
        username = session['username']
        user = get_user_info(username)
        return render_template('paymentPage.html', **userToDict(user))

def userToDict(user):
    d = {}
    d['username'] = user.username
    d['firstname'] = user.firstname
    d['lastname'] = user.lastname
    d['url'] = user.url
    d['mobile_phone'] = user.mobile_phone
    d['description'] = user.description
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

                user = User.query.filter_by(username=username).first()
                user.firstname = firstname
                user.lastname = lastname
                user.url = url
                user.mobile_phone = mobile_phone
                db.session().commit

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
    results = User.query.all()
    users = []
    for item in results:
        users.append(item.username + ' ' + item.firstname)
        print(item.username + ' ' + item.firstname)

    return render_template('list.html', members=users)


if __name__ == "__main__":
    app.run(debug=True)