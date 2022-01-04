import base64

from flask import render_template, request, session, redirect

from app import db, app, bcrypt
from models import User, BankAccount

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
        bank_number = request.form['bank_number']

        print(username, password, firstname, lastname, url, mobile_phone, age, description, bank_number)

        bank_account = BankAccount(bank_number=bank_number, amount=0)
        user = User(username=username, password=password_hash, firstname=firstname,
                    lastname=lastname, url=url, mobile_phone=mobile_phone, age=age, description=description,
                    bank_info=bank_account)

        s = db.session()
        s.add(user)
        s.add(bank_account)
        s.commit()

        message = "New user is created! the username is " + username + " the person id is: " + str(user.id)
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
            return user_info(result.id, uname)
        else:
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')

def get_user_info(username):
    s = db.session()
    result = User.query.filter_by(username=username).first()
    return result


def get_user_info_byUserId(person_id):
    s = db.session()
    result = User.query.filter_by(id=person_id).first()
    return result


def get_bank_info_byUserId(person_id):
    s = db.session()
    result = BankAccount.query.filter_by(user_id=person_id).first()
    return result


@app.route('/userInfo/<person_id>/<username>', methods=['GET', 'POST'])
def user_info(person_id, username):
    # if 'username' in session:
    #     username = session['username']
    user = get_user_info_byUserId(person_id)
    return render_template('paymentPage.html', **userToDict(user))


@app.route('/userInfo_for_market/<person_id>', methods=['GET', 'POST'])
def user_info_for_market(person_id):
    print(person_id)
    user = get_user_info_byUserId(person_id)
    print(user.username)

    # return render_template('paymentPage.html', **userToDict(user))


@app.route('/requestPayment/<person_id>/<amount>', methods=['GET', 'POST'])
def requestPayment(person_id, amount):
    print(person_id + " " + amount)

    user = get_user_info_byUserId(person_id)
    bank_amount = get_bank_info_byUserId(person_id)

    amount = int(amount)
    if(bank_amount.amount >= amount): # there is enough money
        message = "transaction is successful for amount of payment " + str(amount) + "\n"
        bank_amount.amount = bank_amount.amount - amount
        db.session().commit()
    else:
        message = "transaction failed for amount of donation " + str(amount)

    return render_template("authorized.txt", username=user.username, amount=amount, message=message, remaining_money=bank_amount.amount)
    # return render_template('paymentPage.html', **userToDict(user), message=message)


@app.route('/donate/<person_id>', methods=['GET', 'POST'])
def donate(person_id):
    if request.method == 'POST':
        user = get_user_info_byUserId(person_id)
        amount = request.form['amountInput']
        print(person_id + " " + amount)
        message = "Transaction is successful for amount of donation " + amount
        # make transaction in db
        bank_info = get_bank_info_byUserId(person_id)
        old_amount = bank_info.amount
        bank_info.amount = old_amount + int(amount)
        db.session().commit()
        return render_template('paymentPage.html', **userToDict(user), message=message)


def userToDict(user):
    d = {}
    d['username'] = user.username
    d['firstname'] = user.firstname
    d['lastname'] = user.lastname
    d['url'] = user.url
    d['mobile_phone'] = user.mobile_phone
    d['description'] = user.description
    d['person_id'] = user.id
    bank_account = user.bank_info
    d['curr_amount'] = bank_account.amount
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
    # host u ekleki herkes ulassin
    app.run(debug=True, host='0.0.0.0')