from app import db, bcrypt, ALLOWED_PHOTO_EXTENSIONS, app
from app.managers.database_manager import User
import hashlib
import os
from werkzeug.utils import secure_filename
from urllib.parse import quote_plus


class RegistrationResult:
    def __init__(self, message, is_data_created, person_id):
        self.message = message
        self.is_data_created = is_data_created
        self.person_id = person_id


class Person:
    def __init__(self, username, password, fullname, image_file, image_url, url,
                 donate_smart_id, image_filename, about_person):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.image_file = image_file
        self.image_url = image_url
        self.url = url
        self.donate_smart_id = donate_smart_id
        self.image_filename = image_filename
        self.about_person = about_person


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS


def get_photo_filename(person):
    image_file = person.image_file
    if image_file and allowed_image_file(image_file.filename):
        file_extension = image_file.filename.split('.')[1]
        filename = secure_filename(person.donate_smart_id + '.' + file_extension)
    return filename


def arrange_person_data(person):
    person.password = bcrypt.generate_password_hash(person.password, 10)

    person.donate_smart_id = hashlib.md5(person.username.encode('utf-8')).hexdigest()
    person.url = "https://prototype.donatesmart.co.uk/profile/" + quote_plus(str(person.donate_smart_id))

    person.image_filename = get_photo_filename(person)
    person.image_url = '/static/assets/profile_pictures/{}'.format(person.image_filename)
    return person


def register_person(form):
    person = Person(form.username.data, form.password.data, form.fullname.data,
                    form.image_file.data, '', '', '', '', form.about_person.data)
    try:
        arranged_person_data = arrange_person_data(person)

        user = User(username=arranged_person_data.username, password=arranged_person_data.password,
                    fullname=arranged_person_data.fullname, donate_smart_id=str(arranged_person_data.donate_smart_id),
                    url=arranged_person_data.url, image_url=arranged_person_data.image_url,
                    about_person=arranged_person_data.about_person)

        s = db.session()
        s.add(user)
        s.commit()

        arranged_person_data.image_file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                          arranged_person_data.image_filename))

        result_message = "New user is created! the username is " + person.username + " the person id is: " + str(user.id)
        is_data_created = True
        user = User.query.filter_by(username=arranged_person_data.username).first()
        return RegistrationResult(result_message, is_data_created, user.id)
    except RuntimeError:
        result_message = "The data couldn't be saved into the system."
        is_data_created = False
        return RegistrationResult(result_message, is_data_created, '')





