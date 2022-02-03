from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.managers.database_manager import User
from flask_wtf.file import FileRequired, FileAllowed, FileField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=20)])
    mobile_phone = StringField('Mobile phone', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    image_file = FileField('Upload Personal Photo', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'])])
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        if not password_check(password.data):
            raise ValidationError('Password should be at least 4 character, at most 20 character '
                                  'including at least one number, one uppercase and lowercase')

    def validate_mobile_phone(self, mobile_phone):
        if not mobile_phone.data.isdigit():
            raise ValidationError('Please control mobile phone')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
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
