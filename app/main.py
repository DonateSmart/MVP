from flask import render_template, request

from app import db, app
from app.database_manager.models import User
from app.managers.person_manager import FormParametersForPerson, Person, register_person
from managers.payment.payment_paypal import payment_paypal, execute_paypal

# source venv/bin/activate
# run Flask application from terminal
# export FLASK_APP=main.py
# flask run


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        if request.form.get(FormParametersForPerson.username.name) is not None \
                and request.form.get(FormParametersForPerson.password.name) is not None\
                and request.form.get(FormParametersForPerson.fullname.name) is not None \
                and request.form.get(FormParametersForPerson.mobile_phone.name) is not None \
                and request.form.get(FormParametersForPerson.bank_number.name) is not None:

            username = request.form[FormParametersForPerson.username.name]
            password = request.form[FormParametersForPerson.password.name]
            fullname = request.form[FormParametersForPerson.fullname.name]
            mobile_phone = request.form[FormParametersForPerson.mobile_phone.name]
            bank_number = request.form[FormParametersForPerson.bank_number.name]

            person = Person(username, password, fullname, mobile_phone, bank_number)
            message = register_person(person)
        return render_template('index.html', message=message)
    else:
        return render_template('index.html')


def get_user_info_byUserId(person_id):
    s = db.session()
    result = User.query.filter_by(id=person_id).first()
    return result


@app.route('/payment/<amount>', methods=['POST'])
def payment(amount):
    return payment_paypal(amount)


@app.route('/execute', methods=['POST'])
def execute():
    return execute_paypal(request)


@app.route('/donate/<person_id>', methods=['GET', 'POST'])
def user_info(person_id):
    user = get_user_info_byUserId(person_id)
    if user is not None:
        return render_template('paymentPage.html', **userToDict(user))
    else:
        return render_template('404.html')


def userToDict(user):
    d = {}
    d['username'] = user.username
    d['fullname'] = user.fullname
    d['mobile_phone'] = user.mobile_phone
    d['person_id'] = user.id
    bank_account = user.bank_info
    d['curr_amount'] = bank_account.amount
    return d


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')