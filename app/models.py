from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    mobile_phone = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=False)


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()