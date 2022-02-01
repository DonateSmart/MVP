from app import db


class HLPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donate_smart_id = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    bank_field = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(250), nullable=False)


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
