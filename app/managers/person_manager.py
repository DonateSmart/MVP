import enum
import logging

from app import db, bcrypt
from app.database_manager.models import User, BankAccount


class SystemMessages(enum.Enum):
    change_username = 'This account name is already in use. Please use different username.'
    password_error = 'Password should be at least 4 characters'
    success_code = 200
    success_message = 'This account is successfully registered into the system.'
    mobile_phone_error = 'Please control mobile phone'
    name_error = 'Name should be at least 2 characters'
    bank_number_error = 'Please control bank number'
    empty_field_error = 'Please fill all the empty fields'


class FormParametersForPerson(enum.Enum):
    username = 'username'
    password = 'password'
    fullname = 'fullname'
    mobile_phone = 'mobile_phone'
    bank_number = 'bank_number'


class Person:
    def __init__(self, username, password, fullname, mobile_phone, bank_number):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.mobile_phone = mobile_phone
        self.bank_number = bank_number


def register_person(person):
    result_message = control_person_field(person)
    logging.info('Try to register the person ', person)

    if result_message == 200:
        encrypted_password = bcrypt.generate_password_hash(person.password, 10)
        bank_account = BankAccount(bank_number=person.bank_number, amount=0)
        user = User(username=person.username, password=encrypted_password, fullname=person.fullname,
                    mobile_phone=person.mobile_phone, bank_info=bank_account)

        try:
            s = db.session()
            s.add(user)
            s.add(bank_account)
            s.commit()
            result_message = "New user is created! the username is " + user.username + " the person id is: " + str(user.id)
        except RuntimeError:
            logging.error('There is an error while registering ', person)
            result_message = "The data couldn't be saved into the system."

    return result_message


def control_person_field(person):
    if len(person.username) == 0 and len(person.fullname) == 00 and len(person.password) == 0 and \
            len(person.mobile_phone) == 0 and len(person.bank_number) == 0:
        return SystemMessages.empty_field_error.value

    if len(person.fullname) < 3:
        return SystemMessages.name_error.value

    if get_user_info(person.username) is not None:
        return SystemMessages.change_username.value

    if len(person.password) < 4:
        return SystemMessages.password_error.value

    if not is_phone_number_valid(person.mobile_phone):
        return SystemMessages.mobile_phone_error.value

    if not person.bank_number.isdigit():
        return SystemMessages.bank_number_error.value

    return SystemMessages.success_code.value


def is_phone_number_valid(s):
    # 1) Begins with 0 or 91
    # 3) Then contains 9 digits
    # pattern = re.compile("(0|91)?[0-9]{9}")
    # return pattern.match(s)
    return s.isdigit()


def get_user_info(username):
    s = db.session()
    result = User.query.filter_by(username=username).first()
    return result

