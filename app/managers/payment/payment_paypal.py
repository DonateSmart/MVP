import logging

from flask import jsonify
import paypalrestsdk
from app import db
from app.managers.database_manager import DonationTransaction
from app.managers.database_manager import User

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "CLIENT_ID",
  "client_secret": "SECRET_KEY" })


class ProcessResult:
    def __init__(self, json_result, is_successful, message):
        self.json_result = json_result
        self.is_successful = is_successful
        self.message = message


def get_payment_json_template(amount, user_id):
    return {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": amount,
                "currency": "USD"},
            "description": "Payment transaction description for user_id: {} amount: {}".format(user_id, amount)}]}


def payment_paypal(amount, user_id):
    payment = paypalrestsdk.Payment(get_payment_json_template(amount, user_id))

    success = False
    if payment.create():
        message = "Payment started for user_id: {} amount: {}".format(user_id, amount)
        logging.info('Payment started for user_id: %s amount: %s payment_id: %s', user_id, amount, payment.id)
        success = True
        print('Payment success!')

    else:
        message = "Error occurred while payment started for user_id: {} amount: {}".format(user_id, amount)
        logging.error('Error occurred while payment started for user_id: %s amount: %s payment error: %s',
                      user_id, amount, payment.error)
        print(payment.error)

    return ProcessResult(jsonify({'paymentID': payment.id}), success, message)


def execute_paypal(request, amount, user_id):
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    user = User.query.filter_by(id=user_id).first()

    if payment.execute({'payer_id': request.form['payerID']}):
        message = "{}£ of donation is successful for {}. Thank you".format(amount, user.username)
        logging.info('Payment executed for user_id: %s amount: %s payment_id: %s payer_id: %s', user_id,
                     amount, payment.id, request.form['payerID'])

        # save transaction in database
        donation_transaction = DonationTransaction(amount=amount, user_id=user_id,
                                                   payer_id=request.form['payerID'], payment_id=payment.id)

        s = db.session()
        s.add(donation_transaction)
        s.commit()

        print('Execute success!')
        success = True
    else:
        logging.info('Error execution started for user_id: %s amount: %s payment_id: %s payer_id: %s payment error: %s',
                     user_id, amount, payment.id, request.form['payerID'], payment.error)
        print(payment.error)

    return ProcessResult(jsonify({'success': success}), success, message)
