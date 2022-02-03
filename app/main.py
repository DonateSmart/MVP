from flask import render_template, request, flash, redirect, url_for

from app import app
from app.managers.database_manager import User
from app.managers.person_manager import register_person
from managers.payment.payment_paypal import payment_paypal, execute_paypal
from app.managers.form_managers import RegistrationForm


@app.route('/')
@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        registration_result = register_person(form)

        if registration_result.is_data_created:
            flash(f'{registration_result.message}!', 'success')
        else:
            flash(f'{registration_result.message}!', 'fail')

        return redirect(url_for('donate', person_id=registration_result.person_id))

    return render_template('index.html', title='Register', form=form)


@app.route('/payment/<amount>/<user_id>', methods=['POST'])
def payment(amount, user_id):
    return payment_paypal(amount, user_id)


@app.route('/execute/<amount>/<user_id>', methods=['POST'])
def execute(amount, user_id):
    a = 5
    return execute_paypal(request, amount, user_id)


@app.route('/donate/<person_id>', methods=['GET', 'POST'])
def donate(person_id):
    user = User.query.filter_by(id=person_id).first()
    if user is not None:
        return render_template('paymentPage.html', user=user)
    else:
        return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')