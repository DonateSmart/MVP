from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    mobile_phone = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=False)


# engine = create_engine('sqlite:///users.db', echo=True)
#
# session = sessionmaker()
# session.configure(bind=engine)
# Base.metadata.create_all(engine)
