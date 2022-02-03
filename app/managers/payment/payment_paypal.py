from flask import jsonify
import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AY3h9HVVS3BQqoL02Q6dAtE2_TD2QiGqz6La0e8OziLUvTrenaQGnTrDeLZUuh-sMPgjxngq53c-oNDM",
  "client_secret": "EF7d2TWEE49ODDDdOHptIOdsp3fiyXw4dhrcmolM2HEAfPM1FcoOzNi9dPRWqoetNYy6tx4mI9jCZvWr" })


def payment_paypal(amount, user_id):
    payment = paypalrestsdk.Payment({
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
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


def execute_paypal(request, amount, user_id):
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})