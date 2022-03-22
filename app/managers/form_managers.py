from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.managers.database_manager import User, Admin
from flask_wtf.file import FileRequired, FileAllowed, FileField
from email_validator import validate_email, EmailNotValidError
from app import logging


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    image_file = FileField('Would you like to upload your photo?', validators=[FileRequired(),
                           FileAllowed(['png', 'jpg', 'jpeg', 'gif'])])
    about_person = StringField('Would you like to talk about yourself?')
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        if not password_check(password.data):
            raise ValidationError('Password should be at least 4 character, at most 20 character '
                                  'including at least one number, one uppercase and lowercase')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            logging.debug('Username is already in use: {} '.format(username.data))
            raise ValidationError('This account name is already in use. Please use different username.')


def password_check(password):
    # Should have at least one number.
    # Should have at least one uppercase and one lowercase character.
    # Should be between 4 to 20 characters long.

    if len(password) < 4 or len(password) > 20 or not any(char.isdigit() for char in password) \
            or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        return False
    else:
        return True


class AdministrationRegistrationForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        if not password_check(password.data):
            raise ValidationError('Password should be at least 4 character, at most 20 character '
                                  'including at least one number, one uppercase and lowercase')


class AdministrationLoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Sign Up')

    # def validate_email(self, email_address):
    #     validate_email(email_address.data)

    def validate_password(self, password):
        if not password_check(password.data):
            # logging.debug('Password is not validated for the username: {} '.format(FlaskForm.email_address.data))
            raise ValidationError('Password should be at least 4 character, at most 20 character '
                                  'including at least one number, one uppercase and lowercase')

    def validate_password_is_correct(self, password):
        admin = Admin.query.filter_by(email_address=FlaskForm.email_address.data).first()
        if admin.password == password:
            raise ValidationError('Password is wrong')
