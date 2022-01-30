import base64
import os

from urllib.parse import quote_plus
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename

from app import db, app, bcrypt, ALLOWED_EXTENSIONS
from app.upload_s3 import upload_file_s3, upload_file_object_s3, s3_upload_small_files
from models import HLPerson
import hashlib


@app.route('/')
def index():
    return redirect(url_for('signup_user'))


# source venv/bin/activate
# run Flask application from terminal
# export FLASK_APP=main.py
# flask run
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/userSignup', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        username = request.form['nameField']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password, 10)
        age = request.form['ageField']
        description = request.form['description']
        bank_field = request.form['bankField']
        image = request.files['fileField']
        content_type = image.content_type
        donate_smart_id = hashlib.md5(username.encode('utf-8')).hexdigest()
        if image and allowed_file(image.filename):
            file_extention = image.filename.split('.')[1]
            filename = secure_filename(donate_smart_id + '.' + file_extention)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # if image:
        #     filename_final = secure_filename(image.filename)
        #
        #     image_url = s3_upload_small_files(inp_file_name=image, s3_bucket_name="test-donatesmart",
        #                                       inp_file_key=filename_final,
        #                                       content_type=content_type)
        #     print(image_url)
        # if image:
        #     final_upload = upload_file_object_s3(image,"test-donatesmart")
        #     print(final_upload)
        donate_smart_id = hashlib.md5(username.encode('utf-8')).hexdigest()
        url = "https://prototype.donatesmart.co.uk/profile/" + quote_plus(str(donate_smart_id))
        user = HLPerson(username=username, donate_smart_id=str(donate_smart_id), password=password_hash, url=url,
                        age=age, description=description,
                        bank_field=bank_field, image_url='/static/assets/profile_pictures/{}'.format(filename))
        s = db.session()
        s.add(user)
        s.commit()
        message = "New user is created!"
        flash(message)
        return redirect(url_for('user_info', person_id=donate_smart_id))

    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        message = 'username or password is wrong'
        conn_success = False
        uname = request.form['username']
        password = request.form['password']

        print(uname, password)

        result = HLPerson.query.filter_by(username=uname).first()

        if result != None:
            if bcrypt.check_password_hash(result.password, password):
                conn_success = True

        if conn_success:
            message = 'connection is successful'
            session['username'] = uname
            return user_info()
        else:
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')




@app.route('/donate/<person_id>', methods=['GET', 'POST'])
def user_info(person_id):
    user = HLPerson.query.filter_by(donate_smart_id = person_id).first()
    if user is not None:
        return render_template('paymentPage.html', user = user)
    return render_template('paymentPage.html')




@app.route('/editUserInfo', methods=['GET', 'POST'])
def edit_user_info():
    if request.method == 'POST':
        if 'username' in session:

            username = session['username']

            if request.form.get('username') != None and request.form.get('firstname') != None and \
                    request.form.get('lastname') != None and request.form.get('url') != None \
                    and request.form.get('mobile_phone') != None:
                message = 'HLPerson info is saved!'

                firstname = request.form['firstname']
                lastname = request.form['lastname']
                url = request.form['url']
                mobile_phone = request.form['mobile_phone']

                # update data in db

                user = HLPerson.query.filter_by(username=username).first()
                user.firstname = firstname
                user.lastname = lastname
                user.url = url
                user.mobile_phone = mobile_phone
                db.session().commit

                return render_template('userInfo.html', username=username, firstname=firstname, lastname=lastname,
                                       url=url, mobile_phone=mobile_phone, message=message)

    else:
        if 'username' in session:
            username = session['username']
            user = get_user_info(username)
            return render_template('editUserInfo.html', user=user)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/listUsers')
def listUsers():
    results = HLPerson.query.all()
    users = []
    for item in results:
        users.append(item.username)

    return render_template('list.html', members=users)


if __name__ == "__main__":
    app.run(debug=True)
