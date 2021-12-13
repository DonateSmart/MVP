from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///users.db', echo=True)
meta = MetaData()
users = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('username', String),
   Column('password', String),
)


def create_user_table():
   meta.create_all(engine)


def main():
   create_user_table()


if __name__ == "__main__":
   main()



