from flask import Flask, render_template, request

import databaseManager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    print('HELLO')
    if request.method == 'POST':
        print(request.form['username'] + " " + request.form['password']);
    return render_template('login.html', error=error)


def save_new_user():
    db = databaseManager.engine
    conn = db.connect()
    print(databaseManager.meta.tables.keys())

    users = databaseManager.users


    ins = users.insert().values(name='vvs', lastname='eqwe')
    conn.execute(ins)

    ins = users.insert().values(name='dasd', lastname='dasdasd')

    conn.execute(ins)

    conn.execute(users.insert(), [
        {'name': 'dasda', 'lastname': 'vv'},
        {'name': 'dasdasadas', 'lastname': 'vvv'},
        {'name': 'sss', 'lastname': 'Sattar'},
        {'name': 'ssss', 'lastname': 'sss'},
    ])


def main():
    save_new_user()


if __name__ == "__main__":
    main()