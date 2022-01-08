from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)

    password = db.Column(db.String(250), nullable=False)

    url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bank_info = db.relationship('BankAccount', backref='user', lazy=True,  uselist=False)


class BankAccount(db.Model):
    bank_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bank_number = db.Column(db.Integer)


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()