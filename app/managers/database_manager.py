from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    fullname = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    donate_smart_id = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    about_person = db.Column(db.String(250), nullable=True)
    donation_transaction_info = db.relationship('DonationTransaction', backref='user', lazy=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


class DonationTransaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payer_id = db.Column(db.String(250), nullable=False)
    payment_id = db.Column(db.String(250), nullable=False)


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
