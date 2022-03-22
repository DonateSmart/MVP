from app import db
from app.managers.database_manager import User, Admin


class RegistrationResult:
    def __init__(self, message, is_data_created, person_id):
        self.message = message
        self.is_data_created = is_data_created
        self.person_id = person_id


def register_admin(form):
    try:
        admin = Admin(email_address=form.email_address.data, password=form.password.data)

        s = db.session()
        s.add(admin)
        s.commit()

        result_message = "New admin is created! the admin is " + admin.email_address + " the person id is: " + \
                         str(admin.id)
        is_data_created = True
        admin = Admin.query.filter_by(email_address=admin.email_address).first()
        return RegistrationResult(result_message, is_data_created, admin.id)
    except RuntimeError:
        result_message = "The data couldn't be saved into the system."
        is_data_created = False
        return RegistrationResult(result_message, is_data_created, '')
