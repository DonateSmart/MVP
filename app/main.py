from flask import render_template, request, flash, redirect, url_for

from app import app
from app.managers.database_manager import User, Admin
from app.managers.person_manager import register_person
from app.managers.payment.payment_paypal import payment_paypal, execute_paypal, ProcessResult
from app.managers.form_managers import RegistrationForm, AdministrationRegistrationForm, AdministrationLoginForm
from app.managers.administration_manager import register_admin
import logging
import socket
import os

os.environ["ENVIRONMENT"] = "DEV"

logging.basicConfig(filename='donate_smart.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


@app.route('/')
@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    form = RegistrationForm()
    logging.debug('Form is validated for the username: {}'.format(form.username.data))

    if request.method == 'POST' and form.validate_on_submit():
        registration_result = register_person(form)
        logging.debug('Registration result will show on : {}'.format(form.username.data))

        if registration_result.is_data_created:
            flash(f'{registration_result.message}!', 'success')
        else:
            flash(f'{registration_result.message}!', 'fail')

        return redirect(url_for('donate', person_id=registration_result.person_id))

    return render_template('index.html', title='Register', form=form)


@app.route('/admin_signup', methods=['GET', 'POST'])
def administration_signup():
    form = AdministrationRegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        registration_result = register_admin(form)
        logging.debug('Registration result will show on : {}'.format(form.email_address.data))
        print(form.email_address.data + " is created")

        if registration_result.is_data_created:
            flash(f'{registration_result.message}!', 'success')
        else:
            flash(f'{registration_result.message}!', 'fail')

        return redirect(url_for('admin_panel', person_id=registration_result.person_id))

    return render_template('example_adminSignUp.html', title='Register', form=form) #???? should return jsoN?


@app.route('/admin_login', methods=['GET', 'POST'])
def administration_login():
    form = AdministrationLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        admin = Admin.query.filter_by(email_address=form.email_address.data).first()

        if admin.password == form.password.data:
            return redirect(url_for('admin_panel', person_id=admin.id))
        else:
            flash('wrong password!', 'fail')

    return render_template('example_adminLogin.html', title='AdministrationLogin', form=form)


@app.route('/adminPanel/<person_id>', methods=['GET', 'POST'])
def admin_panel(person_id):
    admin = Admin.query.filter_by(id=person_id).first()
    print(admin.email_address)
    if admin is not None:
        return render_template('example_adminPanel.html', admin=admin)
    else:
        return render_template('404.html')


@app.route('/donate/<person_id>', methods=['GET', 'POST'])
def donate(person_id):
    hostname = socket.gethostname()
    host_id = socket.gethostbyname(hostname)

    if os.environ["ENVIRONMENT"] == 'DEV':
        host_id = "127.0.0.1:5000"
    else:
        host_id = host_id + ":80"

    print('host: ' + host_id)
    user = User.query.filter_by(id=person_id).first()
    if user is not None:
        return render_template('paymentPage.html', user=user, host_id=host_id)
    else:
        return render_template('404.html')


@app.route('/payment/<amount>/<user_id>', methods=['POST'])
def payment(amount, user_id):
    process_result = payment_paypal(amount, user_id)
    if process_result.is_successful:
        return process_result.json_result
    else:
        flash(f'{process_result.message}!', 'fail')
        return redirect(url_for('donate', person_id=user_id))


@app.route('/execute/<amount>/<user_id>', methods=['POST'])
def execute(amount, user_id):
    process_result = execute_paypal(request, amount, user_id)
    if process_result.is_successful:
        flash(f'{process_result.message}!', 'success')
    else:
        flash(f'{process_result.message}!', 'fail')

    return process_result.json_result


@app.route("/list_users")
def list_users():
    users = User.query.all()
    return render_template('example_listUsers.html', users=users)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
