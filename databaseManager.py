from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    mobile_phone = Column(Integer, nullable=False)
    url = Column(String(250), nullable=False)


engine = create_engine('sqlite:///users.db', echo=True)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
